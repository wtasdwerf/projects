"""
URL configuration for bank_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj_rest_auth/', include('dj_rest_auth.urls')),
    path('products/', include('products.urls')),
    path('dj_rest_auth/signup/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('accounts.urls')),
]


# 1. dj-rest-auth/ ^password/reset/$ [name='rest_password_reset']
# 패스워드 초기화 (이메일로 전송)

# 2. dj-rest-auth/ ^password/reset/confirm/$ [name='rest_password_reset_confirm']
# 패스워드 초기화 (이메일 확인 후 초기화 페이지)

# 3. dj-rest-auth/ ^login/$ [name='rest_login']
# 로그인

# 4. dj-rest-auth/ ^logout/$ [name='rest_logout']
# 로그아웃

# 5. dj-rest-auth/ ^user/$ [name='rest_user_details']
# 유저 정보 반환

# 6. dj-rest-auth/ ^password/change/$ [name='rest_password_change']
# 패스워드 변경

# 7. dj-rest-auth/registration/
# 회원가입

# 프로젝트에서 사용할 주요 기능은 3. 로그인 , 4. 로그아웃 , 5. 유저 정보 반환 , 7. 회원가입 4가지입니다.