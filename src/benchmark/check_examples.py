from bibim.db import mappers, gateways
from bibim.db.session import create_session
from bibim.main.entry import ReferenceImporter

class ExampleChecker(object):
    def __init__(self):
        self.session = create_session('sqlite:///:memory:', debug=True)
        self.wg = gateways.WrapperGateway(self.session)
        self.eg = gateways.ExtractionGateway(self.session)
        
        self.min_range = 2
        self.max_range = 3
        self.example_range = range(self.min_range, self.max_range)

    def run(self):
        base_path = '/home/rxuriguera/benchmark/pages/'
        libraries = ['acm', 'citeulike', 'computerorg', 'econpapers', 'ideas', 'informaworld', 'sciencedirect', 'scientificcommons', 'springer']
        info = {}
        file_pattern = '-local.bib'
    
        for library in libraries:
            print '#### Library %s' % library
            path = ''.join([base_path, library, '/', library, file_pattern])
            print '#### Path: %s' % path
            self._check_examples(path)
        
        print 'Finished'
        
    def _check_examples(self, path):
        importer = ReferenceImporter()
        importer.import_references(path)
        url = self.session.query(mappers.Extraction.result_url).first()
        if not url:
            return
        url = url[0].rsplit('/', 1)[0]
        print url
        example_gateway = gateways.ExampleGateway(self.session, max_examples=10, max_examples_from_db=10, seconds_between_requests=0) 
        examples = example_gateway.get_examples(10, url=url, break_on_max=False)
        self._delete_imported_references()
        
    def _delete_imported_references(self):
        for extraction in self.eg.find_extractions():
            self.eg.delete(extraction)
            
            
if __name__ == '__main__':
    ec = ExampleChecker()
    ec.run()
