
import matplotlib.pyplot as plt #@UnresolvedImport


if __name__ == '__main__':
    labels = ['Confian\c{c}a$< 0.25$',
              '$0.25\\leq$Confian\\c{c}a$<0.5$',
              '$0.5 \\leq$Confian\\c{c}a$< 0.75$',
              '$0.75 \\leq$Confian\\c{c}a', ]
    #colors = ['#4272DB', '#60a63a', '#FFA615', '#7D3883']
    colors = ['#666666', '#60a63a', '#999999', '#333333']
    #markers = ['o', '-', '^', 's']

    # Author Coverage
    field = 'author'
    data = [3.99, 5.62, 7.37, 10.28, 12.63, 14.21, 15.78]


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
    #for i in range(len(data[0])):
        # Skip scholar
    #    if i < 2:
    #        continue
    #   print data[i]
        #line = plt.plot(range(1, len(data) + 1), data[i], marker=markers[i], markersize=5)[0]
    xvalues = range(2, len(data) + 2)
    values = data
    line = plt.plot(xvalues, values)[0]
    line.set_color('#333333')
    line.set_linewidth(2.0)
    lines.append(line)
    
    plt.xticks(range(2, len(data) + 2))
    plt.yticks(range(2, 19, 2))
    plt.axis([1.5, len(data) + 1.5, 0, 20])
    plt.title('Temps mig per camp')
    plt.ylabel('Temps (s)')
    plt.xlabel('Exemples utilitzats')
    plt.grid(True, color='#666666')
    plt.hold(False)

    
    labels.pop(0)
    labels.pop(1)
    #l = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    #plt.legend(lines, engines)
    #plt.figlegend(lines, labels, loc=4)
    #plt.show()
    #plt.legend()
    plt.savefig('results:field-time.pdf', bbox_inches="tight")
