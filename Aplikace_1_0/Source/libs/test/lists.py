'''
Created on 14.4.2013

@author: Meloun
'''

array = [{"a":2, "b":3},{"a":3, "b":4},{"a":5, "b":6}]
list1 = [1,2]
list2 = [1,2]

print list1.items() + list2.items()


list1[1] = 5
(x,y) = list1
print "x",x 
print "y",y 
print type((x,y)), type(list)

a = 3
b = 2

print a - b    
print b - a    
#for index in range(len(array)):
#    print index, array[index], len(array)
#    array.remove(array[index])
     
    
#print enumerate(array)
#for index, item in enumerate(array):
#    print index, item
#    print index, array[index]
#    
#   
#    
#questions = ['name', 'quest', 'favorite color']
#answers = ['lancelot', 'the holy grail', 'blue']
#print zip(questions, answers)
#for q, a in zip(questions, answers):
#    print 'What- is your {0}?  It is {1}.'.format(q, a)   