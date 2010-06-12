
import re
import simplejson #@UnresolvedImport

from bibim.db.session import create_session
from bibim.db import mappers, gateways
from bibim.main.entry import ReferenceImporter
from bibim.main.entry import WrapperGenerator
from bibim.ir.types import SearchResult
from bibim.main.factory import UtilFactory, UtilCreationError
from bibim.main.controllers import IEController, ReferencesController
from bibim.main.entry import WrapperGenerator

class ExtractionStats(object):
    def __init__(self):

        self.info = {}
        
        self.nexamples = 4
        self.base_path = '/home/rxuriguera/benchmark/pages/'
        self.fields = ['addres', 'author', 'isbn', 'issn', 'journal', 'number', 'pages', 'publisher', 'title', 'volume', 'year']
        self.libraries = ['informaworld']#['acm', 'citeulike', 'computerorg', 'econpapers', 'ideas', 'informaworld', 'sciencedirect', 'scientificcommons', 'springer']
        
        self.factory = UtilFactory()
        self.iec = IEController(self.factory, secs_between_reqs=0,
                                wrapper_gen_examples=self.nexamples)
        self.rec = ReferencesController(self.factory)

    def save_msg(self, msg):
        print msg
        self.file.write(''.join([msg, '\n']))
        self.file.flush()
        
    def run(self):
        self.info = {}

        for library in self.libraries:
            lib_info = self.info.setdefault(library, [])
            
            self.run_library(library)
        
        
        
    def run_library(self, library):
        self.file = open(''.join([self.base_path, library, '/extraction-results-', str(self.nexamples), '-corrected.csv']), 'w')
        self.session = create_session(''.join(['sqlite:///', self.base_path, '/', library, '/extraction-stats-', library, '-', str(self.nexamples), '-corrected.db']), debug=True)
        #self.session = create_session('sqlite:///:memory:', debug=True)
        self.wg = gateways.WrapperGateway(self.session)
        self.eg = gateways.ExtractionGateway(self.session)

        
        
        self.save_msg('Extraction results for library: %s' % library)
        
        files = open(''.join([self.base_path, library, '/', 'filelist.txt']), 'r')
        html_url, text_file = files.readline().split(' ', 1)
        files.seek(0)
        url = html_url.rsplit('/', 1)[0]
        
        
        #self.import_generate(library, url)
        

        
        references = []
        for line in files.readlines():
            line = line.strip()
            html_url, text_file = line.split(' ', 1)
            
            text_file = open(text_file, 'r')
            text = text_file.read()
            text_file.close()
            
            top_results = [SearchResult('Some result', html_url)]
            print html_url

            refs, result = self.iec.extract_reference(top_results, text)
            
            if refs:
                references.append(refs[0])
            else:
                references.append(None)
            
        # Load control references
        control_file = ''.join([self.base_path, library, '/extraction-results-control.bib'])
        control = self.rec._parse_entries_file(control_file)
         
        for control, extracted in zip(control, references):
            if not extracted:
                continue
            
            self.save_msg(extracted.entry)
            self.save_msg('\n')
            
            total_control_fields = 0
            total_extracted_fields = 0
            
            correct = 0
            parcial = 0
            error = 0
            
            valid = 0
            invalid = 0
            
            for field in control.fields:
                if field in ['url', 'reference_type', 'reference_id']:
                    continue
                
                control_value = control.get_field(field)
                total_control_fields += 1
                
                extracted_value = extracted.get_field(field)
                if not extracted_value:
                    continue
                
                if extracted_value.valid:
                    valid += 1
                else:
                    invalid += 1
                
                control_value = control_value.value
                extracted_value = extracted_value.value
                
                if type(control_value) is list:
                    self.save_msg('Comparing field %s values:\n\t%s\n\t%s' % (field, simplejson.dumps(control_value), simplejson.dumps(extracted_value)))
                    self.save_msg('\tCHECK MANUALLY')
                    continue
                
                control_value = control_value.strip()
                extracted_value = extracted_value.strip()
                
                control_regex = re.escape(control_value)
                extracted_regex = re.escape(extracted_value)
                
                self.save_msg('Comparing field %s values:\n\t%s\n\t%s' % (field, control_value, extracted_value))
                
                if control_value == extracted_value:
                    correct += 1
                    self.save_msg('\tCorrect')
                elif re.search(control_regex, extracted_value): #or re.match(extracted_regex, control_value):
                    parcial += 1
                    self.save_msg('\tParcial')
                else:
                    error += 1
                    self.save_msg('\tIncorrect')
                
                total_extracted_fields += 1
            
            self.save_msg('')
            self.save_msg('Marked Valid;Marked invalid')
            self.save_msg('%d;%d' % (valid, invalid))
            
            self.save_msg('Total available;Total extracted;Incorrect;Parcial;Correct')
            self.save_msg('%d;%d;%d;%d;%d' % (total_control_fields, total_extracted_fields, error, parcial, correct))
            
            self.save_msg('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
        self.file.close()
        
        
    def import_generate(self, library, url):
        # Import references
        importer = ReferenceImporter()
        importer.import_references(''.join([self.base_path, library, '/', library, '-', str(self.nexamples), '.bib']))
        
        # Generate wrappers
        generator = WrapperGenerator(url)
        generator.set_wrapper_gen_examples(self.nexamples)
        generator.generate_wrappers()    
        
        
if __name__ == '__main__':
    s = ExtractionStats()
    s.run()
