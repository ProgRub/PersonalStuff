import tkinter as TK
from ListsAndFiles import ListsAndFiles

class Screen:
    container = ListsAndFiles()
    window = TK.Tk()
    DEFAULT_FONT1 = ("Times New Roman", 16)
    DEFAULT_FONT2 = ("Times New Roman", 14)
    DEFAULT_FONT3 = ("Times New Roman", 12)
    DEFAULT_BGCOLOR = "#061130"

    def __init__(self, masterFramePreviousScreen):
        masterFramePreviousScreen.destroy()

        #Widget Creation
        self.frm_master = TK.Frame(Screen.window, bg=Screen.DEFAULT_BGCOLOR)
        self.btn_backScreen = TK.Button(self.frm_master,
                                        text="Go Back",
                                        command=self.backScreen,
                                        font=Screen.DEFAULT_FONT3)

        #Widget Placement
        self.frm_master.grid(row=0, column=0)

        Screen.window.bind("<Return>", self.nextScreen)
        Screen.window.bind('<KP_Enter>', self.nextScreen)
        Screen.window.bind("<Escape>", self.backScreen)

    @staticmethod
    def removeWordsFromWord(setOfWords, word):
        dentroParenteses = True
        firstCicle = False
        if word.find("(") != -1 or word.find("[") != -1:
            for wordToRemove in setOfWords:
                while wordToRemove in word:
                    if dentroParenteses:
                        pos1parentes = word.find("(")
                        pos2parentes = word.find(")")
                    if pos1parentes == -1 or not dentroParenteses:
                        pos1parentes = word.find("[")
                        pos2parentes = word.find("]")
                        if pos1parentes == -1:
                            dentroParenteses = True
                            firstCicle = True
                    if not firstCicle:
                        if wordToRemove in word[pos1parentes - 1:pos2parentes +
                                                1]:
                            word = Screen.removeWordsFromWord(
                                setOfWords,
                                word.replace(
                                    word[pos1parentes - 1:pos2parentes + 1],
                                    ""))
                        else:
                            dentroParenteses = False
                    else:
                        aux = word[word.find(")") + 1:]
                        for wordToRemove in setOfWords:
                            while wordToRemove in word:
                                if dentroParenteses:
                                    pos1parentes = aux.find("(")
                                    pos2parentes = aux.find(")")
                                if pos1parentes == -1 or not dentroParenteses:
                                    pos1parentes = aux.find("[")
                                    pos2parentes = aux.find("]")
                                    if pos1parentes == -1:
                                        dentroParenteses = True
                                if wordToRemove in aux[pos1parentes -
                                                       1:pos2parentes + 1]:
                                    aux2 = aux.replace(
                                        aux[pos1parentes - 1:pos2parentes + 1],
                                        "")
                                    word = Screen.removeWordsFromWord(
                                        setOfWords, word.replace(aux, aux2))
                                else:
                                    dentroParenteses = False
        return word


    @staticmethod
    def generateGenreTags(textBox):
        for genre in Screen.container.genresColors:
            textBox.tag_config(Screen.container.correctRapGenre(genre),
                               foreground=Screen.container.genresColors[
                                   Screen.container.correctRapGenre(genre)])

    def backScreen(self, event=None):
        pass

    def nextScreen(self, event=None):
        pass