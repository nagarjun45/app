from flask import Flask
from flask import request
import pymongo
import json
app = Flask(__name__)
@app.route("/",methods = ['GET', 'POST'])
#{"query_type": "discounted_products_list","filters": [{"operand1": "discount","operator": ">","operand2": 5}]}
#Test 1: POST { "query_type": "discounted_products_count|avg_discount", "filters": [{ "operand1": "brand.name", "operator": "==", "operand2": "gucci" }] }
def hello():
  #myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  myclient = pymongo.MongoClient("mongodb+srv://admin:arjun123@cluster0-xwfln.mongodb.net/test?retryWrites=true&w=majority")
  mydb = myclient["project"]
  mytable = mydb['api']
  all_records = mytable.find({})
  if request.method == 'POST':
    post_request = request.get_json(force=True)
    query_type = post_request['query_type']
    print(query_type)
    filters = post_request['filters']
    discounted_products_list = list()
    operand1 = filters[0]['operand1']
    operator = filters[0]['operator']
    if operator == '>' and query_type == 'discounted_products_list':
      operand2 = int(filters[0]['operand2'])
      for record in all_records:
        regular_price = int(record['price']['regular_price']['value'])
        offer_price = int(record['price']['offer_price']['value'])
        discount_percentage = ((regular_price - offer_price)/regular_price) * 100
        if discount_percentage > operand2 :
          discounted_products_list.append(record['_id'])
      return {
      query_type : str(discounted_products_list)   
    }
    if operator == '==' and query_type == 'discounted_products_count|avg_discount' :
      operand2 = filters[0]['operand2']
      discounted_products_count_list = list()
      discount_percentage_add = 0
      for record in all_records:
        if record['brand']['name'] == operand2:
          regular_price = int(record['price']['regular_price']['value'])
          offer_price = int(record['price']['offer_price']['value'])
          discount_percentage = ((regular_price - offer_price)/regular_price) * 100
          discount_percentage_add = discount_percentage_add + discount_percentage
          discounted_products_count_list.append(record['_id'])
      avg_discount = discount_percentage_add / len(discounted_products_count_list)
      return{
        query_type : str(len(discounted_products_count_list)),
        "avg_dicount" : avg_discount
      }







      
  




