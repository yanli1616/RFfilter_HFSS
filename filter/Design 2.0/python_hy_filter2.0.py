# 2nd Butterworth Bandpass 4-8GHz
import hycohanz as hfss
import os
import python_hy_inductor2 as inductor
import python_hy_capacitor2 as capacitor

def vm(x):
    """
    transfer float to string, as the value of property
    :param x:
        float
    :return:
        string
    """
    return str(x) + 'mm'


def increment_name(base, existing):
    """
    check and create new name
    :param base:
        name
    :param existing:
        namelist
    :return:
        new name
    """
    if not base in existing:
        return base
    n = 1
    make_name = lambda: base + str(n)
    while make_name() in existing:
        n += 1
    return make_name()


def exist(x, x_str):
    if x <= 0:
        print (x_str + "<=0")
        exit()
    else:
        return True


[oAnsoftApp, oDesktop] = hfss.setup_interface()
filename = 'C:\Users\dell\Desktop\summer\python-hfss/filter/filter.aedt'

if os.path.exists(filename):
    project = hfss.open_project(oDesktop, filename)
else:
    project = hfss.new_project(oDesktop)

design = hfss.insert_design(project, increment_name('filter 5.0', hfss.get_top_design_list(project)), 'DrivenModal')

oEditor = hfss.set_active_editor(design)

hfss.set_units(oEditor, "mm")

h=0.5
hfss.add_property(design, 'h', vm(h))
a = 10.0
hfss.add_property(design, 'a', vm(a))
b = 10.0
hfss.add_property(design, 'b', vm(b))
var_x=3.0
hfss.add_property(design, 'var_x', vm(var_x))
d0= b / 2 - var_x / 2
hfss.add_property(design, 'd0', 'b/2-var_x/2')
W=0.003
hfss.add_property(design, 'W', vm(W))
W0=0.004
hfss.add_property(design, 'W0', vm(W0))
W1=0.003
hfss.add_property(design, 'W1', vm(W1))
d1 = 2 * var_x / 5 - W / 2
hfss.add_property(design, 'd1', vm(d1))
l0 = var_x / 5 - W1 / 4
hfss.add_property(design, 'l0', vm(l0))

substrate=hfss.create_box(oEditor,
                          0,0,'-h',
                          'a','b','h',
                          Name='Substrate',
                          Color=(143,175,143),
                          Transparency=0.75,
                          MaterialValue='\"sapphire\"')
cpw_filter = hfss.create_rectangle(oEditor, 0, 0, 0, 'a', 'b', Color=(255, 128, 64))

cpw_filter=hfss.subtract(oEditor, [cpw_filter], [hfss.create_rectangle(oEditor, 'a/2-var_x/2', 'b/2-var_x/2', 0, 'var_x',
                                                                       'var_x')])


line1=hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0', 0, 'W', 'l0')
cpw_filter=hfss.unite(oEditor, [cpw_filter, line1])

line2=hfss.create_rectangle(oEditor,'a/2-W/2', 'd0+l0',0,'W','W1')
cpw_filter=hfss.unite(oEditor, [cpw_filter, line2])

line3=hfss.create_rectangle(oEditor,'a/2-W/2','d0+l0+W1',0,'W','l0')
cpw_filter=hfss.unite(oEditor, [cpw_filter, line3])

line4=hfss.create_rectangle(oEditor,'a/2+W/2','d0+l0',0,'d1','W1')
cpw_filter=hfss.unite(oEditor, [cpw_filter, line4])

line5=hfss.create_rectangle(oEditor,'a/2-W/2-d1','d0+l0',0,'d1','W1')
cpw_filter=hfss.unite(oEditor, [cpw_filter, line5])

cpw_filter=capacitor.shunt(oEditor, cpw_filter, x0 = a / 2 + W / 2 + d1, y0 = d0 + l0 + W1 / 2, var_x=var_x/10)

cpw_filter=inductor.shunt(oEditor, cpw_filter, x0 = a / 2 - W / 2 - d1 - var_x / 10, y0 = d0 + l0 + W1 / 2, var_x=var_x/10)

cpw_filter=capacitor.series(oEditor, cpw_filter, x0 = a / 2, y0 = d0 + l0 + W1 + l0, var_x =var_x/10, l3 = 0.276)

line6=hfss.create_rectangle(oEditor,'a/2-W/2','d0+l0+W1+l0+var_x/10',0, 'W', 'l0')
cpw_filter=hfss.unite(oEditor, [cpw_filter, line6])

cpw_filter=inductor.series(oEditor, cpw_filter, x0=a / 2, y0=d0 + l0 + W1 + l0 + var_x/10 + l0)

line7=hfss.create_rectangle(oEditor,'a/2-W/2','d0+l0+W1+l0+var_x/10+l0+var_x/10',0, 'W', 'l0')
cpw_filter=hfss.unite(oEditor, [cpw_filter, line7])

lumped_port1 = hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0', 0, 'W', 'l0/5')
lumped_port2 = hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0+l0+W1+l0+var_x/10+l0+var_x/10+l0-l0/5', 0, 'W', 'l0/5')
cpw_filter = hfss.subtract(oEditor, [cpw_filter], [lumped_port1,lumped_port2])

hfss.assign_perfect_e(design, "PerfectE1", [cpw_filter])

lumped_port1 = hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0', 0, 'W', 'l0/5')
lumped_port2 = hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0+l0+W1+l0+var_x/10+l0+var_x/10+l0-l0/5', 0, 'W', 'l0/5')
hfss.assign_lumpedport(design, '1', [a / 2, d0, 0], [a / 2, d0 + l0 / 5, 0], [lumped_port1])
hfss.assign_lumpedport(design, '2', [a / 2, d0+l0+W1+l0+var_x/10+l0+var_x/10+l0, 0],
                       [a / 2, d0+l0+W1+l0+var_x/10+l0+var_x/10+l0-l0 / 5, 0], [lumped_port2])

setup = hfss.insert_analysis_setup(design, 5)
hfss.insert_frequency_sweep(design, setup, "Sweep1", 1, 20, count=20000)

offset=10
hfss.add_property(design, 'offset', vm(offset))
region = hfss.create_region(oEditor, 'offset')
hfss.assign_perfect_e(design, "PerfectE2", [region])

hfss.solve(design, [setup])

hfss.create_report(design, "S Parameter Plot", ["dB(S(1,1))","dB(S(1,2))"])

raw_input('Press "Enter" to quit HFSS.>')
hfss.save_as_project(oDesktop, filename)
hfss.quit_application(oDesktop)

del oAnsoftApp
del oDesktop
del project
del design
del oEditor