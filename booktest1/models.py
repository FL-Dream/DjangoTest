from django.db import models

# Create your models here.

class User(models.Model):
    """用户"""

    name = models.CharField(max_length=20, db_index=True)