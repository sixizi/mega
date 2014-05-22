import datetime
from mega_web.entity.models import Instance,Business,User
from lib.utils import check_ip,is_int
from server_manage import ServerGet,ServerManage
from conf.GlobalConf import *

MSG_ERR_INSTANCE_NOT_EXITST='instance does not exists!'

class InstanceManage():
    def __init__(self,instance):
        '''
        instance : a dict with instance base info
        '''
        self.inst_id=instance.get("instance_id")    
        self.inst_ip=instance.get("instance_ip")
        self.inst_port=instance.get("instance_port")
        self.inst_level=instance.get("instance_level")
        self.inst_name=instance.get("instance_name")
        self.inst_owner=instance.get("instance_owner")
        self.inst_bussiness=instance.get("instance_bussiness")
        self.inst_online_date=instance.get("instance_online")
        self.inst_dbtype=instance.get("instance_dbtype")
        self.inst_hatype=instance.get("instance_hatype")
        if not self.inst_id:
            self.inst_id=InstanceGet().get_instance_by_ip_port(self.inst_ip, self.inst_port)
        self.msg=''
    def data_check(self):
        if not self.inst_ip or not check_ip(self.inst_ip):
            self.msg+=MSG_ERR_IP
            return False
        if is_int(self.inst_port):
            self.msg+=MSG_ERR_PORT
            return False
        if not self.inst_level:
            self.inst_level=DEFAULT_LEVEL
        if not self.inst_name:
            self.inst_name=self.inst_ip
        if not self.inst_owner:
            self.inst_owner=DEFAULT_OWNER
        if not self.inst_online_date:
            self.inst_online_date=datetime.datetime.now()
        if not self.inst_dbtype:
            self.inst_dbtype=DEFAULT_DBTYPE
        if not self.inst_hatype:
            self.inst_hatype=DEFAULT_HATYPE
        if not self.inst_bussiness:
            self.inst_bussiness=DEFAULT_BUSINESS
        return True
    def add_instance(self):
        '''
            save new instance
            
        '''
        server_id=1
        if not self.data_check():
            return False,self.msg
        is_exist=InstanceGet().get_instance_by_ip_port(self.inst_ip, self.inst_port)
        if is_exist:
            self.msg+=MSG_ERR_INSTANCE_EXITST
            return False,self.msg
            
        is_server_exist=ServerGet().get_server_by_ip(self.inst_ip)
        if not is_server_exist:
            s,msg=ServerManage({'server_ip':self.inst_ip}).add_server()   

        server=ServerGet().get_server_by_ip(self.inst_ip)[0]        
        if server:
            server_id=server["id"]
        #is_owner_exist=
        #is_business_exist=   
        inst=Instance(server_id=server_id,ip=self.inst_ip,port=self.inst_port,level=self.inst_level,name=self.inst_name,business_id=self.inst_bussiness,
                      online_date=self.inst_online_date,owner=self.inst_owner,db_type=self.inst_dbtype,ha_type=self.inst_hatype)
        inst.save()
        return True,self.msg
    def mod_instance(self):
        if not self.inst_id:
            return False,MSG_ERR_INSTANCE_NOT_EXITST
        inst=Instance.objects.get(id=self.inst_id)        
        #inst.ip=self.inst_ip
        #inst.port=self.inst_port
        if self.inst_bussiness:
            inst.business_id=self.inst_bussiness
        if self.inst_level: 
            inst.level=self.inst_level
        if self.inst_name: 
            inst.name=self.inst_name  
        if self.inst_dbtype:              
            inst.db_type=self.inst_dbtype
        if self.inst_hatype:
            inst.ha_type=self.inst_hatype
        if self.inst_online_date:
            inst.online_date=self.inst_online_date
        if self.inst_owner:
            inst.owner=self.inst_owner
        inst.save()
        return True,self.msg
    def stat_instance(self,action=False):
        if not self.inst_id:
            return False,MSG_ERR_INSTANCE_NOT_EXITST
        inst=Instance.objects.get(id=self.inst_id)
        if action:
            inst.stat=STAT_OFFLINE
        else:
            if inst.stat==STAT_ONLINE:
                inst.stat=STAT_OFFLINE
            else:
                inst.stat=STAT_ONLINE
        inst.save()
        return True,self.msg
class InstanceGet():
    def __init__(self):
        self.inst=Instance
    def get_instance(self,instance):
        inst_id=instance.get("instance_id")
        result=self.get_instance_by_id(inst_id)
        business=Business.objects.filter(id=result['business_id']).values('name')[0]
        owner=User.objects.filter(id=result['owner']).values('name')[0]
        result["business"]=business['name']
        result["owner_name"]=owner['name']
        return result
    def get_instance_by_id(self,inst_id=0):
        if inst_id:
            result=self.inst.objects.filter(id=inst_id).values()[0]
        else:
            result=self.inst.objects.all()[0:1].values()[0]
        return result
    
    def get_instance_by_ip_port(self,ip,port=DEFAULT_DB_PORT):
        result=0
        result=self.inst.objects.filter(ip=ip,port=port).values("id")
        return result
    def get_instance_list(self,str_filter,count=10,offset=0):
        result=None
        sql="select i.* ,i.business_id,b.name as business,i.owner as owner_id,u.name as owner from instance i left join business b on i.business_id=b.id left join user u on i.owner=u.id "
        if len(str_filter):
            for f in str_filter:
                sql+=" and %s=%s" % (f,str_filter[f])
        sql+=" order by i.stat desc"
        if count==0:
            result=self.inst.objects.raw(sql)
        else:
            result=self.inst.objects.raw(sql)[offset:count]
        return result 