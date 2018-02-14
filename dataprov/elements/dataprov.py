import os
from collections import defaultdict
from dataprov.elements.generic_element import GenericElement
from dataprov.elements.file import File
from dataprov.elements.history import History
from dataprov.definitions import XML_DIR
from lxml import etree


class Dataprov(GenericElement):
    '''
    Class describing the whole dataprov element.
    This class handles the parsing of input dataprov metadata files.
    
    A datprov model consists of:
    - a 'target': The file which provenance data gets provided
    - a 'history': A list of operations that lead to the target file
    '''
    
    element_name = "dataprov"
    schema_file = os.path.join(XML_DIR, 'dataprov_element.xsd')
    
    def __init__(self, file=None):
        '''
        Initialize an empty object or read directly from file
        '''
        super().__init__()
        if file:
            with open(file, 'r') as xml_file:
                parser = etree.XMLParser()
                tree = etree.parse(xml_file, parser)
                self.from_xml(tree.getroot())
    
    
    def from_xml(self, root, validate=True):        
        self.data = defaultdict()
        # Validate XML against schema
        if validate and not self.validate_xml(root):
            print("XML document does not match XML-schema")
            exit(1)
            
        # Traverse the tree
        # Just for testing
        for child in root:
            print(child.tag)
        
        # Get the target from the xml
        target_ele = root.find('target')
        target = File()
        target.from_xml(target_ele, validate=False)
        self.data['target'] = target
        
        # Get the history from xml
        history_ele = root.find('history')
        history = History()
        history.from_xml(history_ele, validate=False)
        self.data['history'] = history
        

    def to_xml(self):
        '''
        Create a xml ElementTree object from the data attribute. 
        '''
        root = etree.Element(self.element_name)
        # Target
        target_ele = self.data['target'].to_xml()
        target_ele.tag = "target"
        root.append(target_ele)
        # History
        root.append(self.data['history'].to_xml())
        return root