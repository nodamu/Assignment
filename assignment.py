# Osei Bonsu Samuel 5927616
# Adamu Nicholas Osafo 5916916
# 


import numpy as np

lines = input("Enter the number of buses: ")
num_line = int(lines)

start = 1 # We start from bus 1
mat = np.zeros(shape=(num_line,num_line),dtype = np.complex_) # Initialize matrix with zeros
hold = [] #Temporary list to hold row values
sum = 0 # variable to sum row values to produce diagonal values

for i in range(0,num_line):
    for j in range(0,num_line+1):
        if start != j:
            R_val  = input("Enter R_val for {}-{} ".format(start,j)) #Takes in R values
            X_val = input("Enter X_val for {}-{} ".format(start,j)) #Takes in X values
            R = format(float(R_val),'0.2f')  #Set R values to 2 decimal places
            X = format(float(X_val),'0.2f') # Set x VALUES TO 2 DEC PLACES
            if float(R) != 0 or float(X) !=0 :  
                Y = 1 / np.complex(float(R),float(X)) 
                hold.append(Y) #holds row values to later compute diagonals
            else: # To prevent division by zero 
                Y = 0 
                hold.append(Y)
            if j != 0: #To prevent grounds from appearing in  the matrix
                mat[start-1,j-1] = -Y
    for element in hold:
        sum += element # sum row components
    mat[start-1,start-1] = sum
    hold = [] # Reset variable
    sum = 0 # Reset variable
    start +=1 # Add one 


print(mat)  