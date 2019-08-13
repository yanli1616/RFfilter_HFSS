import math

def coth(x):
    return (math.exp(x)+math.exp(-x))/(math.exp(x)-math.exp(-x))

response='Bandstop'
filter_type='Chebyshev'
topology='Shunt First'
order=5             #must be odd if out_impedance is 50 Ohm
cutoff_freq=2e9     #Hz
imput_impedance=50  #Ohm
out_impedance=50    #Ohm
ripple=0.01            #dB

g=[]
beta=math.log(coth(ripple/17.37))
gamma=math.sinh(beta/(2*order))
g.append(2*math.sin(math.pi/(2*order))/gamma)

for i in range(1,order):
    g.append(4*math.sin((2*i+1)*math.pi/(2*order))*math.sin((2*i-1)*math.pi/(2*order))/(g[i-1]*(gamma**2+math.sin(i*math.pi/order)**2)))
print(g)
if response=='Lowpass':
    if topology == 'Shunt First':
        for i in range(0, order):
            if (i % 2) == 0:
                g[i] = g[i] / (50 * 2 * math.pi * cutoff_freq)
            else:
                g[i] = g[i] * 50 / (2 * math.pi * cutoff_freq)
    elif topology == 'Series First':
        for i in range(0, order):
            if (i % 2) == 1:
                g[i] = g[i] / (50 * 2 * math.pi * cutoff_freq)
            else:
                g[i] = g[i] * 50 / (2 * math.pi * cutoff_freq)
    print(g)
elif response=='Highpass':
    if topology=='Shunt First':
        for i in range(0,order):
            if (i%2)==0:
                g[i]=1/(2*math.pi*cutoff_freq*g[i]/50)
            else:
                g[i]=1/(2*math.pi*cutoff_freq*g[i]*50)
    elif topology=='Series First':
        for i in range(0,order):
            if (i%2)==0:
                g[i]=1/(2*math.pi*cutoff_freq*50*g[i])
            else:
                g[i]=1/(2*math.pi*cutoff_freq*g[i]/50)
    print(g)
elif response=='Bandpass':
    g1=[]
    lower_cutoff_freq=4e9
    upper_cutoff_freq=6e9
    omega0=math.sqrt(lower_cutoff_freq*upper_cutoff_freq)
    alpha=omega0/(upper_cutoff_freq-lower_cutoff_freq)
    if topology=='Shunt First':
        for i in range(0,order):
            if (i%2)==0:
                g1.append(alpha*g[i]/(50*2*math.pi*omega0))
                g1.append(1/(alpha*2*math.pi*omega0*g[i]/50))
            else:
                g1.append(1/(alpha*50*g[i]*2*math.pi*omega0))
                g1.append(alpha*50*g[i]/(2*math.pi*omega0))
    if topology=='Series First':
        for i in range(0,order):
            if (i%2)==1:
                g1.append(alpha*g[i]/(50*2*math.pi*omega0))
                g1.append(1/(alpha*2*math.pi*omega0*g[i]/50))
            else:
                g1.append(1/(alpha*50*g[i]*2*math.pi*omega0))
                g1.append(alpha*50*g[i]/(2*math.pi*omega0))
    print(g1)
elif response=='Bandstop':
    g1 = []
    lower_cutoff_freq = 4e9
    upper_cutoff_freq = 6e9
    omega0 = math.sqrt(lower_cutoff_freq * upper_cutoff_freq)
    alpha = omega0 / (upper_cutoff_freq - lower_cutoff_freq)
    if topology == 'Shunt First':
        for i in range(0, order):
            if (i % 2) == 0:
                g1.append(g[i] / (alpha*50 * 2 * math.pi * omega0))
                g1.append(alpha / (2 * math.pi * omega0 * g[i] / 50))
            else:
                g1.append(g[i]*50 / (alpha * 2 * math.pi * omega0))
                g1.append(alpha/ (g[i]*50*2 * math.pi * omega0))
    if topology == 'Series First':
        for i in range(0, order):
            if (i % 2) == 0:
                g1.append(g[i] / (alpha*50 * 2 * math.pi * omega0))
                g1.append(alpha / (2 * math.pi * omega0 * g[i] / 50))
            else:
                g1.append(g[i]*50 / (alpha * 2 * math.pi * omega0))
                g1.append(alpha/ (g[i]*50*2 * math.pi * omega0))
    print(g1)

if (order%2)==0:    # But we should avoid even order since 50Ohm is a typical resistance.
    print("The output impendance should be ",coth(beta/4)**2,"Ohm")