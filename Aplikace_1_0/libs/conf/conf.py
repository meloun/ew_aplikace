#===========================================================================
# LOAD USER CONFIGURATION
#===========================================================================

import libs.db.db_json as db_json

def load(filename, default_conf):
    try:
        db = db_json.Db(filename)
        USER_CONF = db.load_from_file()
        print 'I: Load user configuration.. ' + str(USER_CONF)
    except:        
        USER_CONF = default_conf
        print 'W: Cannot load user configuration, set default..'  + str(USER_CONF)
    return USER_CONF 


if __name__ == "__main__": 
    
    USER_CONF = load('ewitis.conf', {"port": "COM8", "baudrate": 38400})
    print USER_CONF['port']