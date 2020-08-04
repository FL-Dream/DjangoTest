from django.db import models

# Create your models here.

'''
    注意点：
    1、字段命名不允许连续下划线
    
'''

class BookInfoManager(models.Manager):
    """图书管理器类"""
    # 应用场景
    # 1、改变查询结果集
    def all(self):
        # 1、调用父类的all，获取所有数据
        return super().all().filter(isDelete=False)  # QuerySet

    # 2、封装函数：操作模型对应的数据表（增删改查)
    def create_book(self, title, pub_date):
        # 获取self所在的model类

        book = self.model()
        book.btitle = title
        book.bpub_date = title
        book.save()
        return book

# 一类
class BookInfo(models.Model):
    """图书模型类"""
    # CharField索命是一个字符串, max_length指定字符串的最大长度
    btitle = models.CharField(max_length=20, verbose_name='标题') # verbose_name 在后台管理页面中显示自定义标题
    # 出版日期,DateField说明是一个日期类型
    bpub_date = models.DateField()
    # 添加日期 auto_now_add 添加时间
    # add_time = models.DateField(auto_now_add=True)
    # 更新时间 auto_now 更新时间
    update_time = models.DateField(auto_now=True)
    # 阅读量
    bread = models.IntegerField(default=0)
    # 价格,# max_digits 总位数， decimal_places 小数点位数
    bprice = models.DecimalField(max_digits=10, decimal_places=2)
    # 评论量
    bcomment = models.IntegerField(default=0)
    # 逻辑删除
    isDelete = models.BooleanField(default=False)

    # book = models.Manager()  # 自定义一个Manager对象
    objects = BookInfoManager()  # 自定义一个BookInfoManager对象

    def __str__(self):
        return self.btitle

    # @classmethod
    # def create_book(cls, title, pub_date):
    #     # 1、创建一个图书对象
    #     obj = cls()
    #     obj.btitle = title
    #     obj.bpub_date = pub_date
    #     obj.save()
    #     return obj

    def title(self):
        if not self.btitle:
            return ""
        return self.btitle
    title.admin_order_field = 'btitle'
    title.short_description = '书名'

# 多类
class HeroInfo(models.Model):
    """英雄人物类"""
    name = models.CharField(max_length=20)
    # 性别，BooleanFied说明是bool类型，default是默认值
    gender = models.BooleanField(default=False)
    # 备注
    comment = models.CharField(max_length=128)
    # 关系属性 简历图书类和英雄人物类的一对多关系
    book = models.ForeignKey('BookInfo', on_delete=models.SET)

    def __str__(self):
        return self.name


class NewsType(models.Model):
    """新闻类型类"""
    type_name = models.CharField(max_length=20)


class NewsInfo(models.Model):
    """新闻类"""
    # 标题
    title = models.CharField(max_length=128)
    # 发布时间
    pub_data = models.DateTimeField(auto_now_add=True)
    # 信息内容
    content = models.TextField()

    # 关系属性，多对多，定义在哪个类都可以
    news_type = models.ManyToManyField('NewsType')


class EmployeeBasicInfo(models.Model):
    """员工基本信息类"""
    # 姓名
    name = models.CharField(max_length=20)
    # 性别
    gender = models.BooleanField(default=False)
    # 年龄
    age = models.IntegerField()
    # 关系属性，代表员工的详细信息 一对一,写在两个类都可以
    employee_detail = models.OneToOneField('EmployeeDetailInfo', on_delete=models.SET)


class EmployeeDetailInfo(models.Model):
    """员工详细信息类"""
    # 联系地址
    addr = models.CharField(max_length=256)
    # ...
    # 关系属性 一对一关系，写在两个类都可以
    # employee_basic = models.OneToOneField('EmployeeBasicInfo')


class AreaInfo(models.Model):
    """地区模型类"""
    # 地区名称
    title = models.CharField(max_length=20)
    # 关系属性，代表当前地区的父级地区
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'areainfo'  # 指定表明

class PicTest(models.Model):
    """上传图片"""
    goods_pic = models.ImageField(upload_to='booktest')