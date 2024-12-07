# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:23:54 2024

@author: ASUS
"""
import sqlite3
import pandas as pd
from flask import Flask , request
app=Flask(__name__) 




@app.get('/store')
def get_store():
    store=request.args.get('store')
    item=request.args.get('item')
    search_id=request.args.get('id')
    query='''select * from stores'''
    if search_id:
        query=f'''select * from stores where id = "{search_id}"'''
    elif store and item:
        query=f'''select * from stores where store_name={store} and item={item}'''
    elif store:
        query=f'''select * from stores where store_name={store}'''
    elif item:
        query=f'''select * from stores where item={item}'''
    data=sqlite3.connect('gamer_world.db')
    json_data=pd.read_sql(query,data).to_json(orient='records', lines=True)
    return json_data
@app.post('/store')
def alter():
    delete=request.args.get('delete')
    search_id=request.args.get('id')
    client_data=request.get_json()
#-----------------------deletion--------------------------------------------------------------------------------------------------------------------------------------------------
    # delete a data, given id 
    if delete == 'true' and search_id:
        query=f'''delete from stores where id="{search_id}"'''
    # delete a data, given "store name" "item" and "price" 
    elif delete == 'true' and client_data['store_name'] and client_data['item'] and client_data['price'] :
        query=f'''delete from stores where store_name="{client_data['store_name']}" and item = "{client_data['item']}" and price = "{client_data['price']}"'''
    # delete a data, given "store name" and "item" 
    elif delete == 'true' and client_data['store_name'] and client_data['item']:
        query=f'''delete from stores where store_name="{client_data['store_name']}" and item = "{client_data['item']}"'''
    # delete a data, given only "store name" 
    elif delete == 'true' and client_data['store_name']:
        query=f'''delete from stores where store_name="{client_data['store_name']}"'''
    # delete a data, given "price" and "item" 
    elif delete == 'true' and client_data['item'] and client_data['price']:
        query=f'''delete from stores where item = "{client_data['item']}" and price = "{client_data['price']}"'''
    # delete a data, given only "item" 
    elif delete == 'true' and client_data['item']:
        query=f'''delete from stores where item = "{client_data['item']}"'''
    # delete a data, given "store name" and "price" 
    elif delete == 'true' and client_data['store_name'] and client_data['price'] :
        query=f'''delete from stores where store_name="{client_data['store_name']}" and price = "{client_data['price']}"'''
    # delete a data, given only "price" 
    elif delete == 'true' and client_data['price'] :
        query=f'''delete from stores where price = "{client_data['price']}"'''
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------insert data-----------------------------------------------------------------------------------------------------------------------------
    else:
        query = f"INSERT INTO stores (store_name, item, price) VALUES ('{client_data['store_name']}', '{client_data['item']}', {client_data['price']})"
    data=sqlite3.connect('gamer_world.db')
    data.execute(query)
    data.commit()
    json_data=pd.read_sql('select * from stores',data).to_json(orient='records', lines=True)
    return json_data , 201
    
if __name__ =='__main__':
    app.run()
    