from mega_web.entity.models import Business,User
from conf.GlobalConf import *
class BusinessManage():
    def __init__(self,business):
        self.busi_name=business.get("business_name")
        self.busi_owner=business.get("business_owner")
        self.busi_phone=business.get("business_phone")
        self.busi_id=business.get("business_id")
        self.msg=''
    def data_check(self):
        if not self.busi_name:
            self.msg+=MSG_ERR_NAME
            return False
        if not self.busi_owner:
            #self.busi_owner=DEFAULT_BUSI_OWNER
            self.busi_owner=1
        if not self.busi_phone:
            self.busi_phone=0
        return True
    def add_business(self):
        if not self.data_check():
            return False,self.msg
        is_exist=BusinessGet().get_business_by_name(self.busi_name)
        if is_exist:
            self.msg+=MSG_ERR_BUSINESS_EXITST
        busi=Business(name=self.busi_name,owner=self.busi_owner,phone=self.busi_phone)
        busi.save()
        self.msg='success'
        return True,self.msg
    def mod_business(self):
        busi=Business.objects.get(id=self.busi_id)
        busi.name=self.busi_name
        busi.owner=self.busi_owner
        busi.phone=self.busi_phone
        busi.save()
        return True
    def stat_business(self):
        busi=Business.objects.get(id=self.busi_id)
        if busi.stat==STAT_ONLINE:
            busi.stat=STAT_OFFLINE
        else:
            busi.stat=STAT_ONLINE
        busi.save()    

class BusinessGet(): 
    def __init__(self):
        self.busi=Business
    def get_business(self,business):
        busi_id=business.get("business_id")
        result=self.get_business_by_id(busi_id)
        owner=User.objects.filter(id=result['owner']).values('name')[0]
        result["owner_name"]=owner['name']
        return result
    def get_business_by_id(self,busi_id=0):
        if busi_id:
            result=self.busi.objects.filter(id=busi_id).values()[0]
        else:
            result=self.busi.objects.all()[0:1].values()[0]
        return result
    def get_business_by_name(self,name=''):
        if name:
            result=self.busi.objects.filter(name=name).values("id")
        else:
            result=''
        return result
    
    def get_business_list(self,str_filter,count=10,offset=0):
        result=None
        if str_filter:
            column=str_filter[0]
            value=str_filter[1]
            result=self.busi.objects.filter(column=value)[offset:count]
        else:
            result=self.busi.objects.all().order_by('-stat')[offset:count].values()
        for r in result:
            owner=User.objects.filter(id=r['owner']).values('name')[0]
            r['owner_name']=owner['name']
        return result        
            