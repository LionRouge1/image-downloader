import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Hello Window")

# Create a label widget with the text "Hello, World!"
label = tk.Label(root, text="Hello, World!", font=("Helvetica", 16))

# Place the label in the window
label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
