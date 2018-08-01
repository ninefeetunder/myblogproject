from django.urls import path
from . import views


urlpatterns = [
    #http://localhost:8000/myblog/(博客)
    path('',views.blog_list,name='blog_list'),

    #显示一篇博文的详细信息 http://localhost:8000/myblog/1/
    path('<int:blog_pk>/',views.blog_detail,name='blog_detail'),

    #显示一个类型下的博客
    path('type/<int:blog_type_pk>',views.blogs_with_type,name='blogs_with_type'),

    #显示所有博文类型的页面http://localhost:8000/myblog/types/
    path('blogtypes/',views.blogtypes,name='blogtypes'),

    #按日期分类博客文章
    path('date/<int:year>/<int:month>/',views.blogs_with_date,name='blogs_with_date'),

]