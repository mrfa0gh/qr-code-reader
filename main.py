import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageGrab
from pyzbar.pyzbar import decode

def read_qr_code(filepath):
    try:
        image = Image.open(filepath)
        decoded_objects = decode(image)
        if decoded_objects:
            return "\n".join(obj.data.decode('utf-8') for obj in decoded_objects)
        else:
            return "No QR code found in the image."
    except Exception as e:
        return f"Error reading QR code: {str(e)}"

def handle_paste():
    try:
        image = ImageGrab.grabclipboard()
        if image:
            decoded_objects = decode(image)
            if decoded_objects:
                data = "\n".join(obj.data.decode('utf-8') for obj in decoded_objects)
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, data)
                # Copy to clipboard
                root.clipboard_clear()
                root.clipboard_append(data)
            else:
                messagebox.showinfo("Result", "No QR code found in the clipboard image.")
        else:
            messagebox.showerror("Error", "No image found in the clipboard.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read QR code: {e}")

def handle_file_open():
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if filepath:
        data = read_qr_code(filepath)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, data)
        # Copy to clipboard
        root.clipboard_clear()
        root.clipboard_append(data)

def handle_drop(event):
    filepath = event.data.strip('{').strip('}')
    data = read_qr_code(filepath)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, data)
    root.clipboard_clear()
    root.clipboard_append(data)

root = TkinterDnD.Tk()
root.title("QR Code Reader")
root.geometry("600x400")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

paste_button = tk.Button(button_frame, text="Read from Clipboard", command=handle_paste)
paste_button.pack(side=tk.LEFT, padx=5)

file_button = tk.Button(button_frame, text="Open File", command=handle_file_open)
file_button.pack(side=tk.LEFT, padx=5)

output_text = tk.Text(root, wrap=tk.WORD, height=15)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', handle_drop)

root.mainloop()
