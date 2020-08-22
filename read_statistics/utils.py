import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Sum
from django.utils import timezone
from .models import ReadNum,ReadDetail
def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model,obj.id)
    if not request.COOKIES.get(key):
        # 总阅读数记录

        #有的话就get , 没的话就create,created储存是否为创建
        readnum , created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.id)

        # if ReadNum.objects.filter(content_type=ct, object_id=obj.id).count():
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.id)
        # # 不存在阅读记录
        # else:
        #     # 实例化博客
        #     readnum = ReadNum(content_type=ct, object_id=obj.id)
        # 阅读计数加一
        readnum.read_num += 1
        readnum.save()

        #每日博客记录
        date = timezone.now().date()
        readdetail,created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.id, date=date)

        readdetail.read_num += 1
        readdetail.save()
    return key

def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        previous_date = today - datetime.timedelta(days=1)
        dates.append(previous_date.strftime('%m/%d'))
        read_detail = ReadDetail.objects.filter(content_type=content_type,date=previous_date)

        # 对read_detail的read_num进行求和,返回一个 key 为 read_num_sum的字典和值为单天阅读总值的value
        result = read_detail.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums

def get_today_hot_date(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type = content_type,date=today).order_by('-read_num') #找到今天被实例化的ReadDetial
    return read_details[:7] #以read_num属性为基,逆序排序(由大到小)

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')  # 找到今天被实例化的ReadDetial
    return read_details[:7]  # 以read_num属性为基,逆序排序(由大到小)

