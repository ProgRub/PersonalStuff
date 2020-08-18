import tkinter as TK


class ScrollableWidget():
    DEFAULTFONT = ("Times New Roman", 12)
    DEFAULTBGCOLOR = "#061130"
    SCROLLSPEED = 30  #less=faster

    def __init__(self, frm_master, whatBoxes):
        self.whatBoxes = whatBoxes
        self.boxes = []

        self.frame = TK.Frame(frm_master, bg=ScrollableWidget.DEFAULTBGCOLOR)
        self.scrollbar = TK.Scrollbar(self.frame,
                                      command=self.scrollOutput,
                                      orient=TK.VERTICAL)
        for boxType in self.whatBoxes:
            if boxType == "Textbox":
                box = TK.Text(self.frame,
                              bg=ScrollableWidget.DEFAULTBGCOLOR,
                              fg="white",
                              font=ScrollableWidget.DEFAULTFONT,
                              yscrollcommand=self.scrollbar.set)
            elif boxType == "Listbox":
                box = TK.Listbox(self.frame,
                                 bg=ScrollableWidget.DEFAULTBGCOLOR,
                                 fg="white",
                                 font=ScrollableWidget.DEFAULTFONT,
                                 yscrollcommand=self.scrollbar.set)
            box.bind("<MouseWheel>", self.scrollOutputViaMouseWheel)
            self.boxes.append(box)

    def scrollOutput(self, *args):
        for box in self.boxes:
            box.yview(*args)

    def scrollOutputViaMouseWheel(self, event):
        for box in self.boxes:
            box.yview("scroll",
                      -1 * (event.delta // ScrollableWidget.SCROLLSPEED),
                      "units")
        return "break"