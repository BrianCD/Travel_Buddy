from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

import re
import bcrypt

class UserManager(models.Manager):
    def register(self, userData):
        errors = []
        if len(userData["name"]) < 4:
            errors.append("Name must be at least 2 characters")
        if len(userData["username"]) < 4:
            errors.append("Username must be at least 2 characters")
        if len(userData["password"]) < 8:
            errors.append("Invalid Password")
        if userData["password"] != userData["passconf"]:
            errors.append("Password must match confirmation")
        user = None
        if len(errors) == 0:
            user = User(name=userData["name"], username=userData["username"], password=bcrypt.hashpw(userData["password"].encode(), bcrypt.gensalt()))
            user.save()
        return (user, errors)

    def tryLogin(self, name, password):
        try:
            user = self.get(username=name)
            if bcrypt.hashpw(password.encode(), user.password.encode()) != user.password:
                return "Incorrect password"
            return user
        except ObjectDoesNotExist:
            return "User is not registered"

class User(models.Model):
        name = models.CharField(max_length=255)
        username = models.CharField(max_length=255)
        password = models.CharField(max_length=255)
        created_at = models.DateTimeField(auto_now_add = True)
        updated_at = models.DateTimeField(auto_now = True)
        objects = UserManager()
