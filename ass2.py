import numpy as np 

bus = input('Enter the number of buses in the system: ')
lines = input('Enter the number of lines the system has: ')

num_bus = int(bus)
num_lines = int(lines)

v_initial = np.zeros((num_bus),dtype=np.complex)

for k in range(1,num_bus):
    if k != 1:
        print('For bus:{}'.format(k))
        v_init = input('What is the initial voltage of the bus? ')
        v_initial[k-1] = np.complex(v_init)
    else:
        v_init = input('\n What is the slack bus voltage in rectangular form? ')
        v_initial[k-1] = np.complex(v_init)
p_gen = np.zeros((num_bus),dtype= np.complex)
for g in range(1,num_bus):
    if g!=1:
        print('For bus: {}'.format(g))
        p_gen_init = input('\nWhat is the power generated at this bus? ')
        p_gen[g-1] = np.complex(p_gen_init)
    else:
        p_gen[g-1] = 0


# Take the power demand on each generator bus
p_load = np.zeros((num_bus),dtype=np.complex)
for l in range(1,num_bus):
    print('For bus:{}'.format(l))
    p_load_init = input('\nWhat is the load demand at this bus? ')
    p_load[l-1] = np.complex(p_load_init)

p_injected = np.zeros((num_bus),dtype= np.complex)
for m in range(1,num_bus):
    p_injected[m-1] = p_gen[m-1] - p_load[m-1]

Y = np.zeros((num_bus,num_bus),dtype= np.complex)
# The sending and ending bus numbers are requested for as well as the
# impedance using a for loop. In the if statement, once the sending bus is
# not equal to the ending bus, the admittance is negated.

for k in range(1,num_lines):
    SB = input('Enter the sending bus number: ')
    EB = input('Enter the ending bus number: ')
    y_init = input('Enter the admittance of the line: ')
    y = np.complex(y_init)
    if int(SB) != int(EB):
        Y[int(SB),int(EB)] = -y
        Y[int(EB),int(SB)] = Y[int(SB),int(EB)]
    
    print('\n')
# Add all the row y elements and store the in position (y,y) of the matrix 
for y in range(1,num_bus):
    for i in range(1,num_bus):
        if y != i:
            Y[y,y] = Y[y,y] + Y[y,i]
    
    Y[y,y] = -Y[y,y]

# Gauss Seidal Algorithm
V_cal = np.zeros((num_bus),dtype=np.complex)
V_initials = np.zeros((num_bus),dtype=np.complex)
for t in range(1,num_bus):
    V_initials[t] = v_initial[t]

for q in range(1,num_bus):
    Z = 0
    if q != 1:
        for i in range(1,num_bus):
            if i != q:
                Z = Z + (Y[q,i] * v_initial[i])

        V_cal[q] = (1/Y[q,q]) * (np.conj(p_injected[q])/np.conj(v_initial[q]) - Z)
        v_initial[q] = V_cal[q]
    else:
        V_cal[q] = v_initial[q]


V_diff = np.zeros((num_bus),dtype = np.complex)
for f in range(2,num_bus):
    V_diff = np.abs(V_cal - V_initials)

for d in range(2,num_bus):
    V_initials[d] = V_cal[d]

for x in range(2,num_bus):
    while np.real(V_diff[x]) >=0.01 or np.imag(V_diff[x]) >=0.01:
        for b in range(2,num_bus):
            V_initials[d] = V_cal[d]
        for q in range(1,num_bus):
            Z = 0
            if q != 1 :
                for i in range(1,num_bus):
                    if i != q:
                        Z = Z + (Y[q,i] * v_initial[i])

                V_cal[q] = (1/Y[q,q]) * (np.conj(p_injected[q])/np.conj(v_initial[q]) - Z)
                v_initial[q] = V_cal[q]
            else:
                V_cal[q] = v_initial[q]