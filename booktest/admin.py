from django.contrib import admin
from booktest.models import BookInfo, HeroInfo, PicTest


# 后台管理相关文件
# Register your models here.

class BookStackedInline(admin.StackedInline):
    # 写多类的名字
    model = HeroInfo

# 自定义模型管理类
class BookInfoAdmin(admin.ModelAdmin):
    '''图书模型管理类'''
    # 显示那些属性
    list_display = ['id', 'btitle', 'bpub_date', 'title'] # 可以放属性和方法
    list_per_page = 10  # 指定每页显示10条数据
    actions_on_bottom = True # 下面有操作列表
    actions_on_top =  False  # 取消上面的操作列表
    list_filter = ['btitle'] # 右侧过滤栏
    search_fields = ['btitle']  # 列表页上方的搜索框,搜索哪一个

    # 这两个只能用一个
    # fields = ['bpub_date', 'btitle'] # 控制编辑时候顺序
    fieldsets =  (
        ("基本",{'fields':['btitle','bprice']}),
        ("高级", {'fields': ['bpub_date']})
    ) # 编辑分组

    inlines = [BookStackedInline] # 可以在编辑一类的时候控制多类

class HeroInfoAdmin(admin.ModelAdmin):
    """英雄管理类"""

# 注册模型类
# 注册过程中同时把模型管理类注册
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo)
admin.site.register(PicTest)