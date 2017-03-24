from __future__ import unicode_literals
from django.db import models
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def email_validate(self, email):
        return EMAIL_REGEX.match(email)
    def pw_validate(self, password, confirm):
        return password == confirm

class User(models.Model):
    email = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    dateofbirth = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=50)
    text = models.CharField(max_length=400)
    poster = models.ForeignKey(User, related_name='quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class List(models.Model):
    quotes = models.ForeignKey(Quote, related_name= 'fave')
    person = models.ForeignKey(User, related_name= 'unique')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
