import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Account
from westa.settings import SECRET_KEY

class SignUpView(View):
	def post(self, request):
		try:
			data = json.loads(request.body)
			if Account.objects.filter(email =data['email']).exists():
				return JsonResponse({"message":"EMAIL_ALREADY_EXISTS"}, status=400)

			password = data['password']
			password_bcrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
			password_decode = password_bcrypt.decode('utf-8')
			
			Account.objects.create(
				name     = data['name'],
				email    = data['email'],
				user_id  = data['user_id'],
				password = password_decode,
			).save()
			return JsonResponse({"message":"SUCCESS"},status=200)

		except KeyError:
			return JsonResponse({"message":"INVALID_KEYS"}, status=400)
		except json.decoder.JSONDecodeError:
			return JsonResponse({"message":"NO_DATA"}, status=401)

class SignInView(View):
	def post(self, request):
		try:
			data = json.loads(request.body)
			if Account.objects.filter(email = data['email']).exists():
				user				= Account.objects.get(email=data['email'])			
				user_password		= user.password.encode('utf-8')
				entered_password	= data['password'].encode('utf-8')

				if bcrypt.checkpw(entered_password,user_password):
					token = jwt.encode({'id':user.email},SECRET_KEY,algorithm='HS256').decode('utf-8')
					return JsonResponse({"message":token},status=200)
				return JsonResponse({"message":"WRONG_ID_OR_PASSWORD"},status=400)
			return JsonResponse({"message":"WRONG_ID_OR_PASSWORD"},status=401)

		except KeyError:
			return JsonResponse({"message":"INVALID_KEY"}, status=401)

class LoginConfirm:
	def __init__(self,original_function):
		self.original_function = original_function

	def __call__(self, request, *args, **kwargs):
		token = request.headers.get("Authorization", None)
		try:
			if token:
				token_payload	= jwt.decode(token, SECRET_KEY, algorithms="HS256")
				user			= Account.objects.get(email=token_payload['email'])
				request.user	= user
				return self.original_function(self, request, *args, **kwargs)

			return JsonResponse({'message':'LOG_IN_FIRST'}, status=401)

#		except jwt.ExpiredSignatureError:
#			return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)

#		except jwt.DecodeError:
#			return JsonResponse({'message':'INVALID_USER'}, status=401)

		except Account.DoesNotExist:
			return JsonResponse({'message':'INVALID_USER'}, status=401)

class AccountView(View):
	def post(self,request):
		try:
			data = json.loads(request.body)
			user_token_info = jwt.decode(data['token'], SECRET_KEY, algorithm='HS256')

			if Account.objects.filter(email=user_token_info['email'].exists()):
				return JsonResponse({"message":"SUCCESS"},status=200)

			return JsonResponse({"message":"LOG_IN_FIRST"},status=403)
		except KeyError:
			return JsonResponse({"message":"INVALID_KEY"}, status=401)
