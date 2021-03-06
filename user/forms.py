from  django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(
                                            attrs={'class':'form-control','placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(
                                            attrs={'class':'form-control','placeholder':'请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)  # "验证"用户名和密码是否正确，正确返回一个真实的user，否则返回None
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                                max_length=30,
                                min_length=3,
                                widget=forms.TextInput(
                                            attrs={'class':'form-control','placeholder':'请输入3-30位用户名'})) #给自动生成的input标签加上class属性
    email = forms.EmailField(label='邮箱',
                               widget=forms.EmailInput(
                                            attrs={'class':'form-control','placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(
                                            attrs={'class':'form-control','placeholder':'请输入密码'}))
    password_again = forms.CharField(label='再输入一次密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(
                                            attrs={'class':'form-control','placeholder':'请再输入密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入密码不一致')
        return password_again

class ChangeNicknaeForm(forms.Form):
    nickname_new = forms.CharField(
        label='新的昵称',
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入新的昵称'}
        )
    )
    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip() #这里获得的是已经修改过的新的昵称，在request.POST中获得的。
        if nickname_new == '':
            raise ValidationError('新的昵称不能为空')
        else:
            return nickname_new

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}
                               )
    )
    verification_code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '点击“发送”验证码'})
    )