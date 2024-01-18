from bs4 import BeautifulSoup

def parse_html_string(html_string: str):
    # Create a BeautifulSoup object
    html_string = html_string.strip()
    items = html_string.split("\n")

    for i in range(len(items)):
        items[i] = items[i].strip()
    
    html_string = " ".join(items)

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
            if len(element.contents) == 1 and not element.contents[0].name:
                result["text"] = str(element.contents[0]).strip()
            else:
                result['children'] = [build_tree(child) for child in element.contents if child.name is not None]
        return result
    
    # Build the tree dictionary starting from the root
    tree_dict = build_tree(soup)
    return tree_dict.get("children", [])  # Return an empty list if "children" key is not present