import json

from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Comment
from account.models import Account

class CommentView(View):
	def post(self, request):
		try:
			data = json.loads(request.body)
			if Account.objects.filter(name = data['name']).exists():
				Comment.objects.create(
						name		= data['name'],
						content		= data['content'],
				).save()
				return HttpResponse(status=200)
			return JsonResponse({"message":"USER_NAME_NOT_FOUND"}, status=400)
		except KeyError:
			return JsonResponse({"message":"INVALID_KEY"}, status=401)

	def get(self, request):
		comment_data = Comment.objects.values()
		return JsonResponse({'Comment':list(comment_data)},status=200)
