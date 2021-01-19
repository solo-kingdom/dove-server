from django import template

from book.models import BookTag, BookList, HotTagCollection

register = template.Library()


@register.inclusion_tag("module/_tag_list.html")
def show_tag_list():
    """
    获取 书籍标签
    :return:
    """
    tag_bgc_list = ['label-default', 'label-primary', 'label-success', 'label-warning', 'label-danger',
                    'label-info']
    book_tags = BookTag.objects.all()
    book_tag_first = book_tags[:8]
    book_tag_second = book_tags[8:50]
    return {"tag_bgc_list": tag_bgc_list,
            "book_tag_first": book_tag_first,
            "book_tag_second": book_tag_second,
            }


@register.inclusion_tag("module/_booklist_list.html")
def show_booklist_list(page=1):
    """
    获取 书单列表
    :return:
    """
    print(page)
    booklist_list = BookList.objects.all()
    return {"booklist_list": booklist_list, }


@register.inclusion_tag("module/_hot_tag_collections.html")
def show_hot_tag_collections(show_count=-1):
    """
    显示热门标签集合
    :return:
    """
    collections = None
    try:
        collections = HotTagCollection.objects.all()
    except Exception as e:
        print(e)
    return {"collections": collections, "show_count": show_count}
