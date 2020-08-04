from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader, RequestContext
from booktest.models import BookInfo, HeroInfo, PicTest, AreaInfo
from datetime import date
from django.conf import settings

EXCLUDE_IPS = ['192.168.1.56']


def blocked_ips(view_fun):
    def wrapper(request, *view_args, **view_kwargs):
        # 获取浏览器端的IP地址
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in EXCLUDE_IPS:
            return HttpResponse("禁止访问")
        else:
            return view_fun(request, *view_args, **view_kwargs)

    return wrapper


def my_render(request, template_path, context_dict={}):
    # 使用模板文件
    # 1、加载模板文件, 返回模板对象
    temp = loader.get_template(template_path)
    # 2、定义模板上下文:给模板文件传递数据
    # context = RequestContext(request, {}) # Django1.0写法
    context = context_dict  # Django2.0写法，直接传字典
    # 3、模板渲染:产生标准的HTML内容
    res_html = temp.render(context)
    # 4、返回给浏览器
    return HttpResponse(res_html)


# Create your views here.
# 1、定义视图函数
# 2、进行URL配置，建立URL地址和视图的对应关系
def index(request):
    # 进行处理
    # return HttpResponse("Hello World")
    return render(request, 'booktest/index.html', {"content": "hello,world", "list": list(range(0, 9))})


# @blocked_ips
def index2(request):
    return HttpResponse("hello Python")


def show_books(request):
    '''显示图书的信息'''
    # 1、通过M查找图书表中的数据
    books = BookInfo.objects.all()
    return render(request, 'booktest/showbooks.html', {"books": books})


def detail(request, bid):
    '''展示详细信息'''
    # 1、根据id查询图书信息
    book = BookInfo.objects.get(id=bid)
    # 2、查询关联英雄
    heros = book.heroinfo_set.all()
    # 3、使用模板
    return render(request, 'booktest/detail.html', {'book': book, 'heros': heros})


def delete(request, bid):
    '''删除书'''
    # 找书
    book = BookInfo.objects.get(id=bid)
    book.delete()

    # return HttpResponseRedirect('/booktest')
    return redirect('/booktest')


def add(request):
    '''添加书'''
    # 创建书
    book = BookInfo()
    book.btitle = "流星蝴蝶剑"
    book.bpub_date = date(1990, 1, 1)
    book.save()
    # 返回应答，再次访问本页面,重定向
    # return HttpResponseRedirect('/booktest')
    return redirect('/booktest')


def temp_var(request):
    """模板变量"""
    my_dict = {"title": "字典字典"}
    my_list = [1, 2, 3, 4]
    book = BookInfo.objects.get(id=1)
    # 定义上下文
    context = {'my_dict': my_dict, 'my_list': my_list, 'book': book}
    return render(request, 'booktest/temp_var.html', context)


def temp_tags(request):
    """模板标签"""
    books = BookInfo.objects.all()
    return render(request, 'booktest/temp_tags.html', {'books': books})


def temp_filter(request):
    """模板过滤器"""
    books = BookInfo.objects.all()
    return render(request, 'booktest/temp_filter.html', {'books': books})


# temp_inderit
def temp_inherit(request):
    """模板继承"""
    return render(request, 'booktest/child.html')


def html_escape(request):
    """html转义"""
    return render(request, 'booktest/html_escape.html', {'content': '<h1>hello</h1>'})


# @blocked_ips
def index3(request):
    """首页3"""
    # a = 3 + 'a'
    return render(request, 'booktest/index3.html')


def show_upload(request):
    """显示上传图片页面"""
    return render(request, 'booktest/upload_pic.html')


def uplaod_handle(request):
    """上传图片处理"""
    # 1、获取上传的图片
    image = request.FILES.get('pic')
    # 2、创建一个文件
    save_path = '%s/booktest/%s' % (settings.MEDIA_ROOT, image.name)
    with open(save_path, 'wb') as f:
        # 3、获取上传文件的内容并写到创建的文件中
        for content in image.chunks():
            f.write(content)
    # 4、在数据库中保存上传记录
    PicTest.objects.create(goods_pic=('booktest/%s' % image.name))
    # 5、返回
    return HttpResponse('ok')


from django.core.paginator import Paginator


def show_book2(request):
    """分页"""
    # 1、查询出所有信息
    books = BookInfo.objects.filter(btitle__isnull=False)

    # 2、分页，每页显示10条
    paginator = Paginator(books, 10)
    print(paginator.num_pages)
    print(paginator.page_range)

    # 3、获取第一页内容
    # page 是Page类的实例对象
    page = paginator.page(1)
    # 4、使用模板
    return render(request, 'booktest/showbook2.html', {'page': page})


# 前端访问的时候需要传递页码
def show_area(request, page):
    """分页"""

    if not page:
        page = 1

    # 1、查询出所有信息
    areas = AreaInfo.objects.filter(parent__isnull=True).order_by('title')

    # 2、分页，每页显示10条
    paginator = Paginator(areas, 10)
    # print(paginator.num_pages)
    # print(paginator.page_range)

    # 3、获取第一页内容
    # page 是Page类的实例对象
    areas = paginator.page(int(page))
    # 4、使用模板
    return render(request, 'booktest/show_area.html', {'areas': areas})


def area(request):
    """省市县选择案例"""
    return render(request, 'booktest/areas.html')


def prov(request):
    """获取所有省级地区信息"""
    areas = AreaInfo.objects.filter(parent__isnull=True)
    # 遍历拼接json
    data = []
    for area in areas:
        data.append((area.id, area.title))
    return JsonResponse({'data': data})


def city(request, pid):
    """获取所有市级信息"""
    # cities = AreaInfo.objects.get(id=pid).areainfo_set.all()
    cities = AreaInfo.objects.filter(parent__id=pid)
    data = []
    for city in cities:
        data.append((city.id, city.title))
    return JsonResponse({'data': data})


def dis(request, cid):
    """获取所有县级信息"""
    # cities = AreaInfo.objects.get(id=pid).areainfo_set.all()
    diss = AreaInfo.objects.filter(parent__id=cid)
    data = []
    for dis in diss:
        data.append((dis.id, dis.title))
    return JsonResponse({'data': data})
