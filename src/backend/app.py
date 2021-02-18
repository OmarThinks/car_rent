TESTING=True
"""
TESTING=False 	IN CASE OF PRODUCTION
TESTING=True 	IN CASE OF TESTING
"""
from flask import (Flask, abort, jsonify)
from flask_sqlalchemy import SQLAlchemy
import secrets
import os
from __init__ import db, SECRET
from models import (NotReceived, User, #Product, Order, #Image,
	db_drop_and_create_all, populate_tables)
from auth import (requires_auth)
from flask_cors import CORS
from pydantic_models import (validate_model_id, validate_model_id_pydantic,
UserPost, UserUpdatePassword#, ProductPost, OrderPost, OrderUpdate
)
from flask_pydantic import validate


if "SECRET" in os.environ:
	SECRET = os.environ["SECRET"]




class config:
	#SECRET_KEY=os.urandom(32)
	SECRET_KEY=secrets.token_urlsafe(5000)
	basedir = os.path.abspath(os.path.dirname(__file__))
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = "sqlite:///databases/database.sqlite"
	SQLALCHEMY_TRACK_MODIFICATIONS= False


class config_test:
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///databases/test.sqlite"

class config_docker:
	SQLALCHEMY_DATABASE_URI = "sqlite:////database//database.sqlite"


def create_app(DOCKER=False,testing=TESTING):
	app = Flask(__name__)
	app.config.from_object(config)
	if TESTING:
		app.config.from_object(config_test)
	if DOCKER:
		app.config.from_object(config_docker)

	db.app = app
	db.init_app(app)
	db.create_all()

	CORS(app,resources={r"*":{"origins":"*"}})
	@app.after_request
	def after_request(response):
		response.headers.add("Access-Control-allow-Origin","*")
		response.headers.add("Access-Control-allow-Headers",
			"Content-Type,Autorization,true")
		response.headers.add("Access-Control-allow-Methods",
			"GET,PUT,POST,DELETE,OPTIONS")
		db.session.rollback()
		return response













































	@app.route('/r', methods=['GET'])
	def raised():
		# Testng the ability to raise custom responses
		abort(make_response(jsonify({"sucess":True}),200))
		return jsonify({"success":False})












	"""
	1)	"/clear_tables"-------->"GET" , "OPTIONS"
	"""
	@app.route("/clear_tables", methods=["GET"])
	def clear_all_tables():
		test_only()
		db_drop_and_create_all()
		"""
Tests: test_02_populate_test
		"""
		return jsonify({"success":True})








	"""
	2)	"/populate" ->--------->"GET" , "OPTIONS"
	"""
	@app.route("/populate", methods=["GET"])
	def populate_all_tables():
		test_only()
		#This endpoint will clear all the data in the database and
		#populate with new data
		try:
			populate_tables()
			return jsonify({"success":True})
		except:
			abort(422) #Unprocessible
		"""
Tests: test_01_clear_tables
		"""



	"""
	User endpoints:
	post_users
	delete users
	login
	"""


	@app.route("/users/who", methods=["POST"])
	def users_who():
		#This endpoint will tell if the user should pass or not
		#and if his token expired, it will refresh it
		if "cantiin" not in request.cookies:
			abort(401)
		#Now the cookie exists
		token = request.cookies["cantiin"]
		#print(SECRET,flush=True)
		#print(request.cookies,flush=True)
		token_validation = validate_token(
			token=token,secret=SECRET)
		#print(token_validation,flush=True)
		#print("WHO: "+str(token_validation),flush=True)
		if token_validation["case"]==3:
			abort(401)
		if token_validation["case"]==2:
			res=jsonify({"success":True})
			user_id=token_validation["payload"]["uid"]
			res.set_cookie
			response=auth_cookie_response(
				response={"success":True,
				"result":"refreshed expired token",
				"user_id":user_id},
				user_id=user_id)
			return response
		else:
			return jsonify({"success":True,
				"result":"user is logged in",
				"user_id":token_validation["payload"]["uid"]})





	@app.route("/users", methods=["POST"])
	def post_users():
	#This endpoint will add a new user
		try:
			body = request.get_json()
		except:
			abort(make_response(jsonify(
			{"description":"request body can not be parsed to json",
			"message":"bad request"}),400))
			#return my_error(status=400,
			#	description="request body can not be parsed to json")
		try:
			username = body.get("username",None)
			password1 = body.get("password1",None)
			password2 = body.get("password2",None)
		except:
			abort(make_response(jsonify(
			{"description":"there is no request body",
			"message":"bad request"}),400))
			#return my_error(status=400,
			#	description = "there is no request body")

		#Validating inputs one by one
		username_validation = validate_must(
			input=username,type="s",input_name_string="username",
			minimum=2,maximum=150)
		password1_validation = validate_must(
			input=password1,type="s",input_name_string="password1",
			minimum=8,maximum=150)
		password2_validation = validate_must(
			input=password2,type="s",input_name_string="password2",
			minimum=8,maximum=150)

		#Validating inputs a group
		val_group=validate_must_group(
			[username_validation,password1_validation
			,password2_validation])

		#Now we will validate all inputs as a group
		if val_group["case"] == True:
			# Success: they pass the conditions
			username,password1,password2=val_group["result"]
		else:
			# Failure: Something went wrong
			return val_group["result"]
		#Now we have username, password1 and password2 as strings

		#validate that the username has no white spaces
		if " " in username:
			abort(make_response(jsonify(
			{"description":"username can not contain white spaces",
			"message":"unprocessible"}),422))
			#return my_error(status=422,
			#	description="username can not contain white spaces")

		#Validate that this username is unique
		all_users=User.query.all()
		all_names=[str(u.username) for u in all_users]
		if username in all_names:
			abort(make_response(jsonify(
			{"description":"this username already exists",
			"message":"unprocessible"}),422))
			#return my_error(status=422,
			#	description="this username already exists")

		#Validate that these passwords are not the same
		if password1!=password2:
			abort(make_response(jsonify(
			{"description":"please enter the same password",
			"message":"unprocessible"}),422))
			#return my_error(status=422,
			#	description="please enter the same password")

		#Create the user
		new_user = User(username=username, password=password1)

		#Insert the user in the database
		try:
			new_user.insert()
			response=auth_cookie_response(
				response={"success":True,"user":new_user.simple()},
				user_id=new_user.id)
			return response
		except Exception as e:
			raise(e)
			db.session.rollback()
			abort(500)






	@app.route("/users", methods=["DELETE"])
	@requires_auth()
	def delete_users(payload):
	#This endpoint will delete an existing user
		user_id=payload["uid"]
		users_query=User.query
		user_id_validation=validate_model_id(
			input_id=user_id,model_query=users_query
			,model_name_string="user")
		if user_id_validation["case"]==1:
			#The user exists
			user=user_id_validation["result"]

		else:
			#No user with this id, can not convert to int,
			# or id is missing (Impossible)
			return my_error(
				status=user_id_validation["result"]["status"],
				description=user_id_validation
				["result"]["description"])

		#Now, we have "user", this is essential

		try:
			# Finally, deleting the user itself
			user.delete()
			r=jsonify({"success":True,
					"result":"user deleted successfully"})
			cookies=request.cookies
			for co in cookies:
				r.set_cookie(co,value="",expires=-50)
			return r
			#return jsonify({"success":True,
			#	"result":"user deleted successfully"})
		except Exception as e:
			raise(e)
			db.session.rollback()
			abort(500)














	@app.route("/users/login", methods=["POST"])
	def login_users():
	#This endpoint will log the user in
		try:
			body = request.get_json()
		except:
			abort(make_response(jsonify(
			{"description":"request body can not be parsed to json",
			"message":"bad request"}),400))
			#return my_error(status=400,
			#	description="request body can not be parsed to json")
		try:
			username = body.get("username",None)
			password = body.get("password",None)
		except:
			abort(make_response(jsonify(
			{"description":"there is no request body",
			"message":"bad request"}),400))
			#return my_error(status=400,
			#	description = "there is no request body")

		#Validating inputs one by one
		username_validation = validate_must(
			input=username,type="s",input_name_string="username",
			minimum=2,maximum=150)
		password_validation = validate_must(
			input=password,type="s",input_name_string="password",
			minimum=8,maximum=150)

		#Validating inputs a group
		val_group=validate_must_group(
			[username_validation,password_validation])

		#Now we will validate all inputs as a group
		if val_group["case"] == True:
			# Success: they pass the conditions
			username,password=val_group["result"]
		else:
			# Failure: Something went wrong
			return val_group["result"]
		#Now we have username, password and password2 as strings

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
			abort(make_response(jsonify(
			{"description":"wrong username or password",
			"message":"unprocessible"}),422))
			#return my_error(status=422,
			#	description="wrong username or password")
		#now we have the_user_id as integer


		response=auth_cookie_response(
			response={"success":True,
			"result":"logged in successfully",
			"user_id":the_user_id},
			user_id=the_user_id)
		return response

		#return jsonify()


	@app.route("/users/logout", methods=["POST"])
	def logout_users():
	#This endpoint will log the user out
		cookies = request.cookies
		r=jsonify({"success":True,
			"result":"logged out successfully"})
		for co in cookies:
			r.set_cookie(co,value="",expires=-50)
		return r
		#return jsonify({"success":True,
		#	"result":"logged out successfully"})











	@app.route("/users/login/test", methods=["POST"])
	def login_test():
		test_only()
	#This endpoint will log the user in
		response=auth_cookie_response(
			response={"success":True,
			"result":"logged in successfully",
			"user_id":1},
			user_id=1)
		return response


	@app.route("/users/login/expired", methods=["POST"])
	def login_expired():
		test_only()
	#This endpoint will log the user in with expired token
		res = jsonify(
					{"success":True,
					"result":"setting expired token successfully"})
		expired_token=generate_token(user_id=1,secret=SECRET,
    		expiration_delta=timedelta(days=-7),
    		issued_at=datetime.now())
		res.set_cookie('cantiin',
		 value=expired_token["result"],
			httponly=True, samesite='Lax')
		return res,200
















































































	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({"success":False,"error":400,
			"message":"bad request"}),400


	@app.errorhandler(401)
	def unauthorized(error):
		return jsonify({"success":False,"error":401,
			"message":"unauthorized"}),401


	@app.errorhandler(403)
	def forbidden(error):
		return jsonify({"success":False,"error":403,
			"message":"forbidden"}),403


	@app.errorhandler(404)
	def not_found(error):
		return jsonify({"success":False,"error":404,
			"message":"not found"}),404


	@app.errorhandler(405)
	def method_not_allowed(error):
		return jsonify({"success":False,"error":405,
			"message":"method not allowed"}),405


	@app.errorhandler(422)
	def unprocessible(error):
		return jsonify({"success":False,"error":422,
			"message":"unprocessible"}),422


	@app.errorhandler(500)
	def internal_server_error(error):
		return jsonify({"success":False,"error":500,
			"message":"internal server error"}),500



	def test_only():
		if testing == False:
			abort(404)


	return app

if __name__ == '__main__':
	create_app().run()
