from scipy import signal
from sympy import symbols,simplify,fraction,re,im,expand
s=symbols('s')
order=4
ripple=0.01
attenuation=30.0
b,a=signal.ellip(order,ripple,attenuation,1,'low',1,'ba')
print(b,a)

zero,pole,k=signal.ellip(order,ripple,attenuation,1,'low',1,'zpk')
omega=[]
for i in range(len(zero)):
    if im(zero[i])>0:
        omega.append(im(zero[i]))
print(omega)
def elliptic(s, z, p, k):
    num = 1
    den = 1
    for i in range(len(z)):
        num*=(s-z[i])
    for i in range(len(p)):
        den*=(s-p[i])
    return k*num,den

def S11(s,z,p,k):
    b1,a1=elliptic(s,z,p,k)
    b2,a2=elliptic(-s,z,p,k)
    return expand(a1*a2-b1*b2),expand(a1*a2)
p,q=S11(s,zero,pole,k)

factor_num = [float(re(p.coeff(s, i))) for i in range(order ** 2, -1, -1)]
factor_den = [float(re(q.coeff(s, i))) for i in range(order ** 2, -1, -1)]

## KEY POINT: tf2zpk is a function that gives you zeros and poles of a fractional function(and really fast)
zero1, pole1, k1 = signal.tf2zpk(factor_num, factor_den)
for i in range(len(zero1)):
    if((abs(re(zero1[i]))<1e-15)&(abs(im(zero1[i]))<1e-7)):
        zero1[i]=0
for i in range(len(pole1)):
    if((abs(re(pole1[1]))<1e-15)&(abs(im(pole1[1]))<1e-7)):
        pole[i]=0

## We need only points on the left plane
# numerator
p1 = []
for i in range(len(zero1)):
    if re(zero1[i]) < 0:  # without s=0 in case of complexity
        p1.append(zero1[i])
while len(p1) < order:  # put back s=0 since the order is determined
    p1.append(0)
# denominator
q1 = []
for i in range(len(pole1)):
    if re(pole1[i]) < 0:
        q1.append(pole1[i])
while len(q1) < order:
    q1.append(0)
##Transmission zero

##Build S11 with p1,q1
def z_frac(s, p1, q1,k):
    b = 1
    a = 1
    for i in range(order):
        b = b * (s - p1[i])
        a = a * (s - q1[i])
    return expand(a + k*b), expand(a - k*b)  # z=(1+S11)/(1-S11)
p2, q2 = z_frac(s, p1, q1, k1)



def coeff(s, p2, q2):
    numerator = [re(p2.coeff(s, i)) for i in range(order, -1, -1)]
    denominator = [re(q2.coeff(s, i)) for i in range(order, -1, -1)]
    return numerator, denominator
print(coeff(s,p2,q2))


def continued_fraction_expr_series(s, p2, q2):
    numerator, denominator = coeff(s, p2, q2)
    g = [0 for i in range(order)]
    for i in range(order):
        if (numerator[i] - 0 > 0.001) & (denominator[i] - 0 > 0.001):
            g[i] = numerator[i] / denominator[i]
            for j in range(order, i - 1, -1):
                numerator[j] = simplify(numerator[j] - g[i] * denominator[j])
        elif (numerator[i] - 0 < 0.001) & (denominator[i] - 0 > 0.001):
            g[i] = denominator[i] / numerator[i + 1]
            for j in range(order - 1, i - 1, -1):
                denominator[j] = simplify(denominator[j] - g[i] * numerator[j + 1])
        elif (numerator[i] - 0 > 0.001) & (denominator[i] - 0 < 0.001):
            g[i] = numerator[i] / denominator[i + 1]
            for j in range(order - 1, i - 1, -1):
                numerator[j] = simplify(numerator[j] - g[i] * denominator[j + 1])
    return g