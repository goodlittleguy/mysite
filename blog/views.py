from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404,render
from read_statistics.utils import read_statistics_once_read
from .models import Blog, BlogType


def blog_common_date(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每10篇进行分页
    page_number = request.GET.get('page', 1)  # 获取页码参数(GET请求),默认页码为1
    page_of_blogs = paginator.get_page(page_number)  # get_page方法自动将字符数字转化为int,
    # 并在用户输入不合规范的数字后默认返回1
    current_page_number = page_of_blogs.number  # 获取当前页

    # 获取当前页面的之前与之后两个页面,并对无效页面进行过滤
    page_range = list(range(max(1, current_page_number - 2), min(current_page_number + 2, paginator.num_pages + 1)))

    # 加上省略也页
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = dict()
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time','month',order="DESC")
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = blog_common_date(request,blogs_all_list)
    context['blog_types'] = BlogType.objects.all()
    # 得到年月的时间列表
    return render(request,'blog/blog_list.html',context)


def blogs_with_type(request, blogs_type_id):
    blog_type = get_object_or_404(BlogType, id=blogs_type_id)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = blog_common_date(request,blogs_all_list)
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    return render(request,'blog/blogs_with_type.html',context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year = year ,
                                         created_time__month = month)
    context = blog_common_date(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year,month)
    context['blog_types'] = BlogType.objects.all()

    return render(request,'blog/blogs_with_date.html', context)


def blog(request, blog_id):
    blog_detail = get_object_or_404(Blog, id=blog_id)
    read_cookie_key = read_statistics_once_read(request,blog_detail)  # 阅读cookie的标记
    context = dict()
    context['blog'] = blog_detail
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog_detail.created_time ).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog_detail.created_time ).first()
    # 实例化comment
    response = render(request, 'blog/blog.html', context)
    response.set_cookie(read_cookie_key, 'true')  # 后面还可天max_age设置有效期
    return response

