
import matplotlib.pyplot as plt #@UnresolvedImport
from matplotlib.font_manager import FontProperties #@UnresolvedImport
import numpy as np


def plot_bar(values):
    v00, v01, v02 = values

    width = v02
    xpos = 0.0
    h0 = plt.bar([xpos], [1],
                 width=width, color=colors[2], edgecolor=None,
                 linewidth=0.0)
    
    width = v01
    xpos = v02
    h1 = plt.bar([xpos], [1],
                 width=width, color=colors[1], edgecolor=None,
                 linewidth=0.0)
        
    
    width = (1.0 - v01 - v02)
    xpos = v01 + v02
    h2 = plt.bar([xpos], [1],
                 width=width, color=colors[0], edgecolor=None,
                 linewidth=0.0)
    
    return [h0, h1, h2]

def set_plot_look(values):
    plt.axis([0, 1.0, 0, 1])

    v00, v01, v02 = values
    v00 = 1 - v01 - v02

    ticks = []
    labels = []
    if v02:
        ticks.append(v02 / 2)
        labels.append(''.join([str(v02 * 100), '%']))
    if v01: 
        ticks.append(v02 + (v01 / 2))
        labels.append(''.join([str(v01 * 100), '%']))
        
    if v02 == 0.6 and v01 == 0.2:
      pass  
    elif v00: 
        ticks.append(v02 + v01 + (v00 / 2))
        labels.append(''.join([str(v00 * 100), '%']))
        
    plt.xticks(ticks, labels)
    plt.yticks([])

if __name__ == '__main__':
    labels = ['Incorrecte', 'Parcial', 'Correcte']
    #colors = ['#4272DB', '#60a63a', '#FFA615', '#7D3883']
    colors = ['#DDDDDD', '#666666', '#333333']
    #markers = ['o', '-', '^', 's']
    
    
    """
    nexamples = 2
    
    author = {'acm':            [0.0, 0.0, 1.0],
              'springer':       [0.0, 1.0, 0.0],
              'informaworld':   [1.0, 0.0, 0.0],
              'ideas':          [0.0, 0.0, 1.0]
              }
    
    journal = {'acm':           [0.0, 0.4, 0.6],
               'springer':      [0.2, 0.2, 0.6],
               'informaworld':  [1.0, 0.0, 0.0],
               'ideas':         [0.0, 0.0, 1.0]
               }
      
    title = {'acm':             [0.0, 0.0, 1.0],
             'springer':        [0.0, 0.0, 1.0],
             'informaworld':    [1.0, 0.0, 0.0],
             'ideas':           [0.0, 0.0, 1.0]
             }  

    year = {'acm':              [0.0, 0.0, 1.0],
            'springer':         [1.0, 0.0, 0.0],
            'informaworld':     [0.6, 0, 0.4],
            'ideas':            [0.6, 0, 0.4]
            }

    """
    
    ##############################################3
    
    plt.rc("font", family="cmr10")
    plt.rc("font", size=10)
    width = 4.50
    height = 1.0
    
    fig = plt.figure(figsize=(width + 1, height + 1))

    figtitle = 'Correctesa dels camps extrets (wrappers corregits)'
    fig.text(0.5, 0.88, figtitle,
             horizontalalignment='center',
             fontproperties=FontProperties(size=12))
    
    xlabel = 'Camps'
    fig.text(0.5, 0.2, xlabel,
             horizontalalignment='center',
             fontproperties=FontProperties(size=12))
    
    #ylabel = 'Bibliotca'
    #fig.text(0.02, 0.5, ylabel,
    #         verticalalignment='center',
    #         rotation='vertical',
    #         fontproperties=FontProperties(size=12))
    
    

    plt.subplots_adjust(left=0.10, top=0.65, bottom=0.46, right=0.95, hspace=1.0)
    
    #plt.title('Amb %d exemples' % nexamples) 
    bwidth = 1.0

    keys = ['acm', 'springer', 'informaworld', 'ideas']


    values = [0.0, 0.0, 1.0]

    #for i in range(len(keys)):
    #key = keys[i]
    
    bplot = 0
    
    plt.subplot(1, 4, bplot + 1)
    plt.title('"title"') 
    plt.ylabel('informaworld')
    handles = plot_bar(values)           
    set_plot_look(values)
    
    
    
    plt.subplot(1, 4, bplot + 2)
    plt.title('"author"') 
    plot_bar(values)    
    set_plot_look(values)

    plt.subplot(1, 4, bplot + 3)
    plt.title('"journal"') 
    plot_bar(values)  
    set_plot_look(values)


    plt.subplot(1, 4, bplot + 4)
    plt.title('"year"') 
    plot_bar(values)
    set_plot_look(values)

    legend = fig.legend(tuple(handles), ('Correcte', 'Parcialment correcte', 'Incorrecte'), 'lower center', ncol=3)
    legend.draw_frame(False)
    #plt.show()
    plt.savefig(''.join(['results:extraction-corrected.pdf']))
    
    print 'Finished'


