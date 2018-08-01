from django.urls import path
from . import views

urlpatterns = [
    # 登录
    path('login/', views.login, name='login'),
    # 注册
    path('register/', views.register, name='register'),
    # 注销
    path('logout/', views.logout, name="logout"),
    # 用户个人信息
    path('user_info/', views.user_info, name="user_info"),
    #修改用户昵称
    path('change_nickname/', views.change_nickname, name="change_nickname"),
    #绑定邮箱
    path('bind_email/', views.bind_email, name="bind_email")
]