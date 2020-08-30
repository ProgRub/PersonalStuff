import tkinter as TK
from ListsAndFiles import ListsAndFiles


class Screen:
    container = ListsAndFiles(
    )  #this deals with all matters pertaining to updating the files and lists
    window = TK.Tk()  #the main tkinter window
    DEFAULT_FONT1 = ("Times New Roman", 16)
    DEFAULT_FONT2 = ("Times New Roman", 14)
    DEFAULT_FONT3 = ("Times New Roman", 12)
    DEFAULT_BGCOLOR = "#061130"

    def __init__(self, masterFramePreviousScreen):
        masterFramePreviousScreen.destroy(
        )  #this gets rid of the previous "screen", by having all the widgets placed on the master frame and destroying the master frame we get rid of all widgets

        #Widget Creation
        self.frm_master = TK.Frame(Screen.window, bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_title = TK.Label(self.frm_master,
                                  font=Screen.DEFAULT_FONT1,
                                  bg=Screen.DEFAULT_BGCOLOR,
                                  fg="white")
        self.btn_backScreen = TK.Button(self.frm_master,
                                        text="Go Back",
                                        command=self.backScreen,
                                        font=Screen.DEFAULT_FONT3)

        #Widget Placement
        self.frm_master.grid(row=0, column=0)

        Screen.window.bind(
            "<Return>", self.nextScreen
        )  #this makes sure that by clicking enter (from any point in the window) we advance to the next screen
        Screen.window.bind('<KP_Enter>',
                           self.nextScreen)  #same but for num pad enter
        Screen.window.bind(
            "<Escape>", self.backScreen
        )  #this makes sure that by clicking escape we go to the previous screen (if possible)

    """
        Utility method that if a word in the list setOfWords is in word in between () or [] it removes the () or [] and everything in it
        Example: removeWordsFromWord(["Remaster"],"Stairway To Heaven (2009 Remastered)") returns "Stairway To Heaven"
    """
    @staticmethod
    def removeWordsFromWord(setOfWords: list, word:str):
        # firstCicle = False
        if word.find("(") != -1 or word.find(
                "["
        ) != -1:  #first we check if there is even a parenthesis in the word, otherwise there's no need to do anything
            for wordToRemove in setOfWords:
                inRoundParenthesis = True
                while wordToRemove in word:
                    if inRoundParenthesis:  #if this the first time we are checking we first check for the round parenthesis
                        positionStartParenthesis = word.find("(")
                        positionEndParenthesis = word.find(")")
                    if positionStartParenthesis == -1 or not inRoundParenthesis:  #if we don't find the round parenthesis or the word is not in between them, we check for the square parenthesis
                        positionStartParenthesis = word.find("[")
                        positionEndParenthesis = word.find("]")
                    if wordToRemove in word[positionStartParenthesis -
                                            1:positionEndParenthesis + 1]:
                        word = Screen.removeWordsFromWord(
                            setOfWords,
                            word.replace(
                                word[positionStartParenthesis -
                                     1:positionEndParenthesis + 1], "")
                        )  #we call the function again to possibly remove another word of the setOfWords that may be in
                    else: #if the wordToRemove is not in the parenthesis, we call the function in the part of the word after the first instance of ) or ]
                        if not inRoundParenthesis:
                            if word.find("(") != -1:
                                word = word.replace(
                                    word[word.find(")") + 1:],
                                    Screen.removeWordsFromWord(
                                        setOfWords, word[word.find(")") + 1:]))
                            if word.find("[") != -1:
                                word = word.replace(
                                    word[word.find("]") + 1:],
                                    Screen.removeWordsFromWord(
                                        setOfWords, word[word.find("]") + 1:]))
                        inRoundParenthesis = False
        return word.strip()

    @staticmethod
    def generateGenreTags(textBox:TK.Text):
        for genre in Screen.container.genresColors:
            textBox.tag_config(Screen.container.correctRapGenre(genre),
                               foreground=Screen.container.genresColors[
                                   Screen.container.correctRapGenre(genre)])

    def backScreen(self, event=None):
        pass

    def nextScreen(self, event=None):
        pass