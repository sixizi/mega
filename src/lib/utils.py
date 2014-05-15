import re

def check_ip(ip):
    '''
    check the ip address is correct or not
    '''
    result=False
    if ip:
        ip_match = re.match('((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?$)',ip) 
    if ip_match:
        result=True
    return result
def is_int(value):
    try:
        if not isinstance(int(value),int):
            return False
    except:
        return False