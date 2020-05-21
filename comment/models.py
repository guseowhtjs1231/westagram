from django.db import models
from account.models import Account

class Comment(models.Model):
	user		= models.ForeignKey(Account, on_delete=models.CASCADE)
	content		= models.CharField(max_length = 3000)
	created_at	= models.DateTimeField(auto_now_add = True)
	updated_at	= models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'comments'
