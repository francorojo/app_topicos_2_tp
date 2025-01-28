from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from pymemcache.client import base
from simple_rest_client.api import API

app = Flask(__name__)

# create users api instance
users_api = API(
   api_root_url='http://localhost:5001/',  # base api url
   params={},  # default params
   headers={},  # default headers
   timeout=2,  # default timeout in seconds
   append_slash=False,  # append slash to final url
   json_encode_body=True,  # encode body as json
)
users_api.add_resource(resource_name='users')

# create log api instance
log_api = API(
   api_root_url='http://localhost:8000/',  # base api url
   params={},  # default params
   headers={},  # default headers
   timeout=2,  # default timeout in seconds
   append_slash=False,  # append slash to final url
   json_encode_body=True,  # encode body as json
)
log_api.add_resource(resource_name='log')

# Initialize the Limiter
limiter = Limiter(
   key_func=lambda: (request.headers.get('Authorization') or get_remote_address()),
   # Falling back to IP if header is missing
   app=app
)

# Initialize the Cache
client = base.Client(('localhost', 11211))


# START Rate Limit Section
def get_user_type_rate_limit():
   # Access headers
   authorization = request.headers.get('Authorization')
   # Try search in cache
   user_type = client.get(authorization)

   if user_type is None:  # Cache failed and set value
       request_params = {'api_key': authorization,
                         'access_token': 'valid-token'}  # TODO podríamos usar key para sumar seguridad entre servicios
       response = users_api.users.list(body=None, params=request_params, headers={})
       if not response.body:
           user_type = "NOT_REGISTERED"
       else:
           user_type = response.body[0]['type']
       client.set(authorization, user_type, expire=60)  # 60 seconds
   else:
       user_type = user_type.decode('ASCII')

   if user_type == 'PREMIUM':
       return "5 per minute"
   elif user_type == 'FREEMIUM':
       return "3 per minute"
   elif user_type == 'NOT_REGISTERED':
       return "0 per minute"
   else:
       return "1 per minute"


@app.errorhandler(RateLimitExceeded)
def handle_ratelimit_exceeded(e):
   # Access headers
   authorization = request.headers.get('Authorization')
   user_type = client.get(authorization).decode('ASCII')

   if user_type == 'PREMIUM':
       message = "Has superado tu límite de solicitudes por minuto como usuario PREMIUM, debes esperar un momento."
   elif user_type == 'FREEMIUM':
       message = "Has superado tu límite de solicitudes por minuto como usuario FREEMIUM, debes esperar un momento."
   elif user_type == 'NOT_REGISTERED':
       return jsonify({'error': "El usuario no se encuentra registrado."}), 400
   else:
       message = "Has superado tu límite de solicitudes por minuto. Considera contratar un plan para mas accesos."

   log_message('Rate limit error key user: ' + authorization + " - message: " + message, "INFO")
   return jsonify({'error': message}), 429
# END Rate Limit Section


# START Log Section
def log_message(message, tag_type):
   body = {'service': "api core - service",
           'message': message,
           'tag_type': tag_type}
   log_api.log.create(body=body, params={}, headers={})
# END Log Section


@app.route('/service', methods=['POST'])
@limiter.limit(lambda: get_user_type_rate_limit())
def service():
   authorization = request.headers.get('Authorization')
   data = request.get_json()

   if not data:
       log_message('Key user: ' + authorization + " - Invalid or missing JSON data", "ERROR")
       return jsonify({'error': 'Invalid or missing JSON data'}), 400
   else:
       apartments_list = data.get('inputs')
       if not apartments_list:
           return jsonify({'error': 'Missing required fields'}), 400

   log_message('New request key user: ' + authorization + " - Result: " + apartments_list, "INFO")
   return jsonify({'apartments_list': apartments_list, 'Authorization': authorization}), 200