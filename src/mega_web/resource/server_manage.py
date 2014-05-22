from mega_web.entity.models import Server,User
from conf.GlobalConf import *
from lib.utils import check_ip,is_int
import datetime

MSG_ERR_SERVER_NOT_EXITST='server does not exists!'
class ServerManage():
    def __init__(self,server):
        self.server_id=server.get("server_id")
        self.server_ip=server.get("server_ip")
        self.server_name=server.get("server_name")
        self.server_online=server.get("server_online")
        self.server_owner=server.get("server_owner")
        self.server_os=server.get("server_os")
        self.msg=''
        if not self.server_id:
            self.server_id=ServerGet().get_server_by_ip(self.server_ip)
        
    def data_check(self):
        if not self.server_ip or not check_ip(self.server_ip):
            self.msg+=MSG_ERR_IP
            return False
        if not self.server_name:
            self.server_name=self.server_ip
        if not self.server_online:
            self.server_online=datetime.datetime.now()
        if not self.server_os:
            self.server_os=DEFAULT_OS
        if not self.server_owner:
            self.server_owner=DEFAULT_OWNER
        return True
    def add_server(self):
        if not self.data_check():
            return False,self.msg
        isexist=ServerGet().get_server_by_ip(self.server_ip)
        if isexist:
            return False,MSG_ERR_SERVER_EXITST
        server=Server(ip=self.server_ip,name=self.server_name,online_date=self.server_online,owner=self.server_owner,os=self.server_os)
        server.save()
        return True,self.msg
    def mod_server(self):
        if not self.server_id:
            return False,MSG_ERR_SERVER_NOT_EXITST
        server=Server.objects.get(id=self.server_id)
        if self.server_name:
            server.name=self.server_name
        if self.server_os:
            server.os=self.server_os
        if self.server_owner:
            server.owner=self.server_owner
        if self.server_online:
            server.online_date=self.server_online
        server.save()
        return True,self.msg
    def stat_server(self,action=False):
        if not self.server_id:
            return False,MSG_ERR_SERVER_NOT_EXITST
        server=Server.objects.get(id=self.server_id)
        if action:
            server.stat=STAT_OFFLINE
        else:
            if server.stat== STAT_OFFLINE:
                server.stat=STAT_ONLINE
            else:
                server.stat=STAT_OFFLINE
        server.save()
        return True,self.msg
    
class ServerGet():
    def __init__(self):
        self.server=Server
    def get_server(self,server):
        server_id=server.get("server_id")
        result=self.get_server_by_id(server_id)
        return result
    def get_server_by_id(self,server_id=0):
        if server_id:
            result=self.server.objects.filter(id=server_id).values()[0]
        else:
            result=self.server.objects.all()[0:1].values()[0]
        result['online_date']=result["online_date"].strftime(DATETIME_FORMATE)   
        return result
    def get_server_by_ip(self,server_ip=''):
        result=''
        if server_ip:
            result=self.server.objects.filter(ip=server_ip).values('id')
        return result
    def get_server_list(self,str_filter,count=10,offset=0):
        result=None
        if str_filter:
            column=str_filter[0]
            value=str_filter[1]
            result=self.server.objects.filter(column=value)[offset:count]
        else:
            if count==0:
                result=self.server.objects.all().order_by('-stat').values()
            else:
                result=self.server.objects.all().order_by('-stat')[offset:count].values()
        for r in result:
            r['online_date']=r["online_date"].strftime(DATETIME_FORMATE)   
            owner=User.objects.filter(id=r['owner']).values('name')[0]
            r['owner_name']=owner['name']
        return result       