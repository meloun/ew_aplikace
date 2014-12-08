# -*- coding: utf-8 -*-
'''
Created on 16.7.2012

@author: Meloun
'''

#za 1/100s - 1bod. Maximum 500bodu.
def Points_eval(rule, order, time, min = 0, max = 999):
        points = 0

        #rule
        rule = rule.lower()
        
        #make expression
        expression_string = rule.replace("%o%", str(order))
        expression_string = expression_string.replace("%tms%", str(time))       
        
        #evaluate
        try:
            points = eval(expression_string)        
        except SyntaxError:
            print "E: invalid string for evaluation", expression_string

        #restrict
        
        
        if points < min:
            points = min
        if points > max:
            points = max
            
         
                        
        return points


if __name__ == "__main__": 
    rule = "abs(%Tms% - 90000)"
        
    for i in range(1,25):
        print i, Points_eval(rule, i, i, 0, 500000)
