import math
from g_bessel import g_bessel
from freq_response import plot


def coth(x):
    return (math.exp(x)+math.exp(-x))/(math.exp(x)-math.exp(-x))

response='Bandstop' #Lowpass, Highpass, Bandpass, Bandstop
filter_type='Chebyshev'   #Butterworth, Chebyshev, Elliptic, Bessel, Legendre
topology='Series First'     #Series First, Shunt First
order=5
cutoff_freq=1e9     #Hz
imput_impedance=50  #Ohm
out_impedance=50    #Ohm
ripple=0            #dB
attenuation=[0,0,0,0,0]       #dB
g=[]

#compute the prototype element
if filter_type=='Butterworth':
    for i in range(0, order):
        g.append(2 * math.sin((2 * i + 1) * math.pi / (2 * order)))

elif filter_type=='Chebyshev':
    # set the ripple
    ripple = 0.1   #dB

    beta = math.log(coth(ripple / 17.37))
    gamma = math.sinh(beta / (2 * order))
    g.append(2 * math.sin(math.pi / (2 * order)) / gamma)
    for i in range(1, order):
        g.append(4 * math.sin((2 * i + 1) * math.pi / (2 * order)) * math.sin((2 * i - 1) * math.pi / (2 * order)) / (
                    g[i - 1] * (gamma ** 2 + math.sin(i * math.pi / order) ** 2)))

elif filter_type=='Elliptic':
    # set the ripple
    ripple=0.1      #dB

    # set the attenuation
    attenuation=[13.5698,12.0856,13.8785,18.6757,30.5062]
    elliptic=[
        [0.7427,0.7096,0.5412,0.7427],
        [0.3714,0.5664,1.0929,1.1194,0.9244],
        [0.7081,0.7663,0.7357,1.1276,0.2014,4.3812,0.0499],
        [0.4418,0.7165,0.9091,0.8314,0.3627,2.4468,0.8046,0.9986],
        [0.9194,1.0766,0.3422,1.0962,0.4052,2.2085,0.8434,0.5034,2.2085,0.4110]
    ]
    print("Attenuation",attenuation[order-3],"dB")
    g=elliptic[order-3]

elif filter_type=='Bessel':
    #From Bessel Filters 2003, C.Bond.
    #1 Frequency Normalized
    '''bessel=[[2],
       [2.1478055065,0.5755027510],
       [2.2034114362,0.9705118162,0.3374214850],
       [2.2403786449,1.0815160918,0.6725248100,0.2334158032],
       [2.2582170510,1.1110331705,0.8040111711,0.5072406309,0.1743193807],
       [2.2645236380,1.1126429944,0.8537858651,0.6391554024,0.4001898379,0.1364923846],
       [2.2659005520,1.1051644360,0.8690268432,0.7020091536,0.5248927291,0.3258881312,0.1105624499],
       [2.2656071373,1.0955592547,0.8695003726,0.7302566539,0.5935726770,0.4409221408,0.2719107171,0.0919055476],
       [2.2648789238,1.0862838411,0.8638734468,0.7407329931,0.6305951650,0.5107787008,0.3769865473,0.2312912714,0.0779654714],
       [2.2641261600,1.0780948329,0.8560723826,0.7420173503,0.6493354737,0.5528152742,0.4454426979,0.3270699985,0.2000102641,0.0671556901]
       ]'''
    '''bessel=[[2],
            [0.5755027510,2.1478055065],
            [0.3374214850,0.9705118162,2.2034114362],
            [0.2334158032,0.6725248100,1.0815160918,2.2403786449],
            [0.1743193807,0.5072406309,0.8040111711,1.1110331705,2.2582170510],
            [0.1364923846,0.4001898379,0.6391554024,0.8537858651,1.1126429944,2.2645236380],
            [0.1105624499,0.3258881312,0.5248927291,0.7020091536,0.8690268432,1.1051644360,2.2659005520],
            [0.0919055476,0.2719107171,0.4409221408,0.5935726770,0.7302566539,0.8695003726,1.0955592547,2.2656071373],
            [0.0779654714,0.2312912714,0.3769865473,0.5107787008,0.6305951650,0.7407329931,0.8638734468,1.0862838411,2.2648789238],
            [0.0671556901,0.2000102641,0.3270699985,0.4454426979,0.5528152742,0.6493354737,0.7420173503,0.8560723826,1.0780948329,2.2641261600]
            ]
    g=bessel[order-1]'''
    g=g_bessel(order)

elif filter_type=='Legendre':
    g.append(0)

#transformation from lowpass
if response=='Lowpass':
    if filter_type=='Elliptic':
        if topology == 'Shunt First':
            for i in range(0, len(g)):
                if (i-1)%3 == 0:
                    g[i] = g[i] * 50 / (2 * math.pi * cutoff_freq)
                else:
                    g[i] = g[i] / (50 * 2 * math.pi * cutoff_freq)
        elif topology == 'Series First':
            for i in range(0, len(g)):
                if (i-1)%3 == 0:
                    g[i] = g[i] / (50 * 2 * math.pi * cutoff_freq)
                else:
                    g[i] = g[i] * 50 / (2 * math.pi * cutoff_freq)
    else:
        if topology == 'Shunt First':
            for i in range(0, len(g)):
                if (i % 2) == 0:
                    g[i] = g[i] / (50 * 2 * math.pi * cutoff_freq)
                else:
                    g[i] = g[i] * 50 / (2 * math.pi * cutoff_freq)
        elif topology == 'Series First':
            for i in range(0, len(g)):
                if (i % 2) == 1:
                    g[i] = g[i] / (50 * 2 * math.pi * cutoff_freq)
                else:
                    g[i] = g[i] * 50 / (2 * math.pi * cutoff_freq)
    #normalize the form of output
    if filter_type=='Elliptic':
        if topology=='Shunt First':
            for i in range(len(g)):
                if i % 3==0:
                    print('C', i+1-i/3, '=', g[i], 'F')
                elif (i-1)%3==0:
                    print('L', i + 1-(i-1)/3, '=', g[i], 'H')
                else:
                    print('C', i-(i-2)/3, '=', g[i], 'F')
        else:
            for i in range(len(g)):
                if i % 3==0:
                    print('L', i+1-i/3, '=', g[i], 'H')
                elif (i-1)%3==0:
                    print('C', i + 1-(i-1)/3, '=', g[i], 'F')
                else:
                    print('L', i-(i-2)/3, '=', g[i], 'H')
    else :
        if topology == 'Shunt First':
            for i in range(0, order):
                if (i % 2) == 0:
                    print('C', i + 1, '=', g[i], 'F')
                else:
                    print('L', i + 1, '=', g[i], 'H')
        elif topology == 'Series First':
            for i in range(0, order):
                if (i % 2) == 1:
                    print('C', i + 1, '=', g[i], 'F')
                else:
                    print('L', i + 1, '=', g[i], 'H')
    plot(order,cutoff_freq,ripple,attenuation[order-3],filter_type,response)
elif response=='Highpass':
    if filter_type=='Elliptic':
        if topology == 'Shunt First':
            for i in range(0, len(g)):
                if (i-1)%3==0:
                    g[i] = 1 / (2 * math.pi * cutoff_freq * g[i] * 50)
                else:
                    g[i] = 1 / (2 * math.pi * cutoff_freq * g[i] / 50)
        elif topology == 'Series First':
            for i in range(0, len(g)):
                if (i-1)%3==0:
                    g[i] = 1 / (2 * math.pi * cutoff_freq * g[i] / 50)
                else:
                    g[i] = 1 / (2 * math.pi * cutoff_freq * 50 * g[i])

    else:
        if topology == 'Shunt First':
            for i in range(0, len(g)):
                if (i % 2) == 0:
                    g[i] = 1 / (2 * math.pi * cutoff_freq * g[i] / 50)
                else:
                    g[i] = 1 / (2 * math.pi * cutoff_freq * g[i] * 50)
        elif topology == 'Series First':
            for i in range(0, len(g)):
                if (i % 2) == 0:
                    g[i] = 1 / (2 * math.pi * cutoff_freq * 50 * g[i])
                else:
                    g[i] = 1 / (2 * math.pi * cutoff_freq * g[i] / 50)
    # normalize the form of output
    if filter_type=='Elliptic':
        if topology=='Shunt First':
            for i in range(len(g)):
                if i % 3==0:
                    print('L', i+1-i/3, '=', g[i], 'H')
                elif (i-1)%3==0:
                    print('C', i + 1-(i-1)/3, '=', g[i], 'F')
                else:
                    print('L', i-(i-2)/3, '=', g[i], 'H')
        else:
            for i in range(len(g)):
                if i % 3==0:
                    print('C', i+1-i/3, '=', g[i], 'F')
                elif (i-1)%3==0:
                    print('L', i + 1-(i-1)/3, '=', g[i], 'H')
                else:
                    print('C', i-(i-2)/3, '=', g[i], 'F')
    else:
        if topology == 'Shunt First':
            for i in range(0, order):
                if (i % 2) == 1:
                    print('C', i + 1, '=', g[i], 'F')
                else:
                    print('L', i + 1, '=', g[i], 'H')
        elif topology == 'Series First':
            for i in range(0, order):
                if (i % 2) == 0:
                    print('C', i + 1, '=', g[i], 'F')
                else:
                    print('L', i + 1, '=', g[i], 'H')
    plot(order, cutoff_freq, ripple, attenuation[order-3], filter_type, response)

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
    # normalize the form of output
    for i in range(0,order):
        print('C',i+1,'=',g1[2*i],'F')
        print('L',i+1,'=',g1[2*i+1],'H')
    plot(order, [lower_cutoff_freq,upper_cutoff_freq], ripple, attenuation[order-3], filter_type, response)

elif response=='Bandstop':
    g1 = []
    lower_cutoff_freq = 3e9
    upper_cutoff_freq = 7e9
    omega0 = math.sqrt(lower_cutoff_freq * upper_cutoff_freq)
    alpha = omega0 / (upper_cutoff_freq - lower_cutoff_freq)
    if topology == 'Shunt First':
        for i in range(0, order):
            if (i % 2) == 0:
                g1.append(g[i] / (alpha*50 * 2 * math.pi * omega0))
                g1.append(alpha / (2 * math.pi * omega0 * g[i] / 50))
            else:
                g1.append(alpha / (g[i] * 50 * 2 * math.pi * omega0))
                g1.append(g[i]*50 / (alpha * 2 * math.pi * omega0))
    if topology == 'Series First':
        for i in range(0, order):
            if (i % 2) == 1:
                g1.append(g[i] / (alpha*50 * 2 * math.pi * omega0))
                g1.append(alpha / (2 * math.pi * omega0 * g[i] / 50))
            else:
                g1.append(alpha / (g[i] * 50 * 2 * math.pi * omega0))
                g1.append(g[i]*50 / (alpha * 2 * math.pi * omega0))
    # normalize the form of output
    for i in range(0,order):
        print('C',i+1,'=',g1[2*i],'F')
        print('L',i+1,'=',g1[2*i+1],'H')
    plot(order, [lower_cutoff_freq, upper_cutoff_freq], ripple, attenuation[order-3], filter_type, response)