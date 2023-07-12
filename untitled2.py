# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 12:06:09 2021

@author: totsky
"""
import numpy as np
i=0
X_len=6000
Y_len=6000
X_grid = 6
Y_grid = 6
X_stp = (X_len/(X_grid))                      
Y_stp = (Y_len/(Y_grid))

#arr=[]
#arr=[[[0,0]]*X_grid]*Y_grid

arr=[[[0, 0]] * X_grid for i in range(Y_grid)]

#for line in range(Y_grid):     
 #   for cols in range(X_grid):
  #      arr.append([0,0])


print(arr)
print()
print()
print()   
  #  for y in range(0,Y_grid):     
   #    for x in range(0,X_grid):
#       print (int((x*X_stp)+ (X_stp/2)),int((y*Y_stp)+( Y_stp/2)))    
 #      arr[x][y]=[int((x*X_stp)+ (X_stp/2)),int((y*Y_stp)+( Y_stp/2))]
  
   
for y in range(Y_grid):     
    for x in range(X_grid):
        
        a= int((x*X_stp)+(X_stp/2))
        b =int((y*Y_stp)+(Y_stp/2))
        arr[x][y] = [a,b]
print (arr)

for x in range(1,X_grid,2): 
    arr[x]=arr[x][::-1]
     
#arr=list(zip(*arr[::-1]))

print("________________________")
print (arr)
arr = np.rot90(arr, 1)

print("________________________")
print (arr)
