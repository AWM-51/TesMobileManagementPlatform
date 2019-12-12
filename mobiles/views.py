# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render
# Create your views here.
from pandas._libs import json

from mobiles.models import Mobile,MobileMd5,MobileBorrowingRecord,MobileApplicationRecord
from django.forms import model_to_dict
from mobiles.tools import GetMobileMd5,GetUserToken, LoginGetUserToken
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django import forms
from mobiles.models import User
from django.db.models import Q
import time



def tokenVerify(func):
    def Verfiy(request,*args, **kwargs):
        if request.method == 'POST':

            token=request.POST.get('u_token')
            user = User.objects.filter(u_token=token)
            if user:
                userinfo = User.objects.get(u_token=token)
                userinfo_dict = model_to_dict(userinfo)
                new_token = GetUserToken(userinfo_dict)
                if token==new_token:
                    return func(request, *args, **kwargs)
                else:
                    User.objects.filter(u_token=userinfo.u_token).update(u_token=new_token)
                    # return HttpResponseRedirect('/')
                    result = {"result": 'success', "message": '登陆失效'}
                    return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                result = {"result": 'success', "message": '被人踢了'}
                return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            return HttpResponseRedirect('/')

    Verfiy.__name__=func.__name__
    return Verfiy


#定义表单模型
class UserForm(forms.Form):
    username = forms.CharField(label = '用户名 :',max_length = 50)
    password = forms.CharField(label = '密码 :',widget = forms.PasswordInput())

# 管理页面展示
def index(request):
    mobiles=Mobile.objects.all()
    return render(request,"index.html",{'c':mobiles})

#用户登陆验证
def loginVerify(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                newsalt = int(time.time()) - 1562056461
                user.update(salt=newsalt)
                userinfo=User.objects.get(username=username)
                userinfo_dict=model_to_dict(userinfo)
                token=GetUserToken(userinfo_dict)
                User.objects.filter(id=userinfo.id).update(u_token=token)
                mobiles = Mobile.objects.all()
                # return HttpResponseRedirect('/indexHome/',request)
                return render(request, 'index_new.html', {'token': token, 'mobiles': mobiles, 'identity': userinfo_dict.get('identity')})
            else:
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html', {'uf': uf})

def gotoIndex(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        username = uf.cleaned_data['username']
        userinfo = User.objects.get(username=username)
        userinfo_dict = model_to_dict(userinfo)
        mobiles = Mobile.objects.all()
        return render(request, 'index_new.html',
                      {'token': userinfo.u_token, 'mobiles': mobiles, 'identity': userinfo_dict.get('identity')})



# 手机操作页面展示
def mobileIndex(request):
    mid=request.GET.get('mid')
    GetMobileInfo=Mobile.objects.get(id=mid)
    return render(request,"mobileIndex.html",{'GetMobileInfo':GetMobileInfo,'mid':mid})


#借用手机
@tokenVerify
def borrowMobile(request):
    if request.method == 'POST':
        mid=request.POST.get('mid')
        u_token=request.POST.get('u_token')
        user=User.objects.filter(u_token=u_token)
        if user:
            userInfo=model_to_dict(User.objects.get(u_token=u_token))
            mobile=model_to_dict(Mobile.objects.get(id=mid))
            if mobile.get('BorrowStatus')==True:
                try:
                    Mobile.objects.filter(id=mid).update(BorrowStatus=False,BorrowPeopleID=userInfo.get('id'),BorrowPeopleName=userInfo.get('name'))
                    MobileBorrowingRecord.objects.create(mobile_id=mid,BorrowPeopleName=userInfo.get('name'))
                    new_mobile = model_to_dict(Mobile.objects.get(id=mid))
                    result = {"result": 'success', "message": '成功借用','GetMobileInfo':new_mobile}
                except Exception:
                    result = {"result": 'false', "message": '数据库操作失败'}
            else:
                result = {"result": 'false', "message": '该手机已借出'}
        else:
            result = {"result": 'false', "message": '口令无效'}

        return HttpResponse(json.dumps(result), content_type="application/json")



#归还手机
@tokenVerify
def returnMobile(request):
    if request.method == 'POST':
        mid=request.POST.get('mid')
        u_token=request.POST.get('u_token')
        print('mid:'+mid+'  u_token:'+u_token)
        user=User.objects.filter(u_token=u_token,identity=2)
        print(user)
        if user:
            userInfo=model_to_dict(User.objects.get(u_token=u_token))
            mobile=model_to_dict(Mobile.objects.get(id=mid))
            if mobile.get('BorrowStatus')==False:
                try:
                    Mobile.objects.filter(id=mid).update(BorrowStatus=True,BorrowPeopleID=0,BorrowPeopleName='None',applyUserid=0,applyUserName='')
                    MobileBorrowingRecord.objects.create(mobile_id=mid,ReturnPeopleName=userInfo.get('name'))
                    result = {"result": 'success', "message": '成功归还'}
                except Exception:
                    result = {"result": 'false', "message": '数据库操作失败'}
            else:
                result = {"result": 'false', "message": '该手机已经归还，无需操作'}
        else:
            result = {"result": 'false', "message": '无该用户'}
        return HttpResponse(json.dumps(result), content_type="application/json")

@tokenVerify
def borrowRecordList(request):
    if request.method == 'POST':
        mid = request.POST.get('mid')
        u_token = request.POST.get('u_token')
        user = User.objects.filter(u_token=u_token,status=1)
        if user:
            try:
                borrowMobileRecordList=list(MobileBorrowingRecord.objects.filter(mobile_id=mid)
                                            .values('BorrowTime','ReturnTime','BorrowPeopleName','ReturnPeopleName').order_by('-id')[:10])
                result = {"result": 'success', "message": '查询成功', "mobileBorrowRecordList": borrowMobileRecordList}
            except MobileBorrowingRecord.DoesNotExist:
                result = {"result": 'success', "message": '查询成功', "mobileBorrowRecordList": None}
        else:
            result = {"result": 'false', "message": '登陆失效'}
            # uf=UserForm()
            # return render(request,'login.html', {'uf': uf})
        return HttpResponse(json.dumps(result), content_type="application/json")

#获取用户list信息
@tokenVerify
def getUserListInfo(request):
    if request.method == 'POST':
        u_token = request.POST.get('u_token')
        user = User.objects.filter(u_token=u_token, identity=2)
        if user:
            usersList=list(User.objects.filter(identity=1,status=1).values('name','u_token'))
            result = {"result": 'success', "message": '查询成功',"usersList":usersList}
        else:
            result = {"result": 'false', "message": '无权限'}
        return HttpResponse(json.dumps(result), content_type="application/json")


#借用手机2.0
@tokenVerify
def borrowMobile_new(request):
    if request.method == 'POST':
        mid=request.POST.get('mid')
        u_token=request.POST.get('u_token')
        b_token=request.POST.get('b_token')
        user=User.objects.filter(u_token=u_token,identity=2,status=1)
        if user:
            userInfo=model_to_dict(User.objects.get(u_token=b_token))
            mobile=model_to_dict(Mobile.objects.get(id=mid))
            if mobile.get('BorrowStatus')==True:
                try:
                    Mobile.objects.filter(id=mid).update(BorrowStatus=False,BorrowPeopleID=userInfo.get('id'),BorrowPeopleName=userInfo.get('name'))
                    MobileBorrowingRecord.objects.create(mobile_id=mid,BorrowPeopleName=userInfo.get('name'))
                    new_mobile = model_to_dict(Mobile.objects.get(id=mid))
                    result = {"result": 'success', "message": '成功借用','GetMobileInfo':new_mobile}
                except Exception:
                    result = {"result": 'false', "message": '数据库操作失败'}
            else:
                result = {"result": 'false', "message": '该手机已借出'}
        else:
            result = {"result": 'false', "message": '口令无效'}

        return HttpResponse(json.dumps(result), content_type="application/json")


#申请借用手机
@tokenVerify
def applyMobile(request):
    if request.method == 'POST':
        mid=request.POST.get('mid')
        u_token=request.POST.get('u_token')
        user = User.objects.filter(u_token=u_token,identity=1,status=1)
        if user:
            userinfo = User.objects.get(u_token=u_token, identity=1, status=1)
            u_id=userinfo.id
            name=userinfo.name
            isHasNoApplied=Mobile.objects.filter(id=mid,applyUserid=0);
            if isHasNoApplied:
                try:
                    Mobile.objects.filter(id=mid).update(applyUserid=u_id,applyUserName=name)
                    result = {"result": 'false', "message": '申请成功'}
                except Exception:
                    result = {"result": 'false', "message": '数据库操作失败'}
            else:
                result = {"result": 'false', "message": '正在申请中,或被借出'}
        else:
            result = {"result": 'false', "message": '用户状态不正常'}


        return HttpResponse(json.dumps(result), content_type="application/json")

#允许申请通过
@tokenVerify
def allowApplyMobile(request):
    if request.method == 'POST':
        mid=request.POST.get('mid')
        u_token=request.POST.get('u_token')
        u_id=request.POST.get('u_id')
        user = User.objects.filter(u_token=u_token,identity=2,status=1)
        user2 = User.objects.filter(id=u_id, identity=1, status=1)
        if user and user2:
            userinfo = User.objects.get(id=u_id, identity=1, status=1)
            mobile=Mobile.objects.filter(id=mid,BorrowStatus=True,applyUserid=u_id)
            if mobile:
                try:
                    mobile.update(BorrowStatus=False,BorrowPeopleID=u_id,BorrowPeopleName=userinfo.name)
                    MobileBorrowingRecord.objects.create(mobile_id=mid, BorrowPeopleName=userinfo.name)
                    new_mobile = model_to_dict(Mobile.objects.get(id=mid))
                    result = {"result": 'success', "message": '成功借用', 'GetMobileInfo': new_mobile}
                except:
                    result = {"result": 'false', "message": '数据库操作失败'}
            else:
                result = {"result": 'false', "message": '未找到该申请信息'}
        else:
            result = {"result": 'false', "message": '用户状态不正常'}

        return HttpResponse(json.dumps(result), content_type="application/json")


#拒绝申请通过
@tokenVerify
def refuesApplyMobile(request):
    if request.method == 'POST':
        mid=request.POST.get('mid')
        u_token=request.POST.get('u_token')
        u_id=request.POST.get('u_id')
        user = User.objects.filter(u_token=u_token,identity=2,status=1)
        user2 = User.objects.filter(id=u_id, identity=1, status=1)
        if user and user2:
            userinfo = User.objects.get(id=u_id, identity=1, status=1)
            mobile=Mobile.objects.filter(id=mid,BorrowStatus=True,applyUserid=u_id)
            if mobile:
                try:
                    mobile.update(applyUserid=0,applyUserName='')
                    result = {"result": 'success', "message": '拒绝成功'}
                except:
                    result = {"result": 'false', "message": '数据库操作失败'}
            else:
                result = {"result": 'false', "message": '未找到该申请信息'}
        else:
            result = {"result": 'false', "message": '用户状态不正常'}

        return HttpResponse(json.dumps(result), content_type="application/json")

# @tokenVerify
# def filterMobile_url(request):
#
#     if request.method == 'POST':
#         u_token = request.POST.get('u_token')
#         option=request.POST.get('option')
#         return HttpResponseRedirect('/indexHome_filte/?token=' + u_token+'&option='+option)

#筛选手机
@tokenVerify
def filterMobile(request):
    if request.method == 'POST':
        u_token=request.POST.get('u_token')
        user = User.objects.filter(u_token=u_token,status=1)
        option=request.POST.get('option')
        if user:
            userinfo_dict = User.objects.get(u_token=u_token, status=1)
            if option=='1' :#可借
                mobiles = Mobile.objects.filter(BorrowStatus=True)
            elif option=='2' :#不可借
                mobiles = Mobile.objects.filter(BorrowStatus=False)
            elif option=='3' :#申请中
                mobiles = Mobile.objects.filter(~Q(applyUserid=0),BorrowStatus=True)
            elif option=='4':#安卓
                mobiles = Mobile.objects.filter(DType__contains="安卓")
            elif option == '5': # iOS
                mobiles = Mobile.objects.filter(DType__contains="iOS")
            elif option == '0' :
                mobiles = Mobile.objects.all()
            result={'token': u_token, 'mobiles': list(mobiles.values()), 'identity': userinfo_dict.identity,'message':'查询成功'}
        else:
            result = {'token': u_token, 'mobiles': [], 'identity': 0,
                      'message': '查无此人'}
        return HttpResponse(json.dumps(result), content_type="application/json")



