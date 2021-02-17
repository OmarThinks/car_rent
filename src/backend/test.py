import os
import secrets
import unittest
import json
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func 



try:
    from __init__ import *
except:
    from src import *



"""
try:
	from src import SECRET
	from src import EXPIRATION_AFTER
	from src import db
	from .app import *
	from .auth import *
	from .models import (db,Product, Order, User,Image)
	from .functions import *
except:
	from __init__ import *
	from app import *
	from auth import *
	from models import (db,Product, Order, User)
	from functions import *
"""

from flask_cors import CORS
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy
import random
import jwt
import base64


from datetime import timedelta,date,datetime,time
"""
a:models
a_01=user
a_02_=product
a_03_=order
a_04_=image


b:validation Functions




c.1 : Authentication : already there functions
c.2 : Authentication : functions created by me
"""

unittest.TestLoader.sortTestMethodsUsing = None

class CantiinTestCase(unittest.TestCase):
	"""This class represents the trivia test case"""

	def setUp(self):
		# create and configure the app
		self.app = create_app(testing=True) #Flask(__name__)
		self.client = self.app.test_client
		#db.app = self.app
		#db.init_app(self.app)
		db.create_all()        
		
	
	def tearDown(self):
		"""Executed after reach test"""
		print("_+++++++++++++++++++++++++++++++++_")

	#Note: Tests are run alphapetically
	def test_001_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")


	def test_002_drop_all_create_all(self):
		db_drop_and_create_all()
		products = Product.query.all()
		self.assertEqual(len(products),0)
		print("Test 2: db_drop_and_create_all")





	def test_a_1_000_user_intro(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 1 ) User ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")



	def test_a_1_001_user_insert(self):
		user1 = User(username = "useeer1",password="45687")
		user1.insert()
		users = User.query.all()

		self.assertEqual(len(users),1)
		print("Test a_1_1: user insert")


	def test_a_1_002_user_update(self):
		user1 = User.query.get(1)
		user1.name = "modified"
		user1.update()
		user_1 = User.query.get(1)

		self.assertEqual(user_1.name,"modified")
		print("Test a_1_2: user update")



	def test_a_1_003_user_delete(self):
		user1 = User.query.get(1)
		user1.delete()
		users = User.query.all()

		self.assertEqual(len(users),0)
		print("Test a_1_3: user delete")

	def test_a_1_004_populate(self):
		populate_tables()
		users = User.query.all()

		self.assertEqual(len(users),6)
		print("Test a_1_4: Populate Tables")


	def test_a_1_005_user_values(self):
		user = User.query.get(1)

		self.assertEqual(user.id,1)
		self.assertEqual(user.username,"abc")
		self.assertEqual(user.password,"123456789")
		for prod in user.products:
			self.assertEqual(type(prod.id),int)
			self.assertEqual(type(prod.price),float)
			self.assertEqual(type(prod.in_stock),bool)
			self.assertEqual(type(prod.seller_id),int)
		for order in user.orders:
			self.assertEqual(type(order.id),int)
			self.assertEqual(type(order.user_id),int)
			self.assertEqual(type(order.product_id),int)
			self.assertEqual(type(order.amount),int)
		for image in user.images:
			self.assertEqual(type(image.id),int)
			self.assertEqual(type(image.seller_id),int)
			self.assertEqual(type(image.name),str)
			self.assertEqual(type(image.formatting),str)
		print("Test a_1_5: user values")


	def test_a_1_006_user_insert_wrong(self):
		users = User.query.all()
		old_records_number = len(users)
		try:
			#This code will not be executed
			#There are missing required parameters
			user1 = user()
			user1.insert()
			self.assertEqual(True,False)
		except:
			self.assertEqual(True,True)
		
		users = User.query.all()
		new_records_number = len(users)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_1_6: user insert with missing"+
		 "required parameters")



	def test_a_1_007_user_delete_wrong(self):
		users = User.query.all()
		old_records_number = len(users)
		try:
			#This code will not be executed
			#There is no user with the number 0
			user1 = User.query.get(0)
			user1.delete()
			self.assertEqual(True,False)

		except:
			self.assertEqual(True,True)
		
		users = User.query.all()
		new_records_number = len(users)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_1_7: user delete mistake, non-existent"+
		 "user id")



	def test_a_1_008_user_simple(self):
		produc = User.query.get(1).simple()
		#print(produc)

		self.assertEqual(produc["id"],1)
		self.assertEqual(type(produc["id"]),int)

		self.assertEqual(produc["username"],"abc")
		self.assertEqual(type(produc["username"]),str)

		print("Test a_1_8: user simple")

	def test_a_1_009_user_relationship_order(self):
		user = User.query.get(1)
		orders=user.orders
		orders_ids=[order.id for order in orders]
		self.assertEqual(1 in orders_ids,True)
		self.assertEqual(2 in orders_ids,False)
		self.assertEqual(3 in orders_ids,False)
		self.assertEqual(4 in orders_ids,True)
		print("Test a_1_9:user relationship_order")

	def test_a_1_010_user_delete_relationships(self):
		#measuring lengths beofre actions
		users_before = len(User.query.all())
		products_before = len(Product.query.all())
		orders_before = len(Order.query.all())
		images_before = len(Image.query.all())

		#adding a new user
		usr_to_del = User(username="aklmnopq",password="123456789")
		db.session.add(usr_to_del)
		db.session.commit()
		self.assertEqual(len(User.query.all()),users_before+1)

		#adding a new product
		prod_to_del = Product(name="Labtopppp", 
			price=3000, seller_id=usr_to_del.id)
		db.session.add(prod_to_del)
		db.session.commit()
		self.assertEqual(len(Product.query.all()),products_before+1)

		#adding a new order
		ordr_to_del = Order(user_id=usr_to_del.id, product_id=1, amount=1)
		db.session.add(ordr_to_del)
		db.session.commit()
		self.assertEqual(len(Order.query.all()),orders_before+1)

		#adding a new image
		img_to_del = Image(seller_id=usr_to_del.id, name="Labtopfgfgfg", 
			formatting="png")
		db.session.add(img_to_del)
		db.session.commit()
		self.assertEqual(len(Image.query.all()),images_before+1)

		usr_to_del.delete()
		self.assertEqual(len(User.query.all()),users_before)
		self.assertEqual(len(Product.query.all()),products_before)
		self.assertEqual(len(Order.query.all()),orders_before)
		self.assertEqual(len(Image.query.all()),images_before)

		print("Test a_1_10: user delete relationships")


























	def test_a_2_000_product_intro(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 2 ) Product ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")



	def test_a_2_001_product_insert(self):
		db_drop_and_create_all()
		product1 = Product(name = "product1",price = 5.5,
			in_stock=True, seller_id=1)
		product1.insert()
		products = Product.query.all()

		self.assertEqual(len(products),1)
		print("Test a_2_1: Product insert")


	def test_a_2_002_product_update(self):
		product1 = Product.query.get(1)
		product1.name = "modified"
		product1.update()
		product_1 = Product.query.get(1)

		self.assertEqual(product_1.name,"modified")
		print("Test a_2_2: Product update")



	def test_a_2_003_product_delete(self):
		product1 = Product.query.get(1)
		product1.delete()
		products = Product.query.all()

		self.assertEqual(len(products),0)
		print("Test a_2_3: Product delete")

	def test_a_2_004_populate(self):
		populate_tables()
		products = Product.query.all()

		self.assertEqual(len(products),6)
		print("Test a_2_4: Populate Tables")


	def test_a_2_005_product_values(self):
		produc = Product.query.get(1)

		self.assertEqual(produc.id,1)
		self.assertEqual(produc.name,"Labtop")
		self.assertEqual(produc.price,300)
		self.assertEqual(produc.seller_id,1)
		self.assertEqual(produc.in_stock,True)
		print("Test a_2_5: Product values")


	def test_a_2_006_product_insert_wrong(self):
		products = Product.query.all()
		old_records_number = len(products)
		try:
			#This code will not be executed
			#There are missing required parameters
			product1 = Product()
			product1.insert()
			self.assertEqual(True,False)
		except:
			self.assertEqual(True,True)
		
		products = Product.query.all()
		new_records_number = len(products)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_2_6: product insert with missing"+
		 "required parameters")



	def test_a_2_007_product_delete_wrong(self):
		products = Product.query.all()
		old_records_number = len(products)
		try:
			#This code will not be executed
			#There is no product with the number 0
			product1 = Product.query.get(0)
			product1.delete()
			self.assertEqual(True,False)

		except:
			self.assertEqual(True,True)
		
		products = Product.query.all()
		new_records_number = len(products)

		self.assertEqual(old_records_number,
			new_records_number)
		print("Test a_2_7: product delete mistake, non-existent"+
		 "product id")




	def test_a_2_008_get_in_stock_products(self):
		products = get_in_stock_products()
		for product in products:
			self.assertEqual(product.in_stock,True)
		print("Test a_2_8:get in stock products")



	def test_a_2_009_product_simple(self):
		produc = Product.query.get(1).simple()
		#print(produc)

		self.assertEqual(produc["id"],1)
		self.assertEqual(type(produc["id"]),int)

		self.assertEqual(produc["name"],"Labtop")
		self.assertEqual(type(produc["name"]),str)

		self.assertEqual(produc["price"],300)
		self.assertEqual(type(produc["price"]),float)

		self.assertEqual(produc["seller_id"],1)
		self.assertEqual(type(produc["seller_id"]),int)

		self.assertEqual(produc["in_stock"],True)
		self.assertEqual(type(produc["in_stock"]),bool)

		print("Test a_2_9: Product simple")

	def test_a_2_010_product_relationship_order(self):
		product = Product.query.get(1)
		orders=product.orders
		orders_ids=[order.id for order in orders]
		self.assertEqual(1 in orders_ids,True)
		self.assertEqual(2 in orders_ids,True)
		self.assertEqual(3 in orders_ids,False)
		self.assertEqual(4 in orders_ids,True)
		print("Test a_2_10:product relationship_order")














	def test_a_3_000_order_intro(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 3 ) Order ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")





	def test_a_3_001_order_insert(self):
		order1 = Order(user_id=20, product_id=5, amount=5)
		order1.insert()
		orders = Order.query.all()

		self.assertEqual(len(orders),9)
		print("Test a_3_1: Order insert")

	def test_a_3_002_order_insert_wrong_1(self):
		
		before = len(Order.query.all())
		order1 = Order(user_id=20, product_id=5, amount=0)
		order1.insert()
		after = len(Order.query.all())
		self.assertEqual(after,before)
		print("Test a_3_2: Order insert Wrong 1: amount=0")

	def test_a_3_003_order_insert_wrong_2(self):
		before = len(Order.query.all())
		try:
			order1 = Order()
			order1.insert()
			self.assertEqual(True,False)
		except:
			self.assertEqual(True,True)
		after = len(Order.query.all())

		self.assertEqual(before,after)
		print("Test a_3_3: Order insert Wrong 2: missing required"+
			" parameters")


	def test_a_3_004_order_update(self):
		order1 = Order.query.get(1)
		order1.amount = 2
		order1.update()
		order_1 = Order.query.get(1)

		self.assertEqual(order_1.amount,2)
		print("Test a_3_4: Order update")

	def test_a_3_005_order_update_wrong(self):
		before = len(Order.query.all())
		order1 = Order.query.get(8)
		order1.amount = 0
		order1.update()
		after = len(Order.query.all())

		self.assertEqual(before,after+1)
		print("Test a_3_5: Order update wrong: amount=0")



	def test_a_3_006_order_delete(self):
		before = len(Order.query.all())
		order1 = Order.query.get(7)
		order1.delete()
		after = len(Order.query.all())

		self.assertEqual(before,after+1)
		print("Test a_3_6: Order delete")


	def test_a_3_007_order_values(self):
		order = Order.query.get(6)

		self.assertEqual(order.id,6)
		self.assertEqual(order.user_id,2)
		self.assertEqual(order.product_id,3)
		self.assertEqual(order.amount,5)
		self.assertEqual(order.total_cost,0)
		print("Test a_3_7: Order values")




	def test_a_3_008_order_delete_wrong(self):
		before = len(Order.query.all())
		try:
			#This code will not be executed
			#There is no order with the number 700000
			order = Product.query.get(700000)
			order.delete()
			self.assertEqual(True,False)

		except:
			self.assertEqual(True,True)
		
		after = len(Order.query.all())

		self.assertEqual(before,after)
		print("Test a_3_8: order delete mistake, non-existent"+
		 "order id")




	def test_a_3_009_order_simple(self):
		order = Order.query.get(6).simple()
		#print(produc)

		self.assertEqual(order["id"],6)
		self.assertEqual(type(order["id"]),int)
		self.assertEqual(order["user_id"],2)
		self.assertEqual(type(order["user_id"]),int)
		self.assertEqual(order["product_id"],3)
		self.assertEqual(type(order["product_id"]),int)
		self.assertEqual(order["amount"],5)
		self.assertEqual(type(order["amount"]),int)


		print("Test a_3_9: Order simple")

	def test_a_3_010_order_relationship_product(self):
		order = Order.query.get(6)
		product=order.product
		self.assertEqual(product,Product.query.get(3))
		print("Test a_2_10:order relationship_product")

	def test_a_3_011_order_get_dict(self):
		order = Order.query.get(6).get_dict()
		#print(produc)

		self.assertEqual(order["id"],6)
		self.assertEqual(type(order["id"]),int)
		self.assertEqual(order["user_id"],2)
		self.assertEqual(type(order["user_id"]),int)
		self.assertEqual(order["amount"],5)
		self.assertEqual(type(order["amount"]),int)

		self.assertEqual(order["product"]["id"],3)
		self.assertEqual(order["product"]["name"],"Candy")
		self.assertEqual(order["product"]["price"],0.5)
		self.assertEqual(order["product"]["in_stock"],True)
		self.assertEqual(order["product"]["seller_id"],3)

		print("Test a_3_11: Order get_dict")

	def test_a_3_012_order_relationship_product_delete(self):
		p_before=len(Product.query.all())
		#Creating the product to be deleted
		product_del=Product(name="Spoon",price="5",
			in_stock=True,seller_id=1)
		product_del.insert()
		p_del_id=product_del.id
		p_after=len(Product.query.all())
		self.assertEqual(p_after,p_before+1)

		o_before = len(Order.query.all())
		#Creating orders to be deleted
		o_del_1=Order(user_id=1,product_id=p_del_id,amount=1)
		o_del_2=Order(user_id=1,product_id=p_del_id,amount=1)
		o_del_3=Order(user_id=1,product_id=p_del_id,amount=1)
		o_del_4=Order(user_id=1,product_id=p_del_id,amount=1)
		o_del_1.insert();o_del_2.insert();
		o_del_3.insert();o_del_4.insert();
		self.assertEqual(len(Order.query.all()),o_before+4)

		#Making the delete action
		product_del.delete()
		o_after = len(Order.query.all())

		#Testing values
		self.assertEqual(len(Product.query.all()),p_before)
		self.assertEqual(o_before,o_after)
		self.assertEqual(len(Order.query.filter(
			Order.product_id==p_del_id
        ).all()),0)

		print("Test a_2_12:order relationship_product_delete")






	def test_a_4_000_image_intro(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 4 ) Image ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")

	def test_a_4_001_image_insert(self):
		before = len(Image.query.all())
		image1 = Image(seller_id=1, name=5, formatting="png")
		image1.insert()
		after = len(Image.query.all())
		self.assertEqual(after,before+1)
		print("Test a_4_1: Image insert")

	def test_a_4_002_image_update(self):
		image1 = Image.query.get(1)
		image1.name = "Mouse"
		image1.update()
		image_1 = Image.query.get(1)
		self.assertEqual(image_1.name,"Mouse")
		print("Test a_4_2: Image update")

	def test_a_4_003_image_delete(self):
		before = len(Image.query.all())
		image1 = Image.query.get(16)
		image1.delete()
		after = len(Image.query.all())
		self.assertEqual(before,after+1)
		print("Test a_4_3: Image delete")

	def test_a_4_004_image_values(self):
		image = Image.query.get(14)
		self.assertEqual(image.id,14)
		self.assertEqual(image.seller_id,2)
		self.assertEqual(image.name,"Back bag")
		self.assertEqual(image.formatting,"jpg")
		print("Test a_4_4: Image values")

	def test_a_4_005_image_delete_wrong(self):
		before = len(Image.query.all())
		try:
			#This code will not be executed
			#There is no image with the number 700000
			image = Image.query.get(700000)
			image.delete()
			self.assertEqual(True,False)
		except:
			self.assertEqual(True,True)
		after = len(Image.query.all())
		self.assertEqual(before,after)
		print("Test a_4_5: image delete mistake, non-existent"+
		 "image id")

	def test_a_4_006_image_simple(self):
		image = Image.query.get(6).simple()
		self.assertEqual(image["id"],6)
		self.assertEqual(type(image["id"]),int)
		self.assertEqual(image["seller_id"],6)
		self.assertEqual(type(image["seller_id"]),int)
		self.assertEqual(image["name"],"Mouse")
		self.assertEqual(type(image["name"]),str)
		self.assertEqual(image["formatting"],"png")
		self.assertEqual(type(image["formatting"]),str)
		print("Test a_4_6: Image simple")

	def test_a_4_007_image_relationship_seller(self):
		image = Image.query.get(6)
		seller=image.seller
		self.assertEqual(seller,User.query.get(seller.id))
		print("Test a_4_7:image relationship_seller")

	def test_a_4_008_image_get_dict(self):
		image = Image.query.get(6).get_dict()
		self.assertEqual(image["id"],6)
		self.assertEqual(type(image["id"]),int)
		self.assertEqual(image["seller_id"],6)
		self.assertEqual(type(image["seller_id"]),int)
		self.assertEqual(image["name"],"Mouse")
		self.assertEqual(type(image["name"]),str)
		self.assertEqual(image["formatting"],"png")
		self.assertEqual(type(image["formatting"]),str)
		print("Test a_4_8: Image get_dict")











	def test_b_01_001_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=1,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],1)
		self.assertEqual(all_products.get(1),
			validation["result"])
		print("Test b_1_1: validate_model_id: Product 1")

	def test_b_01_002_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=6,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],1)
		self.assertEqual(all_products.get(6),
			validation["result"])
		print("Test b_1_2: validate_model_id: Product 6")

	def test_b_01_003_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=5.5,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],1)
		self.assertEqual(all_products.get(5),
			validation["result"])
		print("Test b_1_3: validate_model_id: Product 5.5")

	def test_b_01_004_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id="3",
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],1)
		self.assertEqual(all_products.get(3),
			validation["result"])
		print("Test b_1_4: validate_model_id: Product '3'")

	def test_b_01_005_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id="i",
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],3)
		self.assertEqual("product id can not be"+
			" converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_1_5: validate_model_id: Product i")

	def test_b_01_006_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=0,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],3)
		self.assertEqual("product id can not be less than"+
			" or equal to 0"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_1_6: validate_model_id: Product 0")

	def test_b_01_007_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=-1,
			model_query=all_products,model_name_string="product")
		self.assertEqual(validation["case"],3)
		self.assertEqual("product id can not be less than"+
			" or equal to 0"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_1_7: validate_model_id: Product -1")

	def test_b_01_008_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=20,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],2)
		self.assertEqual("there is no product with this id"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_1_8: validate_model_id: Product 20")

	def test_b_01_009_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=None,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],4)
		self.assertEqual({'status': 400, 'description': 'product is missing'},
			validation["result"])
		print("Test b_1_9: validate_model_id: Product None")

	def test_b_01_010_validate_model_id(self):
		all_orders = Order.query
		validation = validate_model_id(input_id=3,
			model_query=all_orders,
			model_name_string="order")
		self.assertEqual(validation["case"],1)
		self.assertEqual(all_orders.get(3),
			validation["result"])
		print("Test b_1_10: validate_model_id: Order 7")












	def test_b_02_001_validate_string(self):
		to_validate = "to validate"
		validation = validate_string(
			input_string=to_validate,max_length=100,
			string_name="data")
		self.assertEqual(validation["case"],1)
		self.assertEqual("to validate",
			validation["result"])
		print("Test b_2_1: validate_string: 'to validate'")

	def test_b_02_002_validate_string(self):
		to_validate = 1
		validation = validate_string(
			input_string=to_validate,max_length=100,
			string_name="data")
		self.assertEqual(validation["case"],1)
		self.assertEqual("1",
			validation["result"])
		print("Test b_2_2: validate_string: '1'")

	def test_b_02_003_validate_string(self):
		to_validate = "More Than 3"
		validation = validate_string(
		input_string=to_validate,max_length=3,
			string_name="input")		
		self.assertEqual(validation["case"],2)
		self.assertEqual("maximum input length is 3 letters"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_2_3: validate_string:"+
			" More than max length")

	def test_b_02_004_validate_string(self):
		to_validate = None
		validation = validate_string(
		input_string=to_validate,max_length=3,
			string_name="input")		
		self.assertEqual(validation["case"],3)
		self.assertEqual(validation["result"],None)
		print("Test b_2_4: validate_string:"+
			" None")









	def test_b_3_001_validate_boolean(self):
		validation = validate_boolean(input_boolean=True,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_1: validate_boolean: True")

	def test_b_3_002_validate_boolean(self):
		validation = validate_boolean(input_boolean="True",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_2: validate_boolean: 'True'")

	def test_b_3_003_validate_boolean(self):
		validation = validate_boolean(input_boolean="true",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_3: validate_boolean: 'true'")

	def test_b_3_004_validate_boolean(self):
		validation = validate_boolean(input_boolean=1,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_4: validate_boolean: 1")

	def test_b_3_005_validate_boolean(self):
		validation = validate_boolean(input_boolean="1",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_5: validate_boolean: '1'")

	def test_b_3_006_validate_boolean(self):
		validation = validate_boolean(input_boolean=False,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_6: validate_boolean: False")

	def test_b_3_007_validate_boolean(self):
		validation = validate_boolean(input_boolean="False",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_7: validate_boolean: 'False'")

	def test_b_3_008_validate_boolean(self):
		validation = validate_boolean(input_boolean="false",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_8: validate_boolean: 'false'")

	def test_b_3_009_validate_boolean(self):
		validation = validate_boolean(input_boolean=0,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_9: validate_boolean: 0")

	def test_b_3_010_validate_boolean(self):
		validation = validate_boolean(input_boolean="0",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_10: validate_boolean: '0'")

	def test_b_3_011_validate_boolean_wrong(self):
		validation = validate_boolean(input_boolean="5",
			input_name_string="variable")
		self.assertEqual(validation["case"],2)
		self.assertEqual("variable can not be "+
			"converted to boolean"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_3_11: validate_boolean_wrong:"+
			" '5'")

	def test_b_3_012_validate_boolean(self):
		validation = validate_boolean(input_boolean=None,
			input_name_string="variable")
		self.assertEqual(validation["case"],3)
		self.assertEqual(None,validation["result"])
		print("Test b_3_12: validate_boolean: None")










	def test_b_4_001_validate_integer(self):
		validation = validate_integer(input_integer=5,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_4_1: validate_integer: 5")

	def test_b_4_002_validate_integer(self):
		validation = validate_integer(input_integer=5.0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_4_2: validate_integer: 5.0")

	def test_b_4_003_validate_integer(self):
		validation = validate_integer(input_integer="5.0",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_4_3: validate_integer: '5.0'")

	def test_b_4_004_validate_integer_wrong(self):
		validation = validate_integer(input_integer="i",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_4_4: validate_integer: i")

	def test_b_4_005_validate_integer(self):
		validation = validate_integer(input_integer=0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(0.0,validation["result"])
		print("Test b_4_5: validate_integer: 0")

	def test_b_4_006_validate_integer_wrong(self):
		validation = validate_integer(input_integer=-40,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be less than"+
			" 0"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_4_6: validate_integer: -40")

	def test_b_4_007_validate_integer_wrong(self):
		validation = validate_integer(input_integer=4,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be more than"+
			" 3"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_4_7: validate_integer: >max")

	def test_b_4_008_validate_integer_wrong(self):
		validation = validate_integer(input_integer=None,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],3)
		self.assertEqual(None
			,validation["result"])
		print("Test b_4_8: validate_integer: None")

























	def test_b_5_001_validate_float(self):
		validation = validate_float(input_float=5,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_5_1: validate_float: 5")

	def test_b_5_002_validate_float(self):
		validation = validate_float(input_float=5.0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_5_2: validate_float: 5.0")

	def test_b_5_003_validate_float(self):
		validation = validate_float(input_float="5.0",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_5_3: validate_float: '5.0'")

	def test_b_5_004_validate_float_wrong(self):
		validation = validate_float(input_float="i",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be converted to float"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_5_4: validate_float: i")

	def test_b_5_005_validate_float(self):
		validation = validate_float(input_float=0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(0.0,validation["result"])
		print("Test b_5_5: validate_float: 0")

	def test_b_5_006_validate_float_wrong(self):
		validation = validate_float(input_float=-40,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be less than"+
			" 0"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_5_6: validate_float: -40")

	def test_b_5_007_validate_float_wrong(self):
		validation = validate_float(input_float=4,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be more than"+
			" 3"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_5_7: validate_float: >max")

	def test_b_5_008_validate_float_wrong(self):
		validation = validate_float(input_float=None,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],3)
		self.assertEqual(None
			,validation["result"])
		print("Test b_5_8: validate_float: None")


	def test_b_6_001_validate_base64(self):
		validation = validate_base64(input_string=None,
			input_name_string="input",maximum_length=4,
			minimum_length=0)
		self.assertEqual(validation,{"case":3,"result":None})
		
		validation = validate_base64(input_string=5,
			input_name_string="b64",maximum_length=4,
			minimum_length=0)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 is not a string","status":400}})

		validation = validate_base64(input_string="abcde",
			input_name_string="b64",maximum_length=4,
			minimum_length=0)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 length can not be more than 4 characters"
			,"status":422}})
		
		validation = validate_base64(input_string="a",
			input_name_string="b64",maximum_length=4,
			minimum_length=3)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 length can not be less than 3 characters"
			,"status":422}})
		
		validation = validate_base64(input_string="abcd",
			input_name_string="b64",maximum_length=4,
			minimum_length=3)
		self.assertEqual(validation,{"case":1,"result":"abcd"})
		
		validation = validate_base64(input_string="abcde",
			input_name_string="b64",maximum_length=8,
			minimum_length=3)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 can not be converted to base64"
			,"status":422}})
		
		validation = validate_base64(input_string="abc*",
			input_name_string="b64",maximum_length=8,
			minimum_length=3)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 can not be converted to base64"
			,"status":422}})
		
		validation = validate_base64(input_string="abcd",
			input_name_string="b64",maximum_length=8,
			minimum_length=3)
		self.assertEqual(validation,{"case":1,"result":"abcd"})
		print("Test b_6_1: validate_base64: None")


	def test_b_7_001_validate_formatting(self):		
		validation = validate_formatting(input_formatting="png")
		self.assertEqual(validation,{"case":1,"result":"png"})
		validation = validate_formatting(input_formatting="a")
		self.assertEqual(validation,{"case":2,"result":
			{"description":"minimum formatting length is 2 letters",
			"status":422}})
		validation = validate_formatting(input_formatting="abc")
		self.assertEqual(validation,{"case":2,"result":
			{"description":"abc is not allowed image format",
			"status":422}})
		print("Test b_7_1: validate_formatting:")







	def test_b_6_001_validate__must(self):
		validation = validate__must(input=5,type="f",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual(5.0,validation["result"])
		print("Test b_6_1: validate__must float: 5")

	def test_b_6_002_validate__must(self):
		validation = validate__must(input="unknown",type="f",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data can not be converted to float"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_6_2: validate__must float: 'i'")

	def test_b_6_003_validate__must(self):
		validation = validate__must(input=5,type="i",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual(5,validation["result"])
		print("Test b_6_3: validate__must integer: 5")

	def test_b_6_004_validate__must(self):
		validation = validate__must(input="unknown",type="i",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data can not be converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_6_4: validate__must integer: 'i'")

	def test_b_6_005_validate__must(self):
		validation = validate__must(input=True,type="b",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual(True,validation["result"])
		print("Test b_6_5: validate__must boolean: True")

	def test_b_6_006_validate__must(self):
		validation = validate__must(input="unknown",type="b",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data can not be converted to boolean"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_6_6: validate__must boolean: 'unknown'")

	def test_b_6_007_validate__must(self):
		validation = validate__must(input="dddaaatta",type="s",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual("dddaaatta",validation["result"])
		print("Test b_6_7: validate__must string: 'dddaaatta'")

	def test_b_6_008_validate__must(self):
		try:
			validation = validate__must(input="1",type="wrong",
			input_name_string="my_data",maximum=1000,minimum=-5)
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(True,True)
		print("Test b_6_8: validate__must wrong type: 'wrong'")

	def test_b_6_009_validate__must(self):
		validation = validate__must(input=None,type="i",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		
		print("Test b_6_9: validate__must wrong input: None int")

	def test_b_6_010_validate__must(self):
		validation = validate__must(input=None,type="f",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		
		print("Test b_6_10: validate__must wrong input: None float")

	def test_b_6_011_validate__must(self):
		validation = validate__must(input=None,type="b",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		
		print("Test b_6_11: validate__must wrong input: None bool")

	def test_b_6_012_validate__must(self):
		validation = validate__must(input=None,type="s",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])	
		print("Test b_6_12: validate__must wrong input: None str")

	def test_b_6_013_validate__must(self):
		validation = validate__must(input="abcde",type="b64",
			input_name_string="b64",maximum=1000,minimum=-5)
		self.assertEqual(validation  ,{"case":False,"result":{"description":
		"b64 can not be converted to base64","status":422}})
		print("Test b_6_13: validate__must wrong input: wrong base64")

	def test_b_6_014_validate__must(self):
		validation = validate__must(input="abcd/+/=",type="b64",
			input_name_string="b64",maximum=1000,minimum=-5)
		self.assertEqual(validation  ,{"case":True,"result":"abcd/+/="})
		print("Test b_6_14: validate__must input: correct base64")

	def test_b_6_015_validate__must(self):
		validation = validate__must(input="png",type="frmt",
			input_name_string="formatting")
		self.assertEqual(validation  ,{"case":True,"result":"png"})
		validation = validate__must(input="abc",type="frmt",
			input_name_string="formatting")
		self.assertEqual(validation  ,{"case":False,"result":
			{"description":"abc is not allowed image format","status":422}})
		print("Test b_6_14: validate__must input: correct base64")




	def test_c_1_001_generate_jwt(self):
		payload = {"data":"test"}
		algorithm ='HS256'#HMAC-SHA 256
		secret = 'learning'
		encoded_jwt = jwt.encode(
			payload,secret,algorithm=algorithm)
		self.assertEqual(encoded_jwt,'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoidGVzdCJ9.WHBB33Ktq9mVKGspVK7uxpXxlwQngbyCirKKVX3nQY8')
		print("Test c_1_1: generate_jwt")


	def test_c_1_002_decode_jwt_correct(self):
		encoded_jwt=b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoidGVzdCJ9.WHBB33Ktq9mVKGspVK7uxpXxlwQngbyCirKKVX3nQY8'
		#This is a valid token 
		algorithm ='HS256'#HMAC-SHA 256
		secret = 'learning'
		payload = jwt.decode(encoded_jwt,secret,verify=True,algorithms="HS256")
		self.assertEqual(payload,{"data":"test"})
		print("Test c_1_2: decode_jwt_correct")


	def test_c_1_003_decode_jwt_wrong(self):
		encoded_jwt=b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoidGVzdCJ9.WHBB33Ktq'
		#This is a wrong token 
		algorithm ='HS256'#HMAC-SHA 256
		secret = 'learning'
		try:
			payload = jwt.decode(encoded_jwt,secret,verify=True,algorithms="HS256")
			self.assertEqual(True,False)
		except:
			self.assertEqual(True,True)
		print("Test c_1_3: decode_jwt_wrong")


	def test_c_1_004_bytes_to_string(self):
		b_s = str(b"abc",'utf-8')
		self.assertEqual(b_s,"abc")
		print("Test c_1_4: bytes_to_string")


	def test_c_1_005_datetimes(self):
		d = datetime(year=2005,month=3,day=4)
		#print(d)
		#2005-03-04 00:00:00
		now = datetime.now()
		#print(now)
		#2020-12-23 17:23:43.862041
		months_to_add,days_to_add=-1,3
		#print(now.month)
		#12		
		#future=datetime(year = now.year,
		#	month = now.month+months_to_add,
		#	day=now.day+days_to_add,
		#	hour=now.hour,minute=now.minute,
		#	second=now.second)
		#print(future)
		#2020-11-26 17:23:43
		#the future variable is not the right way to do it
		delta = timedelta(days=50,seconds=27,
		    minutes=5,hours=8,weeks=2)
		#print(delta)
		#64 days, 8:05:27
		example = datetime(year=2005,month=3,day=4)
		new_time=example+delta
		#print(new_time)
		#2005-05-07 08:05:27
		new_time_epoch=int(new_time.timestamp())
		#print(new_time_epoch)
		#1115445927
		new_time_returned=datetime.fromtimestamp(new_time_epoch)
		#print(new_time_returned)
		#2005-05-07 08:05:27
		print("Test c_1_5: datetime manipulation")











	def test_c_2_1_001_generate_jwt(self):
		payload={"a":"b"}
		secret="1"
		encoded = generate_jwt(payload,secret)
		self.assertEqual(encoded,
			{"success":True,"result":
			"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhIjoiYiJ9.C58TEpM7EJdnnZdAztvOCEhzP_sCYpd5nM2ThE_Lmrc"
			})
		print("Test c_2_1_1: generate_jwt")

	def test_c_2_1_002_generate_jwt_fail(self):
		payload='{"a":"b"}'
		#Wrong: This is a string of JSON
		#Not JSON itself 
		secret="1"
		encoded = generate_jwt(payload,secret)
		self.assertEqual(encoded["success"],False)
		print("Test c_2_1_2: generate_jwt_fail")



	def test_c_2_2_001_decode_jwt(self):
		token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhIjoiYiJ9.C58TEpM7EJdnnZdAztvOCEhzP_sCYpd5nM2ThE_Lmrc"
		#This token is verified
		secret = 1
		decoding = decode_jwt(
			encoded_jwt=token,secret=secret)
		self.assertEqual(decoding,
			{"success":True,"result":{"a":"b"}})
		print("Test c_2_2_1: decode_jwt")

	def test_c_2_2_002_decode_jwt_wrong(self):
		token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhIjoiYiJ9.C58TEpM7EJdn"
		#Wrong Token, wrong signature
		secret = 1
		decoding = decode_jwt(
			encoded_jwt=token,secret=secret)
		self.assertEqual(decoding["success"],False)
		print("Test c_2_2_2: decode_jwt_wrong")

	def test_c_2_2_003_decode_jwt_wrong(self):
		token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhIjoiYiJ9.C58TEpM7EJdnnZdAztvOCEhzP_sCYpd5nM2ThE_Lmrc"
		secret = 5
		#Wrong signature, Right Token
		decoding = decode_jwt(
			encoded_jwt=token,secret=secret)
		self.assertEqual(decoding["success"],False)
		print("Test c_2_2_3: decode_jwt_wrong")


	def test_c_2_3_001_generate_token(self):
		user_id = 5
		secret = "abcd"
		expiration= timedelta(days=7)
		issued_at=datetime.now()
		token = generate_token(user_id=user_id,secret=secret,
    		expiration_delta=expiration,
    		issued_at=datetime.now())
		#print(token["result"])
		#fslsdlf.akjdlakjslkjas.askjasdkjhads
		self.assertEqual(token["success"],True)
		decoded_jwt=decode_jwt(token["result"],secret)["result"]
		#print(decoded_jwt)
		#{'uid': 5, 'exp': 1609345799.712798}
		self.assertEqual(decoded_jwt["uid"],5)
		exp_datetime=issued_at+expiration
		self.assertEqual(decoded_jwt["exp"],
			exp_datetime.timestamp())
		print("Test c_2_3_1: generate_token")

	def test_c_2_3_002_generate_token_wrong(self):
		user_id = "abc"
		#user_id should be integer
		secret = "abcd"
		token = generate_token(user_id,secret)
		self.assertEqual(token["success"],False)
		self.assertEqual(token["result"]["status"],400)
		self.assertEqual(token["result"]["description"],
			"user_id can not be converted to integer")
		#user_id can not be converted to int
		print("Test c_2_3_2: generate_token_wrong")

	def test_c_2_3_003_generate_token_wrong(self):
		user_id = 0
		secret = "there"
		token = generate_token(user_id,secret)
		self.assertEqual(token["success"],False)
		self.assertEqual(token["result"]["status"],422)
		self.assertEqual(token["result"]["description"],
			"user_id can not be less than 1")
		#user_id can not be converted to int
		print("Test c_2_3_3: generate_token_wrong")



	def test_c_2_4_001_validate_token_wrong(self):
		wrong_token="a.b.c"
		secret="secret"
		token_validation=validate_token(wrong_token,secret)
		self.assertEqual(token_validation["case"],3)
		self.assertEqual(token_validation["token"],"")
		e1=token_validation["error"]
		e2=jwt.DecodeError('Invalid header padding')
		if type(e1) is type(e2) and e1.args==e2.args:
			self.assertEqual(True,True)
		else:
			self.assertEqual(True,False)
		#print(token_validation)
		#{'case': 3, 'token': '', 'error': 
		#DecodeError('Invalid header padding')}
		#DecodeError is not defined
		print("Test c_2_4_1: validate_token")

	def test_c_2_4_002_decode_jwt_wrong(self):
		secret="secret"
		payload={"userid":1}
		token=generate_jwt(payload,secret)
		token_validation=validate_token(token["result"],secret)
		self.assertEqual(token_validation["case"],3)
		self.assertEqual(token_validation["token"],"")
		self.assertEqual(token_validation["error"],
			"payload does not contain user_id")
		print("Test c_2_4_2: validate_token_wrong")

	def test_c_2_4_003_decode_jwt_wrong(self):
		secret="secret"
		payload={"uid":1}
		token=generate_jwt(payload,secret)
		token_validation=validate_token(token["result"],secret)
		self.assertEqual(token_validation["case"],3)
		self.assertEqual(token_validation["token"],"")
		self.assertEqual(token_validation["error"],
			"payload does not contain expiration_date")
		print("Test c_2_4_3: validate_token_wrong")

	def test_c_2_4_004_decode_jwt_wrong(self):
		secret="secret"
		payload={"uid":"abc","exp":"abc"}
		token=generate_jwt(payload,secret)
		token_validation=validate_token(token["result"],secret)
		self.assertEqual(token_validation["case"],3)
		self.assertEqual(token_validation["token"],"")
		e1=token_validation["error"]
		e2=jwt.DecodeError(
			'Expiration Time claim (exp) must be an integer.')
		if type(e1) is type(e2) and e1.args==e2.args:
			self.assertEqual(True,True)
		else:
			self.assertEqual(True,False)
		print("Test c_2_4_4: validate_token_wrong")

	def test_c_2_4_005_decode_jwt_wrong(self):
		secret="secret"
		expiration = (datetime.now()+
			timedelta(days=7)).timestamp()
		payload={"uid":"abc","exp":expiration}
		token=generate_jwt(payload,secret)
		#print(token)

		token_validation=validate_token(
			token["result"],secret)
		self.assertEqual(token_validation["case"],3)
		self.assertEqual(token_validation["token"],"")
		self.assertEqual(token_validation["error"],
			"user id can not be converted to integer")
		print("Test c_2_4_5: validate_token_wrong")

	def test_c_2_4_006_decode_jwt_wrong(self):
		secret="secret"
		
		expiration = (datetime.now()-timedelta(days=7)).timestamp()
		payload={"uid":1,"exp":expiration}
		token=generate_jwt(payload,secret)
		token_validation=validate_token(token["result"],secret)
		#print(token_validation)
		#validate token does not refresh expired tokens any more
		self.assertEqual(token_validation["case"],2)
		self.assertNotEqual(token_validation["token"],
			token["result"])
		self.assertEqual(token_validation["error"],"expired token")
		"""correct_token = token_validation["token"]
		print(correct_token)
		token_validation=validate_token(correct_token,secret)
		#self.assertEqual(token_validation["case"],1)
		#self.assertEqual(token_validation["token"],correct_token)
		self.assertEqual(token_validation["error"],"")
		#ExpiredSignatureError is not defined"""
		print("Test c_2_4_6: validate_token_wrong")

	def test_c_2_4_007_decode_jwt_correct(self):
		secret="secret"
		expiration = (datetime.now()+timedelta(days=7)).timestamp()
		payload={"uid":1,"exp":expiration}
		token=generate_jwt(payload,secret)
		token_validation=validate_token(token["result"],secret)
		self.assertEqual(token_validation["case"],1)
		self.assertEqual(token_validation["token"],token["result"])
		self.assertEqual(token_validation["error"],"")
		print("Test c_2_4_7: validate_token_correct")

	def test_c_2_4_008_generate_jwt(self):
		secret=secrets.token_urlsafe(10000)
		expiration = (datetime.now()+timedelta(days=7)).timestamp()
		payload={"uid":1,"exp":expiration}
		token=generate_jwt(payload=payload,secret=secret)
		#print("secret: "+str(secret))
		#print("______________")
		#print("token: "+str(token))
		#print("______________")
		#print("encoded: "+
		#	str(jwt.encode(payload,secret,algorithm="HS256")))
		token_validation=validate_token(token["result"],secret)
		#print(token_validation)
		self.assertEqual(token_validation["case"],1)
		self.assertEqual(token_validation["token"],token["result"])
		self.assertEqual(token_validation["error"],"")
		print("Test c_2_4_8: validate_token_correct")

	def test_c_2_4_009_generate_from_random(self):
		secret=str(secrets.token_urlsafe(5000))
		token=generate_token(user_id=1,secret=secret)
		token_validation=validate_token(
			token["result"],secret)
		#print(token_validation)
		self.assertEqual(token_validation["case"],1)
		self.assertEqual(token_validation["token"],token["result"])
		self.assertEqual(token_validation["error"],"")
		print("Test c_2_4_9: generate token random")


	def test_c_2_5_001_is_base64(self):
		self.assertEqual(isBase64("abcd"),True)
		self.assertEqual(isBase64("1234"),True)
		self.assertEqual(isBase64("123"),False) # Not 4 chars
		self.assertEqual(isBase64("123="),True)
		self.assertEqual(isBase64("123*"),False)
		print("Test c_2_5_1: isBase64")

	def test_c_2_6_001_b64_to_image(self):
		self.assertEqual(b64ToImg("abcd","png"),"data:image/png;base64,abcd")
		self.assertEqual(b64ToImg("1234","jpg"),"data:image/jpg;base64,1234")
		print("Test c_2_5_1: isBase64")










# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()