import datetime
from mega_web.entity.models import Database,Business,User,Instance
from instance_manage import InstanceGet,InstanceManage
from conf.GlobalConf import * 
from lib.utils import check_ip,is_int
from business_manage import BusinessGet

MSG_ERR_DATABASE_NOT_EXITST="Database does not exists!"
class DatabaseManage():
    def __init__(self,database):
        self.db_id=database.get("database_id")    
        self.db_instance=database.get("database_instance")
        self.db_level=database.get("database_level")
        self.db_name=database.get("database_name")
        self.db_owner=database.get("database_owner")
        self.db_business=database.get("database_business")
        self.db_ip=database.get("database_ip")
        self.db_port=database.get("database_port")
        self.db_online=database.get("database_online")
        if not self.db_instance:
            self.db_instance=InstanceGet().get_instance_by_ip_port(self.db_ip, self.db_port)
        self.msg=''
        self._get_db()
    
    def _get_db(self):
        try:
            db=DatabaseGet().get_database_unique(self.db_instance, self.db_name)
            if db:
                self.db_id=db[0]['id']
        except:
            self.db_id=None
    def data_check(self):
        if not self.db_name:
            self.msg+=MSG_ERR_NAME
            return False
        if not self.db_ip:
            self.msg+=MSG_ERR_IP
            return False
        if is_int(self.db_port):
            self.msg+=MSG_ERR_PORT
            return False
        if not self.db_level:
            self.db_level=DEFAULT_LEVEL
        if not self.db_online:
            self.db_online=datetime.datetime.now()
        if not self.db_business:
            self.db_business=DEFAULT_BUSINESS
        if not self.db_owner:
            self.db_owner=DEFAULT_OWNER

        return True  
    def add_database(self):
        if not self.data_check():
            return False,self.msg
        is_exist=DatabaseGet().check_database_unique(self.db_instance,self.db_name)
        if is_exist:
            self.msg=MSG_ERR_DB_EXITST
            return False,self.msg
        if not self.db_instance:
            InstanceManage({"instance_ip":self.db_ip,"instance_port":self.db_port}).add_instance()
        instance_id=InstanceGet().get_instance_by_ip_port(self.db_ip, self.db_port)[0]["id"]
        db=Database(instance_id=instance_id,name=self.db_name,business_id=self.db_business,level=self.db_level,owner=self.db_owner,online_date=self.db_online)
        db.save()
        self.msg='Sucess'
        return True,self.msg
    def mod_database(self):
        if not self.db_id:
            return MSG_ERR_DATABASE_NOT_EXITST
        db=Database.objects.get(id=self.db_id)   
        instance_id=InstanceGet().get_instance_by_ip_port(self.db_ip, self.db_port)
        if instance_id:
            db.instance_id=instance_id[0]["id"]
#         db.ip=self.db_ip
#        db.port=self.db_port
#        db.name=self.db_name        
        if self.db_level:
            db.level=self.db_level
        if self.db_owner:
            db.onwer=self.db_owner
        if self.db_business:
            business_id=BusinessGet().get_business_by_name(self.db_business)
            if business_id:
                db.business_id=business_id[0]["id"] 
        if self.db_online:
            db.online_date=self.db_online
        db.save()
        return True,self.msg
    def stat_database(self,action=None):
        if not self.db_id:
            return False,MSG_ERR_DATABASE_NOT_EXITST
        db=Database.objects.get(id=self.db_id)
        if action:
            db.stat=STAT_OFFLINE
        else:
            if db.stat==STAT_ONLINE:
                db.stat=STAT_OFFLINE
            else:
                db.stat=STAT_ONLINE
        db.save()
        return True,self.msg
class DatabaseGet():
    def __init__(self):
        self.db=Database
    def get_database(self,database):
        db_id=database.get("database_id")
        result=self.get_database_by_id(db_id)
        business=Business.objects.filter(id=result['business_id']).values('name')[0]
        owner=User.objects.filter(id=result['owner']).values('name')[0]
        instance=Instance.objects.filter(id=result['instance_id']).values('ip','port')[0]
        result["business"]=business['name']
        result["owner_name"]=owner['name']
        result["ip"]=instance["ip"]
        result["port"]=instance["port"]
        return result
    def get_database_by_id(self,db_id=0):
        
        if db_id:
            result=self.db.objects.filter(id=db_id).values()[0]
        else:
            result=self.db.objects.all()[0:1].values()[0]
        return result
    def check_database_unique(self,instance_id,name):
        return self.db.objects.filter(instance_id=instance_id,name=name).count()
    def get_database_unique(self,instance_id,name):
        return self.db.objects.filter(instance_id=instance_id,name=name).values()
    def get_database_list(self,str_filter,count=10,offset=0):
        result=None
        sql="select d.* ,i.ip,i.port,b.name as business,u.name as owner_name from `databases` d left join \
         instance i on d.instance_id=i.id left join business b on d.business_id=b.id left join user u on d.owner=u.id"
        if str_filter:
            column=str_filter[0]
            value=str_filter[1]
            sql+="and %s=%s"(column,value)
        sql+=" order by stat desc"
        if count==0:
            result=self.db.objects.raw(sql)
        else:
            result=self.db.objects.raw(sql)[offset:count]  
        return result       
            
            