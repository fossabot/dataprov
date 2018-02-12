from collections import defaultdict
from lxml import etree

class DataprovElement:
    '''
    This class describes a generic element of a dataprov object.
    This class provides basic functionalities to read/write the dataprov element.
    '''
    
    element_name = ""
    schema_file = ""
    
    def __init__(self):
        # Empty data attribute
        self.data = defaultdict()
        
        
    def from_xml(self, xml):
        '''
        Populate data attribute from the xml ElementTree object.
        '''
        return
    
    def to_xml(self):
        '''
        Create a xml ElementTree object from the data attribute. 
        '''
    
    
    def validate_xml(self, root):
        '''
        Validate an lxml object against a the XSD schema of this dataprov element.
        '''
        # Read schema file
        with open(self.schema_file, 'r') as schema_file_handler:
            xml_schema_doc = etree.parse(schema_file_handler)
        # Create XML schema
        xml_schema = etree.XMLSchema(xml_schema_doc)
        # Validate
        return xml_schema.validate(root)


    def to_string(self):
        '''
        String representation of the data
        '''
        return


    def print_xml(self, path):
        print('Element name: ', self.element_name)
        print('Schema: ', self.schema_file)
        with open(path, 'r') as xml_file:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(xml_file, parser)
            s = etree.tostring(tree, pretty_print=True)
        with open('./test.xml', 'wb') as f:
            f.write(s)
            
