
import matplotlib.pyplot as plt #@UnresolvedImport
from matplotlib.font_manager import FontProperties #@UnresolvedImport

def plot_bar(values):
    v00, v01, v02 = values #@UnusedVariable

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

    v00, v01, v02 = values #@UnusedVariable
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
    nexamples = 4
    
    author = {'acm':            [0.0, 0.0, 1.0],
             'springer':        [0.0, 0.0, 1.0],
             'informaworld':    [1.0, 0.0, 0.0],
             'ideas':           [0.0, 0.0, 1.0]
             }

    journal = {'acm':           [0.0, 0.4, 0.6],
              'springer':       [0.0, 0.2, 0.8],
              'informaworld':   [0.0, 0.0, 1.0],
              'ideas':          [0.0, 0.0, 1.0]
              }
    
    title = {'acm':             [0.0, 0.0, 1.0],
               'springer':      [0.0, 0.0, 1.0],
               'informaworld':  [0.0, 0.0, 1.0],
               'ideas':         [0.0, 0.0, 1.0]
               }
    
    year = {'acm':              [0.0, 0.0, 1.0],
            'springer':         [0.25, 0.0, 0.75],
            'informaworld':     [0.6, 0.0, 0.4],
            'ideas':            [0.6, 0.0, 0.4]
            }
    
    ##############################################3
    
    plt.rc("font", family="cmr10")
    plt.rc("font", size=10)
    width = 4.50
    height = 3.30
    
    fig = plt.figure(figsize=(width + 1, height + 1))

    figtitle = 'Correctesa dels camps extrets (wrappers generats amb %d exemples)' % nexamples
    fig.text(0.5, 0.95, figtitle,
             horizontalalignment='center',
             fontproperties=FontProperties(size=12))
    
    xlabel = 'Camps'
    fig.text(0.5, 0.13, xlabel,
             horizontalalignment='center',
             fontproperties=FontProperties(size=12))
    
    ylabel = 'Biblioteques'
    fig.text(0.02, 0.5, ylabel,
             verticalalignment='center',
             rotation='vertical',
             fontproperties=FontProperties(size=12))
    
    

    plt.subplots_adjust(left=0.10, top=0.85, bottom=0.23, right=0.95, hspace=1.0)
    
    #plt.title('Amb %d exemples' % nexamples) 
    bwidth = 1.0

    keys = ['acm', 'springer', 'informaworld', 'ideas']


    for i in range(len(keys)):
        key = keys[i]
        
        bplot = i * 4
        
        plt.subplot(4, 4, bplot + 1)
        if not i: plt.title('"title"') 
        plt.ylabel(key)
        handles = plot_bar(title[key])           
        set_plot_look(title[key])
        
        
        
        plt.subplot(4, 4, bplot + 2)
        if not i: plt.title('"author"') 
        plot_bar(author[key])    
        set_plot_look(author[key])
    
        plt.subplot(4, 4, bplot + 3)
        if not i: plt.title('"journal"') 
        plot_bar(journal[key])  
        set_plot_look(journal[key])
    
    
        plt.subplot(4, 4, bplot + 4)
        if not i: plt.title('"year"') 
        plot_bar(year[key])
        set_plot_look(year[key])

    legend = fig.legend(tuple(handles), ('Correcte', 'Parcialment correcte', 'Incorrecte'), 'lower center', ncol=3)
    legend.draw_frame(False)
    #plt.show()
    plt.savefig(''.join(['results:extraction-', str(nexamples), '.pdf']))
    
    print 'Finished'


