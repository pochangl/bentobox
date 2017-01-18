from rest_framework.permissions import BasePermission


class CaptchaPermission(BasePermission):
    def has_permission(self, request, *args):
        return request.data.get("captcha", None) == request.session.get('captcha', 0)

    def has_object_permission(self, *args, **kwargs):
        return self.has_permission(*args, **kwargs)
