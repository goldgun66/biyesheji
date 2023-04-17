from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


class Job(models.Model):
    id = models.BigAutoField(verbose_name='ID', primary_key=True)
    title = models.CharField(verbose_name='职业', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(
        verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    job = models.ForeignKey(verbose_name="职业",
                            to="Job", to_field="id", on_delete=models.CASCADE)
    gender_choices = ((1, '男'), (2, '女'),)
    gender = models.SmallIntegerField(
        verbose_name='性别', choices=gender_choices)

    def confirm(self):
        username = self.clean_data.get('username')
        password = self.clean_data.get('password')
        if not username:
            raise ValidationError('请输入用户名')


class ZiXun(models.Model):
    title = models.CharField(verbose_name='标题', max_length=64)
    text = models.CharField(verbose_name='内容', max_length=5000)
    create_time = models.DateTimeField(verbose_name='创建时间')


class StockList(models.Model):
    ts_code=models.CharField(verbose_name='TS代码', max_length=10)
    symbol=models.CharField(verbose_name='股票代码', max_length=10)
    name=models.CharField(verbose_name='股票名称', max_length=10)
    area=models.CharField(verbose_name='地域', max_length=10)
    industry=models.CharField(verbose_name='所属行业', max_length=10)
    market=models.CharField(verbose_name='市场类型', max_length=10)