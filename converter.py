import tkinter as tk
import xml.etree.ElementTree as ET
import ast

def parse(file_path: str) -> ET:
    try:
        tree = ET.parse(file_path)
        return tree
    except Exception as e:
        raise Exception(f"Error while parsing file : {e}")

def get_direct_children(node: ET.Element) -> list:
    return list(node)

def get_children(node: ET.Element) -> list:
    childs = []
    if len(list(node)) == 0:
        return [node]
    for child in node:
        childs.extend(get_children(child))
    return childs

def generate_nodes(container, node: ET.Element, parent=None, actions: dict[str: callable]|None = None, named_elements: dict[str: any] = {}) -> dict[str: any]:
    if node.tag == 'frame':
        frame = tk.Frame(container, border=1, relief="sunken")
        if 'weight' in node.attrib:
            y = list(parent).index(node)
            container.grid_rowconfigure(y, weight=int(node.attrib['weight']))
            frame.grid(sticky="nsew")
        else:
            frame.pack()
        if 'name' in node.attrib:
            named_elements[node.attrib['name']] = frame
        for child in node:
            named_elements.update(generate_nodes(frame, child, parent=node, actions=actions, named_elements=named_elements))
    
    elif node.tag == 'label':
        label = tk.Label(container, text=node.text)
        label.pack()
        if 'name' in node.attrib:
            named_elements[node.attrib['name']] = label
    
    elif node.tag == 'button':
        command = "" # Valeur par défaut de TKinter
        args = None

        button = tk.Button(container, text=node.text)
        if 'name' in node.attrib:
            named_elements[node.attrib['name']] = button
        if 'args' in node.attrib:
            args = ast.literal_eval(node.attrib['args'])
            new_args = {}
            for key, value in args.items():
                if value in named_elements:
                    new_args[key] = named_elements[value]
                else:
                    raise ValueError(f"Element '{key}' not found in named elements.")
        if 'action' in node.attrib:
            if actions is not None and node.attrib['action'] in actions:
                if args:
                    command = lambda: actions[node.attrib['action']](**new_args)
                else:
                    command = actions[node.attrib['action']]
            else:
                raise ValueError(f"Action '{node.attrib['action']}' not found in actions.")
        button.config(command=command)
        button.pack()
    
    else:
        raise Exception(f"Invalid tag '{node.tag}'.")
    
    return named_elements

def render(path: str, actions: dict[str: callable]|None = None) -> None:
    tree = parse(path)

    # Check root tag
    root = tree.getroot()
    if root.tag != 'tkinter':
        raise ValueError("Root tag must be 'tkinter'.")

    # Get parameters
    title = "XML to Tkinter"
    geometry = "300x300"
    body = None

    childs = get_direct_children(root)
    if len(childs) == 0:
        raise ValueError("Root tag must have at least one child.")
    for child in childs:
        if child.tag == 'head':
            for subchild in child:
                if subchild.tag == 'title':
                    title = subchild.text
                elif subchild.tag == 'geometry':
                    geometry = subchild.text
                else:
                    raise ValueError("Head tag can only have 'title' and 'geometry' tags as children.")
                
                if len(subchild) != 0:
                    raise ValueError("Title and Geometry tags can't have children.")
        elif child.tag == 'body':
            body = child
        else:
            raise ValueError("Root tag can only have 'head' and 'body' tags as children.")

    window = tk.Tk()
    window.title(title)
    window.geometry(geometry)
    elements = {}
    for child in body:
        elements.update(generate_nodes(window, child, parent=body, actions=actions))
    window.mainloop()

# for child in get_children(root):
#     print(f"Tag: {child.tag}, Attrs: {child.attrib}, Text: {child.text}")