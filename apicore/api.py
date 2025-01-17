from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded


app = Flask(__name__)


# Initialize the Limiter
limiter = Limiter(
   key_func=lambda: (request.headers.get('Authorization') or get_remote_address()),  # Falling back to IP if header is missing
   app=app
)




def get_user_type_rate_limit():
   user_type = request.headers.get('X-User-Type', 'guest')  # Default to 'guest' if not provided


   if user_type == 'PREMIUM':
       return "5 per minute"
   elif user_type == 'FREEMIUM':
       return "3 per minute"
   else:
       return "1 per minute"




@app.errorhandler(RateLimitExceeded)
def handle_ratelimit_error(e):
   return jsonify(error="Usted posee el plan FREEMIUM, puede realizar como máximo 5 solicitudes por minuto (RPM). "
                        "Actualice el plan a PREEMIUM o espere unos momentos, gracias!"), 429




@app.errorhandler(RateLimitExceeded)
def handle_ratelimit_exceeded(e):
   user_type = request.headers.get('X-User-Type', 'guest')


   if user_type == 'PREMIUM':
       message = "Has superado tu límite de solicitudes por minuto. Como usuario PREMIUM, puedes esperar un momento " \
                 "y volver a intentarlo, gracias."
   elif user_type == 'FREEMIUM':
       message = "Has superado tu límite de solicitudes por minuto como usuario FREEMIUM. Actualiza a PREMIUM para " \
                 "realizar más solicitudes o vuelve a intentarlo más tarde, gracias."
   else:
       message = "Has superado tu límite de solicitudes por minuto. Considera contratar un plan para mas accesos o " \
                 "espera un momento y vuelve a intetar mas tarde, gracias."


   return jsonify({'error': message}), 429




@app.route("/")
@limiter.limit("3 per minute")  # Specific limit for this endpoint
def hello_world():
   return "<p>Hello, World!</p>"




@app.route('/service', methods=['POST'])
@limiter.limit(lambda: get_user_type_rate_limit())
def service():
   # Access headers
   authorization = request.headers.get('Authorization')
   # Retrieve JSON data from the request
   data = request.get_json()


   if not data:
       return jsonify({'error': 'Invalid or missing JSON data'}), 400


   # Access properties within the JSON data
   apartments_list = data.get('inputs')
   if not apartments_list:
       return jsonify({'error': 'Missing required fields'}), 400


   # Example operations
   print(f"Apartments: {apartments_list}")
   print(f"Authorization: {authorization}")


   return jsonify({'apartments_list': apartments_list, 'Authorization': authorization}), 200