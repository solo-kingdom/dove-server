from django.contrib import admin

# Register your models here.
# 注册自己的 models, 使用django提供的后台管理
from book.models import *
from django.contrib.auth.admin import UserAdmin


# django admin界面显示昵称字段
UserAdmin.list_display += ('nickname',)
UserAdmin.list_filter += ('nickname',)
UserAdmin.fieldsets += (('nickname', {'fields': ('nickname',)}),)

admin.site.register(Book)
admin.site.register(BookScore)
admin.site.register(BookAuthor)
admin.site.register(BookTag)
admin.site.register(BookListTagShip)
admin.site.register(BookTagShip)
admin.site.register(BookInfo)
admin.site.register(BookRemark)
admin.site.register(BookSeries)
admin.site.register(BookList)
admin.site.register(SearchTask)
admin.site.register(HotTagCollection)

