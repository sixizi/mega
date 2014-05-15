#coding:utf-8
import sys
from lib.settings import DbConfig
try:
    import MySQLdb
except ImportError:
    sys.exit("Exceptions.ImportError: No module named MySQLdb\n");
class pymysql(object):
    conn   = None
    
    def __init__(self):
        db=DbConfig()
        self.connect(db.db_host, db.db_user, db.db_pwd, db.db_db, db.db_port, db.db_charset)
    def __del__(self):
        self.close()
    def connect(self,db_host,db_user,db_password,db_name,db_port=3306,db_charset='utf8'):
        try:
            
            self.conn = MySQLdb.connect(host=db_host,user=db_user,passwd=db_password,db=db_name,port=db_port,charset=db_charset)
            self.conn.autocommit(True)
            self.__db_host = db_host
            self.__db_user = db_user
            self.__db_password = db_password
            self.__db_name = db_name
            self.__db_port = db_port
            self.__db_charset = db_charset
            return True
        except Exception,ex:
            print ex
            return False


    def reconnect(self):
        try:
            self.conn = MySQLdb.connect(host=self.__db_host,user=self.__db_user,passwd=self.__db_password,db=self.__db_name,port=self.__db_port,charset=self.__db_charset)
            return True
        except:
            return False
    #def quote(self,queryString):
        #return MySQLdb.escape_string(queryString);
    def query(self,sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor
        except Exception, ex:
            if self.reconnect():
                cursor = self.conn.cursor()
                cursor.execute(sql)
                return cursor
            else:
                return False
                sys.exit("MySQL Query Error:\n"+sql+str(ex)+"\n")
    def execute(self,sql):
        try:
            return self.conn.cursor().execute(sql)
        except Exception,ex:
            return False
            sys.exit("MySQL Query Error:\n"+str(ex)+"\n")

    def fetch(self,cursor):
        return cursor.fetchone()

    def fetchRow(self,sql):
        return self.query(sql).fetchone()

    def fetchOne(self,sql):
        try:
            return self.query(sql).fetchone()[0]
        except:
            return None

    def fetchAll(self,sql):
        return self.query(sql).fetchall()

    def insert(self,table,row):
        sqlArr = []
        for key in row.iterkeys():
            sqlArr.append("%s='%s'"%(key,row[key],))
        sql = "insert into "+table +" set "+str.join(",",sqlArr)
        return self.execute(sql)
    
    def update(self,table,row,where):
        sqlArr = []
        for key in row.iterkeys():
            sqlArr.append("%s='%s'"%(key,row[key],))
        sql = "update "+table +" set "+str.join(",",sqlArr)+" where "+where
        return self.execute(sql)

    def close(self):
        if self.conn:
            self.conn.close()