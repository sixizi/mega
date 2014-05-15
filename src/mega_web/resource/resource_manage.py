from mega_web.entity.models import  Server,Instance,Database,Business
def get_total_count():
    count={}
    count['server']=Server.objects.filter(stat__gt=0).count()
    count['instance']=Instance.objects.filter(stat__gt=0).count()
    count['database']=Database.objects.filter(stat__gt=0).count()
    count['business']=Business.objects.filter(stat__gt=0).count()
    return count
