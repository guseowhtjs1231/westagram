from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Comment(models.Model):
	name       = models.CharField(max_length = 50)
	content       = models.CharField(max_length = 3000)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'comment'
