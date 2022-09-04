from django.contrib import admin
from django.urls import path, re_path # TODO: NOTICE) (SEO) django-debug-toolbar 구동, re_path 추가 (Django>=4.0)
from django.conf import settings              # TODO: NOTICE) (SEO) django-debug-toolbar 구동
from django.conf.urls import include  #, url  # TODO: NOTICE) (SEO) django-debug-toolbar 구동

from user.views import index, login_view, logout_view, register_view, user_list_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("accounts/login/", login_view, name="login"),  # TODO: NOTICE) (SEO) @login_required 활용 경우, 로그인이 안된 경우 django 는 path 를 '~/accounts/login/?next=/users/' 로 생성되므로, urls.py 에서 관련 path 추가
    path("logout/", logout_view, name="logout"),
    path("users/", user_list_view, name="user_list"),
]

# TODO: NOTICE) (SEO) django-debug-toolbar 구동
#   (참조) Django 디버깅 툴 (Django Debug Toolbar) (https://devlink.tistory.com/295)
#   (참조) Django 4.0 url import error (https://forum.djangoproject.com/t/django-4-0-url-import-error/11065)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]  # Django>=4.0
    # urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]  # Django==3.2
