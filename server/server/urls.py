from django.conf.urls import url, include
from django.contrib import admin
from bento import views

urlpatterns = [
    url(r'^api/update', views.UpdateOrderView.as_view()), # 更新用
    url(r'^api/query', views.LookupOrderView.as_view()), # 查詢用
    url(r'^api/cancel', views.CancelOrderView.as_view()), # 取消用
    url(r'^api/order', views.CreateOrderView.as_view()), # 下單用
    url(r'^api/captcha', views.captcha), # 請求新的captcha

    url(r'^api/force_login', views.force_login), # 強制login
    url(r'^api/current_captcha', views.current_captcha), # 偷看captcha值,  debug 用

    url(r'^api/admin/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
]
