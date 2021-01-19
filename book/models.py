# codding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone

# User.add_to_class('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True))    # 添加uuid字段
User.add_to_class('nickname', models.CharField(max_length=200, null=True, default="#"))


class BookScore(models.Model):
    """
    图书 评分
    """
    score = models.CharField(verbose_name='平均分', max_length=50, null=True, default='0.0')
    people_count = models.CharField(verbose_name='评论人数', max_length=50, null=True, default=0)
    max = models.CharField(verbose_name='最高评分', max_length=50, null=True, default='0')
    min = models.CharField(verbose_name='最低评分', max_length=50, null=True, default='0')


class BookAuthor(models.Model):
    """
    图书作者
    """
    # 性别选择
    # MALE = 'MALE'
    # FEMALE = 'FEMALE'
    # OTHER = 'OTHER'
    # SECRET = 'SECRET'
    # SEX_CHOICES = [
    #     (MALE, '男'),
    #     (FEMALE, '女'),
    #     (OTHER, '其他'),
    #     (SECRET, '保密')
    # ]
    # country = models.CharField(verbose_name='国家', max_length=50, null=True, blank=True, default='')
    # sex = models.CharField(verbose_name='性别', max_length=8, choices=SEX_CHOICES, default=SECRET)

    name = models.CharField(verbose_name='作者名称', max_length=100)
    description = models.TextField(verbose_name='作者描述', max_length=10000, null=True, blank=True, default='')

    def __str__(self):
        return self.name


class BookTag(models.Model):
    """
    图书 标签
    """
    name = models.CharField('名称', max_length=100)
    count = models.IntegerField(verbose_name='书籍数量', default=0)

    def __str__(self):
        return self.name


class BookTagShip(models.Model):
    """图书 - 标签关联表"""
    book = models.ForeignKey('Book')
    tag = models.ForeignKey(BookTag)
    count = models.IntegerField(verbose_name='图书包含标签次数', default=0)

    def __str__(self):
        return self.book.name + " - " + self.tag.name


class BookListTagShip(models.Model):
    """书单 - 标签关联表"""
    booklist = models.ForeignKey('BookList')
    tag = models.ForeignKey(BookTag)
    count = models.IntegerField(verbose_name='书单包含标签次数', default=0)

    def __str__(self):
        return self.booklist.name + " - " + self.tag.name


class BookInfo(models.Model):
    """书籍详细信息"""
    origin_title = models.CharField(verbose_name='原作名', max_length=300, null=True, default='')
    subtitle = models.CharField(max_length=300, null=True, default='')
    binding = models.CharField(verbose_name='装帧', max_length=50, default='')
    catalog = models.TextField(verbose_name='目录', max_length=10000, null=True, blank=True, default='')
    pages = models.CharField(verbose_name='页数', max_length=50, null=True, default='')
    publisher = models.CharField(verbose_name='出版社', max_length=300, null=True, default='')
    isbn = models.CharField(max_length=50, null=True, default='')
    url = models.CharField(verbose_name='豆瓣链接', max_length=300, null=True, default='')
    pic_url = models.CharField(verbose_name='豆瓣图片下载地址', max_length=500, null=True, default='')
    douban_id = models.CharField(verbose_name='在豆瓣中的id', max_length=50, null=True, blank=True, default='')
    price = models.CharField(verbose_name='定价', max_length=50, null=True, blank=True, default='')
    pubdate = models.CharField(verbose_name='出版日期', max_length=50, null=True, default='')

    translator = models.ManyToManyField(BookAuthor)


class BookKeyword(models.Model):
    name = models.CharField("关键词", max_length=100, default="", blank=True, null=True)
    weight = models.FloatField("权重", default=0.0)


class BookRecommend(models.Model):
    recommend = models.ForeignKey("Book")
    rate = models.FloatField("推荐度", default=0.0)


class Book(models.Model):
    """
    图书 Model
    """
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='书名', max_length=300, null=True, default='未命名书籍')
    summary = models.TextField('简介', max_length=10000, default="", blank=True)
    pic = models.CharField(verbose_name='本地图片地址', max_length=300, null=True, default='')

    author = models.ManyToManyField(BookAuthor)
    tags = models.ManyToManyField(BookTag, through=BookTagShip)
    score = models.ForeignKey(BookScore, null=True, on_delete=models.CASCADE)
    info = models.ForeignKey(BookInfo, null=True, on_delete=models.CASCADE)
    # 关键词
    keywords = models.ManyToManyField(BookKeyword)
    # 推荐
    recommends = models.ManyToManyField(BookRecommend)

    def __str__(self):
        return self.name


class BookSeries(models.Model):
    """丛书"""
    name = models.CharField(verbose_name='名称', max_length=200, default='')
    douban_id = models.CharField(verbose_name='豆瓣中id', max_length=50, default='')
    books = models.ManyToManyField(Book)


class BookList(models.Model):
    """书单"""
    # uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='书单名称', max_length=200, default="未命名书单")
    summary= models.TextField(verbose_name='书单简介', max_length=10000, default="", blank=True)
    pic = models.CharField(verbose_name='书单图片', max_length=300, null=True, default="no-pic.jpg")
    # 标签; BookTagShip
    tags = models.ManyToManyField(BookTag, through=BookListTagShip)
    # 包含的书籍
    books = models.ManyToManyField(Book, blank=True)
    create_date = models.DateTimeField('书单创建时间', default=timezone.now, null=True)
    update_date = models.DateTimeField(verbose_name='最后添加书籍时间', auto_now=True)
    user = models.ForeignKey(User, null=True, default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        重写save方法, 根据书籍添加标签
        :param args:
        :param kwargs:
        :return:
        """
        if self.id:
            self.update_booklist_tag()
            super(BookList, self).save(*args, **kwargs)
        else:
            super(BookList, self).save(*args, **kwargs)

    def update_booklist_tag(self):
        # 自动添加标签
        for booklist_tag_ship in BookListTagShip.objects.filter(booklist_id=self.id):
            booklist_tag_ship.delete()

        for book in self.books.all():
            for tag in book.tags.all():
                try:
                    booklist_tag_ship = BookListTagShip.objects.filter(booklist_id=self.id, tag_id=tag.id).first()
                    if booklist_tag_ship:
                        # 如果存在
                        booklist_tag_ship.count += 1  # 关系增1
                        booklist_tag_ship.save()  # 保存
                    else:
                        # 如果不存在, 创建并保存
                        booklist_tag_ship = BookListTagShip.objects.create(booklist=self, tag=tag, count=1)
                        booklist_tag_ship.save()
                except Exception as e:
                    print(e)


@receiver(m2m_changed, sender=BookList.books.through)
def booklist_books_changed(sender, instance, **kwargs):
    """对书单里面的书籍进行更改时, 更改书签"""
    instance.update_booklist_tag()


class BookRemark(models.Model):
    booklist = models.ForeignKey(BookTag, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField('评语', max_length=10000, default="", blank=True)
    update_date = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.content[:50]


class SearchTask(models.Model):
    search_type = models.CharField(max_length=100, default="", null=True, blank=True)
    search_keyword = models.CharField(max_length=1000, default="", null=True, blank=True)
    search_start= models.IntegerField(default=0)
    total = models.IntegerField(default=100)

    def __str__(self):
        return self.search_keyword


class HotTagCollection(models.Model):
    """豆瓣热门标签集合"""
    title = models.CharField(max_length=100, default="")
    tags = models.ManyToManyField(BookTag)

    def __str__(self):
        return self.title
