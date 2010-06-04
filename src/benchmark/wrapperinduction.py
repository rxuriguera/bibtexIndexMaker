
from datetime import datetime
import simplejson #@UnresolvedImport

from bibim.db.session import create_session
from bibim.db import mappers, gateways
from bibim.main.entry import ReferenceImporter
from bibim.main.entry import WrapperGenerator


class WrapperInductionStats(object):
    def __init__(self):
        self.session = create_session('sqlite:///:memory:', debug=True)
        self.wg = gateways.WrapperGateway(self.session)
        self.eg = gateways.ExtractionGateway(self.session)
        
        self.min_range = 2
        self.max_range = 7
        self.example_range = range(self.min_range, self.max_range)
        
        self.fields = ['addres', 'author', 'isbn', 'issn', 'journal', 'number', 'pages', 'publisher', 'title', 'volume', 'year']
        
    def run(self):
        base_path = '/home/rxuriguera/benchmark/pages/'
        libraries = ['springer']#['acm', 'citeulike', 'computerorg', 'econpapers', 'ideas', 'informaworld', 'sciencedirect', 'scientificcommons', 'springer']
        
        info = {}
        file_pattern = '-local.bib'
        self.file = open(base_path + 'resultsspr2.csv', 'w')
    

        for library in libraries:
            print '#### WRAPPERS FOR LIBRARY %s' % library
            start = datetime.now()
            self.file.write('Library:;%s\n' % library)
            info[library] = self._library_run(''.join([base_path, library, '/', library, file_pattern]))
            now = datetime.now() 
            self.file.write('Library Elapsed time:;%s\n' % (str(now - start)))
            self.file.write('\n\n')

        """
        info = {'citeulike': [{u'title': [3.0, 0, 0, 0, 3, 0.0, 0.0, 0.0, 1.0]},
                              {u'title': [3.0, 0, 0, 0, 3, 0.0, 0.0, 0.0, 1.0]}],
                'acm': [{u'title': [4.0, 2, 0, 1, 1, 0.5, 0.0, 0.25, 0.25]},
                        {u'title': [5.0, 2, 0, 2, 1, 0.40000000000000002, 0.0, 0.40000000000000002, 0.20000000000000001],
                         u'pub': [5.0, 2, 0, 2, 1, 0.60000000000000002, 0.0, 0.40000000000000002, 0.0]}]}
        """
        self.file.write('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n')
        print info
        self._lib_stats(info)
        self._field_stats(info)
        self.file.close()
        pass
    
    def _lib_stats(self, info):
        cases = self.max_range - self.min_range
        stats = [{} for x in range(cases)]
        
        # info = dict of libraries
        #                    library = list of example_range_data
        #                    ex_range_data = dict of fields
        #                    field = [total, conf1-4, avg1-4]
        
        for lib_info in info.values():
            for case, index in zip(lib_info, range(len(lib_info))):
                for field, value in zip(case.keys(), case.values()):
                    v = stats[index].setdefault(field, [0.0, 0.0, 0.0, 0.0, 0.0])
                    print value
                    
                    v[4] += 1
                    
                    if float(value[8]):
                        v[3] += 1
                    elif float(value[7]):
                        v[2] += 1
                    elif float(value[6]):
                        v[1] += 1
                    elif float(value[5]):
                        v[0] += 1

        for stat, index in zip(stats, range(cases)):
            
            print '\n\nUsing %d examples:' % (index + self.min_range) 
            self.file.write('Wrapper generation using %d examples\n' % (index + self.min_range))
            for field in stat:
                total = stat[field][4]
                line = ''.join([field, ';', str(stat[field][0] / total), ';', str(stat[field][1] / total), ';', str(stat[field][2] / total), ';', str(stat[field][3] / total)])
                print line
                self.file.write(line + '\n')
            self.file.write('\n')

    
    def _field_stats(self, info):
        stats = {}
        cases = self.max_range - self.min_range
        for field in self.fields:
            print '\n\nStats for field: %s' % field
            self.file.write('\n\nStats for field: %s\n' % field)
            field_stats = stats.setdefault(field, [])
            
            self.file.write('[')
            for case in range(cases):
                field_case_stats = [0.0, 0.0, 0.0, 0.0, 0.0]
                field_stats.append(field_case_stats)
                for lib_info in info.values():
                    if lib_info[case].has_key(field):
                        field_info = lib_info[case][field]
                        field_case_stats[0] += 1
                        if float(field_info[8]):
                            field_case_stats[4] += 1
                        elif float(field_info[7]):
                            field_case_stats[3] += 1
                        elif float(field_info[6]):
                            field_case_stats[2] += 1
                        elif float(field_info[5]):
                            field_case_stats[1] += 1
                print 'Using %d exampes' % (case + self.min_range)
                
                print simplejson.dumps(field_case_stats)
                self.file.write(simplejson.dumps(field_case_stats))
                self.file.write(',\n')
            self.file.write(']')
            
    def _library_run(self, path):
    
        library_data = []
        
        importer = ReferenceImporter()
        
        importer.import_references(path)
        url = self.session.query(mappers.Extraction.result_url).first()
        if not url:
            return
        url = url[0].rsplit('/', 1)[0]
        print url
        generator = WrapperGenerator(url)
        
        for i in self.example_range:
            print '#### WRAPPERS USING %d EXAMPLES' % i
            start = datetime.now()
            self.file.write('Using %d examples\n' % i)

            generator.set_wrapper_gen_examples(i)
            generator.generate_wrappers()
            library_data.append(self._get_wrappers_info(url))
            #self.session = create_session('sqlite:///:memory:', debug=True)
            self._delete_generated_wrappers(url)
            now = datetime.now() 
            self.file.write('Elapsed time:;%s\n\n' % (str(now - start)))
            self.file.flush()
        
        self._delete_imported_references()
            
        return library_data
        
    def _get_wrappers_info(self, url):
        collections_info = {}
        for collection in self.wg.find_wrapper_collections(url):
            total = float(len(collection.wrappers))
            
            con01 = len([x for x in collection.wrappers if x.score < 0.25])
            con02 = len([x for x in collection.wrappers if 0.25 <= x.score < 0.5])
            con03 = len([x for x in collection.wrappers if 0.5 <= x.score < 0.75])
            con04 = len([x for x in collection.wrappers if 0.75 <= x.score])
            
            avg01 = con01 / total
            avg02 = con02 / total
            avg03 = con03 / total
            avg04 = con04 / total
            
            collections_info[collection.field] = [total,
                                                  con01, con02, con03, con04,
                                                  avg01, avg02, avg03, avg04]
            self.file.write(''.join([collection.field, ';',
                                     str(total), ';',
                                     str(con01), ';', str(con02), ';',
                                     str(con03), ';', str(con04), ';',
                                     str(avg01), ';', str(avg02), ';',
                                     str(avg03), ';', str(avg04), '\n']))
        return collections_info
    
    def _delete_generated_wrappers(self, url):
        for collection in self.wg.find_wrapper_collections(url):
            self.wg.delete(collection)
    
    def _delete_imported_references(self):
        for extraction in self.eg.find_extractions():
            self.eg.delete(extraction)

if __name__ == '__main__':
    s = WrapperInductionStats()
    s.run()
