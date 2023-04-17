from django.shortcuts import render, HttpResponse, redirect
from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from app01 import models
from django.core.exceptions import ValidationError
from django.contrib import messages
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapForm

import tushare as ts
import pandas as pd

# 导入tushare
# 初始化pro接口
pro = ts.pro_api('b34ed7024641a8e2cc0432ced9a8adebe5254d5d92fec46699b2add9')

# 拉取数据
df = pro.stock_basic(**{
    "ts_code": "",
    "name": "",
    "exchange": "",
    "market": "",
    "is_hs": "",
    "list_status": "",
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "symbol",
    "name",
    "area",
    "industry",
    "market",
])
print(df)
import pandas as pd
import pymysql

        


# Create your views here.
# 登陆界面


class LoginForm(BootStrapForm):
    name = forms.CharField(label="用户名", widget=forms.TextInput, required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(
        render_value=True), required=True)


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    # password = request.POST.get('password')
    # if not username or len(username.strip()) == 0:
    #     return HttpResponse('用户名错误')

    # if not password:
    #     return HttpResponse('密码错误')
    # a = models.UserInfo.objects.filter(
    #     name=username.strip()).filter(password=password)
    # if not a:
    #     return HttpResponse('用户名或密码错误！')
    if form.is_valid():  # 验证成功
        # a=form.cleaned_data.get('username')
        # password=models.UserInfo.objects.filter(name=a).first()
        # print(password)
        # if a=='qq':
        admin_object = models.UserInfo.objects.filter(
            **form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        request.session['info'] = {
            'id': admin_object.id, 'username': admin_object.name}
        return redirect('/index/')
    return render(request, 'login.html', {'form': form})

# def login_confirm(request,username):
#     correct_pwd=models.UserInfo.objects.filter(name=username).password
#     print(correct_pwd)


def logout(request):
    request.session.clear()
    return redirect('/login/')


class RegisterModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        # fields=["mobile","price","level",'status']
        fields = "__all__"

    def __init__(self, *args, **kwargs):  # 添加bootstrap样式“class=form-control”
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # if name =="password":
            #     continue
            field.widget.attrs = {
                "class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']  # 获取用户传入数据
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        return txt_mobile


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {"form": form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "注册成功！")
        return redirect('/login/')
    return render(request, 'register.html', {"form": form})


from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Sequence, DateTime
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def hangqing(request):
    from sqlalchemy import create_engine 
    # engine = create_engine("mysql+pymysql://root:qqzj20001215@localhost3306/biyesheji?charset=utf8") 
    conn=create_engine('mysql+pymysql://root:qqzj20001215@localhost:3306/biyesheji')
   
    # df.to_sql('StockList',engine,if_exists="replace")
    df.to_sql(app01_stocklist, con=conn,index = False , if_exists = 'append', chunksize = None)


    return render(request, "hangqing.html")


class NewsModelForm(BootStrapModelForm):
    class Meta:
        model = models.ZiXun
        # fields=["mobile","price","level",'status']
        fields = "__all__"

    def __init__(self, *args, **kwargs):  # 添加bootstrap样式“class=form-control”
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # if name =="password":
            #     continue
            field.widget.attrs = {
                "class": "form-control", "placeholder": field.label}


def zixun(request):
    form = models.ZiXun.objects.filter().all().order_by('-create_time')
    for item in form:
        if len(item.text) > 60:
            item.text = item.text[0:60]+'...'
    page_object = Pagination(request, form)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()       # 生成页码
    }
    return render(request, "zixun.html", context)


def news_check(request, nid):
    title = "资讯内容"
    form = models.ZiXun.objects.filter(id=nid).first()
    return render(request, 'news_check.html', {"form": form, "title": title})


def tuijian(request):
    return render(request, "tuijian.html")


def user_info(request):
    return render(request, 'userinfo.html')
