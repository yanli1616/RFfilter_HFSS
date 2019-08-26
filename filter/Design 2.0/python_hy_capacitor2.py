import hycohanz as hfss

def i_s(i):
    return str(i)+'mm'

def series(oEditor, cpw_filter, x0=0, y0=0, var_x=0.5,
           l2=0.02, l3=0.3, d=0.001, W=0.003, W1=0.001, W2=0.002, n=8):
    l1 = (var_x - l2 - l3 - l2 - 2 * d) / 2
    

    cl = [hfss.create_rectangle(oEditor, i_s(x0-W/2), i_s(y0), 0, i_s(W), i_s(l1)),
          hfss.create_rectangle(oEditor, i_s(x0-(n-1/2)*W1-(n-1)*W2), i_s(y0+l1), 0, i_s((2*n-1)*W1+2*(n-1)*W2), i_s(l2))]
    for i in range(n):
        cl.append(
            hfss.create_rectangle(oEditor, i_s(x0-(n-1/2)*W1-(n-1)*W2+i*2*(W1+W2)), i_s(y0+l1+l2), 0, i_s(W1),
                                  i_s(d+l3)))
    for i in range(n - 1):
        cl.append(
            hfss.create_rectangle(oEditor, i_s(x0-(n-1/2)*W1-(n-1)*W2+i*2*(W1+W2)+(W1+W2)), i_s(y0+l1+l2+d), 0,
                                  i_s(W1), i_s(d+l3)))
    cl.append(hfss.create_rectangle(oEditor, i_s(x0-(n-1/2)*W1-(n-1)*W2), i_s(y0+l1+l2+l3+2*d), 0,
                                    i_s((2*n-1)*W1+2*(n-1)*W2), i_s(l2)))
    cl.append(hfss.create_rectangle(oEditor, i_s(x0-W/2), i_s(y0 + l1 + l2 + l3 + l2 + 2 * d), 0, i_s(W), i_s(l1)))
    finger = hfss.unite(oEditor, cl)

    cpw_filter = hfss.unite(oEditor, [cpw_filter,finger])
    
    return cpw_filter


def shunt(oEditor, cpw_filter, x0=0, y0=0, var_x=0.5,
          l2=0.02, l3=0.447, d=0.001, W=0.003, W1=0.0011, W2=0.0017, n=8):
    l1 = (var_x - l2 - l3 - l2 - 2 * d) / 2

    cl = [hfss.create_rectangle(oEditor, i_s(x0), i_s(y0-W/2), 0, i_s(l1), i_s(W)),
          hfss.create_rectangle(oEditor, i_s(x0 + l1), i_s(y0 - (n - 1 / 2) * W1 - (n - 1) * W2),  0,
                                i_s(l2), i_s((2 * n - 1) * W1 + 2 * (n - 1) * W2))]
    for i in range(n):
        cl.append(
            hfss.create_rectangle(oEditor, i_s(x0 + l1 + l2),
                                  i_s(y0 - (n - 1 / 2) * W1 - (n - 1) * W2 + i * 2 * (W1 + W2)),
                                   0, i_s(d + l3), i_s(W1)
                                  ))
    for i in range(n - 1):
        cl.append(
            hfss.create_rectangle(oEditor, i_s(x0 + l1 + l2 + d),
                                  i_s(y0 - (n - 1 / 2) * W1 - (n - 1) * W2 + i * 2 * (W1 + W2) + (W1 + W2)),
                                  0,
                                  i_s(d + l3),
                                  i_s(W1)))
    cl.append(
        hfss.create_rectangle(oEditor, i_s(x0 + l1 + l2 + l3 + 2 * d), i_s(y0 - (n - 1 / 2) * W1 - (n - 1) * W2), 0,
                              i_s(l2), i_s((2 * n - 1) * W1 + 2 * (n - 1) * W2)))
    cl.append(
        hfss.create_rectangle(oEditor, i_s(x0 + l1 + l2 + l3 + l2 + 2 * d), i_s(y0 - W / 2), 0, i_s(l1), i_s(W)))
    finger = hfss.unite(oEditor, cl)

    cpw_filter = hfss.unite(oEditor, [cpw_filter, finger])

    return cpw_filter