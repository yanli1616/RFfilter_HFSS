# 2nd Butterworth Bandpass 4-8GHz
import hycohanz as hfss
import os
import python_hy_inductor as inductor
import python_hy_capacitor as capacitor

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

design = hfss.insert_design(project, increment_name('filter 4.0', hfss.get_top_design_list(project)), 'DrivenModal')

oEditor = hfss.set_active_editor(design)

hfss.set_units(oEditor, "mm")

h=0.5
hfss.add_property(design, 'h', vm(h))
a = 10.0
hfss.add_property(design, 'a', vm(a))
b = 10.0
hfss.add_property(design, 'b', vm(b))
d0=1.5
hfss.add_property(design, 'd0', vm(d0))
l0=1.0
hfss.add_property(design, 'l0', vm(l0))
W=0.003
hfss.add_property(design, 'W', vm(W))
W0=0.004
hfss.add_property(design, 'W0', vm(W0))
W1=0.003
hfss.add_property(design, 'W1', vm(W1))
W2=0.0012
hfss.add_property(design, 'W2', vm(W2))


substrate=hfss.create_box(oEditor,
                          0,0,'-h',
                          'a','b','h',
                          Name='Substrate',
                          Color=(143,175,143),
                          Transparency=0.75,
                          MaterialValue='\"sapphire\"')
cpw_filter = hfss.create_rectangle(oEditor, 0, 0, 0, 'a', 'b', Color=(255, 128, 64))

rect1=hfss.create_rectangle(oEditor,'a/2-W0/2','d0',0,'W0','l0')
line1=hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0', 0, 'W', 'l0')
cpw_filter=hfss.subtract(oEditor, [cpw_filter], [rect1])
cpw_filter=hfss.unite(oEditor, [cpw_filter, line1])

rect2=hfss.create_rectangle(oEditor, 'a/2-W0/2','d0+l0',0,'W0','W1')
line2=hfss.create_rectangle(oEditor,'a/2-W/2', 'd0+l0',0,'W0/2+W/2','W1')
cpw_filter=hfss.subtract(oEditor, [cpw_filter], [rect2])
cpw_filter=hfss.unite(oEditor, [cpw_filter, line2])

rect3=hfss.create_rectangle(oEditor,'a/2-W0/2','d0+l0+W1',0,'W0','l0')
line3=hfss.create_rectangle(oEditor,'a/2-W/2','d0+l0+W1',0,'W','l0')
cpw_filter=hfss.subtract(oEditor, [cpw_filter], [rect3])
cpw_filter=hfss.unite(oEditor, [cpw_filter, line3])

rect4=hfss.create_rectangle(oEditor,'a/2-W0/2','d0+l0+W1+l0',0,'W0','W2')
line4=hfss.create_rectangle(oEditor,'a/2-W/2','d0+l0+W1+l0',0,'W0/2+W/2','W2')
cpw_filter=hfss.subtract(oEditor, [cpw_filter], [rect4])
cpw_filter=hfss.unite(oEditor, [cpw_filter, line4])

rect5=hfss.create_rectangle(oEditor,'a/2-W0/2','d0+l0+W1+l0+W2',0,'W0','l0')
line5=hfss.create_rectangle(oEditor,'a/2-W/2','d0+l0+W1+l0+W2',0,'W','l0')
cpw_filter=hfss.subtract(oEditor, [cpw_filter], [rect5])
cpw_filter=hfss.unite(oEditor, [cpw_filter, line5])

rect6=hfss.create_rectangle(oEditor,'a/2+W0/2','d0+l0-0.0025mm',0,'1mm','W1+0.005mm')
line6=hfss.create_rectangle(oEditor,'a/2+W0/2','d0+l0',0,'1mm','W1')
cpw_filter=hfss.subtract(oEditor, [cpw_filter], [rect6])
cpw_filter=hfss.unite(oEditor, [cpw_filter, line6])

rect7=hfss.create_rectangle(oEditor,'a/2+W0/2','d0+l0+W1+l0-0.0025mm',0,'1mm','W2+0.005mm')
line7=hfss.create_rectangle(oEditor,'a/2+W0/2','d0+l0+W1+l0',0,'1mm','W2')
cpw_filter=hfss.subtract(oEditor, [cpw_filter], [rect7])
cpw_filter=hfss.unite(oEditor, [cpw_filter, line7])


cpw_filter=capacitor.shunt(oEditor, cpw_filter, x0 = a / 2 + W0 / 2 + 1, y0 = d0 + l0 + W1 / 2)

cpw_filter=inductor.shunt(oEditor, cpw_filter, x0 = a / 2 + W0 / 2 + 1, y0 = d0 + l0 + W1 + l0 + W2 / 2)

cpw_filter=capacitor.series(oEditor, cpw_filter, x0 = a / 2, y0 = d0 + l0 + W1 + l0 + W2 + l0, var_x = 0.5, var_y = 0.5, l3 = 0.276)

rect8=hfss.create_rectangle(oEditor,'a/2-W0/2','d0+l0+W1+l0+W2+l0+0.5mm',0,'W0','l0')
line8=hfss.create_rectangle(oEditor,'a/2-W/2','d0+l0+W1+l0+W2+l0+0.5mm',0, 'W', 'l0')
cpw_filter=hfss.subtract(oEditor, [cpw_filter], [rect8])
cpw_filter=hfss.unite(oEditor, [cpw_filter, line8])

cpw_filter=inductor.series(oEditor, cpw_filter, x0=a / 2, y0=d0 + l0 + W1 + l0 + W2 + l0 + 0.5 + l0)

rect9=hfss.create_rectangle(oEditor,'a/2-W0/2','d0+l0+W1+l0+W2+l0+0.5mm+l0+0.5mm',0,'W0','l0')
line9=hfss.create_rectangle(oEditor,'a/2-W/2','d0+l0+W1+l0+W2+l0+0.5mm+l0+0.5mm',0,'W','l0')
cpw_filter=hfss.subtract(oEditor, [cpw_filter], [rect9])
cpw_filter=hfss.unite(oEditor, [cpw_filter, line9])

lumped_port1 = hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0', 0, 'W', '0.1mm')
lumped_port2 = hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0+l0+W1+l0+W2+l0+0.5mm+l0+0.5mm+l0-0.1mm', 0, 'W', '0.1mm')
cpw_filter = hfss.subtract(oEditor, [cpw_filter], [lumped_port1,lumped_port2])

hfss.assign_perfect_e(design, "PerfectE1", [cpw_filter])

lumped_port1 = hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0', 0, 'W', '0.1mm')
lumped_port2 = hfss.create_rectangle(oEditor, 'a/2-W/2', 'd0+l0+W1+l0+W2+l0+0.5mm+l0+0.5mm+l0-0.1mm', 0, 'W', '0.1mm')
hfss.assign_lumpedport(design, '1', [a / 2, d0, 0], [a / 2, d0 + 0.1, 0], [lumped_port1])
hfss.assign_lumpedport(design, '2', [a / 2, d0+l0+W1+l0+W2+l0+0.5+l0+0.5+l0, 0],
                       [a / 2, d0+l0+W1+l0+W2+l0+0.5+l0+0.5+l0-0.1, 0], [lumped_port2])

setup = hfss.insert_analysis_setup(design, 5)
hfss.insert_frequency_sweep(design, setup, "Sweep1", 1, 20, count=20000)

region = hfss.create_region(oEditor, "10mm")
hfss.assign_perfect_e(design, "PerfectE2", [region])

hfss.solve(design, [setup])

hfss.create_report(design, "S Parameter Plot", "dB(S(1,1)),dB(S(1,2))")

raw_input('Press "Enter" to quit HFSS.>')
hfss.save_as_project(oDesktop, filename)
hfss.quit_application(oDesktop)

del oAnsoftApp
del oDesktop
del project
del design
del oEditor