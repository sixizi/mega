import datetime
from mega_web.entity.models import Database,Business,User,Instance
from instance_manage import InstanceGet 
from conf.GlobalConf import * 
from lib.utils import check_ip,is_int
from business_manage import BusinessGet

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
        self.msg=''
    def data_check(self):
        if not self.db_name:
            self.msg+=MSG_ERR_NAME
            return False
        if not self.db_level:
            self.msg+=MSG_ERR_LEVEL
            return False
        if is_int(self.db_port):
            self.msg+=MSG_ERR_PORT
            return False
        if not self.db_online:
            self.db_online=datetime.datetime.now()

        return True  
    def add_database(self):
        '''
        database : a dict with database base info
        '''
        if not self.data_check():
            return False,self.msg
        db_instance=self.db_instance
        db_level=self.db_level
        db_name=self.db_name
        db_owner=self.db_owner
        db_bussiness=self.db_business
#get the owner id
        owner_id=DEFAULT_DB_OWNER
        
        is_exist=DatabaseGet().check_database_unique(db_instance,db_name)
        if is_exist:
            self.msg=MSG_ERR_DB_EXITST
            return False,self.msg
        db=Database(instance_id=db_instance,name=db_name,business_id=db_bussiness,level=db_level,owner=owner_id,online_date=self.db_online)
        db.save()
        self.msg='Sucess'
        return True,self.msg
    def mod_database(self):
        db=Database.objects.get(id=self.db_id)
        db.instance_id=InstanceGet().get_instance_by_ip_port(self.db_ip, self.db_port).get("id")
        db.ip=self.db_ip
        db.level=self.db_level
        db.port=self.db_port
        db.name=self.db_name
        db.onwer=self.db_owner
        db.business_id=BusinessGet().get_business_by_name(self.db_business).get("id")
        db.online_date=self.db_online
        db.save()
        return True
    def stat_database(self):
        db=Database.objects.get(id=self.db_id)
        if db.stat==STAT_ONLINE:
            db.stat=STAT_OFFLINE
        else:
            db.stat=STAT_ONLINE
        db.save()
        return True
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
        return self.db.objects.filter(instance_id=instance_id,name=name).values()[0]
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
            
            