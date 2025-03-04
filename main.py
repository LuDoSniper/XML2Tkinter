from . import converter

def toggle(label, button):
    label.config(text="Disabled" if label.cget("text") == "Enabled" else "Enabled")
    button.config(state=f"{'active' if label.cget('text') == 'Enabled' else 'disabled'}")

def add(label):
    label.config(text=str(int(label.cget("text"))+1))

actions = {
    'toggle': toggle,
    'add': add
}

converter.render("xml2tkinter/interfaces/test.xml", actions=actions)
