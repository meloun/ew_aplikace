"""
multi_pipe.py
"""
from multiprocessing import Process, Pipe
import time

def reader(pipe):
    output_p, input_p = pipe
    input_p.close()    # We are only reading
    while True:
        try:
            msg = output_p.recv()    # Read from the output pipe and do nothing
        except EOFError:
            break
        time.sleep(0.0001)

def writer(count, input_p):
    print "writer"
    for ii in xrange(0, count):
        input_p.send(1)             # Write 'count' numbers into the input pipe

if __name__=='__main__':
    for count in [10**3, 10**4]:
        print "AA"
        output_p, input_p = Pipe()
        #reader_p = Process(target=reader, args=((output_p, input_p),))
        #reader_p.start()     # Launch the reader process

        _start = time.time()
        print "A"
        for ii in xrange(0, 10000):
            input_p.send(1)             # Write 'count' numbers into the input pipe
        print "C"

        
        output_p.close()       # We no longer need this part of the Pipe()
        input_p.close()        # Ask the reader to stop when it reads EOF
        #reader_p.join()
        print "Sending %s numbers to Pipe() took %s seconds" % (count, (time.time() - _start))
        
        
        