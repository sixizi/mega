from mega_web.entity.models import Instance 
from lib.utils import check_ip,is_int
class InstanceManage():
    def __init__(self,instance):
        '''
        instance : a dict with instance base info
        '''
        self.inst_ip=instance.get("instance_ip")
        self.inst_port=instance.get("instance_port")
        self.inst_level=instance.get("instance_level")
        self.inst_name=instance.get("instance_name")
        self.inst_bussiness=instance.get("instance_bussiness")
        self.msg=''
    def data_check(self):
        if not self.inst_ip or not check_ip(self.inst_ip):
            self.msg+='Invalid IP'
            return False
        if is_int(self.inst_port):
            self.msg+='Invalid PORT'
            return False
        if not self.inst_level:
            self.msg+='Invalid LEVEL'
            return False
        if not self.inst_name:
            self.msg+='Invalid NAME'
            return False
        return True
    def add_instance(self):
        '''
            save new instance
        '''
        if not self.data_check():
            return False,self.msg
        is_exist=InstanceGet().get_instance_by_ip_port(self.inst_ip, self.inst_port)
        if is_exist:
            self.msg+='Instance already exists'
            return False,self.msg
        inst=Instance(server_id=1,ip=self.inst_ip,port=self.inst_port,level=self.inst_level,name=self.inst_name,business_id=self.inst_bussiness)
        inst.save()
        return True,self.msg
    def mod_instance(self):
        inst_id=self.instance.get("instance_id")    
        inst=Instance.objects.get(id=inst_id)
        inst.ip=self.instance.get("instance_ip")
        inst.port=self.instance.get("instance_port")
        inst.level=self.instance.get("instance_level")
        inst.save()
        return True
    def stat_instance(self):
        inst_id=self.instance.get("instance_id")    
        inst=Instance.objects.get(id=inst_id)
        if inst.stat==1:
            inst.stat=0
        else:
            inst.stat=1
        inst.save()
        return True
class InstanceGet():
    def __init__(self):
        self.inst=Instance
    def get_instance(self,instance):
        inst_id=instance.get("instance_id")
        result=self.get_instance_by_id(inst_id)
        return result
    def get_instance_by_id(self,inst_id=0):
        if inst_id:
            result=self.inst.objects.filter(id=inst_id).values()[0]
        else:
            result=self.inst.objects.all()[0:1].values()[0]
        return result
    
    def get_instance_list(self,str_filter,count=10,offset=0):
        result=None
        if str_filter:
            column=str_filter[0]
            value=str_filter[1]
            result=self.inst.objects.filter(column=value)[offset:count]
        else:
            result=self.inst.objects.all().order_by('-stat')[offset:count].values()
        return result       
#unuse    
    def get_instance_by_ip_port(self,ip,port=3306):
        result=None
        result=self.inst.objects.filter(ip=ip,port=port).values("id")
        return result