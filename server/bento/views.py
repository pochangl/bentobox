import random
from rest_framework import generics, mixins
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Order
from captcha.image import ImageCaptcha
from .permissions import CaptchaPermission

image_captcha = ImageCaptcha()

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

    def get_object(self):
        """
            存取資料時, 皆需要id跟resNo為依據
        """
        data = self.request.data
        return get_object_or_404(self.get_queryset(), id=data["id"], resNo=data["resNo"])


class CancelOrderView(OrderMixin, generics.DestroyAPIView):
    """
        取消訂單
    """
    def post(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


class LookupOrderView(OrderMixin, generics.RetrieveAPIView):
    """
        查詢定單
    """
    def post(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)


class UpdateOrderView(OrderMixin, generics.UpdateAPIView):
    """
        更新訂單
    """
    def post(self, *args, **kwargs):
        return self.update(*args, **kwargs)


class CreateOrderView(OrderMixin, generics.CreateAPIView):
    """
        下訂單
    """
    permission_classes = (CaptchaPermission,)
