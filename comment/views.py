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
						contents	= data['contents'],
				).save()

				return HttpResponse(status=200)
			return JsonResponse({"message":"SIGN_UP_FIRST"}, status=400)
		#	return JsonResponse({"message":"TRY_AGAIN"}, status=401)
		except KeyError:
			return JsonResponse({"message":"NO_DATA_ENTERED"}, status=405)

		except Account.DoesNotExist:
			return JsonResponse({"message":"SIGN_UP_FIRST"}, status=404)

	def get(self, request):
		comment_data = Comment.objects.values()

		if len(comment_data)==0:
			return JsonResponse({'Message':'NO_COMMENTS'}, status=404)

		return JsonResponse({'Comment':list(comment_data)},status=200)
