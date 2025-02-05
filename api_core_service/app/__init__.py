from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymemcache.client import base
from flask_limiter.errors import RateLimitExceeded
from app.utils import user_by_api_key, log

app = Flask(__name__)

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
       response = user_by_api_key(authorization)
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

   log('Rate limit error key user: ' + authorization + " - message: " + message, "INFO")
   return jsonify({'error': message}), 429
# END Rate Limit Section

from . import routes
