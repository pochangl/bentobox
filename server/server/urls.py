from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from bento import views



urlpatterns = [
    url(r'^api/admin/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




# urlpatterns = [
#    url(r'^api/create_order', views.CreateOrderView.as_view()), # 下單用
#    url(r'^api/order/(?P<pk>\w+)/(?P<id>\w+)', views.OrderView.as_view()), # 操作用
#    url(r'^api/captcha', views.captcha), # 請求新的captcha
#
#    url(r'^api/force_login', views.force_login), # 強制login
#    url(r'^api/current_captcha', views.current_captcha), # 偷看captcha值,  debug 用
#
#    url(r'^api/admin/', include('rest_framework.urls', namespace='rest_framework')),
#    url(r'^admin/', admin.site.urls),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
