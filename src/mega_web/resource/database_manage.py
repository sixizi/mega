from mega_web.entity.models import Database
from instance_manage import InstanceGet 
class databaseManage():
    def __init__(self,database):
        self.database=database
    def add_database(self):
        '''
        database : a dict with database base info
        '''
        #db_ip=self.database.get("database_ip")
        db_instance=self.database.get("database_instance")
        db_level=self.database.get("database_level")
        db_name=self.database.get("database_name")
        db_owner=self.database.get("database_owner")
        db_bussiness=self.database.get("database_business")
#get the owner id
        owner_id=1
        db=Database(instance_id=db_instance,name=db_name,business_id=db_bussiness,level=db_level,owner=owner_id)
        db.save()
        return True
    def mod_database(self):
        db_id=self.database.get("database_id")    
        db=Database.objects.get(id=db_id)
        db.ip=self.database.get("database_ip")
        db.port=self.database.get("database_port")
        db.level=self.database.get("database_level")
        db.save()
        return True
    def stat_database(self):
        db_id=self.database.get("database_id")    
        db=Database.objects.get(id=db_id)
        if db.stat==1:
            db.stat=0
        else:
            db.stat=1
        db.save()
        return True
class databaseGet():
    def __init__(self):
        self.db=Database
    def get_database(self,database):
        db_id=database.get("database_id")
        result=self.get_database_by_id(db_id)
        return result
    def get_database_by_id(self,db_id=0):
        if db_id:
            result=self.db.objects.filter(id=db_id).values()[0]
        else:
            result=self.db.objects.all()[0:1].values()[0]
        return result
    
    def get_database_list(self,str_filter,count=10,offset=0):
        result=None
        sql="select d.* ,i.ip,i.port,b.name as business from `databases` d,instance i,business b where d.instance_id=i.id and d.business_id=b.id"
        if str_filter:
            column=str_filter[0]
            value=str_filter[1]
            sql+="and %s=%s"(column,value)
        sql+=" order by stat desc"
        result=self.db.objects.raw(sql)[offset:count]  
        return result       
            
            