from . import converter

def display():
    print("caca")

def add(frame):
    frame.config(text=str(int(frame.cget("text"))+1))

actions = {
    'display': display,
    'add': add
}

converter.render("xml2tkinter/interfaces/test.xml", actions=actions)
