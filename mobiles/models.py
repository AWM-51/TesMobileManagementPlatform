# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#用户表
#status(1:正常,2:异常)
#identity(1：用户，2：管理员)
class User(models.Model):
    name=models.CharField(max_length=60)
    username = models.CharField(max_length=60,default='',unique = True)
    password = models.CharField(max_length=60,default='')
    creatTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    status=models.IntegerField(default=1)
    identity=models.IntegerField(default=1)
    u_token=models.CharField(max_length=100,default='notoken')
    salt=models.IntegerField(default=0)

#手机

class Mobile(models.Model):
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    modelType=models.CharField(max_length=50)
    DID=models.CharField(max_length=30)
    DType=models.CharField(max_length=30)
    SysVersion=models.CharField(max_length=50)
    BorrowStatus=models.BooleanField(default=True)
    applyUserid=models.IntegerField(default=0)
    applyUserName = models.CharField(max_length=30,default='')
    # BorrowStatus = models.IntegerField(default=0)
    BorrowPeopleID = models.IntegerField()
    BorrowPeopleName=models.CharField(max_length=60,default='None')
    def __str__(self):
        return self.modelType

#手机借用记录
class MobileBorrowingRecord(models.Model):
    mobile_id=models.IntegerField()
    # mobile=models.ForeignKey(Mobile,on_delete=models.CASCADE)
    BorrowTime=models.DateTimeField(auto_now_add=True)
    ReturnTime=models.DateTimeField(auto_now_add=True)
    BorrowPeopleName=models.CharField(max_length=60)
    ReturnPeopleName = models.CharField(max_length=60)

#设备号的md5值
class MobileMd5(models.Model):
    mobile_id = models.IntegerField()
    md5=models.CharField(max_length=100)
    creatTime=models.DateTimeField(auto_now_add = True)
    updateTime=models.DateTimeField(auto_now = True)


#手机申请记录表
#status 1:申请中 2:申请成功 0：申请失败
class MobileApplicationRecord(models.Model):
    mobile_id = models.IntegerField()
    user_id=models.IntegerField()
    status=models.IntegerField()
    creatTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)









