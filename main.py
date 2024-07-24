import cv2
import tkinter as tk
from tkinter import OptionMenu, StringVar
from PIL import Image, ImageTk

class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam App")
        
        self.available_sources = self.get_available_video_sources()
        self.selected_source = StringVar(root)
        self.selected_source.set(self.available_sources[0][0])
        self.selected_source.trace('w', self.change_source)
        
        self.vid = cv2.VideoCapture(self.available_sources[0][1])
        
        self.canvas = tk.Canvas(root)
        self.canvas.pack()
        
        self.source_menu = OptionMenu(root, self.selected_source, *[source[0] for source in self.available_sources])
        self.source_menu.pack(pady=5)
        
        self.update()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_available_video_sources(self):
        sources = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                sources.append((f"Camera {i}", i))
                cap.release()
        return sources

    def change_source(self, *args):
        self.vid.release()
        source_id = next(source[1] for source in self.available_sources if source[0] == self.selected_source.get())
        self.vid = cv2.VideoCapture(source_id)
        
        # Adjust canvas size according to the new video source
        width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas.config(width=width, height=height)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(10, self.update)

    def on_closing(self):
        self.vid.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root)
    root.mainloop()
