import os
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, func
import json
from sqlalchemy.orm import backref, relationship, scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
import types
from sqlalchemy.orm.collections import InstrumentedList

from __init__ import db

SUPPORTED_TYPES = [int,str,float,bool,type(None)]
RESTRICTED_FIELDS=["password"]

from flask_sqlalchemy.model import DefaultMeta

"""
NotReceived
This class is used when the dada is not received
By default, it will have the value of None
None != Not received
"""
class NotReceived():
	pass



"""
validate_key

- Inputs:
	- the_object: dict or object
		- The Object, or the dict of the data to be validated
		- Example:
			- user_to_insert (as an object)
			- {"id":1,"username":"abc","password":"pass"}
	- key: str:
		- the key of the dict that contains the data
		- Example:
			- "id"
	- id: bool : default = False
		- Should we pass the id or not
		- True: let the id pass
		- False: do not le the id pass (Default)
	- unsupported : bool: default = False
		- pass unsupported data types, not in SUPPORTED_TYPES list
		- If the type was unsupported, it must have the simple function
		- True: let it pass
		- False: do not let it pass (Default)
	- dangerous : bool: default = False
		- pass dangerous keys, in SUPPORTED_TYPES list
		- True: let it pass
		- False: do not let it pass (Default)
- Function:
	- telling us whether we should let this key of this object or dict pass or not
- Output:
	- True: let ths pass
	- False: do not let this key pass
"""
def validate_key(the_object,key:str,
	id:bool=False,
	unsupported:bool = False,
	dangerous:bool=False):
	if type(the_object) == dict:
		the_attribute = the_object[key]
	else:
		the_attribute = getattr(the_object, key)

	# Validating fields startng with "_"
	if key[0] == "_":
		return False
	# Validating NotReceived
	if type(the_attribute) == type(NotReceived):
		return False
	# Validating id
	if key.lower() == "id" and id == False:
		return False
	# Validating supported types
	if ((type(the_attribute)not in SUPPORTED_TYPES) and (unsupported==True)):
		if type(the_attribute) == types.MethodType:
			return False
		if key in ["metadata","query"]:
			return False
		if type(type(the_attribute)) == DefaultMeta:
			return True
		if ((type(the_attribute) == InstrumentedList)):
			return True
		return False
	if type(the_attribute) not in SUPPORTED_TYPES:
		return False
	# validating dangerous fields
	if ((key.lower() in RESTRICTED_FIELDS) and (dangerous==False)):
		return False
	return True


"""
get_dict

- Inputs:
	- the_object: dict or object
		- The Object, or the dict of the data to be validated
		- Example:
			- user_to_insert (as an object)
			- {"id":1,"username":"abc","password":"pass"}
	- id: bool : default = False
		- Should we pass the id or not
		- True: let the id pass
		- False: do not le the id pass (Default)
	- unsupported : bool: default = False
		- pass unsupported data types, not in SUPPORTED_TYPES list
		- If the type was unsupported, it must have the simple function
		- True: let it pass
		- False: do not let it pass (Default)
	- dangerous : bool: default = False
		- pass dangerous keys, in SUPPORTED_TYPES list
		- True: let it pass
		- False: do not let it pass (Default)
- Function:
	- convert the object or the dict to a validated dict of fileds
	- The fuelds will be validated, and you will get the clean fields
		and their values only
- Output:
	- dict clean
"""
def get_dict(the_object,id:bool=False,
	unsupported:bool = False,
	dangerous:bool=False):
	keys_list=[]
	if type(the_object)==dict:
		for key in the_object:
			keys_list.append(key)
	else:
		keys_list = dir(the_object)
	toReturn = {}
	for key in keys_list:
		if validate_key(the_object,key,id,unsupported,dangerous):
			if type(the_object)==dict:
				toReturn[key] = the_object[key]
				continue
			toReturn[key] = getattr(the_object,key)
	return toReturn



class MyModel():
	# For creating the model
	def __init__(self, **kwargs):
		#dangerous = True, we may need to enter the password
		validated_kwargs = get_dict(kwargs,dangerous=True,id=False)
		for key in validated_kwargs:
			setattr(self,key,validated_kwargs[key])
	# For inserting the model in the db
	def insert(self):
		#print(self)
		try:
			db.session.add(self)
			db.session.commit()
		except:
			db.session.rollback()
	# For updating the model
	def update(self,**kwargs):
		try:
			#restrcted = True, we may need to update the password
			validated_kwargs = get_dict(kwargs,dangerous=True)
			for key in validated_kwargs:
				setattr(self,key,validated_kwargs[key])
			db.session.commit()
		except:
			db.session.rollback()
	# For deleting the model from the db
	def delete(self):
		try:
			db.session.delete(self)
			db.session.commit()
		except:
			db.session.rollback()
	# getting the attributes of the model, inculding id, but not dangerous fields
	def simple(self):
		# Prepare to delete all the keys starting with "_", or key == "id"
		validated_self = get_dict(self, id=True)
		toReturn = {}
		for key in validated_self:
			toReturn[key] = validated_self[key]
		return toReturn
	# For printng the model
	def __repr__(self):
		print("rpr")
		return json.dumps(self.simple())
	# For getting the model and the forigen keys of the model
	def deep(self):
		toReturn = {}
		validated_self = get_dict(self, id=True,unsupported=True)
		for key in validated_self:
			if validate_key(self,key,id=True) == True:
				# Here key is normal or id, not unsupported
				toReturn[key] = validated_self[key]
				continue
			# If it has this function, then it is a column in the table
			try:
				toReturn[key] = validated_self[key].simple()
			except Exception as e:
				toReturn[key] = []
				children_list = validated_self[key]
				for child in children_list:
					toReturn[key].append(child.simple())
		return toReturn



'''
User
a persistent product entity, extends the base SQLAlchemy Model
id,username,password

Relationships:
products,orders,images

'''
class User(db.Model,MyModel):
	#__metaclass__=MyModel
	__tablename__="user"
	# Autoincrementing, unique primary key
	id = db.Column(Integer(), primary_key=True)
	# String username
	username = db.Column(String(), unique=True, nullable=False)
	# username could be like "fish"
	# username has to be unique
	# not allowing several users to have the same username
	password =  db.Column(String(), unique=False, nullable=False)
	# Password is a string
	# Example: "12345", "abc"
	# it doesn't have to be unique



	products = db.relationship("Product",cascade="all, delete-orphan",
		passive_deletes=False,backref="seller")
	orders = db.relationship("Order",cascade="all, delete-orphan",
		passive_deletes=False,backref="buyer")
	#images = db.relationship("Image",cascade="all, delete-orphan",
	#	passive_deletes=False,backref="seller")

	def __init__(self,**kwargs):
		MyModel.__init__(self,**kwargs)


'''
Product
a persistent product entity, extends the base SQLAlchemy Model
id,name,price,in_stock,seller_id
'''
class Product(db.Model, MyModel):
	__tablename__="product"
	# Autoincrementing, unique primary key
	id = db.Column(Integer(), primary_key=True)
	# String name
	name = db.Column(String(), unique=False, nullable=False)
	# name could be like "Labtop"
	# name dowsn't have to be unique
	# allowing several users to sell the same product
	price =  db.Column(Float(), unique=False, nullable=False)
	# Price is a float
	# Example: 5.0, 6.0 , 50.0, 0.5
	# It should be float, allowing things with low
	# price to be sold
	in_stock =  db.Column(Boolean(), unique=False,
		nullable=False, default=True)
	# in_stock is a boolean
	# Example: True, False
	# it represents whether this product is for sale or not
	# True = For sale, can be displayed to customers
	# False = now for sale, can not be displayed to customers
	seller_id = db.Column(Integer(),ForeignKey("user.id"),
	 unique=False, nullable=False)
	#seller_id = Column(Integer(), unique=False, nullable=False)
	# seller_id
	# This is the id of the seller user
	# The user who sells this product
	# it is an integer
	# Example: 1, 2 or 3
	orders = db.relationship("Order",cascade="all, delete-orphan",
		passive_deletes=False,backref="product")


	"""orders = db.relationship("Order",backref=backref('product',
						#uselist=True,
						#cascade='all,delete-orphan'
						cascade="all, delete",
						),passive_deletes=False)"""

	#def __init__(self,**kwargs):
	#	print("product self init")
	#	self.name = kwargs["name"]
	#	self.price = kwargs["price"]
	#	self.in_stock = True
	#	self.seller_id = kwargs["seller_id"]
	#	#MyModel.__init__(self,**kwargs)




"""
Order:
id, user_id, product_id, amount
"""
class Order(db.Model, MyModel):
	__tablename__="order"
	# Autoincrementing, unique primary key
	id = db.Column(Integer(), primary_key=True)
	# String name
	user_id =db.Column(Integer(),ForeignKey("user.id"),
	 unique=False, nullable=False)
	# user_id
	# This is the id of the user who ordered the products
	# it is an integer
	# Example: 1, 2 or 3
	product_id  = db.Column(Integer(),ForeignKey("product.id"))
	# product_id is an integer
	# it refers to the product.id in the products table
	# Example: 1, 2 , 3
	amount =  db.Column(Integer(), unique=False, nullable=False)
	# amount is an integer
	# Example: 5, 6, 50
	#product = relationship("Product", back_populates="orders")
	def __init__(self,**kwargs):
		MyModel.__init__(self,**kwargs)

	def insert(self):
		if self.amount>0:
			MyModel.insert(self)
		db.session.rollback()

	def update(self, **kwargs):
		MyModel.update(self,**kwargs)
		if self.amount<= 0:
			self.delete()


'''
Image
a persistent product entity, extends the base SQLAlchemy Model
id,seller_id,name,formatting

The image will be stroed with it's id
'''
"""

No more adding features
Learn new things


class Image(db.Model, MyModel):
	__tablename__="image"
	# Autoincrementing, unique primary key
	id = db.Column(Integer(), primary_key=True)
	seller_id = db.Column(Integer(),ForeignKey("user.id"),
	 unique=False, nullable=False)
	# This is the id of the seller user
	# The user who sells this product
	# it is an integer
	# Example: 1, 2 or 3
	name = db.Column(String(), unique=False, nullable=False)
	# image name could be like "fish"
	# image name can not to be unique
	# not allowing several users to have the same username
	formatting =  db.Column(String(), unique=False, nullable=False)
	# formattng is a string that represents the type of image
	# There can be only 2 types: "png" , "jpg"
	# it can not be unique

	def __init__(self,**kwargs):
		MyModel.__init__(self,**kwargs)"""






#init_db()
"""
user = User(username = "abc", password = "123", id = 123)
print(user)
print(user.__dict__)
print(type(user.__dict__["password"]))
"""
#user.insert()
#user.create({"username":123})
#print(user)
#print(dir(user))


def db_drop_and_create_all():
	db.session.close()
	db.drop_all()
	db.create_all()



def populate_tables():
	db_drop_and_create_all()
	users = list()
	users.append(User(username="abc",password="123456789"))
	users.append(User(username="abcde",password="456abcderrrt"))
	users.append(User(username="klmn",password="fde123987byt"))
	users.append(User(username="rtb",password="uytkltyopi889"))
	users.append(User(username="cool",password="freezererer"))
	users.append(User(username="water",password="TankTankTank"))
	db.session.add_all(users)
	db.session.commit()


	products = list()
	products.append(Product(
		name="Labtop", price=300, seller_id="1"))
	products.append(Product(
		name="Mobile", price=100, seller_id="2", in_stock=False))
	products.append(Product(
		name="Candy", price=.5, seller_id="3", in_stock=True))
	products.append(Product(
		name="Table", price=150, seller_id="1", in_stock=False))
	products.append(Product(
		name="Keyboard", price=5, seller_id="2", in_stock=True))
	products.append(Product(
		name="Mouse", price=4, seller_id="1", in_stock=True))
	db.session.add_all(products)
	db.session.commit()

	orders = list()
	#id, user, product, amount
	orders.append(Order(user_id="1", product_id=1, amount=1))
	orders.append(Order(user_id="2", product_id=1, amount=4))
	orders.append(Order(user_id="3", product_id=2, amount=3))
	orders.append(Order(user_id="1", product_id=1, amount=2))
	orders.append(Order(user_id="2", product_id=2, amount=1))
	orders.append(Order(user_id="2", product_id=3, amount=5))
	orders.append(Order(user_id="1", product_id=4, amount=20))
	orders.append(Order(user_id="3", product_id=5, amount=4))

	db.session.add_all(orders)
	db.session.commit()

	"""images = list()
	#id, user, product, amount
	images.append(Image(seller_id="1", name="Labtop",
		formatting="png"))
	images.append(Image(seller_id="2", name="Mobile",
		formatting="jpg"))
	images.append(Image(seller_id="3", name="Lobtop",
		formatting="png"))
	images.append(Image(seller_id="4", name="Mobile",
		formatting="jpg"))
	images.append(Image(seller_id="5", name="Keyboard",
		formatting="png"))
	images.append(Image(seller_id="6", name="Mouse",
		formatting="png"))
	images.append(Image(seller_id="1", name="USB",
		formatting="png"))
	images.append(Image(seller_id="2", name="Notebook",
		formatting="png"))
	images.append(Image(seller_id="3", name="Spoon",
		formatting="jpg"))
	images.append(Image(seller_id="4", name="Fork",
		formatting="png"))
	images.append(Image(seller_id="5", name="Camera",
		formatting="png"))
	images.append(Image(seller_id="6", name="Radio",
		formatting="jpg"))
	images.append(Image(seller_id="1", name="Pen",
		formatting="png"))
	images.append(Image(seller_id="2", name="Back bag",
		formatting="jpg"))
	images.append(Image(seller_id="3", name="Wireless Headphones",
		formatting="png"))

	db.session.add_all(images)
	db.session.commit()"""






def get_in_stock_products():
    products = Product.query.filter(Product.in_stock==True
        ).order_by(Product.id).all()
    toReturn = []
    for product in products:
    	toReturn.append(product.simple())
    return toReturn
