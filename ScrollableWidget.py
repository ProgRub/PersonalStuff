import tkinter as TK


class ScrollableWidget():
    DEFAULTFONT = ("Times New Roman", 12)
    DEFAULTBGCOLOR = "#061130"
    SCROLLSPEED = 25  #less=faster

    def __init__(self, frm_master: TK.Frame, whatBoxes :list):
        self.whatBoxes = whatBoxes #the list of how many and what boxes to create (either Listbox or Text)
        self.boxes = [] #the list of actual boxes (TK entities) created

        self.frame = TK.Frame(frm_master, bg=ScrollableWidget.DEFAULTBGCOLOR)
        self.scrollbar = TK.Scrollbar(self.frame,
                                      command=self.scrollOutput,
                                      orient=TK.VERTICAL) #the scrollbar that is controlling all boxes
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
            box.bind("<MouseWheel>", self.scrollOutputViaMouseWheel) #this makes sure we can scroll the boxes with the mouse wheel
            self.boxes.append(box)

    def scrollOutput(self, *args): #method to change the y view of the boxes by clicking and dragging the scrollbar
        for box in self.boxes:
            box.yview(*args)

    def scrollOutputViaMouseWheel(self, event): #method to change the y view of the boxes based on the mouse wheel travel
        for box in self.boxes:
            box.yview("scroll",
                      -1 * (event.delta // ScrollableWidget.SCROLLSPEED),
                      "units")
        return "break"