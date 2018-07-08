from datetime import timedelta, datetime, date
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.utils.encoding import smart_text
from django.utils import timezone 
from django.utils.text import slugify
from django.utils.timesince import timesince


PUBLISH_CHOICES = [
        ('computer', 'máy tính'),
        ('mobile', 'điện thoại'),
        ('technology', 'công nghệ'),
        ('games', 'games'),
    ]

class PostModelQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def kind(self):
        return self.filter(kind="computer")

    def post_title_items(self, value):
        return self.filter(title__icontains=value)

    def search(self, query):
        lookups = (Q(title__icontains=query) | 
                  Q(content__icontains=query)
                  )
        return self.filter(lookups).distinct()


class PostModelManager(models.Manager):
    def get_queryset(self):
        return PostModelQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        qs = self.get_queryset().active()
        return qs

    def get_timeframe(self, date1, date2):
        #giả định đối tượng datetime
        qs = self.get_queryset()
        qs_time_1 = qs.filter(publish_date__gte=date1)
        qs_time_2 = qs_time_1.filter(publish_date__lt=date2) # Q Lookups
        return qs_time_2

    def search(self, query):
        return self.get_queryset().active().search(query)

class PostModel(models.Model):
    id              = models.BigAutoField(primary_key=True)
    active          = models.BooleanField(default=True) # trống trong cơ sở dữ liệu
    title           = models.CharField(
                            max_length=240, 
                            verbose_name='Tiêu Đề:', 
                            unique=True,
                            error_messages={
                                "unique": "Tiêu đề này không phải là duy nhất, vui lòng thử lại.",
                                "blank": "Trường này là bắt buộc, vui lòng thử lại."
                            },
                            help_text='Tiêu đề phải là duy nhất.')
    slug            = models.SlugField(null=True, blank=True, )
    img             = models.ImageField(null=True, blank=True, upload_to='blog/', verbose_name='Ảnh:')
    content         = models.TextField(null=True, blank=True, verbose_name='Nội Dung:')
    kind            = models.CharField(max_length=120, choices=PUBLISH_CHOICES, verbose_name='Kiểu Bài Đăng:')
    view_count      = models.IntegerField(default=0, verbose_name='Lượt Xem:')
    publish_date    = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now, verbose_name='Ngày Xuất Bản:')
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, verbose_name='Người Đăng Bài:', related_name='author_blog1')
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = PostModelManager()
    other = PostModelManager()

    def save(self, *args, **kwargs):
        super(PostModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Bài Đăng'
        verbose_name_plural = 'Bài Đăng'

    def __unicode__(self): #python 2
        return smart_text(self.title) #self.title

    def __str__(self): #python 3
        return smart_text(self.title)
'''
    @property
    def age(self):
        if self.kind== 'kind':
            now = datetime.now()
            publish_time = datetime.combine(
                                self.publish_date,
                                datetime.now().min.time()
                        )
            try:
                difference = now - publish_time
            except:
                return "không xác định"
            if difference <= timedelta(minutes=1):
                return 'vừa nãy'
            return '{time} trước đây'.format(time= timesince(publish_time).split(', ')[0])
        return "Chưa xuất bản"
'''


def blog_post_model_pre_save_receiver(sender, instance, *args, **kwargs):
    print("trước khi lưu")
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title) 

pre_save.connect(blog_post_model_pre_save_receiver, sender=PostModel)

def blog_post_model_post_save_receiver(sender, instance, created, *args, **kwargs):
    print("sau khi lưu")
    print(created)
    if created:
        if not instance.slug and instance.title:
            instance.slug = slugify(instance.title)
            instance.save()

post_save.connect(blog_post_model_post_save_receiver, sender=PostModel)


class Comment(models.Model):
    post = models.ForeignKey(PostModel, on_delete= models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='author_blog2')
    body = models.TextField(verbose_name="Bình luận")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Bình luận:'
        verbose_name_plural = 'Bình luận:'