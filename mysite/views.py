import datetime
from django.utils import timezone
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.core.cache import cache
from read_statistics.utils import get_seven_days_read_date,get_today_hot_date,get_yesterday_hot_data
from blog.models import Blog


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    # 根据read_details条目里的date条目并小于今天,大于等于7天前,筛选博客,这时单个博客可能会因为因为最近7天多次观看,而出现多次
    blogs = Blog.objects\
                .filter(read_details__date__lt=today,read_details__date__gte=date)\
                .values('id','title').annotate(read_num_sum = Sum('read_details__read_num'))\
                .order_by('-read_num_sum')  # 将包含 id , title , read_num_sum 为键的各个已将相同id , title,的键合并的字
    # 典按照read_num_sum逆序排列
    return blogs[:7]


def get_30_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    # 根据read_details条目里的date条目并小于今天,大于等于7天前,筛选博客,这时单个博客可能会因为因为最近7天多次观看,而出现多次
    blogs = Blog.objects\
                .filter(read_details__date__lt=today,read_details__date__gte=date)\
                .values('id','title').annotate(read_num_sum = Sum('read_details__read_num'))\
                .order_by('-read_num_sum')  # 将包含 id , title , read_num_sum 为键的各个已将相同id , title,的键合并的字
    # 典按照read_num_sum逆序排列
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_date(blog_content_type)
    # 获取7天热门博客缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days',hot_blogs_for_7_days, 3600)  # 键,值,缓存时间(秒)
    context = dict()
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_date(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_data_for_7_days'] = get_7_days_hot_blogs()
    context['hot_data_for_30_days'] = get_30_days_hot_blogs()
    return render(request, 'home.html', context)

