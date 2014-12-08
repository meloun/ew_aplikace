import sqlite3
import threading
import random
import string
import os

DB = "tmp/test_db.db"

if not os.path.exists(DB):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    #c.execute("""create table test ( foo int)""")
    conn.close()


def work(name):
    conn = sqlite3.connect(DB, 15)
    c = conn.cursor()    
    j = 0
    errors = 0
    succesful = 0
    while True:    
        attempt = 1
        if random.random() > .5:
            #v = random.randint(0, 10000)
            while True:
                #print name,": insert into test values (?, ?)", (j,name)
                try:
                    c.execute("insert into test values (?, ?)", (j,name))
                    succesful = succesful + 1
                    if attempt != 1:
                        print "%i. attempt succesfull" % (attempt), name,": insert into test values (?, ?)", (j,name)
                    break
                except:
                    errors = errors + 1
                    attempt = attempt + 1 
                    print "E: %s %i/%i" % (name, errors, succesful), ": insert into test values (?, ?)", (j,name)                    
            j = j + 1
        else:
            c.execute("select count(*) from test")
            #print name,": select count(*) from test"        
        conn.commit()


threads = []

for i in xrange(10):
    thread_name = "#"+str(i)+"#"
    t = threading.Thread(target = lambda:work(thread_name))
    t.setDaemon(True)
    t.start()
    threads.append(t)
    print "zakladam:",i 

while True:
    pass