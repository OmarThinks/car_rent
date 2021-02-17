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


class UserUpdatePassword(BaseModel):
	password1 : password_con
	password2 : password_con

	@validator('password2')
	def passwords_match(cls, value, values, **kwargs):
		if 'password1' in values and value != values['password1']:
			raise ValueError('passwords do not match')
		return value










"""class ProductPost(BaseModel):
	name : product_name_con
	price : product_price_con
	in_stock : bool=True













class OrderPost(BaseModel):
	product_id : id_con
	amount : amount_con

	@validator('product_id')
	def product_exists(cls, value):
		# Validatng that this product really exists
		validate_model_id_pydantic(Product, value)
		#Validating that the product is in stock before ordering it
		product_in_stock = Product.query.get(value).in_stock
		if not product_in_stock:
			raise ValueError('this product is not in stock, '+
				'so it can not be ordered')
		return value


class OrderUpdate(BaseModel):
	# product id can not be modified
	amount : amount_con"""









the_tst=constr(strip_whitespace=True, min_length=1,max_length=5)



class TestHere(BaseModel):
  a: str = None
  b: str = None

  @validator('b')
  def check_a_or_b(cls, v, values):
    if 'a' not in values and not b:
      raise ValueError('either a or b is required')
    return b
"""
external_data = {
	'id': '123',
	'signup_ts': '2019-06-01 12:22',
	'friends': [1, 2, '3'],
}
user = User(**external_data)
"""









#Image
"""image_name_con = constr(strip_whitespace=True, min_length=3,max_length=200)
formatting_con = constr(strip_whitespace=True, min_length=2,max_length=15)
image_b64_con = constr(strip_whitespace=True, min_length=4,max_length=250000)
# accepted frmats of images
IMAGE_ACCEPTED_FROMATS=["png","jpg"]
"""







"""class ProductUpdate(BaseModel):
	name : product_name_con = NotReceived()
	price : product_price_con = NotReceived()
	in_stock : bool = NotReceived()

	def __init__(self, **kwargs):
		BaseModel.__init__(self, **kwargs)
		#print(self.dict())
		if type(self.name) != NotReceived:
			return
		if type(self.price) != NotReceived:
			return
		if type(self.in_stock) != NotReceived:
			return
		raise ValueError(json.dumps([{"loc": ["in_stock"],
			"msg": "you must at least enter one value to change",
			"type": "value_error"}]))"""
"""def ProductUpdate(**kwargs):
	toReturn = ProductUpdatee(**kwargs)
	if type(toReturn.name) != NotReceived:
		return toReturn
	if type(toReturn.price) != NotReceived:
		return toReturn
	if type(toReturn.in_stock) != NotReceived:
		return toReturn
	raise ValueError('You must at least enter one value to change')"""








"""class ImagePost(BaseModel):
	name :  image_name_con
	formatting : formatting_con
	image_b64 : image_b64_con

	@validator('formatting')
	def formatting_in_range(cls, value):
		if value not in IMAGE_ACCEPTED_FROMATS:
			raise ValueError('this format "'+str(value)+'" is not in the list of '+
				"accpted formats "+ str(IMAGE_ACCEPTED_FROMATS))
		return value


	@validator('image_b64')
	def b64_is_b64(cls, value):
		try:
			base64.b64decode(value)
		except:
			raise ValueError('this image is not base64')
		return value

class Image_Update(BaseModel):
	name : image_name_con = NotReceived()
	formatting : formatting_con = NotReceived()
	image_b64 : image_b64_con = NotReceived()

	@validator('formatting')
	def formatting_in_range(cls, value):
		if value not in IMAGE_ACCEPTED_FROMATS:
			raise ValueError('this format "'+str(value)+'" is not in the list of '+
				"accpted formats "+ str(IMAGE_ACCEPTED_FROMATS))
		return value

	@validator('image_b64')
	def b64_is_b64(cls, value):
		try:
			base64.b64decode(value)
		except:
			raise ValueError('this image is not base64')
		return value

def ImageUpdate(**kwargs):
	img = Image_Update(**kwargs)
	if type(img.name) != NotReceived :
		return img
	if type(img.formatting) != NotReceived :
		return img
	if type(img.image_b64) != NotReceived :
		return img
	raise ValueError(json.dumps([{"loc": ["image_b64"],
		"msg": "you must at least enter one value to change",
		"type": "value_error"}]))"""
