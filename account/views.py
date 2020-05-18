import json


from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Account



class SignUpView(View):
	def post(self, request):
		try:
			data = json.loads(request.body)
			if Account.objects.filter(email =data['email']).exists():
				return JsonResponse({"message":"ALREADY_SIGNED_UP_EMAIL"}, status=400)
			data = json.loads(request.body)
			Account.objects.create(
				name     = data['name'],
				email    = data['email'],
				password = data['password'],
			).save()
        
			return HttpResponse(status=200)

		except KeyError:
			return JsonResponse({"message":"NO_DATA_ENTERED"}, status=405)


	def get(self, request):
		user_data = Account.objects.values()
		return JsonResponse({'account':list(user_data)}, status=200)


class SignInView(View):
	def post(self, request):
		try:
			data = json.loads(request.body)
			try:
				if Account.objects.filter(email = data['email']).exists():
					user = Account.objects.get(email=data['email'])
				
					if user.password == data['password']:
						return HttpResponse(status=200)
			
					return JsonResponse({"message":"WRONG_ID_OR_PASSWORD"},status=401)
				return JsonResponse({"message":"WRONG_ID_OR_PASSWORD"},status=400)

			except KeyError:
				return JsonResponse({"message":"INVALID_KEYS"}, status=400)
		except KeyError:
			return JsonResponse({"message":"NO_DATA_ENTERED"}, status=405)
