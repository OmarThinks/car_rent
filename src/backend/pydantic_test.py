import unittest
from pydantic_models import (UserPost, UserUpdatePassword, UserLogin,
#ProductPost,#OrderPost, OrderUpdate,
validate_model_id,
validate_model_id_pydantic, TestHere)
import json
from models import NotReceived, populate_tables, User#, Product
from app import create_app

from pydantic import ValidationError

import base64

unittest.TestLoader.sortTestMethodsUsing = None


class pydanticTestCase(unittest.TestCase):
	"""This class represents the trivia test case"""

	def setUp(self):
		#db_drop_and_create_all()

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
	def test_000001_test(self):
		# Creating the app
		create_app()

		# Populating
		populate_tables()
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")



	def test_a_1_1_validate_model_id(self):
		# Model exists
		self.assertEqual(validate_model_id(User,1),True)
		# Model does not exist
		self.assertEqual(validate_model_id(User,10000000000),False)
		try:
			# model is not model
			validate_model_id(123,10000000000)
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(str(e),"validate_model_id:expected the type "+
				"of SQLAlchemy, but found the type of <class 'int'> instead")
		print("Test a_1_1: validate_model_id success")


	def test_a_1_2_validate_model_id_pydantic(self):
		# Model exists: nOo errors raised
		validate_model_id_pydantic(User,1)
		try:
			# Model does not exist
			self.assertEqual(validate_model_id_pydantic(User,10000000000),False)
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(str(e),"there is no User with this id: 10000000000")
		try:
			# model is not model
			validate_model_id(123,10000000000)
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(str(e),"validate_model_id:expected the type "+
				"of SQLAlchemy, but found the type of <class 'int'> instead")
		print("Test a_1_2: validate_model_id success")









	def test_b_001_01_1_UserPost(self):
		toValidate = {"username":123,"password1":7890123456,"password2":"7890123456"}
		user = UserPost(**toValidate)
		self.assertEqual(user.dict(),{"username":"123","password1":"7890123456",
			"password2":"7890123456"})
		print("Test b_1_1_1:UserPost Successful")

	def test_b_001_01_2_UserPost(self):
		toValidate = {}
		try:
			user = UserPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": ["username"],
				"msg": "field required","type": "value_error.missing"},
				{"loc": ["password1"],"msg": "field required",
				"type": "value_error.missing"
				},{"loc": ["password2"],"msg": "field required",
				"type": "value_error.missing"
				}])
		print("Test b_1_1_2:UserPost:Fail:all missing required")

	def test_b_001_01_3_UserPost(self):
		toValidate = {"password1":{},"username":{},"password2":{}}
		try:
			user = UserPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": ["username"],
				"msg": "str type expected","type": "type_error.str"},{"loc": [
				"password1"],"msg": "str type expected","type": "type_error.str"
				},{"loc": ["password2"],"msg": "str type expected",
				"type": "type_error.str"}])
		print("Test b_1_1_3:UserPost:Fail:not string")


	def test_b_001_01_4_UserPost(self):
		# username contains spaces
		# password mismatch
		# passwords lebgth less than 8
		# Note, did not notice password mismatch,
		# because password 1 did not pass the validation
		toValidate = {"username":"My Name","password1":"123","password2":"789"}
		try:
			user = UserPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			# print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": ["username"],
				"msg": "username should not contain a space",
				"type": "value_error"},{"loc": ["password1"],
				"msg": "ensure this value has at least 5 characters",
				"type": "value_error.any_str.min_length","ctx": {
				"limit_value": 5}},{"loc": ["password2"],
				"msg": "ensure this value has at least 5 characters",
				"type": "value_error.any_str.min_length","ctx": {
				"limit_value": 5}}])
		print("Test b_1_1_4:UserPost:Fail:username contains spaces, short password")

	def test_b_001_01_5_UserPost(self):
		# password mismatch
		# Username already exists
		toValidate = {"username":"abc","password1":"123456789999999000000000",
		"password2":"12345678"}
		try:
			user = UserPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{
				'loc': ['username'], 'msg': 'this username already exists',
				'type': 'value_error'}, {'loc': ['password2'], 'msg':
				'passwords do not match', 'type': 'value_error'}])
		print("Test b_1_1_5:UserPost:Fail:password mismatch")

	def test_b_001_01_6_UserPost(self):
		# adding unknown attribute
		# This attribute will not be returned
		# Testing White spaces
		toValidate = {"username":" MyName ","password1":"12345678",
		"password2":"12345678", "unknown":"abc"}
		user = UserPost(**toValidate)
		self.assertEqual(user.dict(),{"username":"MyName","password1":"12345678",
		"password2":"12345678"})
		print("Test b_1_1_6:UserPost:Added unknown value:Cleaned")








	def test_b_001_02_1_UserUpdatePassword(self):
		toValidate = {"password1":7890123456,"password2":"7890123456"}
		user = UserUpdatePassword(**toValidate)
		self.assertEqual(user.dict(),{"password1":"7890123456",
			"password2":"7890123456"})
		print("Test b_1_2_1:UserUpdatePassword Successful")

	def test_b_001_02_2_UserUpdatePassword(self):
		toValidate = {}
		try:
			user = UserUpdatePassword(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[
				{"loc": ["password1"],"msg": "field required","type": "value_error.missing"
				},{"loc": ["password2"],"msg": "field required","type": "value_error.missing"
				}])
		print("Test b_1_2_2:UserUpdatePassword:Fail:all missing required")

	def test_b_001_02_3_UserUpdatePassword(self):
		toValidate = {"password1":{},"password2":{}}
		try:
			user = UserUpdatePassword(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": [
				"password1"],"msg": "str type expected","type": "type_error.str"
				},{"loc": ["password2"],"msg": "str type expected",
				"type": "type_error.str"}])
		print("Test b_1_2_3:UserUpdatePassword:Fail:not string")


	def test_b_001_02_4_UserUpdatePassword(self):
		# username contains spaces
		# password mismatch
		# passwords lebgth less than 8
		# Note, did not notice password mismatch,
		# because password 1 did not pass the validation
		toValidate = {"password1":"123","password2":"789"}
		try:
			user = UserUpdatePassword(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": ["password1"
				],"msg": "ensure this value has at least 5 characters",
				"type": "value_error.any_str.min_length",
				"ctx": {"limit_value": 5}},{"loc": ["password2"],
				"msg": "ensure this value has at least 5 characters",
				"type": "value_error.any_str.min_length",
				"ctx": {"limit_value": 5}}])
		print("Test b_1_2_4:UserUpdatePassword:Fail:short password")

	def test_b_001_02_5_UserUpdatePassword(self):
		# password mismatch
		toValidate = {"password1":"123456789999999000000000",
		"password2":"12345678"}
		try:
			user = UserUpdatePassword(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['password2'], 'msg': 'passwords do not match', 'type': 'value_error'}])
		print("Test b_1_2_5:UserUpdatePassword:Fail:password mismatch")

	def test_b_001_02_6_UserUpdatePassword(self):
		# adding unknown attribute
		# This attribute will not be returned
		toValidate = {"password1":"12345678",
		"password2":"12345678", "unknown":"abc"}
		user = UserUpdatePassword(**toValidate)
		self.assertEqual(user.dict(),{"password1":"12345678",
		"password2":"12345678"})
		print("Test b_1_2_6:UserUpdatePassword:Added unknown value:Cleaned")









	def test_b_001_01_1_UserPost(self):
		toValidate = {"username":123,"password1":7890123456,"password2":"7890123456"}
		user = UserPost(**toValidate)
		self.assertEqual(user.dict(),{"username":"123","password1":"7890123456",
			"password2":"7890123456"})
		print("Test b_1_1_1:UserPost Successful")

	def test_b_001_01_2_UserPost(self):
		toValidate = {}
		try:
			user = UserPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": ["username"],
				"msg": "field required","type": "value_error.missing"},
				{"loc": ["password1"],"msg": "field required",
				"type": "value_error.missing"
				},{"loc": ["password2"],"msg": "field required",
				"type": "value_error.missing"
				}])
		print("Test b_1_1_2:UserPost:Fail:all missing required")

	def test_b_001_01_3_UserPost(self):
		toValidate = {"password1":{},"username":{},"password2":{}}
		try:
			user = UserPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": ["username"],
				"msg": "str type expected","type": "type_error.str"},{"loc": [
				"password1"],"msg": "str type expected","type": "type_error.str"
				},{"loc": ["password2"],"msg": "str type expected",
				"type": "type_error.str"}])
		print("Test b_1_1_3:UserPost:Fail:not string")


	def test_b_001_01_4_UserPost(self):
		# username contains spaces
		# password mismatch
		# passwords lebgth less than 8
		# Note, did not notice password mismatch,
		# because password 1 did not pass the validation
		toValidate = {"username":"My Name","password1":"123","password2":"789"}
		try:
			user = UserPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			# print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": ["username"],
				"msg": "username should not contain a space",
				"type": "value_error"},{"loc": ["password1"],
				"msg": "ensure this value has at least 5 characters",
				"type": "value_error.any_str.min_length","ctx": {
				"limit_value": 5}},{"loc": ["password2"],
				"msg": "ensure this value has at least 5 characters",
				"type": "value_error.any_str.min_length","ctx": {
				"limit_value": 5}}])
		print("Test b_1_1_4:UserPost:Fail:username contains spaces, short password")

	def test_b_001_01_5_UserPost(self):
		# password mismatch
		# Username already exists
		toValidate = {"username":"abc","password1":"123456789999999000000000",
		"password2":"12345678"}
		try:
			user = UserPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{
				'loc': ['username'], 'msg': 'this username already exists',
				'type': 'value_error'}, {'loc': ['password2'], 'msg':
				'passwords do not match', 'type': 'value_error'}])
		print("Test b_1_1_5:UserPost:Fail:password mismatch")

	def test_b_001_01_6_UserPost(self):
		# adding unknown attribute
		# This attribute will not be returned
		# Testing White spaces
		toValidate = {"username":" MyName ","password1":"12345678",
		"password2":"12345678", "unknown":"abc"}
		user = UserPost(**toValidate)
		self.assertEqual(user.dict(),{"username":"MyName","password1":"12345678",
		"password2":"12345678"})
		print("Test b_1_1_6:UserPost:Added unknown value:Cleaned")





















	"""def test_b_002_01_1_ProductPost(self):
		toValidate = {"name":"    123  ","price":789,"in_stock":True}
		product = ProductPost(**toValidate)
		#print(product.dict())
		self.assertEqual(product.dict(),{'name': '123',
			'price': 789.0, 'in_stock': True})
		print("Test b_2_1_1:ProductPost Successful")

	def test_b_002_01_2_ProductPost(self):
		toValidate = {}
		try:
			product = ProductPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			# print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'field required', 'type': 'value_error.missing'},
				{'loc': ['price'], 'msg': 'field required', 'type':
				'value_error.missing'}])
		print("Test b_2_1_2:ProductPost:Fail:all missing required")

	def test_b_002_01_3_ProductPost(self):
		# Wrong data types
		toValidate = {"name":{},"price":{},"in_stock":{}}
		try:
			product = ProductPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc':
				['name'], 'msg': 'str type expected', 'type':
				'type_error.str'}, {'loc': ['price'], 'msg':
				'value is not a valid float', 'type':
				'type_error.float'}, {'loc': ['in_stock'], 'msg':
				'value could not be parsed to a boolean', 'type':
				'type_error.bool'}])
		print("Test b_2_1_3:ProductPost:Fail: Wrong data types")

	def test_b_002_01_4_ProductPost(self):
		# Short product name
		# Very cheap price
		toValidate = {"name":"    a  ","price":.01, "in_stock":True}
		try:
			product = ProductPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'ensure this value has at least 3 characters',
				'type': 'value_error.any_str.min_length', 'ctx':
				{'limit_value': 3}}, {'loc': ['price'], 'msg':
				'ensure this value is greater than or equal to 0.1',
				'type': 'value_error.number.not_ge', 'ctx':
				{'limit_value': 0.1}}])
		print("Test b_2_1_4:ProductPost:Fail:short name, cheap price")

	def test_b_002_01_5_ProductPost(self):
		# long product name
		# Very expensive price
		toValidate = {"name":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"+
		"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"+
		"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
		"price":1000000000000000000000000000000000000000,"in_stock":True}
		try:
			product = ProductPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'ensure this value has at most 100 characters',
				'type': 'value_error.any_str.max_length', 'ctx':
				{'limit_value': 100}}, {'loc': ['price'], 'msg':
				'ensure this value is less than or equal to 1000000',
				'type': 'value_error.number.not_le', 'ctx':
				{'limit_value': 1000000}}])
		print("Test b_2_1_5:ProductPost:Fail:long name, expensive price")"""









	"""def test_b_002_02_1_ProductUpdate(self):
		# successful test
		toValidate = {"name":"    123  ","price":789,"in_stock":True}
		product = ProductUpdate(**toValidate)
		self.assertEqual(product.dict(),{"name":"123","price":789,"in_stock":True})
		print("Test b_2_2_1:ProductUpdate Successful")

	def test_b_002_02_2_ProductUpdate(self):
		# successful test: Not received
		toValidate = {"name":123}
		product = ProductUpdate(**toValidate)
		#print((product.dict()))
		self.assertEqual(product.name,"123")
		self.assertEqual(type(product.price),NotReceived)
		self.assertEqual(type(product.in_stock),NotReceived)
		#self.assertEqual(product.dict(),{"username":"123","password":NotReceived()})
		print("Test b_2_2_2:ProductUpdate Successful Missing fields")

	def test_b_002_02_3_ProductUpdate(self):
		toValidate = {}
		try:
			product = ProductUpdate(**toValidate)
			#print(product.dict())
			self.assertEqual(True,False)
		except Exception as e:
			#print(str(e))
			self.assertEqual(json.loads(str(e)),[{'loc':
				['in_stock'], 'msg':
				'you must at least enter one value to change',
				'type': 'value_error'}])
		print("Test b_2_2_3:ProductUpdate:Fail:all missing required")

	def test_b_002_02_4_ProductUpdate(self):
		# Wrong data types
		toValidate = {"name":{},"price":{},"in_stock":{}}
		try:
			product = ProductUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc':
				['name'], 'msg': 'str type expected', 'type':
				'type_error.str'}, {'loc': ['price'], 'msg':
				'value is not a valid float', 'type':
				'type_error.float'}, {'loc': ['in_stock'], 'msg':
				'value could not be parsed to a boolean', 'type':
				'type_error.bool'}])
		print("Test b_2_2_4:ProductUpdate:Fail: Wrong data types")

	def test_b_002_02_5_ProductUpdate(self):
		# Short product name
		# Very cheap price
		toValidate = {"name":"    a  ","price":.01, "in_stock":True}
		try:
			product = ProductUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'ensure this value has at least 3 characters',
				'type': 'value_error.any_str.min_length', 'ctx':
				{'limit_value': 3}}, {'loc': ['price'], 'msg':
				'ensure this value is greater than or equal to 0.1',
				'type': 'value_error.number.not_ge', 'ctx':
				{'limit_value': 0.1}}])
		print("Test b_2_2_5:ProductUpdate:Fail:short name, cheap price")

	def test_b_002_02_6_ProductUpdate(self):
		# long product name
		# Very expensive price
		toValidate = {"name":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"+
		"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"+
		"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
		"price":1000000000000000000000000000000000000000,"in_stock":True}
		try:
			product = ProductUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'ensure this value has at most 100 characters',
				'type': 'value_error.any_str.max_length', 'ctx':
				{'limit_value': 100}}, {'loc': ['price'], 'msg':
				'ensure this value is less than or equal to 1000000',
				'type': 'value_error.number.not_le', 'ctx':
				{'limit_value': 1000000}}])
		print("Test b_2_2_6:ProductUpdate:Fail:long name, expensive price")"""






















	"""def test_b_003_01_1_OrderPost(self):
		toValidate = {"product_id":"  3   ","amount":"   5 "}
		order = OrderPost(**toValidate)
		#print(order.dict())
		self.assertEqual(order.dict(),
			{'product_id': 3, 'amount': 5})
		print("Test b_3_1_1:OrderPost Successful")

	def test_b_003_01_2_OrderPost(self):
		toValidate = {}
		try:
			order = OrderPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['product_id'],
				'msg': 'field required', 'type': 'value_error.missing'},
				{'loc': ['amount'], 'msg': 'field required', 'type':
				'value_error.missing'}])
		print("Test b_3_1_2:OrderPost:Fail:all missing required")

	def test_b_003_01_3_OrderPost(self):
		toValidate = {"product_id":{},"amount":{}}
		try:
			order = OrderPost(**toValidate)
			self.assertEqual()
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['product_id'],
			'msg': 'value is not a valid integer', 'type':
			'type_error.integer'}, {'loc': ['amount'], 'msg':
			'value is not a valid integer', 'type': 'type_error.integer'}])
		print("Test b_3_1_3:OrderPost:Fail:wrong data types")


	def test_b_003_01_4_OrderPost(self):
		# product_id less than 0
		# amount less than 0
		toValidate = {"product_id":"-1","amount":"-1"}
		try:
			order = OrderPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['product_id'],
				'msg': 'ensure this value is greater than 0', 'type':
				'value_error.number.not_gt', 'ctx': {'limit_value': 0}},
				{'loc': ['amount'], 'msg': 'ensure this value is greater than -1',
				'type': 'value_error.number.not_gt', 'ctx': {'limit_value': -1}}])
		print("Test b_3_1_4:OrderPost:Fail:id less than 0, amount less than 0")

	def test_b_003_01_5_OrderPost(self):
		# non existent product id
		# very big amount
		toValidate = {"product_id":"50000000","amount":"10000000000000000000"}

		try:
			order = OrderPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['product_id'],
				'msg': 'there is no Product with this id: 50000000', 'type':
				'value_error'}, {'loc': ['amount'], 'msg':
				'ensure this value is less than 1000', 'type':
				'value_error.number.not_lt', 'ctx': {'limit_value': 1000}}])
		print("Test b_3_1_5:OrderPost:non existent product id, big amount")

	def test_b_003_01_6_OrderPost(self):
		# a product that is not in stock
		toValidate = {"product_id":"2","amount":"10"}
		try:
			order = OrderPost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['product_id'],
			'msg': 'this product is not in stock, so it can not be ordered',
			'type': 'value_error'}])
		print("Test b_3_1_6:OrderPost:a product that is not in stock")




















	def test_b_003_02_1_OrderUpdate(self):
		# product id is an additional value
		toValidate = {"product_id":"  3   ","amount":"   5 "}
		order = OrderUpdate(**toValidate)
		#print(order.dict())
		self.assertEqual(order.dict(),
			{'amount': 5})
		print("Test b_3_2_1:OrderUpdate Successful")

	def test_b_003_02_2_OrderUpdate(self):
		toValidate = {}
		try:
			order = OrderUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[
				{'loc': ['amount'], 'msg': 'field required', 'type':
				'value_error.missing'}])
		print("Test b_3_2_2:OrderUpdate:Fail:all missing required")

	def test_b_003_02_3_OrderUpdate(self):
		toValidate = {"amount":{}}
		try:
			order = OrderUpdate(**toValidate)
			self.assertEqual()
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['amount'], 'msg':
			'value is not a valid integer', 'type': 'type_error.integer'}])
		print("Test b_3_2_3:OrderUpdate:Fail:wrong data type")


	def test_b_003_02_4_OrderUpdate(self):
		# amount less than 0
		toValidate = {"amount":"-1"}
		try:
			order = OrderUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[
				{'loc': ['amount'], 'msg': 'ensure this value is greater than -1',
				'type': 'value_error.number.not_gt', 'ctx': {'limit_value': -1}}])
		print("Test b_3_2_4:OrderUpdate:Fail:amount less than 0")

	def test_b_003_02_5_OrderUpdate(self):
		# very big amount
		# product id is additional, and it will not be returned
		toValidate = {"product_id":"50000000","amount":"10000000000000000000"}

		try:
			order = OrderUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['amount'], 'msg':
				'ensure this value is less than 1000', 'type':
				'value_error.number.not_lt', 'ctx': {'limit_value': 1000}}])
		print("Test b_3_2_5:OrderUpdate:non existent product id, big amount")"""
































	"""def test_b_004_01_1_ImagePost(self):
		toValidate = {"name":"abc","formatting":"png", "image_b64":"1111"}
		img = ImagePost(**toValidate)
		#print(img.dict())
		self.assertEqual(img.dict(),
			{'name': 'abc', 'formatting': 'png', 'image_b64': '1111'})
		print("Test b_3_1_1:ImagePost Successful")

	def test_b_004_01_2_ImagePost(self):
		toValidate = {}
		try:
			img = ImagePost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'field required', 'type': 'value_error.missing'},
				{'loc': ['formatting'], 'msg': 'field required',
				'type': 'value_error.missing'}, {'loc': ['image_b64'],
				'msg': 'field required', 'type': 'value_error.missing'}])
		print("Test b_4_1_2:ImagePost:Fail:all missing required")

	def test_b_004_01_3_ImagePost(self):
		toValidate = {"name":{},"formatting":{}, "image_b64":{}}
		try:
			img = ImagePost(**toValidate)
			self.assertEqual()
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'str type expected', 'type': 'type_error.str'},
				{'loc': ['formatting'], 'msg': 'str type expected',
				'type': 'type_error.str'}, {'loc': ['image_b64'],
				'msg': 'str type expected', 'type': 'type_error.str'}])
		print("Test b_4_1_3:ImagePost:Fail:wrong data types")


	def test_b_004_01_4_ImagePost(self):
		# short name
		# non existent formatting
		# short image
		toValidate = {"name":"a","formatting":"gif", "image_b64":""}
		try:
			img = ImagePost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'ensure this value has at least 3 characters',
				'type': 'value_error.any_str.min_length', 'ctx':
				{'limit_value': 3}}, {'loc': ['formatting'], 'msg':
				"this format \"gif\" is not in the list of accpted formats"+
				" ['png', 'jpg']", 'type': 'value_error'}, {'loc':
				['image_b64'], 'msg':
				'ensure this value has at least 4 characters',
				'type': 'value_error.any_str.min_length', 'ctx':
				{'limit_value': 4}}])
		print("Test b_4_1_4:ImagePost:Fail:short name and image, "+
			"rejected formatting")

	def test_b_004_01_5_ImagePost(self):
		# long name
		# long image
		toValidate = {"name":"a"*201,"formatting":"png",
		"image_b64":"a"*250001}

		try:
			img = ImagePost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'], 'msg':
				'ensure this value has at most 200 characters', 'type':
				'value_error.any_str.max_length', 'ctx': {'limit_value':
				200}}, {'loc': ['image_b64'], 'msg':
				'ensure this value has at most 250000 characters', 'type':
				'value_error.any_str.max_length', 'ctx':
				{'limit_value': 250000}}])
		print("Test b_4_1_5:ImagePost:long image and name ")

	def test_b_004_01_6_ImagePost(self):
		# image can not be converted to b64
		toValidate = {"name":"abc","formatting":"png",
		"image_b64":"bbbbb"}

		try:
			img = ImagePost(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['image_b64'],
				'msg': 'this image is not base64', 'type': 'value_error'}])
		print("Test b_4_1_6:ImagePost:Can not be converted to base64")"""






















	"""def test_b_004_02_1_ImageUpdate(self):
		# product id is an additional value
		toValidate = {"name":"abc","formatting":"png", "image_b64":"1111"}
		img = ImageUpdate(**toValidate)
		#print(img.dict())
		self.assertEqual(img.dict(),
			{'name': 'abc', 'formatting': 'png', 'image_b64': '1111'})
		print("Test b_4_2_1:ImageUpdate Successful")

	def test_b_004_02_2_ImageUpdate(self):
		toValidate = {}
		try:
			img = ImageUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(str(e)))
			self.assertEqual(json.loads(str(e)),[{'loc': ['image_b64'],
				'msg': 'you must at least enter one value to change',
				'type': 'value_error'}])
		print("Test b_4_2_2:ImageUpdate:Fail:all missing required")

	def test_b_004_02_3_ImageUpdate(self):
		toValidate = {"name":{},"formatting":{}, "image_b64":{}}
		try:
			img = ImageUpdate(**toValidate)
			self.assertEqual()
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'str type expected', 'type': 'type_error.str'},
				{'loc': ['formatting'], 'msg': 'str type expected',
				'type': 'type_error.str'}, {'loc': ['image_b64'],
				'msg': 'str type expected', 'type': 'type_error.str'}])
		print("Test b_4_2_3:ImageUpdate:Fail:wrong data type")


	def test_b_004_02_4_ImageUpdate(self):
		# short name
		# non existent formatting
		# short image
		toValidate = {"name":"a","formatting":"gif", "image_b64":""}
		try:
			img = ImageUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'ensure this value has at least 3 characters',
				'type': 'value_error.any_str.min_length', 'ctx':
				{'limit_value': 3}}, {'loc': ['formatting'], 'msg':
				"this format \"gif\" is not in the list of accpted formats"+
				" ['png', 'jpg']", 'type': 'value_error'}, {'loc':
				['image_b64'], 'msg':
				'ensure this value has at least 4 characters',
				'type': 'value_error.any_str.min_length', 'ctx':
				{'limit_value': 4}}])
		print("Test b_4_2_4:ImageUpdate:Fail:amount less than 0")

	def test_b_004_02_5_OrderUpdate(self):
		# long name
		# long image
		toValidate = {"name":"a"*201,"formatting":"png",
		"image_b64":"a"*250001}

		try:
			img = ImageUpdate(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['name'],
				'msg': 'ensure this value has at most 200 characters',
				'type': 'value_error.any_str.max_length', 'ctx':
				{'limit_value': 200}}, {'loc': ['image_b64'], 'msg':
				'ensure this value has at most 250000 characters',
				'type': 'value_error.any_str.max_length', 'ctx':
				{'limit_value': 250000}}])
		print("Test b_4_2_5:ImageUpdate:non existent product id, big amount")"""

	"""def test_b_004_02_6_OrderUpdate(self):
		# very big amount
		# product id is additional, and it will not be returned
		toValidate = {"name":123}
		img = ImageUpdate(**toValidate)
		self.assertEqual(type(img.formatting),NotReceived)
		self.assertEqual(type(img.image_b64),NotReceived)"""
	"""try:
			print(order.dict())
			#self.assertEqual(True,False)
		except Exception as e:
			print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['amount'], 'msg':
				'ensure this value is less than 1000', 'type':
				'value_error.number.not_lt', 'ctx': {'limit_value': 1000}}])"""
		#print("Test b_4_2_6:ImageUpdate:Not Received")


















	def test_here(self):
		#n = '0'*8
		#print(n)
		json.loads(json.dumps([{"loc": ["in_stock"],
			"msg": "You must at least enter one value to change",
			"type": "value_error"}]))
		toValidate = {}
		try:
			data = TestHere(**toValidate)
			#print(data)
			#print(data.dict())
		except Exception as e:
			print(json.loads(e.json()))
			pass
		print("Test")










































# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()
