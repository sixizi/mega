from mega_web.entity.models import Business
class BusinessManage():
    def __init__(self,business):
        self.busi=business
    def add_business(self):
        busi_name=self.busi.get("business_name")
        busi_owner=self.busi.get("business_owner")
        busi_phone=self.busi.get("business_phone")
        busi=Business(name=busi_name,owner=busi_owner,phone=busi_phone)
        busi.save()
        return True
    def mod_business(self):
        busi_id=self.busi.get("business_id")
        busi=Business.objects.get(id=busi_id)
        busi.name=self.busi.get("business_name")
        busi.owner=self.busi.get("business_owner")
        busi.phone=self.busi.get("business_phone")
        busi.save()
        return True
    def stat_business(self):
        pass
    


class BusinessGet(): 
    def __init__(self):
        self.busi=Business
    def get_business(self,business):
        busi_id=business.get("business_id")
        result=self.get_business_by_id(busi_id)
        return result
    def get_business_by_id(self,busi_id=0):
        if busi_id:
            result=self.busi.objects.filter(id=busi_id).values()[0]
        else:
            result=self.busi.objects.all()[0:1].values()[0]
        return result
    
    def get_business_list(self,str_filter,count=10,offset=0):
        result=None
        if str_filter:
            column=str_filter[0]
            value=str_filter[1]
            result=self.busi.objects.filter(column=value)[offset:count]
        else:
            result=self.busi.objects.all().order_by('-stat')[offset:count].values()
        return result        
            