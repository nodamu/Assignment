import numpy as np

num_of_buses = input('How many buses? ')
num_of_lines = input('How many lines? ')
num_of_buses = int(num_of_buses)
num_of_lines = int(num_of_lines)

dt = np.dtype(np.complex)
initial_volts = np.zeros((num_of_buses, num_of_buses), dtype=np.complex)

for i in range(num_of_buses):
    if i != 0:
        I = i+1
        initial_volts[i] = float(
            input('what is the initial voltage for bus {}? \t) '.format(str(I))))
    else:
        initial_volts[i] = float(
            input('what is the slack bus voltage? (the voltage for bus {}) '.format(str(I))))

# taking the actual powers

gen_power_P = np.zeros((num_of_buses, num_of_buses), dtype=np.complex)
for p in range(num_of_buses):
    if p != 0:
        P = p+1
        gen_power_P[p] = float(input(
            'what is the power (P) generated at bus {}? '.format(str(P))))
    else:
        gen_power_P[p] = 0

gen_power_Q = np.zeros((num_of_buses, num_of_buses), dtype=np.complex)
for q in range(num_of_buses):
    if q != 0:
        Q = q+1
        gen_power_Q[q] = float(input(
            'what is the power (Q) generated at bus {}? '.format(str(Q))))
    else:
        gen_power_Q[q] = 0

injected_power = np.zeros((num_of_buses, num_of_buses), dtype=np.complex)
for g in range(num_of_buses):
    injected_power[p] = gen_power_P[g]+gen_power_Q[g]

print('\n')
print("Details for Admittance matrix")
Y = np.zeros((num_of_buses, num_of_buses), dtype=np.complex)
for i in range(num_of_lines):
    sending_bus = input('input the sending bus number ')
    ending_bus = input('what is the ending bus number? ')
    y = input('what is the admitance in complex numbers? ')

    sending_bus = float(sending_bus) - 1
    ending_bus = float(ending_bus) - 1
    y = complex(y)

    if sending_bus != ending_bus:
        Y[sending_bus][ending_bus] = -y
        Y[ending_bus][sending_bus] = Y[sending_bus][ending_bus]

for a in range(num_of_buses):
    for b in range(num_of_buses):
        if a != b:
            Y[a, a] = np.add(Y[a, a], Y[a, b])
    Y[a, a] = -Y[a, a]


# Gauss Seidal
calc_volt = np.zeros((num_of_buses, num_of_buses), dtype=np.complex)
new_volt = np.zeros((num_of_buses, num_of_buses), dtype=np.complex)
for a in range(num_of_buses):
    new_volt[a] = initial_volts[a]
for b in range(num_of_buses):
    z = 0
    if b != 0:
        for c in range(num_of_buses):
            if c != b:
                z = z + (Y[b][c]) * initial_volts[c]

    calc_volt[b] = (1 / (Y[b][b])) * \
        (((gen_power_P[b]-gen_power_Q[b])/initial_volts[c])-z)
    initial_volts[b] = calc_volt[b]
    else:
        calc_volt[b] = initial_volts[b]

print(calc_volt)

volt_differences = np.zeros((num_of_buses, num_of_buses), dtype=np.complex)

for v in range(num_of_buses):
    volt_differences = abs(calc_volt-initial_volts)
for d in range(num_of_buses):
    initial_volts[d] = calc_volt[d]
for n in range(num_of_buses):
    while realpart(volt_differences[n]) or imaginary(volt_differences[n]) >= 0.001:
        for m in range(num_of_buses):
            volt_differences[n] = abs(calc_volt[n]) - initial_volts[n]
        for o in range(num_of_buses):
            initial_volts[o] = calc_volt[o]
        for p in range(num_of_buses):
            z = 0
            if p != 0:
                for q in range(num_of_buses):
                    if q != p:
                        z = z + ((Y[p][q]) * (initial_volts[q]))
                calc_volt[p] = (
                    1/Y[p][p]) * (((gen_power_P[p]-gen_power_Q[p])/initial_volts[p])-z)
                initial_volts[p] = calc_volt[p]
            else:
                calc_volt[p] = initial_volts[p]
print(calc_volt)
