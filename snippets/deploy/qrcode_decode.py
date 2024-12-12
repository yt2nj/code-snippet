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

import traceback
from datetime import datetime
import tkinter as tk
import tkinter.font as tk_font
from tkinter import scrolledtext

import cv2
from pyzbar import pyzbar


def fetch():
    capture = cv2.VideoCapture(0)
    readable = []
    errormsg = []

    while True:
        try:
            # get raw webcam frame
            ret, frame = capture.read()
            if not ret:
                raise cv2.error("video capture fail")

            # flip frame and display
            frame = cv2.flip(frame, 1)
            cv2.imshow("webcam", frame)
            key = cv2.waitKey(333)

            # close window if triggered
            flag_press_q = key in (ord("q"), ord("Q"))
            flag_click_x = cv2.getWindowProperty("webcam", cv2.WND_PROP_VISIBLE) < 1
            if any((flag_press_q, flag_click_x)):
                break

            # decode and make readable
            decoded = pyzbar.decode(frame)
            current = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
            if decoded:
                for qrcode in decoded:
                    readable.append((current, qrcode.data))
                break

        except:
            errormsg.append((current, traceback.format_exc()))

    capture.release()
    cv2.destroyAllWindows()
    return readable, errormsg


def main():
    readable, errormsg = fetch()
    if not any((readable, errormsg)):
        return

    root = tk.Tk()
    root.title("webcam qrcode decode result")

    frame = tk.Frame(root)
    frame.pack(padx=8, pady=8)

    text_widget = scrolledtext.ScrolledText(frame, state="normal", width=64, height=16)
    text_widget.pack()

    for stamp, binary in readable:
        text_widget.insert(tk.END, "@ {}\n".format(stamp), "inverse")
        escaped = repr(binary.decode("utf-8"))[1:-1]
        escaped = "\n".join(escaped.split("\\n"))
        text_widget.insert(tk.END, "{}\n".format(escaped), "blue")
        escaped = repr(binary)[2:-1]
        text_widget.insert(tk.END, "{}\n".format(escaped), "green")

    for stamp, msg in errormsg:
        text_widget.insert(tk.END, "@ {}\n".format(stamp), "inverse")
        text_widget.insert(tk.END, "{}\n".format(msg), "red")

    text_widget.config(state="disabled", font=tk_font.Font(family="Fixedsys", size=16))

    text_widget.tag_config("inverse", background="black", foreground="white")
    text_widget.tag_config("blue", background="white", foreground="blue")
    text_widget.tag_config("green", background="white", foreground="green")
    text_widget.tag_config("red", background="white", foreground="red")

    root.mainloop()


if __name__ == "__main__":
    main()
