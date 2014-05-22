#API 

##通用API

##资源池API
*	def get_all_instance(model=None,stat=0,count=0):
    
    return all instance object as a list of  dicts and an error code sign the result, 0 means success
    
    keys:
    	
    	id ip port server_id name  level stat business_id business owner_id owner db_type ha_type online_date
    
        
    model :the model who do the api calling
    
    stat:   
    
    		0 all  (default) 
            1 only the online instance 
            2 only the offline instances
 
    count: counts of instances for return ,default 0(all)
    
* def get_all_server(model=None,stat=0,count=0):
 
    return a list of dicts and an error code sign the result, 0 means success
    
    keys: 
    	
    	id,ip,name,os,stat,owner,owner_name,online_date
    
    model :the model who do the api calling
    
    stat: 
    	
    		0 all  (default)  
            1 only the online instance 
            2 only the offline instances
    
    
    count: counts of instances for return ,default 0(all)

* def get_all_db(model=None,stat=0,count=0):
  
    return a list of dicts and an error code sign the result, 0 means success
  
    keys: 
    
		id,ip,port,name,level,instance_id,business_id,business,owner,owner_nameo,nline_date,stat
     
    model :the model who do the api calling
  
    stat: 
    		
    		0 all  (default)  
            1 only the online instance 
            2 only the offline instances

    count: counts of instances for return ,default 0(all)    
* def get_instance(model=None,ip=None,port=3306):
  
    Return a dict of instance data and an error code 
  
    keys : 
    	
    	id ip port server_id stat name level db_type online_date business_id  owner ha_type
  
	model:the model who do the api calling
  
    ip : instance ip
  
    port: port(default 3306)
 
* def get_database(model=None,ip=None,port=3306,db=None):

    Return a dict of database data and an error code

    keys :
    
	    id name level online_date business_id instance_id owner  stat

    model:the model who do the api calling

    ip : instance ip

    port: port(default 3306)

    db :  name of database

* def get_server(model=None,ip=None):
  
    Return a dict of server data and an error code
  
    keys :
    
    	stat name  ip online_date owner os id
  
    model:the model who do the api calling
  
    ip : server ip

* def add_server(ip,**args):
  
    Return an error code for the result of server add. 0 means success
  
    ip : server ip 
  
    args: server base info ,if not given ,default value will be used
  
    keys:server_name,server_online,server_owner,server_os 
* def mod_server(ip,**args):
  
    Return an error code for the result of server modify. 0 means success
  
    ip : server ip 
  
    args: server base info 
  
    keys:
    	
    	server_name,server_online,server_owner,server_os 
 
* def del_server(ip):

    Return an error code for the result of server del. 0 means success

    ip : server ip 
 
* def add_instance(ip,port,**args):
  
    Return an error code for the result of instance add. 0 means success
  
    ip: instance ip 
  
    port: instance port
  
    args:
    	
    	instance_level  instance_name  instance_bussiness instance_online instance_owner instance_dbtype instance_hatype
    
    If the server does not exists ,a new server will be add automatic
* def mod_instance(ip,port,**args):

	Return an error code for the result of server modify. 0 means success

    ip: instance ip 

    port: instance port

    args:
    	
    	instance_level  instance_name  instance_bussiness instance_online instance_owner instance_dbtype instance_hatype
* def del_instance(ip,port):
  
    Return an error code for the result of instance del. 0 means success
  
    ip : server ip 
  
    port : instance port
* def add_database(db,ip,port,**args):
 
    Return an error code for the result of instance add. 0 means success
 
    ip : server ip 
 
    db: db name
 
    port: instance port
 
    args: server base info ,if not given ,default value will be used

    keys:
    
    	database_ip database_port database_name database_level database_owner database_business database_online

    if the instance does not exists ,a new instance will be add automatic
* def mod_database(ip,port,db,**args):
  
    Return an error code for the result of database modify. 0 means success
  
    ip : server ip 
  
    db: db name
  
    port: instance port
  
    args: database base info ,if not given ,default value will be used
    
    keys:
    
    	database_ip database_port database_name database_level database_owner database_business database_online
   
* def del_database(ip,port,db):

    Return an error code for the result of database del. 0 means success

    ip : server ip 

    port : instance port

    db: db name
