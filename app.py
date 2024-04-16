from flask import Flask, render_template, request, redirect, url_for, flash
from flask_paginate import Pagination, get_page_args
import pymysql.cursors
import re
from string import digits

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='FoundNight20!',
                             db='onlinestoredb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

@app.route('/')
def products():
    try:
        with connection.cursor() as cursor:
            # Getting total length of table in mysql as an integer
            
            cursor.execute("SELECT COUNT(*) FROM onlinestoredb.product_master")
            total_num = str(cursor.fetchall())
            total_num = int(re.sub("[^0-9]", "", total_num))
            
            # Pagination initialization
            
            page = request.args.get('page', 1, type=int)
            per_page = 10
            start = (page - 1) * per_page
            total_pages = (total_num + per_page - 1) // per_page
            
            # Pagination table viewing
            
            newsql = "SELECT DISTINCT Item_no, Name, Price, Description, Warranty FROM onlinestoredb.product_master LIMIT " + str(start) + ", " + str(per_page)
            cursor.execute(newsql)
            pagination_result = cursor.fetchall()
            
            # Old table viewing not being used
            
            sql= "SELECT DISTINCT Item_no, Name, Price, Description, Warranty FROM product_master"
            cols = ['Item_no', 'Name', 'Price', 'Description', 'Warranty']
            cursor.execute(sql)
            result = cursor.fetchall()
            
            # Not working unused code
            
            cursor.execute("SELECT Item_no from product_master")
            result2 = str(cursor.fetchall())
            result2 = (re.sub("[^0-9]", "", result2))
            print(result2)
            item_number_list = [int(x) for x in str(result2)]
            print(item_number_list)   
        return render_template("view_products.html", items=pagination_result, cols=cols, total_pages=total_pages, page=page, success='')
    except Exception as e:
        return render_template("view_products.html", items=[], cols=[], success='Unnable to view products: ' + str(e))
    
@app.route('/addProducts')
def add_products_page():
    print ('reached add products')
    return render_template("add_products.html", success='')

@app.route('/addProductsReq', methods=['GET'])
def add_products():
    Item_no = int(request.args.get('Item_no').strip())
    Name = request.args.get('Name').strip()
    Price = float(request.args.get('Price').strip())
    Description = request.args.get('Description').strip()
    Warranty = int(request.args.get('Warranty').strip())
    print ('Form inputs line reached')
    if Item_no == '' or Name == '' or Price == '' or Description == '' or Warranty == '':
        print ('no inputs')
        return render_template("add_products.html", success='Please fill all fields.')
    try:
        print ('before insert query')
        with connection.cursor() as cursor:
            sql = 'INSERT INTO `product_master` (`Item_no`, `Name`, `Price`, `Description`, `Warranty`) VALUES (%s, %s, %s, %s, %s)'
            print ("sql", sql)
            cursor.execute(sql, (Item_no, Name, Price, Description, Warranty))
            connection.commit()
        return render_template("add_products.html", sucess='Sucessful')
    except Exception as e:
        print ('exception', e)
        return render_template("add_products.html", success='Unable to add product: ' + str(e))

@app.route('/updateProducts')
def update_products_page():
    return render_template("update_products.html", success='')

@app.route('/updateProductsReq', methods=['GET'])
def update_products():
    Item_no = int(request.args.get('Item_no').strip())
    Name = request.args.get('Name').strip()
    Price = float(request.args.get('Price').strip())
    Description = request.args.get('Description').strip()
    Warranty = int(request.args.get('Warranty').strip())

    if Item_no == '' or Name == '' or Price == '' or Description == '' or Warranty == '':
        return render_template("add_products.html", success='Please fill all fields.')
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `product_master` SET `Name`=%s,`Price`=%s,`Description`=%s, `Warranty`=%s where `Item_no`=%s"
            print(sql + " sql printed")
            cursor.execute(sql, (Name, Price, Description, Warranty, Item_no))
            connection.commit()
            return render_template("update_products.html", success='Successful')
    except Exception as e:
        return render_template("update_products.html", success='Can\'t update Paper: ' + str(e))
    
@app.route('/deleteProducts')
def delete_products_page():
    return render_template("delete_products.html", success='')

@app.route('/deleteProductsReq', methods=['GET'])
def delete_products():
    Item_no = int(request.args.get('Item_no').strip())
    if Item_no == '':
        return render_template("delete_products.html", success='Item number cannot be empty')
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `product_master` WHERE `Item_no`=%s"
            cursor.execute(sql, Item_no)
            connection.commit()
            return render_template("delete_products.html", success='Successful')
    except Exception as e:
        return render_template("delete_products.html", success='Can\'t delete paper: ' + str(e))
    
if __name__ == "__main__":
    app.run(debug=False)