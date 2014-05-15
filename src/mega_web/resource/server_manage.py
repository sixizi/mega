from mega_web.entity.models import Server
class ServerManage():
    def __init__(self,server):
        self.server=server
    def add_server(self):
        '''
        server  a dict with server base info 
        '''
        server_ip=self.server.get("server_ip")
        server_name=self.server.get("server_name")
        server_online=self.server.get("server_online")
        server_owner=self.server.get("server_owner")
        server_os=self.server.get("server_os")
        server=Server(ip=server_ip,name=server_name,online_date=server_online,owner=server_owner,os=server_os)
        server.save()
        return True    
    def mod_server(self):
        server_id=self.server.get("server_id")
        server=Server.objects.get(id=server_id)
        server.name=self.server.get("server_name")
        server.ip=self.server.get("server_ip")
        server.os=self.server.get("server_os")
        server.owner=self.server.get("server_owner")
        server.online_date=self.server.get("server_online")
        server.save()
        return True   
    def stat_server(self):
        server_id=self.server.get("server_id")
        server=Server.objects.get(id=server_id)
        if server.stat== 0:
            server.stat=1
        else:
            server.stat=0
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
        result['online_date']=result["online_date"].strftime("%Y-%m-%d %H:%M:%S")   
        return result
    
    def get_server_list(self,str_filter,count=10,offset=0):
        result=None
        if str_filter:
            column=str_filter[0]
            value=str_filter[1]
            result=self.server.objects.filter(column=value)[offset:count]
        else:
            result=self.server.objects.all().order_by('-stat')[offset:count].values()
        return result       