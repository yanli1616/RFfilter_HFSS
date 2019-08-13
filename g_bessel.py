from scipy import signal
from sympy import symbols,simplify,fraction,re,expand
def g_bessel(n):
    order = n  # order is given
    s = symbols('s')  # as a variable

    # reverse Bessel Function
    def bessel(s):
        b = [0 for i in range(order + 1)]
        b[0] = 1
        b[1] = 1 + s
        for i in range(1, order):
            b[i + 1] = b[i] + (s ** 2) * b[i - 1] / (4 * i ** 2 - 1)
        return simplify(b[order])

    # Transfer function
    def S12(s):
        return 1 / bessel(s)

    # F function
    def F(s):
        return S12(s) * S12(-s)

    # p,q are numerator and denominator of S11, respectively
    p, q = fraction(simplify(1 - F(s)))
    p = expand(p)
    q = expand(q)
    # factor_num,factor_den are coefficients of polynomial p,q
    factor_num = [float(p.coeff(s, i)) for i in range(order ** 2, -1, -1)]
    factor_den = [float(q.coeff(s, i)) for i in range(order ** 2, -1, -1)]
    ## KEY POINT: tf2zpk is a function that gives you zeros and poles of a fractional function(and really fast)
    zero, pole, k = signal.tf2zpk(factor_num, factor_den)

    ## We need only points on the left plane
    # numerator
    p1 = []
    for i in range(len(zero)):
        if re(zero[i]) < 0:  # without s=0 in case of complexity
            p1.append(zero[i])
    while len(p1) < order:  # put back s=0 since the order is determined
        p1.append(0)
    # denominator
    q1 = []
    for i in range(len(pole)):
        if re(pole[i]) < 0:
            q1.append(pole[i])
    while len(q1) < order:
        q1.append(0)

    ##Build S11 with p1,q1
    def z_frac(s, p1, q1):
        b = 1
        a = 1
        for i in range(order):
            b = b * (s - p1[i])
            a = a * (s - q1[i])
        return expand(a + b), expand(a - b)  # z=(1+S11)/(1-S11)

    # p2,q2 are numerator and denominator of Zin, respectively
    p2, q2 = z_frac(s, p1, q1)

    # p2,q2's coefficients are real now,but because of floats and approximation, the imaginary parts are very close to 0
    def coeff(s, p2, q2):
        numerator = [re(p2.coeff(s, i)) for i in range(order, -1, -1)]
        denominator = [re(q2.coeff(s, i)) for i in range(order, -1, -1)]
        return numerator, denominator

    ## continuous fraction equation
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
    return continued_fraction_expr_series(s,p2,q2)