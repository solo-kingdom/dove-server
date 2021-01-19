# coding: utf-8
from django.conf.urls import url
from book.view import views, common_views, views_user, views_booklist, views_book, views_search, views_tag

urlpatterns = [
    url(r'^$', views_booklist.booklist, name='index'),
    # url(r'^page/(?P<page>\d+)/?$', views.index, name='index_with_page'),

    # 书籍详情
    url(r'^bookdetail/(?P<book_id>\d+)?/*$', views_book.book_detail, name="book_detail"),
    # 通过豆瓣url获取书籍信息
    url(r'^book/url/*$', views.get_douban_book_from_url, name="get-book-from-url"),

    # 将书籍添加到多个书单
    url(r'^book/add-to-booklists/', views.book_add_to_booklists, name="book-add-to-booklists"),

    # 评语
    url(r'^book-remark/?$', views.book_remark, name='book-remark'),

    # 搜索
    url(r'^search/?$', views_search.search, name='search'),
    url(r'^search/booklist/?$', views_search.search_booklist, name='search-booklist'),
    url(r'^search/book/?$', views_search.search_book, name='search-book'),
    # url(r'^search/tag/(?P<keyword>\S+)?/?$', views_search.search_booklist, name='search-tag'),
    # url(r'^search/page/(?P<page>\d+)/?$', views.search, name='search_with_page'),
    # url(r'^search/(?P<search_type>[a-zA-Z]+)/page/(?P<page>\d+)/?$', views.search, name='search'),

    # 发现
    url(r'^find/?$', views.find, name='find'),
    url(r'^find/page/(?P<page>\d+)/?$', views.find, name='find_with_page'),

    # 测试
    url(r'^test$', views.test, name='test'),
    url(r'^your-ip/?$', views.your_ip, name='your-ip'),

]

urlpatterns += [
    # 标签
    url(r'^tag/(?P<tag_id>\d+)/book/?$', views_tag.tag_book, name='tag-book'),
    url(r'^tag/(?P<tag_id>\d+)/booklist/?$', views_tag.tag_booklist, name='tag-booklist'),
    url(r'^tag/hot/?$', views_tag.hot_tag_collection, name='tag-hot-collection'),
]

# 书单相关url
urlpatterns += [
    # 书单详情
    url(r'^booklist/(?P<booklist_id>\d+)/?$', views_booklist.booklist_detail, name='booklist_detail'),
    url(r'^booklist/(?P<booklist_id>\d+)/(?P<page>\d+)/?$', views_booklist.booklist_detail, name='booklist_detail_with_page'),

    # 修改书单
    url(r'^booklist/add/?$', views_booklist.add_booklist, name='add-booklist'),
    url(r'^booklist/update/?$', views_booklist.booklist_update, name='update-booklist'),
    url(r'^booklist/delete/?$', views_booklist.booklist_delete, name='delete-booklist'),
    url(r'^booklist/book/add/?$', views_booklist.booklist_add_book, name='booklist-add-book'),
    url(r'^booklist/book/delete/?$', views_booklist.booklist_delete_book, name='booklist-delete-book'),
]

# 用户相关url
urlpatterns += [
    # 用户书单列表
    url(r'^user/register/?$', views_user.user_register, name='register'),
    url(r'^user/login/?$', views_user.user_login, name='login'),
    url(r'^user/logout/?$', views_user.user_logout, name='logout'),
    url(r'^user/booklist/get/?$', views.user_booklist_get, name='user-booklist-get'),
    # 用户主页
    url(r'^user/profile/?$', views_user.user_profile, name='user-profile'),
    url(r'^user/profile/update/?$', views_user.user_profile_update, name='user-profile-update'),
    url(r'^user/(?P<user_id>\d+)?/?$', views_user.user_page, name='user-page'),
]

urlpatterns += [
    # 如果都没有匹配, 返回404页面
    url(r'', common_views.return_404_page, name='404-page'),
    # url(r'^scrapy$', views.scrapy, name='scrapy'),
]