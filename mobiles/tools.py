import time
import hashlib
from django.forms import model_to_dict

#每两个整点之间的值不一致
def GetMobileMd5(mobile):
    id = str(mobile.get('id',''))
    modelType = mobile.get('modelType','')
    DID = mobile.get('DID','')
    SysV = mobile.get('SysVersion','')
    salt = int(int(time.time()) / 7200)
    SecretKey='EWesadcsamaswi&asd2^agsdaswisnxasj'+id+modelType+DID+str(salt)+SysV
    m1 = hashlib.md5()
    # 使用md5对象里的update方法md5转换
    m1.update(SecretKey.encode("utf-8"))
    token = m1.hexdigest()
    return token

#每两个整点之间的值不一致
def GetUserToken(User):
    username = User.get('username','')
    password = User.get('password','')
    # token = User.get('u_token','')
    salt = User.get('salt')
    salt2 = int((int(time.time())-salt) /(8*3600))
    SecretKey='(*^#!KLjEWeaswi&asfd2^ag2f4s1wisgnxj'+str(username)+str(password)+'a9091&(*'+str(salt)+str(salt2)+str(salt)
              #+str(int(time.time()))
    m1 = hashlib.md5()
    # 使用md5对象里的update方法md5转换
    m1.update(SecretKey.encode("utf-8"))
    token = m1.hexdigest()
    return token

#每两个整点之间的值不一致
def LoginGetUserToken(User):
    username = User.get('username','')
    password = User.get('password','')
    # token = User.get('u_token','')
    salt = int(time.time())-1562056461
    salt2 = int((int(time.time())-salt) /(8*3600))
    SecretKey='(*^#!KLjEWeaswi&asfd2^ag2f4s1wisgnxj'+str(username)+str(password)+'a9091&(*'+str(salt)+str(salt2)+str(salt)
              #+str(int(time.time()))
    m1 = hashlib.md5()
    # 使用md5对象里的update方法md5转换
    m1.update(SecretKey.encode("utf-8"))
    token = m1.hexdigest()
    return token