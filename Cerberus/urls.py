"""Cerberus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf.urls import url
from django.urls import path,include
from django.contrib import admin
from mobiles import views as mobilesView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mobileIndex/$',mobilesView.mobileIndex),
    url(r'^login/',mobilesView.loginVerify),
    url(r'^indexHome/',mobilesView.gotoIndex),
    url(r'^toBorrow/',mobilesView.borrowMobile),
    url(r'^toReturn/',mobilesView.returnMobile),
    url(r'^getMobileBorroeRecord/',mobilesView.borrowRecordList),
    url(r'^getUserListInfo/',mobilesView.getUserListInfo),
    url(r'^toBorrowNew/',mobilesView.borrowMobile_new),
    url(r'^applyMobile/',mobilesView.applyMobile),
    url(r'^allowApplyMobile/',mobilesView.allowApplyMobile),
    url(r'^refuesApplyMobile/',mobilesView.refuesApplyMobile),
    url(r'^filterMobile/',mobilesView.filterMobile),
    # url(r'^indexHome_filte/*/',mobilesView.filterMobile),
    path('mobiles/',include('mobiles.urls')),

]
