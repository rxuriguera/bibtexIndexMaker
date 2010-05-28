
import matplotlib.pyplot as plt #@UnresolvedImport

import numpy as np


if __name__ == '__main__':
    engines = ['Google', 'Scholar', 'Bing', 'Yahoo']
    #colors = ['#4272DB', '#60a63a', '#FFA615', '#7D3883']
    colors = ['#666666', '#60a63a', '#999999', '#BBBBBB']
    #markers = ['o', '-', '^', 's']
    
    data = [[2.1600000000000001, 1.8, 1.76, 1.24, 1.76, 1.48, 1.4399999999999999, 1.3200000000000001, 1.04, 0.92000000000000004, 0.92000000000000004],
            [2.1600000000000001, 1.8, 1.76, 1.24, 1.76, 1.48, 1.4399999999999999, 1.3200000000000001, 1.04, 0.92000000000000004, 0.92000000000000004],
            [1.3999999999999999, 2.04, 2.6800000000000002, 2.0800000000000001, 1.5600000000000001, 1.3600000000000001, 1.24, 1.0800000000000001, 0.92000000000000004, 0.64000000000000001, 0.64000000000000001],
            [2.1600000000000001, 2.0800000000000001, 2.1200000000000001, 1.28, 1.28, 1.04, 1.0800000000000001, 1.0, 0.68000000000000005, 0.59999999999999998, 0.52000000000000002]]
    total_files = 5
    
    plt.rc("font", family="cmr10")
    plt.rc("font", size=10)
    
    width = 4.5
    height = 2.0
    #plt.rc("figure.subplot", left=(22 / 72.27) / width)
    #plt.rc("figure.subplot", right=(width - 10 / 72.27) / width)
    #plt.rc("figure.subplot", bottom=(14 / 72.27) / height)
    #plt.rc("figure.subplot", top=(height - 7 / 72.27) / height)
    plt.figure(figsize=(width + 1, height + 1))
    plt.subplots_adjust(left=0.125, bottom=0.15, right=0.95, top=0.9)
        
    
    plt.subplot(111)
    plt.plot()
    plt.hold(True)
    lines = []
    for i in range(len(data)):
        # Skip scholar
        if i == 1:
            continue
        print data[i]
        #line = plt.plot(range(1, len(data) + 1), data[i], marker=markers[i], markersize=5)[0]
        line = plt.plot(range(1, len(data[i]) + 1), data[i])[0]
        line.set_color(colors[i])
        line.set_label(engines[i])
        line.set_linewidth(2.0)
        lines.append(line)
    
    plt.xticks(range(1, len(data[0]) + 1))
    plt.yticks(range(0, 4, 1))
    plt.axis([0, len(data[0]) + 1, 0, 3.5])
    plt.title('Consultes')
    plt.ylabel('Primera consulta amb bons resultats')
    plt.xlabel('Llargada de la consulta (paraules)')
    plt.grid(True, color='#666666')
    plt.hold(False)

    
    engines.pop(1)
    #l = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    #plt.legend(lines, engines)
    #plt.figlegend(lines, engines, loc=4)
    #plt.show()
    #plt.legend()
    plt.savefig('test.pdf', bbox_inches="tight")
