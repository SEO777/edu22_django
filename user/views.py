from django.contrib.auth import get_user_model, login, logout, authenticate  # TODO: NOTICE) (SEO) authenticate 활용
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm  # TODO: NOTICE) (SEO) AuthenticationForm 활용
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm

SET_PAGINATOR_PER_PAGE = 15
User = get_user_model()


# SEO: root path 로 들어올 때 실행되는 함수
def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: NOTICE) (SEO) 로그인 성공하면 '/' 로 리다이렉트, 로그인 실패하면 로그인 페이지에서 메시지 표출
        #   (참조) CH02-04 Django Login, Logout (Django 제공 Forms)
        #   (참조) django 04. 장고 개인 프로젝트 2 - 인증 (회원가입, 로그인) (https://wayhome25.github.io/django/2017/03/01/django-99-my-first-project-2/)
        form = AuthenticationForm(request, request.POST)
        msg = '가입되어 있지 않거나 로그인 정보가 잘못 되었습니다.'
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)  # 실제로는 email 에 해당됨
            print(username)
            print(raw_password)
            print(user)
            if user is not None:
                msg = '로그인 성공'
                print(msg)
                login(request, user)
                return HttpResponseRedirect("/")
        return render(request, "login.html", {"form": form, "msg": msg})
    else:
        # TODO: 2. login 할 때 form을 활용해주세요
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요
    # TODO: NOTICE) (SEO) 코딩
    #   (참조) CH02-04 Django Login, Logout (Django 제공 Forms)
    logout(request)
    return HttpResponseRedirect("/")


# TODO: NOTICE) (SEO) 코딩
#   (참조) CH02-04 Django Login, Logout (Django 제공 Forms)
# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
# TODO: NOTICE) (SEO) 로그인 요구, 아래 중 하나의 방법 사용 가능
#   A. @login_required 활용 경우, settings.py 에서 LOGIN_URL = '/login' 추가
#   B. @login_required 활용 경우, 로그인이 안된 경우 django 는 path 를 '~/accounts/login/?next=/users/' 로 생성되므로, urls.py 에서 관련 path 추가
#   C. @login_required 비활용 경우, 아래 주석처리 함수로 처리
@login_required
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    page = max(int(request.GET.get('page', 1)), int(request.GET.get('p', 1)))  # qurey 파라미터에 key: 'page' 또는 'p' 가 없으면 1
    print('page:', page)
    users = User.objects.all().order_by('id')             # user query (주의!!! not 클래스 Users)  ('id': id 오름차순, '-id': id 내림차순 )
    paginator = Paginator(users, SET_PAGINATOR_PER_PAGE)  # 하나의 페이지에 표출되는 user 수
    users = paginator.get_page(page)                      # qurey 파라미터에 'page' 또는 'p' 가 있으면 해당 페이지
    return render(request, "users.html", {"users": users})

# # TODO: NOTICE) (SEO) 코딩
# #   (참조) CH02-04 Django Login, Logout (Django 제공 Forms)
# # TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
# # @login_required  # 로그인 요구
# def user_list_view(request):
#     # TODO: 7. /users 에 user 목록을 출력해주세요
#     # TODO: 9. user 목록은 pagination이 되게 해주세요
#     if request.user.is_authenticated:
#         page = max(int(request.GET.get('page', 1)), int(request.GET.get('p', 1)))  # qurey 파라미터에 key: 'page' 또는 'p' 가 없으면 1
#         print('page:', page)
#         users = User.objects.all().order_by('id')             # user query (주의!!! not 클래스 Users)  ('id': id 오름차순, '-id': id 내림차순 )
#         paginator = Paginator(users, SET_PAGINATOR_PER_PAGE)  # 하나의 페이지에 표출되는 user 수
#         users = paginator.get_page(page)                      # qurey 파라미터에 'page' 또는 'p' 가 있으면 해당 페이지
#         return render(request, "users.html", {"users": users})
#     else:
#         # TODO: NOTICE) (SEO) 로그인 안 된 상태에서 /users 접근시 다른 페이지 (/login 경로) 로 redirect 된다.
#         return HttpResponseRedirect("/login/")
'''
http://abc.com/user/1?name=admin
'''
