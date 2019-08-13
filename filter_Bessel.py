from sympy import symbols,simplify,fraction,solve,re,expand
import numpy as np

#目前看来，时间最长的一部应该在判断哪些点在左平面的部分，因为solve得到的解为解析解，如何转化为数值解，是一个问题，也许可以借助matlab或者mathematica

s=symbols('s')
n=4
def bessel(s):
    b=[0 for i in range(n+1)]
    b[0]=1
    b[1]=1+s
    for i in range(1,n):
        b[i+1]=b[i]+(s**2)*b[i-1]/(4*i**2-1)
    return simplify(b[n])
def S12(s):
    return 1/bessel(s)
def F(s):
    return S12(s)*S12(-s)
p,q=fraction(simplify(1-F(s)))
p=expand(p)

q=expand(q)


sol_p=solve(p,s)
sol_q=solve(q,s)
print(sol_p,sol_q)

# numerator
p1=[]
for i in range(len(sol_p)):
    sol_p[i]=simplify(sol_p[i]).evalf()
    if re(sol_p[i])<0:
        p1.append(sol_p[i])
while len(p1)<n:
    p1.append(0)
print(p1)
# denominator
q1=[]
for i in range(len(sol_q)):
    sol_q[i] = simplify(sol_q[i]).evalf()
    if re(sol_q[i]) < 0:
        q1.append(sol_q[i])
while len(q1)<n:
    q1.append(0)
print(q1)

def rho(s,p1,q1):
    rho_value=1
    for i in range(n):
        rho_value=rho_value*(s-p1[i])/(s-q1[i])
    return rho_value

Rho=rho(s,p1,q1)

p2,q2=fraction(simplify((1+Rho)/((1-Rho))))
p2=expand(p2)
print(p2)

q2=expand(q2)
print(q2)


def continued_fraction_expr_series(p2,q2,s):
    numerator=[p2.coeff(s,i) for i in range(n,-1,-1)]
    print(numerator)
    denominator=[q2.coeff(s,i) for i in range(n,-1,-1)]
    print(denominator)
    g=[0 for i in range(n)]
    for i in range(n):
        if (numerator[i]-0>0.001)&(denominator[i]-0>0.001):
            g[i]=numerator[i]/denominator[i]
            for j in range(n,i-1,-1):
                numerator[j]=simplify(numerator[j]-g[i]*denominator[j])
        elif (numerator[i]-0<0.001)&(denominator[i]-0>0.001):
            g[i]=denominator[i]/numerator[i+1]
            for j in range(n-1,i-1,-1):
                denominator[j]=simplify(denominator[j]-g[i]*numerator[j+1])
        elif (numerator[i]-0>0.001)&(denominator[i]-0<0.001):
            g[i]=numerator[i]/denominator[i+1]
            for j in range(n-1,i-1,-1):
                numerator[j]=simplify(numerator[j]-g[i]*denominator[j+1])
    g[i]=g[i].evalf()
    return g

print(continued_fraction_expr_series(p2,q2,s))