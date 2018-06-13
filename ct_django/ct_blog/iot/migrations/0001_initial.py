# Generated by Django 2.0.5 on 2018-05-29 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_iot', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(error_messages={'blank': 'Trường này là bắt buộc, vui lòng thử lại.', 'unique': 'Tiêu đề này không phải là duy nhất, vui lòng thử lại.'}, help_text='Tiêu đề phải là duy nhất.', max_length=240, unique=True, verbose_name='Tiêu Đề:')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('img', models.ImageField(null=True, upload_to='iot/', verbose_name='Ảnh:')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Nội Dung:')),
                ('publish', models.CharField(choices=[('draft', 'nháp'), ('publish', 'công khai'), ('private', 'riêng tư')], default='draft', max_length=120, verbose_name='Kiểu Bài Đăng:')),
                ('view_count', models.IntegerField(default=0, verbose_name='Lượt Xem:')),
                ('publish_date', models.DateField(default=django.utils.timezone.now, verbose_name='Ngày Xuất Bản:')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người Đăng Bài:')),
            ],
            options={
                'verbose_name': 'Bài Đăng',
                'verbose_name_plural': 'Đăng Bài',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='iot.PostModel'),
        ),
    ]
