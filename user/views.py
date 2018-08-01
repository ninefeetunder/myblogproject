import string
import random
from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import LoginForm, RegForm, ChangeNicknaeForm, BindEmailForm
from django.contrib.auth.models import User
from .models import Profile


def login(request):
    '''
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(request, username=username, password=password)  #验证用户名和密码是否正确，正确返回一个真实的user，否则返回None
    referer = request.META.get('HTTP_REFERER',reverse('home')) #找到用户是在哪个页面登录的信息（网址）,否则就解析别名为home的url
    if user is not None:
        auth.login(request, user)  #验证成功后登录
        return redirect(referer) #重定向到用户登录的页面
    else:
        return render(request,'error.html',{'message':'用户名或密码不正确！'}) #返回错误页面
    '''
    if request.method == 'POST':  #POST提交数据，GET加载页面
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  #检查提交的数据是否有效,会执行LoginForm对象的clean方法
            user = login_form.cleaned_data['user']
            auth.login(request, user)  # 验证成功后登录
            return redirect(request.GET.get('from',reverse('home')))  # 重定向到用户登录的页面，获得在from中的url
    else:
        login_form = LoginForm()  #实例化

    context = {}
    context['login_form'] = login_form
    return render(request,'user/login.html',context)

def register(request):
    if request.method == 'POST':  #POST提交数据，GET加载页面
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)#创建用户
            user.save()
            #登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()  #实例化

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def change_nickname(request):
    redirect_to = request.GET.get('from',reverse('home'))

    if request.method == 'POST':
        form = ChangeNicknaeForm(request.POST)
        if form.is_valid():
            nickname_new  = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknaeForm()
    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def bind_email(request):
    redirect_to = request.GET.get('from',reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST)
        if form.is_valid():
            pass
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    email = request.GET.get('email', '')
    data = {}
    if email != '':
        #生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['bind_email_code'] = code

        send_mail(
            '绑定邮箱',
            '验证码： %s' % code,
            '1285499453@qq.com',
            [email],
            fail_silently=False,
        )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)