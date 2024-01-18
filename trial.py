# from tags_dict import *

# print(Div(id="div1", className="container", style={"border": "1px solid black"}, children = [
#     P(id="para", className="text-lg font-bold", innerHTML="Hi there", style={"color": "white"}),
#     P(id="para", className="text-lg font-bold", innerHTML="Hi there", style={"color": "white"})
# ]))

from bs4 import BeautifulSoup
from document import HTMLElement, Document
from elem_attrs import attributes, getreverse

doc = Document()
def buildElem(tree):
    elem_tree = []
    for item in tree:
        elem = HTMLElement(item['tag'], doc, innerHTML="")
        for attribute, value in item.get('attributes', {}).items():
            setattr(elem, getreverse(attribute), value)
        elem.children = buildElem(item.get('children', []))
        elem_tree.append(elem)
    return elem_tree

    

def parse_html_string(html_string):
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # Define a function to recursively build the tree dictionary
    def build_tree(element):
        result = {'tag': element.name}
        if element.attrs:
            for i, j in element.attrs.items():
                if type(j) == list:
                    element.attrs[i] = " ".join(j)
            result['attributes'] = element.attrs
        if element.contents:
            result['children'] = [build_tree(child) for child in element.contents if child.name is not None]
        return result
    
    # Build the tree dictionary starting from the root
    tree_dict = build_tree(soup)

    items = buildElem(tree_dict['children'])
    return items

# Example usage
html_string = '<div id="div1" class="container hi"><h1>Title</h1><p>Paragraph</p></div>'
tree = parse_html_string(html_string)
print(tree)
