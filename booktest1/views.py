from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta


# Create your views here.

def index(request):
    return render(request, 'booktest1/index.html')


def login(request):
    """显示登录页面"""
    username = request.COOKIES.get('username')
    if not username:
        username = ""
    isLogin = request.session.get('isLogin')
    if isLogin:
        return render(request, 'booktest1/index.html')
    return render(request, 'booktest1/login.html', {'username': username})


def login_check(request):
    """登录验证"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    remname = request.POST.get('remname')
    # 登录校验
    # 模拟
    if username == 'admin' and password == '123':
        response = render(request, 'booktest1/index.html')
        if remname == 'on':
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
        request.session['isLogin'] = True
        return response
    else:
        return render(request, 'booktest1/login.html')


def ajax_test(request):
    """ajax页面"""
    return render(request, 'booktest1/ajaxtest.html')


def ajax_handle(request):
    """ajax处理"""
    return JsonResponse({"code": 1})


def login_ajax(request):
    """ajax登录页面"""
    return render(request, 'booktest1/loginajax.html')


def ajax_login(request):
    """ajax请求处理等"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 登录校验
    # 模拟
    if username == 'admin' and password == '123':
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


def set_cookie(request):
    """设置cookie"""
    response = HttpResponse('设置cookie')
    # 设置一个cookie信息，名字为num，值为1

    response.set_cookie('num', 1, max_age=3600 * 24 * 14)  # 自己计算时间
    response.set_cookie('num1', 2, expires=datetime.now() + timedelta(days=14))  # 通过函数计算
    # 返回response
    return response


def get_cookie(request):
    """获取cookie信息"""
    num = request.COOKIES.get('num')

    return HttpResponse(num)


def set_session(request):
    """设置session"""
    request.session['name'] = '张三'
    request.session.set_expiry(30 * 24 * 3600) # 设置session时间
    return HttpResponse("设置成功")


def get_session(request):
    """获取session"""
    name = request.session.get('name', default="没有值")
    return HttpResponse(name)
