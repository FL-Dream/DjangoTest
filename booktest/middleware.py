from django.http import HttpResponse


# 文件名就这样写，固定名

class BlockedIPSMiddleware:
    """中间件类"""

    def __init__(self, get_response):
        """服务器重启之后，接收第一个请求时调用"""
        self.get_response = get_response
        # One-time configuration and initialization.
        print('----init----')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.process_request(request) # 废弃方法必须这样执行
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        print('-----call------')
        self.process_response(request, response) # 废弃方法必须这样执行，无法截断流程

        return response

    def process_request(self, request):
        """产生request对象之后，URL匹配之前调用"""
        print('----process_request-----')
        # 没有用
        return HttpResponse('process_reqeust')

    EXCLUDE_IPS = ['192.168.1.56']

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        """视图函数调用之前会调用"""
        print('--------process_view-----')
        # 获取浏览器端的IP地址
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockedIPSMiddleware.EXCLUDE_IPS:
            return HttpResponse("禁止访问")
        # 可以用
        # return HttpResponse('process_view')
    def process_response(self, request, response):
        """视图函数调用之后，内容返回浏览器之前"""
        print('---------process_response------')
        return response


    def process_exception(self, request, exception):
        """视图函数引发异常时调用"""
        print('-------process_exception')

    def process_template_response(self, request, response):
        """视图被完成执行后调用"""
        print("-------process_template_response--------")
        return response
