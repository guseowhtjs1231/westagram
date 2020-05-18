from django.db import models
from django.conf import settings
from django.utils import timezone

class Account(models.Model):
	name       = models.CharField(max_length = 50)
	email      = models.CharField(max_length = 100, unique=True)
	password   = models.CharField(max_length = 300)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	
	class Meta:
		db_table = 'account_account'

