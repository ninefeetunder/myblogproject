from django.shortcuts import get_object_or_404,render
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .models import Blog,BlogType
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm


def get_blog_list_common_data(request,blogs_all_list):
    """各个函数的部分代码打包"""
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) #（所有博客的列表，一页上要有的篇数），返回一个分页器
    #从前端那里获得page的值，默认为1
    page_num = request.GET.get('page', 1)  # 活取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)# 包含这一页的文章列表，其实是个分页的对象
    blog_types = BlogType.objects.all()
    currentr_page_num = page_of_blogs.number#获取当前页的页码数
    #获取当前页码以及前后两页的页码，包括特殊情况的页码
    page_range = list(range(max(currentr_page_num-2,1),currentr_page_num)) + list(range(currentr_page_num,min(currentr_page_num+2,paginator.num_pages)+1))
    #添加省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    #加上首页和最后一页页码
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = Blog.objects.dates('created_time','month',order='DESC')

    return context


def blog_list(request):
    #分页操作
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_all_list)
    return render(request,'myblog/blog_list.html',context)

def blog_detail(request,blog_pk):
    """显示具体文章"""
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)  #在这里获得的是Blog
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk) #获得了这篇博客的所有评论对象

    context = {}
    context['comments'] = comments
    context['blog']= blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt = blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt = blog.created_time).first()
    context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_pk})
    response = render(request,'myblog/blog_detail.html',context)  #响应
    response.set_cookie(read_cookie_key,'true') #阅读cookie标记
    return response

def blogs_with_type(request,blog_type_pk):
    """显示一个类型下的博客"""
    blogtype = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blogtype)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogtype'] = blogtype
    return render(request,'myblog/blogs_with_type.html',context)


def blogtypes(request):
    """显示所有文章类型"""
    blogtypes = BlogType.objects.all()
    context = {'blogtypes':blogtypes}
    return render(request,'myblog/blogtypes.html',context)

def blogs_with_date(request,year,month):
    """按时间分类"""
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request,'myblog/blogs_with_date.html',context)





