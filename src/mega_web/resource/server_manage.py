from mega_web.entity.models import Server,User
from conf.GlobalConf import *
from lib.utils import check_ip,is_int
import datetime

class ServerManage():
    def __init__(self,server):
        self.server_id=server.get("server_id")
        self.server_ip=server.get("server_ip")
        self.server_name=server.get("server_name")
        self.server_online=server.get("server_online")
        self.server_owner=server.get("server_owner")
        self.server_os=server.get("server_os")
        self.msg=''
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
            self.server_owner=DEFAULT_SERVER_OWNER
        return True
    def add_server(self):
        '''
        server  a dict with server base info 
        '''
        if not self.data_check():
            return False,self.msg
        server=Server(ip=self.server_ip,name=self.server_name,online_date=self.server_online,owner=self.server_owner,os=self.server_os)
        server.save()
        return True    
    def mod_server(self):
        server=Server.objects.get(id=self.server_id)
        server.name=self.server_name
        server.ip=self.server_ip
        server.os=self.server_os
        server.owner=self.server_owner
        server.online_date=self.server_online
        server.save()
        return True   
    def stat_server(self):
        server=Server.objects.get(id=self.server_id)
        if server.stat== STAT_OFFLINE:
            server.stat=STAT_ONLINE
        else:
            server.stat=STAT_OFFLINE
        server.save()
        return True
    
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
            result=self.server.objects.all().order_by('-stat')[offset:count].values()
        for r in result:
            r['online_date']=r["online_date"].strftime(DATETIME_FORMATE)   
            owner=User.objects.filter(id=r['owner']).values('name')[0]
            r['owner_name']=owner['name']
        return result       