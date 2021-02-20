import secrets
import json
from flask import request, _request_ctx_stack,abort,jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from functions import *
#from app import *
from datetime import timedelta,date,datetime,time
import os
import sys
import jwt
import base64
from models import User

try:
    from __init__ import *
except:
    from src import *



if "SECRET" in os.environ:
    SECRET = os.environ["SECRET"]
"""
Inputs:
    - payload:  Type must be dictionary
    - secret:   Type must be string

Outputs:
    -A dictionary:
        - success:  True or False
        - result:
            - If suucess=True: The JWT Token
            - If success=False:The error
"""
def generate_jwt(payload,secret):
    algorithm = "HS256"
    try:
        #print("jwt secret: "+str(secret))
        encoded_jwt = jwt.encode(
            payload,secret,algorithm=algorithm)
        return {"success":True,
        "result":str(encoded_jwt)}
    except Exception as e:
        return{"success":False,"result":e}





"""
Inputs:
    - encoded_jwt:  Type must be String
    - secret:       Type must be string

Outputs:
    -A dictionary:
        - success:  True or False
        - result:
            - If suucess=True: The Payload as a dictionary
            - If success=False:The error
"""
def decode_jwt(encoded_jwt,secret):
    secret=str(secret)
    try:
        result = jwt.decode(
            encoded_jwt, secret,algorithms="HS256",verify=True)
        return {"success":True,"result":result}
    except jwt.ExpiredSignatureError:
        result = jwt.decode(
            encoded_jwt, secret,algorithms="HS256",
            options={"verify_exp":False})
        return {"success":True,"result":result}
    except Exception as e:
        return {"success":False,"result":e}







def generate_token(user_id,secret=SECRET,
    expiration_delta=EXPIRATION_AFTER,
    issued_at=datetime.now()):

    user_id_validation=validate_integer(
    input_integer=user_id,input_name_string="user_id",
    maximum=10000000000000000000000000000000000000000,minimum=1)
    secret_validation=validate_string(
        input_string=secret,string_name="secret",minimum_length=3,
    max_length=100000000000000000000000000000000000000000)

    #Now we will validate user_id
    if user_id_validation["case"] == 1:
        # Success: they pass the conditions
        user_id=user_id_validation["result"]
    else:
        # Failure: Something went wrong
        return {"success":False,
        "result":user_id_validation["result"]}

    #Now we will validate secret
    if secret_validation["case"] == 1:
        # Success: they pass the conditions
        secret=secret_validation["result"]
    else:
        # Failure: Something went wrong
        return {"success":False,
        "result":secret_validation["result"]}

    expiration_datetime=issued_at+expiration_delta
    expiration_epoch=expiration_datetime.timestamp()

    payload = { "uid" : user_id , "exp" : expiration_epoch }
    jwt_generated = generate_jwt(payload=payload,secret=secret)
    return jwt_generated




"""
Inputs:
    - token:    string of the token
    - secret:   string of the secret
Outputs:
    - { "case":      1 or 2 or 3,
        "token":    string of token to be assigned
        "error":    the error message
        "payload:   the payload of the token"}
        -   "case":
            -   1:  success
            -   2:  expired token
            -   3:  something went wrong
        -   "token":
            -   case:1: the same old token
            -   case:2: token refreshed
            -   case:3: "" empty string (You must delete the cookie)
        -   "error":
            -   case:1: "" empty string
            -   case:2: "expired token"
            -   case:3: "error message"
        -   "payload":
            -   case:1: payload
            -   case:2: expired payload
            -   case:3: ""empty string
            -   NOTE:   exp in payload is the old expiration

"""
def validate_token(token,secret):
    decoded_jwt = decode_jwt(token,secret)
    #print(decoded_jwt)
    payload=""
    if decoded_jwt["success"]:
        payload=decoded_jwt["result"]
    else:
        return {"case":3,"token":"",
        "error":decoded_jwt["result"],"payload":""}
        #{"success":False,"result":error string}
    #Now we Have Payload
    user_id=0
    expiration=0
    try:
        user_id=payload["uid"]
    except:
        return {"case":3,"token":"",
        "error": "payload does not contain user_id"}
    try:
        expiration=payload["exp"]
    except:
        return {"case":3,"token":"",
        "error": "payload does not contain expiration_date",
        "payload":""}


    user_id_validation=validate_model_id(
        input_id=user_id,model_query=User.query,
        model_name_string="user")
    #print("user_id_validation: "+str(
    #    user_id_validation["result"].id),
    #   flush=True)
    #validate_integer(
    #input_integer=user_id,input_name_string="user_id",
    #maximum=10000000000000000000000000000000000000000,minimum=1)
    exp_validation=validate_integer(
        input_integer=expiration,input_name_string="expiration",
    maximum=10000000000000000000000000000000000000000,minimum=1)

    #Now we will validate user_id
    if user_id_validation["case"] == 1:
        # Success: they pass the conditions
        user_id=user_id_validation["result"].id
    else:
        # Failure: Something went wrong
        return {"case":3,"token":"",
        "error": user_id_validation["result"]["description"],
        "payload":""}

    #Now we will validate exp
    if exp_validation["case"] == 1:
        # Success: they pass the conditions
        exp=exp_validation["result"]
    else:
        # Failure: Something went wrong
        return {"case":3,"token":"",
        "error": exp_validation["result"]["description"],
        "payload":""}

    now_epoch=int(datetime.now().timestamp())
    if now_epoch>exp:
        #Expired token
        case = 2
        new_token=generate_token(user_id,secret)["result"]
        error="expired token"
    else:
        #Valid Token
        case = 1
        new_token=token
        error=""
    #print(secret,flush=True)
    return {"case":case,"token":new_token,"error":error,
    "payload":payload}













def auth_cookie_response(response,user_id,exp=None):
    response = jsonify(response)
    cookie_value = generate_token(
        user_id=user_id,secret=SECRET)["result"]
    response.headers.add("Authorization",cookie_value)
    """if exp==None:
        response.headers.add('Authorization',cookie_value
        #,httponly=True, samesite='Lax',
        #expires=datetime.now()+EXPIRATION_AFTER
        )
    else:
        response.headers.add('Authorization',cookie_value
        #,httponly=True,samesite='Lax',expires=exp
        )"""
    return response

def auth_cookie_response_new(response,user_id,exp=None):
    response = jsonify(response)
    cookie_value = generate_token(
        user_id=user_id,secret=SECRET)["result"]
    response.headers.add("Authorization",cookie_value)

    """if exp==None:
        print("case 1", flush=True)
        response.headers.add("Authorization",cookie_value)
        response.headers.add('Authorization',cookie_value
        #,httponly=False, samesite='Lax',
        #expires=datetime.now()+EXPIRATION_AFTER
        )
    else:
        response.headers.add("Authorization",cookie_value)
        response.headers.add('Authorization',cookie_value
        #,httponly=False,samesite='Lax',expires=exp
        )"""
    return response




def cookie_auth():
    if "Authorization" not in request.headers:
        abort(401)
    #Now the cookie exists
    token = request.headers["Authorization"]
    token_validation = validate_token(token=token,secret=SECRET)
    #print(token_validation["case"],flush=True)
    #print(token_validation,flush=True)
    if token_validation["case"]==3 or token_validation["case"]==2:
        abort(401)
    return token_validation["payload"]












def get_token_auth_cookie():
    """Obtains the Access Token from the Authorization Cookie
    """

    auth = request.headers.get("Authorization", None)
    if not auth:

        abort(401)
        raise AuthError({"code": "authorization_missing",
                        "description":
                            "Authorization is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        abort(401)
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        abort(401) # No token Sent
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        abort(401)
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token










def requires_auth():
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            #return f(*args, **kwargs)
            payload = cookie_auth()
            #check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
























def datetime_to_epoch(input):
    pass








#Defining the variables from my auth0 account
AUTH0_DOMAIN = 'domain'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

"""



"""

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """

    auth = request.headers.get("Authorization", None)
    if not auth:

        abort(401)
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        abort(401)
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        abort(401) # No token Sent
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        abort(401)
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if permission == "public": return
    if permission == "": return
    if permission in payload["permissions"]:
        return
    abort(401)


















'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    try:
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
    except:
        abort(401)#non existent user
    try:
        unverified_header = jwt.get_unverified_header(token)
    except:
        abort(401) # Wrong signature
    rsa_key = {}
    for key in jwks["keys"]:
        try:
            key["kid"]
            unverified_header["kid"]
        except:
            abort(401)
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            abort(401)#Token is expiered
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            abort(401)
            raise AuthError({"code": "invalid_claims",
                            "description":
                                "incorrect claims,"
                                "please check the audience and issuer"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                    "description":
                        "incorrect claims,"
                        "please check the audience and issuer"}, 401)

        except Exception:
            abort(401)
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

        _request_ctx_stack.top.current_user = payload
        #return f(*args, **kwargs)
    raise AuthError({"code": "invalid_header",
                    "description": "Unable to find appropriate key"}, 401)

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


"""
Old function reference
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            #return f(*args, **kwargs)
            if permission == "": return f(*args, **kwargs)
            if permission == "public": return f(*args, **kwargs)
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(#payload,
                *args, **kwargs)

        return wrapper
    return requires_auth_decorator
"""
