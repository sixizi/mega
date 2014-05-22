from mega_web.resource import instance_manage,server_manage,database_manage
import logging
log = logging.getLogger("api")

ERR_CODE_DEFAULT=None  #INIT CODE :Noenmeaning
ERR_CODE_UNKOWN=-1  #UNKONW ERROR
ERR_CODE_SUCCESS=0   #NO ERROR OCCUR
ERR_CODE_INVALID=2   #INVALID ARGUMENTS

def get_all_instance(model=None,stat=0,count=0,role=None):
    """
        return all instance object as a list of  dicts
    and an error code sign the result, 0 means success
    keys: id,ip,port,server_id,  name  level stat business_id business owner_id owner db_type ha_type online_date
        
    model :the model who do the api calling
    stat:   0 all  (default)  
            1 only the online instance 
            2 only the offline instances
    count: counts of instances for return ,default 0(all)
    role : 1 get the master list
            >1 get the slave list
    """
    err_code=ERR_CODE_DEFAULT
    result=[]
    filter={}
    if stat == 1:
        filter['i.stat']=1
    if stat == 2:
        filter['i.stat']=0
    if role == 1:
        filter['i.role']=1
    if role >1:
        filter['i.role']=2            
    try :
        data=instance_manage.InstanceGet().get_instance_list(filter,count)
        if data:
            for d in data:
                result.append(dict(d.__dict__))
        err_code=ERR_CODE_SUCCESS
        log.info('Get instance list success for %s',model)

    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return result,err_code

def get_all_server(model=None,stat=0,count=0):
    """
    return a list of dicts
    and an error code sign the result, 0 means success
    keys: id,ip,name,os,stat,owner,owner_name,online_date
    model :the model who do the api calling
    stat:   0 all  (default)  
            1 only the online instance 
            2 only the offline instances
    count: counts of instances for return ,default 0(all)

    """
    err_code=ERR_CODE_DEFAULT
    data=None
    result=[]
    filter=None
    if stat==1:
        filter='stat=1'
    if stat==2:
        filter='stat=0'
    try:
        data=server_manage.ServerGet().get_server_list(filter, count)
        if data:
            for d in data:
                result.append(dict(d))
        err_code=ERR_CODE_SUCCESS
        log.info("Get server list sucess for %s",model)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return result,err_code    

def get_all_db(model=None,stat=0,count=0):
    """
    return a list of dicts
    and an error code sign the result, 0 means success
    keys: id,ip,port,name,level,instance_id,business_id,business,owner,owner_nameo,nline_date,stat
    model :the model who do the api calling
    stat:   0 all  (default)  
            1 only the online instance 
            2 only the offline instances
    count: counts of instances for return ,default 0(all)    
    """
    err_code=ERR_CODE_DEFAULT
    result=[]
    try :
        if stat ==1:
            filter='stat=1'
        elif stat==2:
            filter='stat=0'
        else:
            filter=None            
        data=database_manage.DatabaseGet().get_database_list(filter, count)
        if data:
            for d in data:
                result.append(dict(d.__dict__))
        err_code=ERR_CODE_SUCCESS
        log.info('Get server list success for %s',model)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return result,err_code
    
def get_instance(model=None,ip=None,port=3306):
    """
    Return a dict of instance data and an error code 
    keys : id ip port server_id stat name level db_type online_date business_id  owner ha_type 
    model:the model who do the api calling
    ip : instance ip
    port: port(default 3306)
    
    """
    err_code=ERR_CODE_DEFAULT
    inst_id=None
    data=[]
    if not ip :
        err_code=ERR_CODE_INVALID
        return None,err_code
    try:
        inst_id=instance_manage.InstanceGet().get_instance_by_ip_port(ip, port)
        if inst_id:
            data=instance_manage.InstanceGet().get_instance_by_id(inst_id[0]["id"])
            err_code=ERR_CODE_SUCCESS
            log.info("Get instance info success for %s %s:%s",model,ip,port)
        else:
            data=None
            log.error("Failed to get instance info ,instance id not found")
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return data,err_code
    

def get_database(model=None,ip=None,port=3306,db=None):
    """
    Return a dict of database data and an error code
    keys :id name level online_date business_id instance_id owner  stat
    model:the model who do the api calling
    ip : instance ip
    port: port(default 3306)
    db :  name of database
    """
    err_code=ERR_CODE_DEFAULT
    inst_id=None
    data=[]
    if not ip or not db :
        err_code=ERR_CODE_INVALID
        return None,err_code
    try:
        inst_id=instance_manage.InstanceGet().get_instance_by_ip_port(ip, port)
        if inst_id:
            data=database_manage.DatabaseGet().get_database_unique(inst_id[0]["id"], db)
            err_code=ERR_CODE_SUCCESS 
            log.info("Get database info success for %s %s:%s %s",model,ip,port,db)
   
        else:
            data=None
            log.error("Failed to get instance info ,instance id not found")
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return data,err_code
def get_server(model=None,ip=None):
    """
    Return a dict of server data and an error code
    keys : stat name  ip online_date owner os id 
    model:the model who do the api calling
    ip : server ip
    """
    err_code=ERR_CODE_DEFAULT
    data=[]
    if not ip :
        err_code=ERR_CODE_INVALID
        return None,err_code
    try:
        server_id=server_manage.ServerGet().get_server_by_ip(ip)
        if server_id:
            data=server_manage.ServerGet().get_server_by_id(server_id)
            err_code=ERR_CODE_SUCCESS 
            log.info("Get server info success for %s %s",model,ip)
        else: 
            log.error("Get server info failed for %s %s",model,ip)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return data,err_code

def add_server(ip,**args):
    """
    Return an error code for the result of server add. 0 means success
    ip : server ip 
    args: server base info ,if not given ,default value will be used
    keys:server_name,server_online,server_owner,server_os 
    """
    err_code=ERR_CODE_DEFAULT
    if not ip :
        return ERR_CODE_INVALID
    try:        
        if len(args) == 0:
            result,msg=server_manage.ServerManage({"server_ip":ip}).add_server()
        else:
            args["server_ip"]=ip
            result,msg=server_manage.ServerManage(args).add_server()
        if result:
            err_code=ERR_CODE_SUCCESS
            log.info("Server has been added:%s",ip)
        else:
            err_code=ERR_CODE_UNKOWN
            log.error("Server added failed:%s %s",ip,msg)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return err_code
def mod_server(ip,**args):
    """
    Return an error code for the result of server modify. 0 means success
    ip : server ip 
    args: server base info ,
    keys:server_name,server_online,server_owner,server_os 
    """
    err_code=ERR_CODE_DEFAULT
    if not ip:
        return ERR_CODE_INVALID
    try:
        if len(args)==0:
            return ERR_CODE_INVALID
        else:
            args["server_ip"]=ip
            result,msg=server_manage.ServerManage(args).mod_server()
        if result:
            err_code=ERR_CODE_SUCCESS
            log.info("Server modified success:%s",ip)
        else:
            err_code=ERR_CODE_UNKOWN
            log.error("Server modified failed:%s %s",ip,msg)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return err_code
        
def del_server(ip):
    """
    Return an error code for the result of server del. 0 means success
    ip : server ip 
    """
    err_code=ERR_CODE_DEFAULT
    if not ip:
        return ERR_CODE_INVALID
    try:
        result,msg=server_manage.ServerManage({"server_ip":ip}).stat_server()
        if result:
            err_code=ERR_CODE_SUCCESS
            log.info("Server has been deleted:%s",ip)
        else:
            err_code=ERR_CODE_UNKOWN
            log.error("Server deleted failed:%s %s",ip,msg)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return err_code        
    
def add_instance(ip,port,**args):
    """
    Return an error code for the result of instance add. 0 means success
    ip: instance ip 
    port: instance port
    args:instance_level  instance_name  instance_bussiness instance_online instance_owner instance_dbtype instance_hatype
    
    If the server does not exists ,a new server will be add automatic

    """
    err_code=ERR_CODE_DEFAULT
    if not (ip or port):
        return ERR_CODE_INVALID
    try:
        if len(args) == 0:
            result,msg=instance_manage.InstanceManage({"instance_ip":ip,"instance_port":port}).add_instance()
        else:
            args["instance_ip"]=ip
            args["instance_port"]=port
            result,msg=instance_manage.InstanceManage(args).add_instance()
        if result:
            err_code=ERR_CODE_SUCCESS
            log.info("Instance has been added: %s:%s ",ip,port)
        else:
            err_code=ERR_CODE_UNKOWN
            log.error("Instance added failed: %s:%s %s",ip,port,msg)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return err_code
            
def mod_instance(ip,port,**args):
    """
    Return an error code for the result of server modify. 0 means success
    ip: instance ip 
    port: instance port
    args:instance_level  instance_name  instance_bussiness instance_online instance_owner instance_dbtype instance_hatype
    """
    err_code=ERR_CODE_DEFAULT
    if not (ip or port):
        return ERR_CODE_INVALID
    try:
        if len(args)==0:
            return ERR_CODE_INVALID
        args["instance_ip"]=ip
        args["instance_port"]=port
        result,msg=instance_manage.InstanceManage(args).mod_instance()
        if result:
            err_code=ERR_CODE_SUCCESS
            log.info("Instance modified success:%s %s",ip,port)
        else:
            err_code=ERR_CODE_UNKOWN
            log.error("Instance modified failed: %s:%s %s",ip,port,msg)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return err_code

    
def del_instance(ip,port):
    """
    Return an error code for the result of instance del. 0 means success
    ip : server ip 
    port : instance port
    """
    err_code=ERR_CODE_DEFAULT
    if not (ip or port):
        return ERR_CODE_INVALID
    try:
        result,msg=instance_manage.InstanceManage({"instance_ip":ip,"instance_port":port}).stat_instance(True)
        if result:
            err_code=ERR_CODE_SUCCESS
            log.info("Instance has been deleted:%s:%s",ip,port)
        else:
            err_code=ERR_CODE_UNKOWN
            log.error("Instance deleted failed:%s:%s %s",ip,port,msg)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return err_code        
    
def add_database(ip,port,db,**args):
    """  
    Return an error code for the result of instance add. 0 means success
    ip : server ip 
    db: db name
    port: instance port
    args: server base info ,if not given ,default value will be used
    keys:database_ip database_port database_name database_level database_owner database_business database_online

    if the instance does not exists ,a new instance will be add automatic
    """
    err_code=ERR_CODE_DEFAULT
    if not (db or ip or port) :
        return ERR_CODE_INVALID
    try:
        if len(args)==0:
            result,msg=database_manage.DatabaseManage({"database_name":db,"database_ip":ip,"database_port":port}).add_database()
        else:
            args["database_name"]=db
            args["database_ip"]=ip
            args["database_port"]=port
            result,msg=database_manage.DatabaseManage(args).add_database()
        if result:
            err_code=ERR_CODE_SUCCESS
            log.info("Database has been added:%s",ip)
        else:
            err_code=ERR_CODE_UNKOWN
            log.error("Database added failed:%s %s",ip,msg)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return err_code
    
            
def mod_database(ip,port,db,**args):
    """
    Return an error code for the result of database modify. 0 means success
    ip : server ip 
    db: db name
    port: instance port
    args: database base info ,if not given ,default value will be used
        keys:database_ip database_port database_name database_level database_owner database_business database_online
    """
    err_code=ERR_CODE_DEFAULT
    if not (ip or db or port):
        return ERR_CODE_INVALID
    try:
        if len(args)==0:
            return ERR_CODE_INVALID
        else:
            args["database_ip"]=ip
            args["database_name"]=db
            args["database_port"]=port
            result,msg=database_manage.DatabaseManage(args).mod_database()
        if result:
            err_code=ERR_CODE_SUCCESS
            log.info("Database modified success:%s",ip)
        else:
            err_code=ERR_CODE_UNKOWN
            log.error("Database modified failed:%s %s",ip,msg)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return err_code
def del_database(ip,port,db):
    """
    Return an error code for the result of database del. 0 means success
    ip : server ip 
    port : instance port
    db: db name
    """
    err_code=ERR_CODE_DEFAULT
    if not (ip or port or db):
        return ERR_CODE_INVALID
    try:
        result,msg=database_manage.DatabaseManage({"database_ip":ip,"database_port":port,"database_name":db}).stat_database(True)
        if result:
            err_code=ERR_CODE_SUCCESS
            log.info("Database has been deleted:%s:%s %s",ip,port,db)
        else:
            err_code=ERR_CODE_UNKOWN
            log.error("Database deleted failed:%s:%s %s %s",ip,port,db,msg)
    except Exception as ex:
        err_code=ERR_CODE_UNKOWN
        log.error(ex)
    return err_code        
    
    