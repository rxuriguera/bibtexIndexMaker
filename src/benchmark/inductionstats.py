'''
Created on 26/05/2010

@author: rxuriguera
'''

def run():
    file = open('/home/rxuriguera/benchmark/pages/4examples.csv')
    data = {}
    confidence_coverage = {}
    files = {}
    
    distinct_confidence_coverage = {}
    
    for line in file.readlines():
        line = line.strip()
        if line == '':
            continue

        line = line.split(';')
        
        confidence_coverage.setdefault(line[0], [0.0, 0.0, 0.0, 0.0])
        if float(line[6]):
            confidence_coverage[line[0]][0] += 1
        if float(line[7]):
            confidence_coverage[line[0]][1] += 1
        if float(line[8]):
            confidence_coverage[line[0]][2] += 1
        if float(line[9]):
            confidence_coverage[line[0]][3] += 1
            
        files.setdefault(line[0], 0.0)
        files[line[0]] += 1
        
        values = data.setdefault(line[0], ([], [], [], []))
        values[0].append(float(line[6]))
        values[1].append(float(line[7]))
        values[2].append(float(line[8]))
        values[3].append(float(line[9]))
        

        distinct_coverage = distinct_confidence_coverage.setdefault(line[0], [0.0, 0.0, 0.0, 0.0])
        if float(line[9]):
            distinct_coverage[3] += 1
        elif float(line[8]):
            distinct_coverage[2] += 1
        elif float(line[7]):
            distinct_coverage[1] += 1
        elif float(line[6]):
            distinct_coverage[0] += 1

            
            
    print data
    print confidence_coverage
    print files
    
    #print 'No confidence'
    #for l, x, y in zip(confidence_coverage.keys(), confidence_coverage.values(), files.values()):
        #print '%9s %f' % (l, (x[0] / y))

    #print
    #print 'Low confidence'
    #for l, x, y in zip(confidence_coverage.keys(), confidence_coverage.values(), files.values()):
        #print '%9s %f' % (l, (x[1] / y))

    #print
    #print 'Confident'
    for l, x, y in zip(confidence_coverage.keys(), confidence_coverage.values(), files.values()):
        #print '%9s %f' % (l, (x[2] / y))        
        print ''.join([l, ';', str(x[0] / y), ';', str(x[1] / y), ';', str(x[2] / y), ';', str(x[3] / y)])
        
    print
    print

    for l, x, y in zip(confidence_coverage.keys(), distinct_confidence_coverage.values(), files.values()):
        #print '%9s %f' % (l, (x[2] / y))        
        print ''.join([l, ';', str(x[0] / y), ';', str(x[1] / y), ';', str(x[2] / y), ';', str(x[3] / y)])


if __name__ == '__main__':
    run()
