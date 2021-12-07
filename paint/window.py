import argparse
import os
import subprocess
import tkinter as tk


class PaintApp:
    def __init__(self, root, cls_label):
        self.root = root
        cls_label_unicode_list = str(cls_label.encode("unicode-escape")).split("\\")
        cls_label_unicode = cls_label_unicode_list[-1][:-1]
        self.path = f"./paint/data/{cls_label_unicode}"
        os.makedirs(self.path, exist_ok=True)
        self.save_path = "./paint/data/"
        self.setup_menu()
        self.setup_tool_bar()
        self.setup_tool_bar_buttons()
        self.setup_tol_bar_countLabel()
        self.setup_canvas_frame()
        self.bind_shortcut()
        self.old_x = None
        self.old_y = None
        self.bind_mouse()
        self.count_num = 1

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.setup_file_menu(menubar)
        self.root.config(menu=menubar)

    def setup_file_menu(self, menubar):
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="保存", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.exit)
        menubar.add_cascade(label="メニュー", menu=file_menu, underline=1)

    def exit(self):
        root.destroy()

    def setup_tool_bar(self):
        self.tool_bar = tk.Frame(self.root, width=50, bg="red")
        self.tool_bar.pack(fill="x", side="top")

    def setup_tol_bar_countLabel(self):
        self.count_text = tk.StringVar()
        self.count_text.set("dataset canvas")
        self.count_label = tk.Label(self.tool_bar, textvariable=self.count_text)
        self.count_label.pack(side="top")

    def setup_tool_bar_buttons(self):
        self.clear_button = tk.Button(self.tool_bar, text="clear", command=self.clear_canvas)
        self.clear_button.pack(side="right")

    def changeCounterText(self):
        self.count_text.set(f"{str(self.count_num).zfill(5)}.png saved! Current counter: {self.count_num+1}")

    def setup_canvas_frame(self):
        self.canvas_frame = tk.Frame(self.root, width=442, height=442, bg="white")
        self.canvas_frame.pack(expand=1, fill="both", side="right")
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=338, height=338, scrollregion=(0, 0, 600, 600))
        self.setup_scroll_bar()
        self.canvas.pack(expand=1, fill="both", side="right")
        self.canvas.create_rectangle(-10, -10, 360, 360, fill="black")

    def setup_scroll_bar(self):
        scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        scroll_x.config(command=self.canvas.xview)
        scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        scroll_y.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(-10, -10, 360, 360, fill="black")

    def bind_shortcut(self):
        self.root.bind("<Control-s>", self.save_file)

    def save_file(self, event=None):
        # file_name=filedialog.asksaveasfilename(filetypes=[("All Files",("*.ps"))],title="保存")
        file_name_ps = f"{str(self.count_num).zfill(5)}.ps"
        file_name = os.path.join(self.path, file_name_ps)
        self.canvas.postscript(file=file_name, colormode="color")
        print(file_name)
        if len(file_name) != 0:
            file_name_without_ex, _ = file_name_ps.split(".")
            # im=Image.open(io.BytesIO(ps.encode("utf-8")))
            # im.save(f"{file_name_without_ex}.png")
            subprocess.run(
                [
                    "convert",
                    os.path.join(self.path, f"{file_name_without_ex}.ps"),
                    os.path.join(self.path, f"{file_name_without_ex}.png"),
                ]
            )
            subprocess.run(["rm", os.path.join(self.path, f"{file_name_without_ex}.ps")])
            self.clear_canvas()
            self.changeCounterText()
            self.count_num += 1

    def bind_mouse(self):
        self.canvas.bind("<B1-Motion>", self.on_mouse_pressed)
        self.canvas.bind("<Button1-ButtonRelease>", self.on_mouse_released)

    def on_mouse_pressed(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(
                self.old_x,
                self.old_y,
                event.x,
                event.y,
                width=5.0,
                fill="white",
                capstyle=tk.ROUND,
                smooth=tk.TRUE,
                splinesteps=36,
            )
            # self.draw.line((self.old_x,self.old_y,event.x,event.y),fill="black",width=5)
        self.old_x = event.x
        self.old_y = event.y

    def on_mouse_released(self, event):
        self.old_x, self.old_y = None, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cls")
    args = parser.parse_args()
    os.makedirs("./paint/data", exist_ok=True)
    root = tk.Tk()
    app = PaintApp(root, args.cls)
    root.mainloop()
