import unittest
from models import (NotReceived, validate_key,
MyModel, User, Product, Order, #Image,
	populate_tables, db_drop_and_create_all,get_dict, get_in_stock_products)
from app import create_app
from __init__ import db


unittest.TestLoader.sortTestMethodsUsing = None

class modelsTestCase(unittest.TestCase):
	"""This class represents the trivia test case"""

	def setUp(self):
		#db_drop_and_create_all()
		create_app()
		# create and configure the app
		#self.app = create_app(testing=True) #Flask(__name__)
		#self.client = self.app.test_client
		#db.app = self.app
		#db.init_app(self.app)
		#db.create_all()
		pass

	def tearDown(self):
		"""Executed after reach test"""
		print("_+++++++++++++++++++++++++++++++++_")

	#Note: Tests are run alphapetically
	def test_001_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")


	def test_002_test(self):
		db_drop_and_create_all()
		print("Test 2:db_drop_and_create_all")


	def test_0a_1_1_1_validate_key(self):
		the_dict = {"id":41,"password":"abc","username":"tryu","bool1":True,"bool2":False,
		"nr":NotReceived()}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key))
		self.assertEqual([False,False,True,True,True,False],validated)
		print("Test 0a_1_1_1 : validate_key: success")

	def test_0a_1_1_2_validate_key(self):
		the_dict = {"id":41,"password":"abc","username":"tryu","bool1":True,"bool2":False,
		"nr":NotReceived()}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,id=True))
		self.assertEqual([True,False,True,True,True,False],validated)
		print("Test 0a_1_1_2 : validate_key: success")

	def test_0a_1_1_3_validate_key(self):
		the_dict = {"id":41,"password":"abc","username":"tryu","bool1":True,"bool2":False,
		"nr":NotReceived()}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,dangerous = True))
		self.assertEqual([False,True,True,True,True,False],validated)
		print("Test 0a_1_1_3 : validate_key: success")

	def test_0a_1_1_4_validate_key(self):
		the_dict = {"id":41,"password":"abc","username":"tryu","bool1":True,"bool2":False,
		"nr":NotReceived()}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,dangerous = True))
		self.assertEqual([False,True,True,True,True,False],validated)
		print("Test 0a_1_1_4 : validate_key: success")

	def test_0a_1_1_5_validate_key(self):
		the_dict = {"iD":41,"password":"abc","username":"tryu","bool1":True,"bool2":False,
		"nr":NotReceived(), "unsupported":{}}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,dangerous = True, unsupported=True))
		#print(validated)
		self.assertEqual([False,True,True,True,True,False,False],validated)
		print("Test 0a_1_1_5 : validate_key: success")

	def test_0a_1_1_6_validate_key(self):
		user = User(username = "abc", password = "pass")
		the_dict = {"ID":41,"password":"abc","username":"tryu","bool1":True,"bool2":False,
		"nr":NotReceived(), "unsupported1":{}, "unsupported2":user}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key,dangerous = True, unsupported=True))
		#print(validated)
		self.assertEqual([False,True,True,True,True,False,False,True],validated)
		print("Test 0a_1_1_6 : validate_key: success")

	def test_0a_1_1_7_validate_key(self):
		user = User(username = "abc", password = "pass")
		the_dict = {"Id":41,"paSSword":"abc","username":"tryu","bool1":True,"bool2":False,
		"nr":NotReceived(), "unsupported1":{}, "unsupported2":user}
		validated = []
		for key in the_dict:
			validated.append(validate_key(the_dict,key, unsupported=False))
		self.assertEqual([False,False,True,True,True,False,False,False],validated)
		print("Test 0a_1_1_7 : validate_key: success")

	def test_0a_1_1_8_validate_key(self):
		user = User(username = "abc", password = "pass")
		class tst(object):
			def __init__(self):
				self.Id = 41
				self.paSSword = "abc"
				self.username = "tryu"
				self.bool1 = True
				self.bool2 = False
				self.nr = NotReceived()
				self.unsupported1 = {}
				self.unsupported2 = user
		validation_obj = tst()
		validated = []
		for key in ["Id","paSSword","username","bool1","bool2","nr","unsupported1",
				"unsupported2"]:
			validated.append(validate_key(validation_obj,key, unsupported=False))
		self.assertEqual([False,False,True,True,True,False,False,False],validated)
		print("Test 0a_1_1_8 : validate_key: with object")


	def test_0a_1_2_1_get_dict(self):
		user = User(username = "abc", password = "pass")
		class tst(object):
			def __init__(self):
				self.Id = 41
				self.paSSword = "abc"
				self.username = "tryu"
				self.bool1 = True
				self.bool2 = False
				self.nr = NotReceived()
				self.unsupported1 = {}
				self.unsupported2 = user
		validation_obj = tst()
		the_dict = get_dict(validation_obj)
		self.assertEqual(the_dict,{"username":"tryu","bool1":True,"bool2":False})
		the_dict = get_dict(validation_obj, id=True,dangerous=True)
		self.assertEqual(the_dict,{"username":"tryu","bool1":True,"bool2":False,
			"paSSword":"abc","Id":41})
		print("Test 0a_1_2_1 : get_dict: with object")

	def test_0a_1_2_2_get_dict(self):
		user = User(username = "abc", password = "pass")
		the_dict = get_dict(user, id=True,dangerous=True)
		user.insert()
		the_dict = get_dict(user, id=True,dangerous=True)
		self.assertEqual(the_dict,{"username":"abc","password":"pass","id":1})
		user.delete()
		print("Test 0a_1_2_2 : get_dict: with object")

	def test_0a_1_2_3_get_dict(self):
		user = User(username = "abc", password = "pass")
		the_dict = {"Id":41,"paSSword":"abc","username":"tryu","bool1":True,"bool2":False,
		"nr":NotReceived(),"unsupported1":{},"unsupported2":user}
		validated = get_dict(the_dict, id=True,dangerous=True)
		self.assertEqual(validated,{"username":"tryu","bool1":True,"bool2":False,
			"paSSword":"abc","Id":41})

		validated = get_dict(the_dict)
		self.assertEqual(validated,{"username":"tryu","bool1":True,"bool2":False})
		print("Test 0a_1_2_3 : get_dict: with dict")











	def test_0a_1_2_1_MyModel(self):
		user = User(username = "abc",password="456")
		self.assertEqual(user.username,"abc")
		self.assertEqual(user.password,"456")
		print("Test 0a_1_2_1 : MyModel: success")

	def test_0a_1_2_2_MyModel(self):
		try:
			user = User(username = "abc",password="456", bla=789)
		except Exception as e:
			self.assertEqual(str(e),"'bla' is an invalid keyword argument for User")
		print("Test 0a_1_2_2 : MyModel: success")

	def test_0a_1_2_3_MyModel(self):
		user = User(username = "abc",password="abc")
		self.assertEqual(user.simple(),{"username":"abc","id":None})
		user.insert()
		self.assertEqual(user.simple(),{"username":"abc","id":1})
		prod = Product(name="789",price=123,seller_id=1)
		self.assertEqual(prod.simple(),{"name":"789","price":123,
			"seller_id":1,"id":None,"in_stock":None,"seller":None})
		prod.insert()
		self.assertEqual(prod.simple(),{"name":"789","price":123,
			"seller_id":1,"id":1,"in_stock":True})
		prod.delete()
		user.delete()
		print("Test 0a_1_2_3 : MyModel: success")

	def test_0a_1_2_4_MyModel(self):
		#Trying to add the user with id, and seeing how the d will be neglected
		user = User(username = "abc",password="abc",id=1000000000000000)
		self.assertEqual(user.simple(),{"username":"abc","id":None})
		print("Test 0a_1_2_3 : MyModel: success")

	def test_0a_1_2_5_MyModel(self):
		user = User(username = "abc",password="456")
		db.session.add(user)
		db.session.commit()
		self.assertEqual(user.password,"456")
		print("Test 0a_1_2_5 : MyModel: success")

	def test_0a_1_3_1_MyModel(self):
		db_drop_and_create_all()
		# Creating the user
		user_to_del = User(username = "abc",password="456")
		db.session.add(user_to_del)
		db.session.commit()
		self.assertEqual(len(User.query.all()),1)

		prod_to_del1 = Product(name = "abc",price=456,seller_id=user_to_del.id)
		prod_to_del2 = Product(name = "abcdef",price=4567,seller_id=user_to_del.id)
		db.session.add_all([prod_to_del1,prod_to_del2])
		db.session.commit()
		self.assertEqual(len(Product.query.all()),2)

		order_to_del1 = Order(
			user_id = user_to_del.id,product_id=prod_to_del1.id,amount=1)
		order_to_del2 = Order(
			user_id = user_to_del.id,product_id=prod_to_del2.id,amount=3)
		order_to_del3 = Order(
			user_id = user_to_del.id,product_id=prod_to_del2.id,amount=5)
		db.session.add_all([order_to_del1,order_to_del2,order_to_del3])
		db.session.commit()
		self.assertEqual(len(Order.query.all()),3)

		#img_to_delete1=Image(seller_id=1,name="abc",formatting = "png")
		#img_to_delete2=Image(seller_id=1,name="abce",formatting = "jpg")
		#db.session.add_all([img_to_delete1,img_to_delete2])
		#db.session.commit()
		#self.assertEqual(len(Image.query.all()),2)

		# Trying to delete

		#img_to_delete2.delete()
		#self.assertEqual(len(Image.query.all()),1)
		order_to_del3.delete()
		self.assertEqual(len(Order.query.all()),2)
		prod_to_del2.delete()
		self.assertEqual(len(Order.query.all()),1)
		self.assertEqual(len(Product.query.all()),1)
		user_to_del.delete()
		#self.assertEqual(len(Image.query.all()),0)
		self.assertEqual(len(Order.query.all()),0)
		self.assertEqual(len(Product.query.all()),0)
		self.assertEqual(len(User.query.all()),0)

		print("Test 0a_1_3_1 : MyModel: relationships")


	def test_0a_1_4_1_MyModel(self):
		# Testing update
		# Creating the user
		user_to_del = User(username = "abc",password="456")
		user_to_del.insert()
		user_dict = get_dict(user_to_del,id=True,dangerous=True)
		self.assertEqual(user_dict,{"id":1,"username":"abc","password":"456"})
		user_to_del.update(id=14,username="478",password = "prt")
		user_dict = get_dict(user_to_del,id=True,dangerous=True)
		self.assertEqual(user_dict,{"id":1,"username":"478","password":"prt"})
		user_to_del.delete()
		print("Test 0a_1_4_1 : MyModel: update")

	def test_0a_1_5_1_MyModel_deep(self):
		# Testing update
		# Creating the user
		user_to_del = User(username = "abc",password="456")
		user_to_del.insert()
		prod = Product(name="789",price=123,seller_id=1)
		prod.insert()
		self.assertEqual(user_to_del.deep(),
			{'id': 1, #'images': [],
			'orders': [], 'products':
			[{'id': 1, 'in_stock': True, 'name': '789', 'price': 123.0,
			 'seller_id': 1}], 'username': 'abc'})
		self.assertEqual(prod.deep(),{'id': 1, 'in_stock': True,
			'name': '789', 'orders': [], 'price': 123.0, 'seller':
			{'id': 1, 'username': 'abc'}, 'seller_id': 1})
		print("Test 0a_1_5_1 : MyModel: deep")
















	def test_a_1_000_user_intro(self):
		print("")
		print("")
		print("_+++++++++++++++++++++++++++++++++_")
		print("_+++++++++++++++++++ Models : 1 ) User ++_")
		print("_+++++++++++++++++++++++++++++++++_")
		print("")
		print("")

	def test_a_1_001_user_insert(self):
		db_drop_and_create_all()
		user1 = User(username = "useeer1",password="45687")
		user1.insert()
		users = User.query.all()

		self.assertEqual(len(users),1)
		print("Test a_1_1: user insert")


	def test_a_1_002_user_update(self):
		user1 = User.query.get(1)
		#user1.name = "modified"
		user1.update(name="modified")
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
		"""for image in user.images:
			self.assertEqual(type(image.id),int)
			self.assertEqual(type(image.seller_id),int)
			self.assertEqual(type(image.name),str)
			self.assertEqual(type(image.formatting),str)"""
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
		#images_before = len(Image.query.all())

		#adding a new user
		usr_to_del = User(username="aklmnopq",password="123456789")
		db.session.add(usr_to_del)
		db.session.commit()
		self.assertEqual(len(User.query.all()),users_before+1)
		#adding a new product
		prod_to_del = Product(name="Labtopppp",
			price=3000, seller_id=7)
		db.session.add(prod_to_del)
		db.session.commit()


		self.assertEqual(len(Product.query.all()),products_before+1)

		#adding a new order
		ordr_to_del = Order(user_id=usr_to_del.id, product_id=1, amount=1)
		db.session.add(ordr_to_del)
		db.session.commit()
		self.assertEqual(len(Order.query.all()),orders_before+1)

		#adding a new image
		#img_to_del = Image(seller_id=usr_to_del.id, name="Labtopfgfgfg",
		#	formatting="png")
		#db.session.add(img_to_del)
		#db.session.commit()

		#self.assertEqual(len(Image.query.all()),images_before+1)
		#print(usr_to_del.deep())
		usr_to_del.delete()
		self.assertEqual(len(User.query.all()),users_before)
		self.assertEqual(len(Product.query.all()),products_before)
		self.assertEqual(len(Order.query.all()),orders_before)
		#self.assertEqual(len(Image.query.all()),images_before)

		print("Test a_1_10: user delete relationships")

	def test_a_1_011_user_deep(self):
		#measuring lengths beofre actions
		usr = User.query.get(6)
		self.assertEqual(usr.deep(),
			{'id': 6,
			'orders': [], 'products': [],
			'username': 'water'})
		print("Test a_1_11: user deep")


























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
		#product1.name = "modified"
		product1.update(name="modified")
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

		#db.session.rollback()

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
			self.assertEqual(product["in_stock"],True)
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

	def test_a_2_011_product_deep(self):
		#measuring lengths beofre actions
		self.assertEqual(Product.query.get(3).deep(),
			{'id': 3, 'in_stock': True, 'name': 'Candy',
			'orders': [{'amount': 5, 'id': 6, 'product_id': 3,
			'user_id': 2}], 'price': 0.5, 'seller': {'id': 3,
			'username': 'klmn'}, 'seller_id': 3})
		print("Test a_2_11: product deep")














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


	#amount = 0 is the function of pydantic
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
		order1.update(amount = 2)
		order_1 = Order.query.get(1)

		self.assertEqual(order_1.amount,2)
		print("Test a_3_4: Order update")


	#This is the function of pydantic
	#This will not be done on the level of SQLAlchemy
	def test_a_3_005_order_update_wrong(self):
		before = len(Order.query.all())
		order1 = Order.query.get(8)
		order1.update(amount=0)
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
		print("Test a_3_10:order relationship_product")

	"""
	In the update there is no attribute called get_dict

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

		print("Test a_3_11: Order get_dict")"""

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

		print("Test a_3_12:order relationship_product_delete")

	def test_a_3_013_order_deep(self):
		self.assertEqual(Order.query.get(1).deep(),
			{'amount': 2, 'buyer': {'id': 1, 'username': 'abc'},
			'id': 1, 'product': {'id': 1, 'in_stock': True,
			'name': 'Labtop', 'price': 300.0, 'seller_id': 1},
			'product_id': 1, 'user_id': 1}
			)
		print("Test a_3_13: order deep")


	"""def test_a_4_000_image_intro(self):
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
		#image1.name = "Mouse"
		image1.update(name="Mouse")
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

	def test_a_4_008_image_deep(self):
		self.assertEqual(Image.query.get(1).deep(),
			{'formatting': 'png', 'id': 1, 'name': 'Mouse',
			'seller': {'id': 1, 'username': 'abc'}, 'seller_id': 1})
		print("Test a_4_08: image deep")"""

	"""
	get dict is deprecated

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
		print("Test a_4_8: Image get_dict")"""
























# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()
