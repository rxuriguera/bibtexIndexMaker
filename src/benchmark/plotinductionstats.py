
import matplotlib.pyplot as plt #@UnresolvedImport

import numpy as np


if __name__ == '__main__':
    labels = ['Confian\c{c}a$< 0.25$',
              '$0.25\\leq$Confian\\c{c}a$<0.5$',
              '$0.5 \\leq$Confian\\c{c}a$< 0.75$',
              '$0.75 \\leq$Confian\\c{c}a', ]
    #colors = ['#4272DB', '#60a63a', '#FFA615', '#7D3883']
    colors = ['#666666', '#60a63a', '#666666', '#333333']
    #markers = ['o', '-', '^', 's']

    # Author Coverage
    author_field = 'author'
    author_data = [[9.0, 0.0, 0.0, 4.0, 5.0],
                    [9.0, 0.0, 0.0, 4.0, 5.0],
                    [9.0, 0.0, 0.0, 2.0, 7.0],
                    [9.0, 0.0, 1.0, 2.0, 6.0],
                    [9.0, 0.0, 1.0, 3.0, 5.0],
                    [9.0, 0.0, 1.0, 3.0, 5.0],
                    [9.0, 0.0, 1.0, 0.0, 8.0]]

    # Title coverage
    title_field = 'title'
    title_data = [[9.0, 0.0, 0.0, 2.0, 7.0],
                    [9.0, 0.0, 0.0, 2.0, 7.0],
                    [9.0, 0.0, 0.0, 0.0, 9.0],
                    [9.0, 0.0, 0.0, 0.0, 9.0],
                    [9.0, 0.0, 0.0, 0.0, 9.0],
                    [9.0, 0.0, 0.0, 1.0, 8.0],
                    [9.0, 0.0, 0.0, 0.0, 9.0]]

    year_field = 'year'
    year_data = [[9.0, 0.0, 0.0, 4.0, 5.0],
                    [9.0, 0.0, 1.0, 4.0, 4.0],
                    [9.0, 0.0, 2.0, 2.0, 5.0],
                    [9.0, 1.0, 1.0, 3.0, 4.0],
                    [9.0, 1.0, 0.0, 4.0, 4.0],
                    [9.0, 1.0, 1.0, 4.0, 3.0],
                    [9.0, 0.0, 1.0, 3.0, 5.0]]
    
  
    journal_field = 'journal'
    journal_data = [[8.0, 0.0, 0.0, 1.0, 7.0],
                    [8.0, 0.0, 0.0, 1.0, 7.0],
                    [8.0, 0.0, 0.0, 0.0, 8.0],
                    [8.0, 0.0, 0.0, 1.0, 7.0],
                    [8.0, 0.0, 0.0, 1.0, 7.0],
                    [8.0, 0.0, 0.0, 2.0, 6.0],
                    [8.0, 0.0, 0.0, 1.0, 7.0]]

    volume_field = 'volume'
    volume_data = [[8.0, 0.0, 0.0, 3.0, 5.0],
                    [8.0, 0.0, 1.0, 4.0, 3.0],
                    [8.0, 0.0, 0.0, 4.0, 4.0],
                    [8.0, 0.0, 4.0, 1.0, 3.0],
                    [8.0, 0.0, 3.0, 3.0, 2.0],
                    [8.0, 0.0, 3.0, 3.0, 2.0],
                    [7.0, 0.0, 4.0, 1.0, 2.0]]
 
    pages_field = 'pages'
    pages_data = [[8.0, 1.0, 0.0, 4.0, 3.0],
                    [8.0, 1.0, 1.0, 4.0, 2.0],
                    [8.0, 1.0, 0.0, 4.0, 3.0],
                    [8.0, 1.0, 2.0, 4.0, 1.0],
                    [8.0, 1.0, 2.0, 4.0, 1.0],
                    [8.0, 1.0, 3.0, 3.0, 1.0],
                    [7.0, 1.0, 3.0, 1.0, 2.0]]

    #author_data      title_data      year_data      journal_data      volume_data      pages_data
    #author_field     title_field     year_field     journal_field     volume_field     pages_field
    
    data = year_data
    field = year_field
    
    
    
    plt.rc("font", family="cmr10")
    plt.rc("font", size=10)
    
    width = 4.50
    height = 2.0
    """
    width = 2.25
    height = 1.0
    """
    
    
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
    
    xvalues = range(2, len(data) + 2)
    values = [(x[3] + x[4]) * 100 / x[0] for x in data]
    line = plt.plot(xvalues, values)[0]
    line.set_color('#999999')
    line.set_linestyle('dashed')
    line.set_label('')
    line.set_linewidth(2.0)
    lines.append(line)
    
    for i in range(len(data[0])):
        # Skip scholar
        if i <= 2:
            continue
        print data[i]
        #line = plt.plot(range(1, len(data) + 1), data[i], marker=markers[i], markersize=5)[0]
        xvalues = range(2, len(data) + 2)
        
        
        values = [x[i] * 100 / x[0] for x in data]
        
        
        line = plt.plot(xvalues, values)[0]
        line.set_color(colors[i - 1])
        line.set_label(labels[i - 1])
        line.set_linewidth(2.0)
        lines.append(line)
    
    
    plt.xticks(range(2, len(data) + 2))
    plt.yticks(range(10, 101, 10))
    plt.axis([1.5, len(data) + 1.5, 0, 110])
    plt.title('Cobertura pel camp "%s"' % field)
    plt.ylabel('Percentatge de casos coberts')
    plt.xlabel('Exemples utilitzats')
    """

    
    

    plt.xticks(range(2, len(data) + 2))
    plt.yticks(range(20, 101, 20))
    plt.axis([1.5, len(data) + 1.5, 0, 110])
    plt.title('"%s"' % field)
    plt.ylabel('Casos coberts')
    plt.xlabel('Exemples')
"""
    
    plt.grid(True, color='#666666')
    plt.hold(False)

    
    labels.pop(0)
    labels.pop(1)
    #l = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    #plt.legend(lines, engines)
    #plt.figlegend(lines, labels, loc=4)
    #plt.show()
    #plt.legend()
    plt.savefig(''.join(['results:coverage-', field, '.pdf']), bbox_inches="tight")
