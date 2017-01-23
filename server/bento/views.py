import random
from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import requires_csrf_token
from .models import Order
from captcha.image import ImageCaptcha
from .permissions import CaptchaPermission

image_captcha = ImageCaptcha()
