import logging
class Logger:
    def __init__(self,level=3):
        self.level=3
    def log(self,model,msg,type):
        """write logs for all info and types as
            0 : debug   1:error   2:warning  3:info """
        LEVELS = {0: logging.DEBUG,
                  3: logging.INFO,
                  2: logging.WARNING,
                  1: logging.ERROR}
        level=LEVELS.get(type,logging.NOTSET)   
        logging.basicConfig(level=level,
                            filename='/tmp/mysql_manage.log',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)s %(name)-12s %(levelname)-5s %(message)s')
        logger=logging.getLogger(model)
        if type==0:
            logger.debug(msg)
        elif type==1:
            logger.error(msg)
        elif type==2:
            logger.warning(msg)
        elif type==3:
            logger.info(msg)
        else:
            logger.info(msg)
if __name__=="__main__":
    log=Logger()
    log.log("model", "msg", 1)
