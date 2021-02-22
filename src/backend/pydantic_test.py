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











	def test_b_001_03_1_UserLogin(self):
		toValidate = {"username":"   abc  ","password":123456789}
		user = UserLogin(**toValidate)
		self.assertEqual(user.dict(),
		{"username":"abc","password":1})
		print("Test b_1_3_1:UserLogin Successful")

	def test_b_001_03_2_UserLogin(self):
		toValidate = {}
		try:
			user = UserLogin(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": ["username"],
				"msg": "field required","type": "value_error.missing"},
				{"loc": ["password"],"msg": "field required",
				"type": "value_error.missing"
				}])
		print("Test b_1_3_2:UserLogin:Fail:all missing required")

	def test_b_001_03_3_UserLogin(self):
		toValidate = {"password":{},"username":{}}
		try:
			user = UserLogin(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{"loc": ["username"],
				"msg": "str type expected","type": "type_error.str"},{"loc": [
				"password"],"msg": "str type expected","type": "type_error.str"
				}])
		print("Test b_1_3_3:UserLogin:Fail:not string")


	def test_b_001_03_4_UserLogin(self):
		# Non existent username
		toValidate = {"username":"My Name","password":"12378974564231"}
		try:
			user = UserLogin(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['password'],
			'msg': 'wrong username or password',
			'type': 'value_error'}])
		print("Test b_1_3_4:UserLogin:Fail:non existent username")

	def test_b_001_03_5_UserLogin(self):
		# password mismatch
		# Username already exists
		toValidate = {"username":"abc","password":"12345",
		"password2":"12345678"}
		try:
			user = UserLogin(**toValidate)
			self.assertEqual(True,False)
		except Exception as e:
			#print(json.loads(e.json()))
			self.assertEqual(json.loads(e.json()),[{'loc': ['password'],
			'msg': 'wrong username or password',
			'type': 'value_error'}])
		print("Test b_1_3_5:UserPost:Fail:wrong password")



































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
