from typing import List, Optional
from pydantic import (BaseModel,
	ValidationError, validator, constr, conint, confloat)
from models import NotReceived, User#, Product
import json

import base64





# General
id_con = conint(gt=0)


# User
username_con = constr(strip_whitespace=True, min_length=3,max_length=40)
password_con = constr(strip_whitespace=False, min_length=5,max_length=100)

#Product Name
"""product_name_con = constr(strip_whitespace=True, min_length=3,max_length=100)
product_price_con = confloat(ge=.1, le=1000000)


# Order
amount_con = conint(gt=-1, lt=1000)"""




"""
validate_model_id
- Inputs:
	- model: the SQLAlchemy model
	- id: the int of the id
- Function:
	- Make sure that this model exists
	- raise error if it was not an integer
- Output:
	- True: This model exists
	- False: This model does not exist
"""

def validate_model_id(model,id:int):
	try:
		if model.query.get(id) == None:
			return False
		return True
	except:
		raise ValueError("validate_model_id:expected the "+
			"type of SQLAlchemy, but found "+
			"the type of "+str(type(model))+" instead")




"""
validate_model_id_pydantic
- Inputs:
	- model: the SQLAlchemy model
	- id: the int of the id
- Function:
	- raise correct error if the model does not exist
- Output:
	- No output, only error are raised
"""
def validate_model_id_pydantic(model,id:int):
	model_name = model.__name__
	if validate_model_id(model,id) == True:
		pass
	else:
		raise ValueError("there is no "+ model_name +
		 " with this id: " +str(id))





class UserPost(BaseModel):
	username : username_con
	password1 : password_con
	password2 : password_con

	@validator('username')
	def name_cant_contain_space(cls, value):
		# Validating that username does not have any spaces
		if ' ' in value:
			raise ValueError('username should not contain a space')
		#Validate that this username is unique
		all_users=User.query.all()
		all_names=[str(u.username) for u in all_users]
		if value in all_names:
			raise ValueError('this username already exists')
		return value

	@validator('password2')
	def passwords_match(cls, value, values, **kwargs):
		if 'password1' in values and value != values['password1']:
			raise ValueError('passwords do not match')
		return value

class UserLogin(BaseModel):
	username : username_con
	password : password_con

	@validator('password')
	def wrong_username_or_password(cls, value, values, **kwargs):
		username = values["username"]
		password = value
		users=User.query.all()

		#Validate that this username and password are correct
		all_users=User.query.all()
		the_user_id="";

		for usr in all_users:
			if (str(usr.username) == str(username) and
				str(usr.password) == str(password)):
				the_user_id=usr.id # Here we go the user id
				break
		if the_user_id=="":
			raise ValueError('wrong username or password')
		# The Id will be passed to avoid redununt username search
		return the_user_id


class UserUpdatePassword(BaseModel):
	password1 : password_con
	password2 : password_con

	@validator('password2')
	def passwords_match(cls, value, values, **kwargs):
		if 'password1' in values and value != values['password1']:
			raise ValueError('passwords do not match')
		return value







the_tst=constr(strip_whitespace=True, min_length=1,max_length=5)



class TestHere(BaseModel):
  a: str = None
  b: str = None

  @validator('b')
  def check_a_or_b(cls, v, values):
    if 'a' not in values and not b:
      raise ValueError('either a or b is required')
    return b
