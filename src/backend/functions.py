"""
Functions:

- my_error(status=404 ,description=""):
- get_in_stock_products()


- validate_model_id(input_id,model_query,model_name_string)
- validate_string(input_string,max_length,string_name)
- validate_boolean(input_boolean,input_name_string)
- validate_integer(input_integer,input_name_string,maximum,minimum)
- validate_float(input_float,input_name_string,maximum,minimum)



- db_drop_and_create_all()
- populate_tables()




- QUESTIONS_PER_PAGE = 10
- def paginate_questions(questions_list,pagination)
- def question_search(input_text)


"""

try:
	from __init__ import *
except:
	from src import *



ALLOWED_IMAGE_FORMATS=["png","jpg"]




import json
from flask import Flask, request, jsonify, abort
import base64
# Creatng a function to print the error in an approperiate way 
#with detailed info
def my_error(status=404 ,description=""):
	
	if status not in [400,401,403,404,405,422,500]:
		raise Exception("status is "+str(status)
			+ ", not in [[400,401,403,404,405,422,500]]")
	if status == 400: message = "bad request"
	elif status == 401: message = "unauthorized"
	elif status == 403: message = "forbidden"
	elif status == 404: message = "not found"
	elif status == 405: message = "method not allowed"
	elif status == 422: message = "unprocessible"
	else : message = "internal server error"

	error_dict = {"success": False, 
		"error": status,"message": message,}

	if description == "": return jsonify(error_dict),status
	
	error_dict["description"] = description
	return jsonify(error_dict),status















def get_in_stock_products():
    return Product.query.filter(Product.in_stock==True
        ).order_by(Product.id).all()





"""
This function has 3 inputs:
1)	input_id: an integer, to be valiudated that 
		it exists or not in the table
		Example: 1, 2 or 50
2)	model_query: this is the query of the model
		Example: Product.query, Order.query
3)	name_tring: the name of the table
		Example: "product", "order"

Output:
-	{case,result}
case:1
	-	Successful: id exists
	-	result = correct output
case:2
	-	UnSuccessful: id does not exist
	-	result = [] (empty list)

case:3
	- 	Failed:	there was an error while validating
	- 	result:	error message
case:4
	-	Failed input is none
	- 	result:	None

"""
def validate_model_id(input_id,model_query,model_name_string):
	#Validate that model id has a value, not None
	if input_id == None: return {"case":4,"result":{"status":400, 
			"description":model_name_string+
			" is missing"}}
	
	#Validate that model id can be converted to int
	try:
		id = int(input_id)
	except:
		return {"case":3,"result":{"status":400, 
			"description":model_name_string+
			" id can not be converted to integer"}} 
		#[False,my_error(status=400, description=model_name_string+" id can not be converted to integer")]
	
	#Validate that id is not negative or zero
	if id<=0:
		return {"case":3,"result":{"status":422, 
			"description":model_name_string+ 
			" id can not be less than"+
			" or equal to 0"}} 

	try:
		item = model_query.filter_by(id=id).all()
	except Exception as e:
		return {"case":3,"result":{"status":400, 
			"description":model_name_string+
			" id can not be converted to integer"}} 
	if len(item) == 0 :
		return {"case":2,"result":{"status":422, 
			"description":"there is no " +model_name_string+
			" with this id"}} 

	return {"case":1,"result":item[0]}





def validate_string(input_string,string_name,minimum_length=0,
	max_length=1000000):
	#Validate that input has a value, not None
	if input_string == None: return {"case":3,"result":None}
	
	#Validate that input can be converted to string
	try:
		result = str(input_string)
	except:
		return {"case":2,"result":{"status":400, 
			"description":string_name+
			" can not be converted to string"}} 
	
	#Validate that input length is less that 100
	if len(result)>max_length:
		return {"case":2,"result":{"status":422, 
			"description":"maximum "+ string_name
			+" length is "+str(max_length)+" letters"}} 

	if len(result)<minimum_length:
		return {"case":2,"result":{"status":422, 
			"description":"minimum "+ string_name
			+" length is "+str(minimum_length)+" letters"}} 

	return {"case":1,"result":result}







def validate_boolean(input_boolean,input_name_string):
	#Validate that product input_boolean has a value, not None
	if input_boolean == None: return {"case":3,"result":None}
	
	#Validate that input_boolean can be converted to boolean

	found_it=False

	if (input_boolean==True or input_boolean=="true" or
	 input_boolean=="True" or input_boolean==1 or
	  input_boolean=="1"):
		found_it=True
		result=True
	if (input_boolean==False or input_boolean=="false" or
	 input_boolean=="False" or input_boolean==0 or
	  input_boolean=="0"):
		found_it=True
		result=False


	if found_it == True:
		return {"case":1,"result":result}
	return {"case":2,"result":{"status":400, 
			"description":input_name_string+" can not be "+
			"converted to boolean"}} 







def validate_integer(
	input_integer,input_name_string,maximum,minimum):
	#Validate that input has a value, not None
	if input_integer == None: return {"case":3,"result":None}
	
	#Validate that input can be converted to int
	try:
		result = int(input_integer)
	except:
		return {"case":2,"result":{"status":400, 
			"description":input_name_string+
			" can not be converted to integer"}} 
	
	#Validate that input is not less than minimum
	if result<int(minimum):
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be less than "+ str(minimum)}} 

	#Validate that input is not more than maximum
	if result>int(maximum):
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be more than "+ str(maximum)}} 
	return {"case":1,"result":result}



def validate_float(
	input_float,input_name_string,maximum,minimum):
	#Validate that input has a value, not None
	if input_float == None: return {"case":3,"result":None}
	
	#Validate that input can be converted to float
	try:
		result = float(input_float)
	except:
		return {"case":2,"result":{"status":400, 
			"description":input_name_string+
			" can not be converted to float"}} 
	
	#Validate that input is not less than minimum
	if result<float(minimum):
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be less than "+ str(minimum)}} 

	#Validate that input is not more than maximum
	if result>float(maximum):
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be more than "+ str(maximum)}} 
	return {"case":1,"result":result}



def validate_base64(
	input_string,input_name_string,maximum_length,minimum_length):
	#Validate that input has a value, not None
	if input_string == None: return {"case":3,"result":None}

	#Validate that input is string
	if type(input_string)!= str:
		return {"case":2,"result":{"status":400, 
			"description":input_name_string+
			" is not a string"}}
		 
	#Validate that input length is not less than minimum
	if len(input_string)<minimum_length:
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" length can not be less than "+ str(minimum_length)+ " characters"}} 

	#Validate that input length is not more than maximum
	if len(input_string)>maximum_length:
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" length can not be more than "+ str(maximum_length)+ " characters"}} 

	validation = isBase64(input_string)
	if validation == True:
		return {"case":1,"result":input_string}
	else:
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be converted to base64"}} 

def validate_formatting(input_formatting):
	validation = validate_string(input_formatting,"formatting",minimum_length=2,
	max_length=20)
	if validation["case"] != 1:
		return validation
	input_formatting = validation["result"]
	if input_formatting not in ALLOWED_IMAGE_FORMATS:
		return {"case":2,"result":{"status":422, 
			"description":str(input_formatting)+" is not allowed image format"}} 
	return {"case":1,"result":input_formatting}







"""
type:
	- "s" : String
	- "i" : Integer
	- "f" : Float
	- "b" : Boolean
	- "b64" : base64
	- "frmt": Image Formatting

"""
def validate__must(input,type,
	input_name_string,maximum=0,minimum=0):
	validation=0;
	if type == "s":
		validation= validate_string(
			input_string=input,
			max_length=maximum,string_name=input_name_string,
			minimum_length=minimum)
	elif type == "i":
		validation= validate_integer(
	input_integer=input,input_name_string=input_name_string,
	maximum=maximum,minimum=minimum)
	elif type == "f":
		validation= validate_float(
	input_float=input,input_name_string=input_name_string,
	maximum=maximum,minimum=minimum)
	elif type == "b":
		validation = validate_boolean(input_boolean=input
			,input_name_string=input_name_string)
	elif type == "b64":
		validation = validate_base64(
			input_string=input,input_name_string=input_name_string,
			maximum_length=maximum,minimum_length=minimum)
	elif type == "frmt":
		validation = validate_formatting(input_formatting=input)
	else:
		raise Exception("validate_must: type is"+str(type)
			+ "and it can not be like this, it should be: "+
			"'s', 'i', 'f' or 'b'")
	if validation["case"] == 1:
		# Success: correct data type
		return {"case":True,
		"result": validation["result"]}
	elif validation["case"] == 2:
		# Failure: Can't convert to correct data type
		return {"case":False,
		"result": {"status":validation["result"]["status"],
			"description":validation["result"]["description"]}}
	else:
		# no Input is given, result = None
		return  {"case":False,
		"result": {"status":400,"description":
			input_name_string+" is missing"}}





def validate_must(input,type,
	input_name_string,maximum=0,minimum=0):
	
	validation=validate__must(input=input,type=type,
	input_name_string=input_name_string,
	maximum=maximum,minimum=minimum)

	if validation["case"]:
		return validation
	return  {"case":False,
		"result": my_error(
		status=validation["result"]["status"]
			,description=validation["result"]["description"])}





def validate_must_group(validations_list):
	to_return=[]
	for val in validations_list:
		if val["case"]==True:
			to_return.append(val["result"])
		else: 
			return {"case":False,"result":val["result"]}
	return {"case":True,"result":to_return}  







# pass function will validate whther the input is base 64 or not
# True:base64
# False:Not base64
def isBase64(input_string):
	if type(input_string)!=str:
		return False
	if len(input_string)%4 != 0:
		return False
	for char in input_string:
		base64_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
		"n","o","p","q","r","s","t","u","v","w","x","y","z",
		"A","B","C","D","E","F","G","H","I","J","K","L","M",
		"N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
		"1","2","3","4","5","6","7","8","9","0","/","=","+"]
		if char not in base64_list:
			return False
	return True



"""
Inputs:
	- b64String: This is a string that has been validated to be b64
	- formatting: "png" ot "jpg" or a value in the ALLOWED_IMAGE_FORMATS list
"""
def b64ToImg(b64String,formatting):
	return "data:image/"+formatting+";base64,"+b64String


"""
We wil see how the frontend handles this first

Inputs:
	- imgString: a string that has been validated to 



def imgToB64(imgString):
	return "data:image/"+formatting+";base64,"+b64String
"""




def db_drop_and_create_all():
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

    images = list() 
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
    db.session.commit()





QUESTIONS_PER_PAGE = 10


def paginate_questions(questions_list,pagination):
	#This function will return a 
	#(Paginated, fomatted) list of questions
	min_index=(pagination-1) * QUESTIONS_PER_PAGE
	max_index=(pagination) * QUESTIONS_PER_PAGE
	paginated_formatted_questions_list = list()
	for index,question in enumerate(questions_list):
		if index >= min_index:
			if index < max_index:
				paginated_formatted_questions_list.append(
					question.format())
	return paginated_formatted_questions_list






"""
This method searches inside The question model.

Input: String to be searched
Output: Fomatted list of questions matching the search
"""
def question_search(input_text):
	search_query = input_text.strip()
	#To remove the spqce from the beginning and the end of string
	search_query = "%"+search_query+"%"
	all_questions = db.session.query(Question).filter(
		Question.question.ilike(search_query)).all()
	to_return = [question.format() for question in all_questions]
	return to_return





