from django.shortcuts import render
import json

from django.views import View
from django.http  import JsonResponse, HttpResponse
from .models      import Comment
# Create your views here.


class CommentView(View):
	def post(self, request):
		data = json.loads(request.body)
		Comment.objects.create(
			name     = data['name'],
			content     = data['content'],
		).save()

		return JsonResponse({'message':'SUCCESS'}, status=200)

	def get(self, request):
		comment_data = Comment.objects.values()

		return JsonResponse({'Comment':list(comment_data)}, status=200)

