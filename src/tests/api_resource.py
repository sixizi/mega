import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mega_web.settings")
sys.path.append('..')
from apis.resource import *

def test_getdata():
    model='test'
    data,errno=get_all_instance(model)
    report('All instance list',data,errno)
    data,errno=get_all_server(model)
    report('All server list',data,errno)
    data,errno=get_all_db(model)
    report('All db list',data,errno)
    ip=data[0]["ip"]
    data,errno=get_instance(model,ip,3306)
    report('Instance info',data,errno)
#    print data
    data,errno=get_database(model,ip,3306,'db1')
    report('database info',data,errno)
#    print data
    data,errno=get_server(model,ip)
    report('server info',data,errno)
#    print data
    errno =add_server('1.1.1.1',server_name='test1')
    report('add server','',errno)
    errno =mod_server('1.1.1.1',server_name='test2',server_os='unix')
    report('mod server','',errno)
    errno =del_server('1.1.1.2')
    report('del server','',errno)
    errno =add_instance('2.2.2.2',3307,instance_name='test1')
    report('add instance','',errno)
    
    #for d in data :
        #for e in d :
    #    print d
def report(model,data,errno):
    if errno==0:
        msg='OK'
    else:
        msg='FAILED'
    print model,":",msg #,type(data),':',len(data)
def main():
    test_getdata()
if __name__=="__main__":
    print "Tests for resource: OK|FAILED"
    main()
    