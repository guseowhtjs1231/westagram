from django.shortcuts import render
import json


from django.views import View
from django.http  import JsonResponse, HttpResponse
from .models      import Account

# Create your views here.


class AccountView(View):
	def post(self, request):
		data = json.loads(request.body)
		Account.objects.create(
				name     = data['name'],
				email    = data['email'],
				password = data['password']
		).save()
        
		return JsonResponse({'message':'SUCCESS'}, status=200)


	def get(self, request):
		user_data = Account.objects.values()
	
		return JsonResponse({'account':list(user_data)}, status=200)
class SignIn(View):
	def post(self, request):
		data = json.loads(request.body)

		try:
			if Account.objects.filter(name = data['name']).exists():
				user = Account.objects.get(name=data['name'])

				if user.password == data['password']:
					return HttpResponse(status=200)
				return HttpResponse(status=401)
			return HttpResponse(status=400)

		except KeyError:
			return JsonResponse({"message":"INVALID_KEYS"}, status=400)
