"""
conda env
    conda create --name qr-enc-dec --yes
    conda activate qr-enc-dec
    conda install python==3.10.10 --yes

pip install
    pip install pillow opencv-python
    pip install qrcode pyzbar

on windows
    // #include <direct.h>
    #include <windows.h>
    int main(int argc, char** argv) {
        // chdir("D:");
        system("C:\\path\\to\\pythonw.exe C:\\path\\to\\script.py");
        return 0;
    }
"""

import io
import tkinter as tk

from PIL import Image, ImageTk
import qrcode


GLOBAL_PHOTO = None


def make(document):
    buffer = io.BytesIO()
    qrc = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=16,
        border=4,
    )
    qrc.add_data(document)
    qrc.make(fit=True)
    qrc_img = qrc.make_image(fill_color="black", back_color="white")
    qrc_img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def present(frame, entry):
    for widget in frame.winfo_children():
        widget.destroy()

    document = entry.get()
    buffer = make(document)

    image = Image.open(buffer)
    photo = ImageTk.PhotoImage(image)

    global GLOBAL_PHOTO
    GLOBAL_PHOTO = photo

    label = tk.Label(frame, image=photo)
    label.pack()


def main():
    root = tk.Tk()
    root.title("qrcode display")

    upper = tk.Frame(root)
    upper.pack()

    lower = tk.Frame(root)
    lower.pack()

    entry = tk.Entry(upper)
    entry.pack()

    button = tk.Button(upper, text="qr encode", command=lambda: present(lower, entry))
    button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
