import json

from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Account

class SignUpView(View):
	def post(self, request):
		try:
			data = json.loads(request.body)
			if Account.objects.filter(email =data['email']).exists():
				return JsonResponse({"message":"EMAIL_ALREADY_EXISTS"}, status=400)
			Account.objects.create(
				name     = data['name'],
				email    = data['email'],
				password = data['password'],
			).save()
        
			return HttpResponse(status=200)

		except KeyError:
			return JsonResponse({"message":"INVALID_KEY"}, status=401)
		except json.decoder.JSONDecodeError:
			return JsonResponse({"message":"NO_DATA"}, status=401)

class SignInView(View):
	def post(self, request):
		try:
			data = json.loads(request.body)
			if Account.objects.filter(email = data['email']).exists():
				user = Account.objects.get(email=data['email'])			
				if user.password == data['password']:
					return HttpResponse(status=200)
				return JsonResponse({"message":"WRONG_ID_OR_PASSWORD"},status=401)
			return JsonResponse({"message":"WRONG_ID_OR_PASSWORD"},status=401)
		except KeyError:
			return JsonResponse({"message":"INVALID_KEY"}, status=401)
