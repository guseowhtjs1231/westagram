import json

from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Comment
from account.models import Account
from account.views import LoginConfirm

class CommentView(View):
	@LoginConfirm
	def post(self, request):
		try:
			data = json.loads(request.body)
			Comment.objects.create(
					user_id		= data['user_id'],
					content		= data['content'],
				).save()
			return HttpResponse(status=200)
		except KeyError:
			return JsonResponse({"message":"INVALID_KEY"}, status=401)
	@LoginConfirm
	def get(self, request):
		comment_data = Comment.objects.values()
		return JsonResponse({'Comment':list(comment_data)},status=200)
