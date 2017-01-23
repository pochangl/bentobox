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

def force_login(request):
    if not request.user.is_authenticated():
        user = User.objects.get(id=1)
        login(request, user)
    return HttpResponse()

@requires_csrf_token
def captcha(request):
    """
        captcha 頁面
        每次存取這個頁面就會給一個新的captcha, 並存在 session裡
    """
    text = ''.join(random.choice('0123456789abcdef') for i in range(5))
    image_data = image_captcha.generate(text)
    request.session['captcha'] = text
    return HttpResponse(image_data.read(), content_type="image/png")


def current_captcha(request):
    """
        看captcha的值, 作弊用的
    """
    return HttpResponse(request.session['captcha'])

class OrderMixin(object):
    """
        訂單的基本設定, 這不是一個頁面, 只是每個訂單頁面的基本設定
        其它頁面會繼承這個設定
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [SessionAuthentication]


class OrderView(OrderMixin, generics.RetrieveUpdateDestroyAPIView):
    """
        任何訂單相關的操作
    """
    def get_queryset(self):
        return super(OrderView, self).get_queryset().filter(id=self.kwargs['id'])


class CreateOrderView(OrderMixin, generics.CreateAPIView):
    """
        下訂單
    """
    permission_classes = (CaptchaPermission,)
