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
			Account.objects.create(
				name     = data['name'],
				email    = data['email'],
				password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8'),
			).save()
			return HttpResponse(status=200)
		
		except KeyError:
			return JsonResponse({"message":"INVALID_KEY"}, status=401)
		except json.decoder.JSONDecodeError:
			return JsonResponse({"message":"NO_DATA"}, status=401)

	def get(self, request):
		user_data= Account.objects.values()
		return JsonResponse({'account':list(user_data)}, status=200)

class SignInView(View):
	def post(self, request):
		try:
			data = json.loads(request.body)
			if Account.objects.filter(email = data['email']).exists():
				user = Account.objects.get(email=data['email'])			
				userpassword = user.password.encode('utf-8')
				if bcrypt.checkpw(data['password'].encode('utf-8'),userpassword):
					token = jwt.encode({'id':user.email},SECRET_KEY,algorithm='HS256').decode('utf-8')
					return JsonResponse({"message":token},status=200)
				return JsonResponse({"message":"WRONG_ID_OR_PASSWORD"},status=401)
			return JsonResponse({"message":"WRONG_ID_OR_PASSWORD"},status=401)
		except KeyError:
			return JsonResponse({"message":"INVALID_KEY"}, status=401)
