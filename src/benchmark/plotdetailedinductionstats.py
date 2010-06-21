
import matplotlib.pyplot as plt #@UnresolvedImport
from matplotlib.font_manager import FontProperties #@UnresolvedImport
import numpy as np

def set_plot_look(i=0, y=4):
    plt.axis([-0.5, 3, 0, y])
    labels = ('Ca', 'Cb', 'Cc') if i == 3 else ('', '', '')
    
    plt.xticks(np.arange(3) + (bwidth / 2), labels) #@UndefinedVariable
    plt.yticks(range(1, y))


if __name__ == '__main__':
    labels = ['Confian\c{c}a$< 0.25$',
              '$0.25\\leq$Confian\\c{c}a$<0.5$',
              '$0.5 \\leq$Confian\\c{c}a$< 0.75$',
              '$0.75 \\leq$Confian\\c{c}a', ]
    #colors = ['#4272DB', '#60a63a', '#FFA615', '#7D3883']
    colors = ['#666666', '#60a63a', '#999999', '#333333']
    #markers = ['o', '-', '^', 's']
    

    
  
    nexamples = 2
    y = 5
    title = {'acm':             [0, 0, 1, 2],
             'springer':        [0, 0, 0, 2],
             'informaworld':    [0, 0, 0, 2],
             'ideas':           [0, 0, 0, 2]
             }

    author = {'acm':            [0, 0, 0, 2],
              'springer':       [0, 0, 0, 1],
              'informaworld':   [0, 0, 2, 0],
              'ideas':          [0, 0, 2, 1]
              }
    
    journal = {'acm':           [0, 0, 1, 1],
               'springer':      [0, 0, 0, 1],
               'informaworld':  [1, 0, 0, 3],
               'ideas':         [0, 0, 0, 1]
               }
    
    year = {'acm':              [0, 0, 2, 1],
            'springer':         [0, 0, 2, 0],
            'informaworld':     [0, 0, 0, 2],
            'ideas':            [0, 0, 1, 1]
            }
    
    """ 
    nexamples = 4
    y = 5
    title = {'acm':             [0, 1, 0, 2],
             'springer':        [0, 0, 0, 2],
             'informaworld':    [0, 1, 0, 2],
             'ideas':           [0, 0, 0, 2]
             }

    author = {'acm':            [0, 2, 1, 1],
              'springer':       [0, 2, 0, 1],
              'informaworld':   [0, 2, 1, 0],
              'ideas':          [0, 3, 0, 1]
              }
    
    journal = {'acm':           [0, 14, 0, 2],
               'springer':      [1, 0, 0, 1],
               'informaworld':  [1, 2, 1, 2],
               'ideas':         [0, 0, 0, 1]
               }
    
    year = {'acm':              [0, 3, 0, 2],
            'springer':         [0, 6, 0, 2],
            'informaworld':     [0, 1, 1, 1],
            'ideas':            [0, 1, 2, 0]
            }
    
      
    nexamples = 6
    y = 5
    title = {'acm':             [1, 0, 1, 1],
             'springer':        [0, 0, 0, 2],
             'informaworld':    [2, 0, 1, 2],
             'ideas':           [0, 0, 0, 2]
             }

    author = {'acm':            [5, 1, 1, 1],
              'springer':       [2, 0, 1, 1],
              'informaworld':   [3, 1, 0, 0],
              'ideas':          [3, 0, 0, 1]
              }
    
    journal = {'acm':           [12, 2, 0, 2],
               'springer':      [4, 0, 0, 1],
               'informaworld':  [5, 1, 1, 1],
               'ideas':         [0, 0, 0, 1]
               }
    
    year = {'acm':              [4, 0, 1, 1],
            'springer':         [4, 4, 0, 2],
            'informaworld':     [1, 0, 4, 0],
            'ideas':            [1, 2, 1, 0]
            }
    """ 
    plt.rc("font", family="cmr10")
    plt.rc("font", size=10)
    width = 4.50
    height = 4.50
    
    fig = plt.figure(figsize=(width + 1, height + 1))
    
    
    figtitle = 'Wrappers generats amb %d exemples' % nexamples
    fig.text(0.55, 0.95, figtitle,
             horizontalalignment='center',
             fontproperties=FontProperties(size=12))
    
    xlabel = 'Camps'
    fig.text(0.55, 0.17, xlabel,
             horizontalalignment='center',
             fontproperties=FontProperties(size=12))
    
    ylabel = 'Biblioteques'
    fig.text(0.02, 0.5, ylabel,
             verticalalignment='center',
             rotation='vertical',
             fontproperties=FontProperties(size=12))
    
    
    cLegend = 'Ca: $0.25\\leq$Confidence$ < 0.50$'
    fig.text(0.37, 0.10, cLegend,
             horizontalalignment='left',
             fontproperties=FontProperties(size=12))
    
    cLegend = 'Cb: $0.50 \\leq$Confidence$< 0.75$'
    fig.text(0.37, 0.06, cLegend,
             horizontalalignment='left',
             fontproperties=FontProperties(size=12))
    
    cLegend = 'Cc: $0.75 \\leq$Confidence'
    fig.text(0.37, 0.02, cLegend,
             horizontalalignment='left',
             fontproperties=FontProperties(size=12))
    
    plt.subplots_adjust(left=0.14, top=0.88, bottom=0.27, right=0.98)
    
    #plt.title('Amb %d exemples' % nexamples) 
    bwidth = 0.5
    color = '#888888'


    keys = ['acm', 'springer', 'informaworld', 'ideas']


    for i in range(len(keys)):
        key = keys[i]
        
        bplot = i * 4
        
        plt.subplot(4, 4, bplot + 1)
        if not i: plt.title('"title"') 
        plt.ylabel(key)
        h = plt.bar([0, 1, 2], title[key][1:], width=bwidth, color=color,
                    linewidth=0.0)
        set_plot_look(i, y)
        
        plt.subplot(4, 4, bplot + 2)
        if not i: plt.title('"author"') 
        h = plt.bar([0, 1, 2], author[key][1:], width=bwidth, color=color,
                    linewidth=0.0)
        set_plot_look(i, y)
    
        plt.subplot(4, 4, bplot + 3)
        if not i: plt.title('"journal"') 
        h = plt.bar([0, 1, 2], journal[key][1:], width=bwidth, color=color,
                    linewidth=0.0)
        set_plot_look(i, y)
    
    
        plt.subplot(4, 4, bplot + 4)
        if not i: plt.title('"year"') 
        h = plt.bar([0, 1, 2], year[key][1:], width=bwidth, color=color,
                    linewidth=0.0)
        set_plot_look(i, y)



    #plt.show()
    plt.savefig(''.join(['results:nwrappers-', str(nexamples), '.pdf']))
    print 'Finished'
