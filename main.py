from references import references_list
import xml.etree.ElementTree as ET

file_name = 'Trabalho 1 - GABRIEL BRAICO DORNAS.xml'

root = ET.Element('references')

for index, item in enumerate(references_list):
    reference = ET.SubElement(root, f'reference_{index}')

    for key, value in item.items():
        child = ET.SubElement(reference, f'dc_{key}')
        child.text = str(value)

tree = ET.ElementTree(root)

ET.indent(tree, space="  ", level=0)

tree.write(file_name, encoding='utf-8', xml_declaration=True)
print(f'File "{file_name}" created.')

try:
    ET.parse(file_name)
    print('XML is well-formed')
except ET.ParseError as e:
    print('XML is NOT well-formed:', e)
