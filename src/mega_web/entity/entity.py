from django.db import models

class Server(models.Model):
    class Meta(object):
        db_table='server'
      
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    online_date = models.DateTimeField(default=0)
    stat= models.IntegerField(default=1)

class Instance(models.Model):
    class Meta(object):
        db_table='instance'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50) 
    server_id =  models.IntegerField(null=False)
    ip = models.CharField(max_length=20)    
    port = models.IntegerField(null=False)
    owner =  models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    business_id = models.IntegerField(default=0)
    #mysql oracle etc
    db_type = models.CharField(max_length=10)
    #none mha mmm keepalived
    ha_type = models.CharField(max_length=10)
    #1 master >1 slave
    role= models.IntegerField(default=1)
    
    stat= models.IntegerField(default=1)
    online_date = models.DateTimeField(default=0)


class Database(models.Model):
    class Meta(object):
        db_table='databases'
    
    id = models.AutoField(primary_key=True)
    instance_id = models.IntegerField(null=False)
    name = models.CharField(max_length=16)
    business_id = models.IntegerField()
    level = models.IntegerField()
    owner = models.IntegerField()
    stat= models.IntegerField(default=1)
    online_date = models.DateTimeField(default=0)


class User(models.Model):
    class Meta(object):
        db_table='user'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32) 
    #dba op diaosi
    role = models.IntegerField()
    sign = models.IntegerField()
    pwd =  models.CharField(max_length=10)
    p_id = models.IntegerField()
    phone = models.IntegerField()
    stat= models.IntegerField(default=1)
    
class Business(models.Model):
    class Meta(object):
        db_table='business'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16) 
    owner = models.IntegerField()
    phone = models.IntegerField()
    stat= models.IntegerField(default=1)

    
    