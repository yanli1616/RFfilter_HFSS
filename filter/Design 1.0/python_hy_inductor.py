import hycohanz as hfss

def i_s(i):
    return str(i)+'mm'

def shunt(oEditor, cpw_filter, x0=0, y0=0, var_x=0.5, l4=0.01, W3=0.003, r0=0.0024, r1=0.0024, n=4):
    l3 = var_x / 2 - r0 - n * r1
    if(l3<=0):
        print "Parametrics<0"
        exit()
    d3 = var_x / 2 - W3 / 2 - r0 - r1 - l4
    if(d3<=0):
        print "Parametrics<0"
        exit()

    rect=hfss.create_rectangle(oEditor, i_s(x0), i_s(y0-var_x/2), 0, i_s(var_x), i_s(var_x))

    cl = [hfss.create_polyline(oEditor,
                               [i_s(x0), i_s(x0+l3)],
                               [i_s(y0), i_s(y0)],
                               [0, 0],
                               IsPolylineCovered=False,
                               ),
          hfss.create_EQbasedcurve(oEditor,
                                   i_s(x0 + l3) + '+' + i_s(r0) + '*sin(_t)',
                                   i_s(y0+r0)+'-'+i_s(r0)+'*cos(_t)',
                                   '0',
                                   0, 'pi/2',
                                   0,
                                  )]

    for i in range(n - 1):
        if i % 2 == 0:
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0+l3+r0+i*2*r1), i_s(x0+l3+r0+i*2*r1)],
                                           [i_s(y0+r0),
                                            i_s(y0+r0+l4)],
                                           [0, 0],
                                           IsPolylineCovered=False))
            cl.append(hfss.create_EQbasedcurve(oEditor,
                                               i_s(x0+l3+r0+r1+i*2*r1)+'-'+i_s(r1)+'*cos(_t)',
                                               i_s(y0+r0+l4)+'+'+i_s(r1)+'*sin(_t)',
                                               '0',
                                               0, 'pi',
                                               0))
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0 + l3 + r0+2*r1 + i * 2 * r1), i_s(x0 + l3 + r0+2*r1 + i * 2 * r1)],
                                           [i_s(y0 + r0+l4),
                                            i_s(y0 + r0)],
                                           [0, 0],
                                           IsPolylineCovered=False))
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0+l3+r0+2*r1+i*2*r1), i_s(x0+l3+r0+2*r1+i*2*r1)],
                                           [i_s(y0+r0),i_s(y0-r0)],
                                           [0, 0],
                                           IsPolylineCovered=False))
        else:
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0 + l3 + r0 + i * 2 * r1), i_s(x0 + l3 + r0 + i * 2 * r1)],
                                           [i_s(y0 - r0),
                                           i_s(y0 - r0 - l4)],
                                           [0, 0],
                                           IsPolylineCovered=False))
            cl.append(hfss.create_EQbasedcurve(oEditor,
                                               i_s(x0 + l3 + r0 + r1 + i * 2 * r1) + '-' + i_s(r1) + '*cos(_t)',
                                               i_s(y0 - r0 - l4) + '-' + i_s(r1) + '*sin(_t)',
                                               '0',
                                               0, 'pi',
                                               0))
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0 + l3 + r0 + 2 * r1 + i * 2 * r1), i_s(x0 + l3 + r0 + 2 * r1 + i * 2 * r1)],
                                           [i_s(y0 - r0 - l4),
                                            i_s(y0 - r0)],
                                           [0, 0],
                                           IsPolylineCovered=False))
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0 + l3 + r0 + 2 * r1 + i * 2 * r1), i_s(x0+l3+r0+2*r1+i*2*r1)],
                                           [i_s(y0 - r0), i_s(y0 + r0)],
                                           [0, 0],
                                           IsPolylineCovered=False))
    if n % 2 == 0:
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0 + l3 + r0 + (n-1) * 2 * r1), i_s(x0 + l3 + r0 + (n-1) * 2 * r1)],
                                       [i_s(y0 - r0),
                                        i_s(y0 - r0 - l4)],
                                       [0, 0],
                                       IsPolylineCovered=False))
        cl.append(hfss.create_EQbasedcurve(oEditor,
                                           i_s(x0 + l3 + r0 + r1 + (n-1) * 2 * r1) + '-' + i_s(r1) + '*cos(_t)',
                                           i_s(y0 - r0 - l4) + '-' + i_s(r1) + '*sin(_t)',
                                           '0',
                                           0, 'pi',
                                           0))
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0 + l3 + r0 + 2 * r1 + (n-1) * 2 * r1), i_s(x0 + l3 + r0 + 2 * r1 + (n-1) * 2 * r1)],
                                       [i_s(y0 - r0 - l4),
                                        i_s(y0 - r0)],
                                       [0, 0],
                                       IsPolylineCovered=False))
        cl.append(hfss.create_EQbasedcurve(oEditor,
                                           i_s(x0 + l3 + r0 + n * 2 * r1 + r0) + '-' + i_s(r0) + '*cos(_t)',
                                           i_s(y0-r0)+'+'+i_s(r0)+'*sin(_t)',
                                           '0',
                                           0, 'pi/2',
                                           0,
                                           Name='Quarter_Line'))
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0 + l3 + r0 + n * 2 * r1 + r0),
                                        i_s(x0 + l3 + r0 + n * 2 * r1 + r0 + l3)],
                                       [i_s(y0), i_s(y0)],
                                       [0, 0],
                                       IsPolylineCovered=False))
    else:
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0 + l3 + r0 + (n - 1) * 2 * r1), i_s(x0 + l3 + r0 + (n - 1) * 2 * r1)],
                                       [i_s(y0 + r0),
                                        i_s(y0 + r0 + l4)],
                                       [0, 0],
                                       IsPolylineCovered=False))
        cl.append(hfss.create_EQbasedcurve(oEditor,
                                           i_s(x0 + l3 + r0 + r1 + (n - 1) * 2 * r1) + '-' + i_s(r1) + '*cos(_t)',
                                           i_s(y0 + r0 + l4) + '+' + i_s(r1) + '*sin(_t)',
                                           '0',
                                           0, 'pi',
                                           0))
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0 + l3 + r0 + 2 * r1 + (n - 1) * 2 * r1),
                                        i_s(x0 + l3 + r0 + 2 * r1 + (n - 1) * 2 * r1)],
                                       [i_s(y0 + r0 + l4),
                                        i_s(y0 + r0)],
                                       [0, 0],
                                       IsPolylineCovered=False))
        cl.append(hfss.create_EQbasedcurve(oEditor,
                                           i_s(x0 + l3 + r0 + n * 2 * r1 + r0) + '-' + i_s(r0) + '*cos(_t)',
                                           i_s(y0 + r0) + '-' + i_s(r0) + '*sin(_t)',
                                           '0',
                                           0, 'pi/2',
                                           0,
                                           Name='Quarter_Line'))
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0 + l3 + r0 + n * 2 * r1 + r0),
                                        i_s(x0 + l3 + r0 + n * 2 * r1 + r0 + l3)],
                                       [i_s(y0), i_s(y0)],
                                       [0, 0],
                                       IsPolylineCovered=False))

    cl = hfss.unite(oEditor, cl)

    temp_l = hfss.create_polyline(oEditor, [i_s(x0), i_s(x0)], [i_s(y0-W3/2), i_s(y0+W3/2)], [0, 0],
                                  IsPolylineClosed=False)
    meander = hfss.sweep_along_path(oEditor, [temp_l], [cl])
    cpw_filter = hfss.subtract(oEditor, [cpw_filter], [rect])
    cpw_filter = hfss.unite(oEditor, [cpw_filter,meander[0]])

    return cpw_filter


def series(oEditor, cpw_filter, x0=0, y0=0, var_x=0.5, l4=0.01, W3=0.003, n=4, r0=0.0024, r1=0.0024):
    l3 = var_x / 2 - r0 - n * r1
    if (l3 <= 0):
        print "Parametrics<0"
        exit()
    d3 = var_x / 2 - W3 / 2 - r0 - r1 - l4
    if (d3 <= 0):
        print "Parametrics<0"
        exit()

    rect = hfss.create_rectangle(oEditor, i_s(x0-var_x/2), i_s(y0), 0, i_s(var_x), i_s(var_x))

    cl = [hfss.create_polyline(oEditor,
                               [i_s(x0), i_s(x0)],
                               [i_s(y0), i_s(y0+l3)],
                               [0, 0],
                               IsPolylineCovered=False,
                               ),
          hfss.create_EQbasedcurve(oEditor,
                                   i_s(x0-r0)+'+'+i_s(r0)+'*cos(_t)',
                                   i_s(y0+l3)+'+'+i_s(r0)+'*sin(_t)',
                                   '0',
                                   0, 'pi/2',
                                   0,
                                   )]

    for i in range(n - 1):
        if i % 2 == 0:
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0-r0), i_s(x0-r0-l4)],
                                           [i_s(y0+l3+r0+i*2*r1), i_s(y0+l3+r0+i*2*r1)],
                                           [0, 0],
                                           IsPolylineCovered=False))
            cl.append(hfss.create_EQbasedcurve(oEditor,
                                               i_s(x0-r0-l4)+'-'+i_s(r1)+'*sin(_t)',
                                               i_s(y0+l3+r0+r1+i*2*r1)+'-'+i_s(r1)+'*cos(_t)',
                                               '0',
                                               0, 'pi',
                                               0))
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0-r0-l4), i_s(x0-r0)],
                                           [i_s(y0+l3+r0+2*r1+i*2*r1),
                                            i_s(y0+l3+r0+2*r1+i*2*r1)],
                                           [0, 0],
                                           IsPolylineCovered=False))
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0-r0),i_s(x0+r0)],
                                           [i_s(y0+l3+r0+2*r1+i*2*r1),
                                            i_s(y0+l3+r0+2*r1+i*2*r1)],
                                           [0, 0],
                                           IsPolylineCovered=False))
        else:
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0+r0),i_s(x0+r0+l4)],
                                           [i_s(y0+l3+r0+i*2*r1),
                                            i_s(y0+l3+r0+i*2*r1)],
                                           [0, 0],
                                           IsPolylineCovered=False))
            cl.append(hfss.create_EQbasedcurve(oEditor,
                                               i_s(x0+r0+l4)+'+'+i_s(r1)+'*sin(_t)',
                                               i_s(y0+l3+r0+r1+i*2*r1)+'-'+i_s(r1)+'*cos(_t)',
                                               '0',
                                               0, 'pi',
                                               0))
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0+r0+l4),i_s(x0+r0)],
                                           [i_s(y0+l3+r0+2*r1+i*2*r1),
                                            i_s(y0+l3+r0+2*r1+i*2*r1)],
                                           [0, 0],
                                           IsPolylineCovered=False))
            cl.append(hfss.create_polyline(oEditor,
                                           [i_s(x0+r0),i_s(x0-r0)],
                                           [i_s(y0+l3+r0+2*r1+i*2*r1),
                                            i_s(y0+l3+r0+2*r1+i*2*r1)],
                                           [0, 0],
                                           IsPolylineCovered=False))
    if n % 2 == 0:
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0+r0),i_s(x0+r0+l4)],
                                       [i_s(y0+l3+r0+(n-1)*2*r1),
                                        i_s(y0+l3+r0+(n-1)*2*r1)],
                                       [0, 0],
                                       IsPolylineCovered=False))
        cl.append(hfss.create_EQbasedcurve(oEditor,
                                           i_s(x0+r0+l4)+'+'+i_s(r1)+'*sin(_t)',
                                           i_s(y0+l3+r0+r1+(n-1)*2*r1)+'-'+i_s(r1)+'*cos(_t)',
                                           '0',
                                           0, 'pi',
                                           0))
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0+r0+l4),i_s(x0+r0)],
                                       [i_s(y0+l3+r0+2*r1+(n-1)*2*r1),
                                        i_s(y0 + l3 + r0 + 2 * r1 + (n - 1) * 2 * r1)],
                                       [0, 0],
                                       IsPolylineCovered=False))
        cl.append(hfss.create_EQbasedcurve(oEditor,
                                           i_s(x0+r0)+'-'+i_s(r0)+'*sin(_t)',
                                           i_s(y0+l3+r0+n*2*r1+r0)+'-'+i_s(r0)+'*cos(_t)',
                                           '0',
                                           0, 'pi/2',
                                           0,
                                           ))
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0), i_s(x0)],
                                       [i_s(y0+l3+r0+n*2*r1+r0),
                                        i_s(y0+l3+r0+n*2*r1+r0+l3)],
                                       [0, 0],
                                       IsPolylineCovered=False))
    else:
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0-r0),i_s(x0-r0-l4)],
                                       [i_s(y0+l3+r0+(n-1)*2*r1),
                                        i_s(y0+l3+r0+(n-1)*2*r1)],
                                       [0, 0],
                                       IsPolylineCovered=False))
        cl.append(hfss.create_EQbasedcurve(oEditor,
                                           i_s(x0-r0-l4)+'-'+i_s(r1)+'*sin(_t)',
                                           i_s(y0+l3+r0+r1+(n-1)*2*r1)+'-'+i_s(r1)+'*cos(_t)',
                                           '0',
                                           0, 'pi',
                                           0))
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0-r0-l4),i_s(x0-r0)],
                                       [i_s(y0+l3+r0+2*r1+(n-1)*2*r1),
                                        i_s(y0+l3+r0+2*r1+(n-1)*2*r1)],
                                       [0, 0],
                                       IsPolylineCovered=False))
        cl.append(hfss.create_EQbasedcurve(oEditor,
                                           i_s(x0-r0)+'+'+i_s(r0)+'*sin(_t)',
                                           i_s(y0+l3+r0+n*2*r1+r0)+'-'+i_s(r0)+'*cos(_t)',
                                           '0',
                                           0, 'pi/2',
                                           0,
                                           ))
        cl.append(hfss.create_polyline(oEditor,
                                       [i_s(x0),i_s(x0)],
                                       [i_s(y0+l3+r0+n*2*r1+r0),
                                        i_s(y0+l3+r0+n*2*r1+r0+l3)],
                                       [0, 0],
                                       IsPolylineCovered=False))

    cl = hfss.unite(oEditor, cl)

    temp_l = hfss.create_polyline(oEditor, [i_s(x0+W3/2), i_s(x0-W3/2)], [i_s(y0), i_s(y0)], [0, 0],
                                  IsPolylineClosed=False)
    meander = hfss.sweep_along_path(oEditor, [temp_l], [cl])
    cpw_filter = hfss.subtract(oEditor, [cpw_filter], [rect])
    cpw_filter = hfss.unite(oEditor, [cpw_filter, meander[0]])

    return cpw_filter