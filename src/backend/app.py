TESTING=True
"""
TESTING=False 	IN CASE OF PRODUCTION
TESTING=True 	IN CASE OF TESTING
"""
from flask import (Flask, abort, jsonify, make_response, request)
from flask_sqlalchemy import SQLAlchemy
import secrets
import os
from __init__ import db, SECRET
from models import (NotReceived, User, #Product, Order, #Image,
	db_drop_and_create_all, populate_tables)
from auth import (requires_auth, auth_cookie_response ,
auth_cookie_response_new, validate_token)
from flask_cors import CORS
from pydantic_models import (validate_model_id_pydantic,
UserPost, UserUpdatePassword, UserLogin#, ProductPost, OrderPost, OrderUpdate
)
from flask_pydantic import validate
from functions import validate_model_id

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
			"*,Content-Type,true")
		response.headers.add("Access-Control-allow-Methods",
			"GET,PUT,POST,DELETE,OPTIONS")
		response.headers.add("Access-Control-Expose-Headers",
			"Authorization,Set-Cookie")
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
		the_401_error = jsonify({
			"error": 401,"message": "unauthorized",
			"success": False})
		the_401_error.headers.add("Authorization","")


		if "Authorization" not in request.headers:
			return the_401_error,401
		#Now the cookie exists
		token = request.headers["Authorization"]
		#print(SECRET,flush=True)
		#print(request.cookies,flush=True)
		token_validation = validate_token(
			token=token,secret=SECRET)
		#print(token_validation,flush=True)
		#print("WHO: "+str(token_validation),flush=True)
		if token_validation["case"]==3:
			return the_401_error,401

		if token_validation["case"]==2:
			res=jsonify({"success":True})
			user_id=token_validation["payload"]["uid"]
			response=auth_cookie_response(
				response={"success":True,
				"result":"refreshed expired token",
				"user_id":user_id},
				user_id=user_id)
			return response
		else:
			res = jsonify({"success":True,
				"result":"user is logged in",
				"user_id":token_validation["payload"]["uid"]})
			res.headers.add("Authorization",token)
			return res





	@app.route("/users", methods=["POST"])
	@validate()
	def post_users(body:UserPost):
	#This endpoint will add a new user
		username = body.username
		password = body.password1
		#return jsonify({"success":True,
		#"username":username,"password":password
		#})


		#Create the user
		new_user = User(username=username, password=password)

		#Insert the user in the database
		try:
			new_user.insert()
			response=auth_cookie_response(
				response={"success":True,"user":new_user.simple()},
				user_id=new_user.id)
			return response
		except Exception as e:
			raise(e)
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
	@validate()
	def login_users(body:UserLogin):
	#This endpoint will log the user in
		the_user_id = body.password
		response=auth_cookie_response(
			response={"success":True,
			"result":"logged in successfully",
			"user_id":the_user_id},
			user_id=the_user_id)
		return response



	@app.route("/users/logout", methods=["POST"])
	def logout_users():
	#This endpoint will log the user out
		cookies = request.cookies
		r=jsonify({"success":True,
			"result":"logged out successfully"})
		r.headers.add("Authorization","")
		return r











	@app.route("/users/login/test", methods=["POST"])
	def login_test():
		test_only()
	#This endpoint will log the user in
		response=auth_cookie_response_new(
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
