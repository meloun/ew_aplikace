'''cconvert integer(time in ms) to string (HH:MM:SS:mSmS)'''
def time_to_string(time):
    hours = time / (100*60*60)
    
    time = time % (100*60*60)
    minutes = time / (100*60)
    
    time = time % (100*60)
    seconds = time / (100)
    
    milliseconds = time % (100)
    
    return '%02d:%02d:%02d,%02d' %(hours, minutes, seconds, milliseconds)