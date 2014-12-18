# -*- coding: utf-8 -*-
import libs.db.db_json as db_json
import time
import datetime


class Presets(db_json.Db):
    
    def __init__(self, filename, data_restore = {}):                
        
        #json file isntance        
        self.db = db_json.Db(filename, data_restore)
                            
    
    def GetPreset(self, presetname):
        try:
            preset = self.db.load()[presetname]
        except KeyError:
            preset = None
        return preset


from ewitis.data.DEF_PRESETS import DEF_PRESETS
print "I: Presets init"
presets = Presets('conf/presets.json', DEF_PRESETS)

#test
if __name__ == "__main__":    
    mypresets = Presets('conf/presets.json', DEF_PRESETS)
    print mypresets.GetPreset("blizak")                        