import tkinter as tk

window = tk.Tk()
window.title("XML to Tkinter")
window.geometry("800x600")

# Create a frame
frame = tk.Frame(window)
frame.grid(sticky="nsew")
frame2 = tk.Frame(window)
frame2.grid(sticky="nsew")

# Create a label
label = tk.Label(frame, text="Hello World!")
label.pack()

label = tk.Label(frame2, text="Hello World!!!!!!!!!!")
label.pack()

# Create a button
button = tk.Button(frame, text="Click Me!")
button.pack()

button = tk.Button(frame2, text="Click Me 2!")
button.pack()

window.grid_rowconfigure(0, weight=2)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

window.mainloop()