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