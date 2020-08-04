# 自定义过滤器
# 过滤器本质就是Python函数
import django.template

# 创建一个Library对象
register = django.template.Library()


@register.filter
def mod(num):
    """判断num是否为奇数"""
    return num % 2 == 1
