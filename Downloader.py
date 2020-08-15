import os
import time
import threading
import winsound
import webbrowser
import urllib.request
from urllib.request import Request, urlopen
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT, TDRC
import tkinter as TK
import tkinter.filedialog as filedialog
import xml.etree.ElementTree as ET

OneDrive = os.path.join('C:', os.path.sep, 'Users', 'ruben',
                        'Onedrive - Universidade da Madeira', 'Ano_2',
                        'Semestre_2')
ACaulas = os.path.join(OneDrive, 'AC', 'Aulas')
ACpl = os.path.join(OneDrive, 'AC', 'PL')
ACtp = os.path.join(OneDrive, 'AC', 'TP')
ACfreq = os.path.join(OneDrive, 'AC', 'Frequências')
ACgeral = os.path.join(OneDrive, 'AC')
MNIOtp = os.path.join(OneDrive, 'MNIO', 'TP')
MNIOformularios_geral = os.path.join(OneDrive, 'MNIO')
POOaulas = os.path.join(OneDrive, 'POO', 'Aulas')
POOpl = os.path.join(OneDrive, 'POO', 'PL')
POOgeral = os.path.join(OneDrive, 'POO')
TFCaulas = os.path.join(OneDrive, 'TFC', 'Aulas')
TFCtp = os.path.join(OneDrive, 'TFC', 'TP')
TFCgeral = os.path.join(OneDrive, 'TFC')

DEFAULT_FONT1 = ("Times New Roman", 16)
DEFAULT_FONT2 = ("Times New Roman", 14)
DEFAULT_FONT3 = ("Times New Roman", 12)
DEFAULT_BGCOLOR = "#061130"
SCROLLSPEED = 30  #less=faster

#TODO: comment the code
#TODO: separate into class multiple textboxes one scrollbar


class Screen:
    tempoAtual = time.time()
    window = TK.Tk()
    baseDirectory = os.path.dirname(__file__)

    def __init__(self, masterFramePreviousScreen):
        masterFramePreviousScreen.destroy()

        #Widget Creation
        self.frm_master = TK.Frame(Screen.window,
                                   height=700,
                                   width=1200,
                                   bg=DEFAULT_BGCOLOR)

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

    def backScreen(self, event=None):
        pass

    def nextScreen(self, event=None):
        pass


class InitialScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)
        #getting directories from file
        auxFile = os.path.join(Screen.baseDirectory, "auxFiles",
                               "DownloaderDirectories.xml")
        tree = ET.parse(auxFile)
        root = tree.getroot()
        self.downloadsDir = root.find('downloaddir').text
        self.musicOriginDir = root.find('musicorigindir').text
        auxFile = os.path.join(Screen.baseDirectory, "auxFiles",
                               "DetailsMusic.xml")
        tree = ET.parse(auxFile)
        root = tree.getroot()
        self.musicDestinyDir = root.find('directory').text

        #Widget Creation
        self.lbl_title = TK.Label(
            self.frm_master,
            text=
            "Welcome to the Download Helper!\nYou want help moving files related to school or music?",
            bg=DEFAULT_BGCOLOR,
            font=DEFAULT_FONT1,
            fg="white")
        self.btn_schoolVersion = TK.Button(self.frm_master,
                                           font=DEFAULT_FONT3,
                                           text="School",
                                           command=self.schoolScreen)
        self.btn_musicVersion = TK.Button(self.frm_master,
                                          font=DEFAULT_FONT3,
                                          text="Music (Downloaded)",
                                          command=self.musicScreen)
        self.btn_musicModifiedVersion = TK.Button(
            self.frm_master,
            font=DEFAULT_FONT3,
            text="Music (Files Modified)",
            command=self.albumLyricsScreen)
        self.btn_grimeArtistsExceptions = TK.Button(
            self.frm_master,
            text="Grime Artists And Exceptions",
            font=DEFAULT_FONT3,
            command=self.grimeArtistsExceptionsScreen)
        self.frm_whichDirectories = TK.Frame(self.frm_master,
                                             width=750,
                                             bg=DEFAULT_BGCOLOR)
        self.lbl_whichDirectories = TK.Label(
            self.frm_whichDirectories,
            text="Choose the respective directories",
            font=DEFAULT_FONT1,
            bg=DEFAULT_BGCOLOR,
            fg="white")
        self.lbl_downloadsDirectory = TK.Label(self.frm_whichDirectories,
                                               text="Downloads",
                                               font=DEFAULT_FONT2,
                                               bg=DEFAULT_BGCOLOR,
                                               fg="white")
        self.ent_downloadsDirectory = TK.Entry(self.frm_whichDirectories,
                                               width=60,
                                               state=TK.NORMAL,
                                               font=DEFAULT_FONT3)
        self.lbl_musicOriginDirectory = TK.Label(self.frm_whichDirectories,
                                                 text="Origin Music",
                                                 font=DEFAULT_FONT2,
                                                 bg=DEFAULT_BGCOLOR,
                                                 fg="white")
        self.ent_musicOriginDirectory = TK.Entry(self.frm_whichDirectories,
                                                 width=60,
                                                 state=TK.NORMAL,
                                                 font=DEFAULT_FONT3)
        self.lbl_musicDestinyDirectory = TK.Label(self.frm_whichDirectories,
                                                  text="Destiny Music",
                                                  font=DEFAULT_FONT2,
                                                  bg=DEFAULT_BGCOLOR,
                                                  fg="white")
        self.ent_musicDestinyDirectory = TK.Entry(self.frm_whichDirectories,
                                                  width=60,
                                                  state=TK.NORMAL,
                                                  font=DEFAULT_FONT3)
        i = 0
        while i < 3:
            self.btn_chooseDirectory = TK.Button(
                self.frm_whichDirectories,
                text="Open",
                command=lambda i=i: self.chooseDirectory(i),
                font=DEFAULT_FONT3)
            self.btn_chooseDirectory.grid(row=i + 1, column=2)
            i += 1

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=200)
        self.btn_schoolVersion.grid(row=2, column=1)
        self.btn_musicVersion.grid(row=3, column=1)
        self.btn_musicModifiedVersion.grid(row=4, column=1)
        self.btn_grimeArtistsExceptions.grid(row=5, column=1)
        self.frm_whichDirectories.grid(row=1, column=0)
        self.lbl_whichDirectories.grid(row=0, column=0)
        self.lbl_downloadsDirectory.grid(row=1, column=0)
        self.ent_downloadsDirectory.grid(row=1, column=1)
        self.lbl_musicOriginDirectory.grid(row=2, column=0)
        self.ent_musicOriginDirectory.grid(row=2, column=1)
        self.lbl_musicDestinyDirectory.grid(row=3, column=0)
        self.ent_musicDestinyDirectory.grid(row=3, column=1)

        #Widget Configuration
        self.ent_downloadsDirectory.insert(TK.END, str(self.downloadsDir))
        self.ent_downloadsDirectory.config(state="readonly")
        self.ent_musicOriginDirectory.insert(TK.END, str(self.musicOriginDir))
        self.ent_musicOriginDirectory.config(state="readonly")
        self.ent_musicDestinyDirectory.insert(TK.END,
                                              str(self.musicDestinyDir))
        self.ent_musicDestinyDirectory.config(state="readonly")

    def chooseDirectory(self, whichOne):
        aux = filedialog.askdirectory(initialdir=os.path.join(
            "C:", os.path.sep, "Users", "ruben", "Desktop")).replace(
                "/", "\\")
        if aux != "":
            if whichOne == 0:
                self.downloadsDir = aux
                ent_Directory = self.ent_downloadsDirectory
                auxFile = os.path.join(Screen.baseDirectory, "auxFiles",
                                       "DownloaderDirectories.xml")
                tree = ET.parse(auxFile)
                root = tree.getroot()
                directory = root.find('downloaddir')
            elif whichOne == 1:
                self.musicOriginDir = aux
                ent_Directory = self.ent_musicOriginDirectory
                auxFile = os.path.join(Screen.baseDirectory, "auxFiles",
                                       "DownloaderDirectories.xml")
                tree = ET.parse(auxFile)
                root = tree.getroot()
                directory = root.find('musicorigindir')
            else:
                self.musicDestinyDir = aux
                ent_Directory = self.ent_musicDestinyDirectory
                auxFile = os.path.join(Screen.baseDirectory, "auxFiles",
                                       "DetailsMusic.xml")
                tree = ET.parse(auxFile)
                root = tree.getroot()
                directory = root.find('directory')
            directory.text = aux
            tree.write(auxFile)
            ent_Directory.config(state=TK.NORMAL)
            ent_Directory.delete(0, 'end')
            ent_Directory.insert(TK.END, aux)
            ent_Directory.config(state="readonly")
            # auxFile = open(os.path.join(Screen.auxFilesDir, "auxFiles",
            #                             "DownloaderDirectories.txt"),
            #                "w",
            #                encoding="utf-8")
            # auxFile.writelines([
            #     self.downloadsDir + "\n", self.musicOriginDir + "\n",
            #     self.musicDestinyDir + "\n"
            # ])
            # auxFile.close()

    def schoolScreen(self):
        SchoolScreen(self.frm_master, self.downloadsDir)

    def musicScreen(self):
        MusicScreen(self.frm_master, self.musicOriginDir, self.musicDestinyDir,
                    True)

    def albumLyricsScreen(self):
        AlbumAndLyricsScreen(
            self.frm_master,
            [
                os.path.join(self.musicDestinyDir, f)
                for f in os.listdir(self.musicDestinyDir)
                if os.path.join(self.musicDestinyDir, f).endswith(".mp3") and
                os.path.getmtime(os.path.join(self.musicDestinyDir, f)) >  #0
                (Screen.tempoAtual -
                 5 * 60)  #files modified in the last 5 minutes
            ])

    def grimeArtistsExceptionsScreen(self):
        GrimeArtistsAndExceptionsScreen(self.frm_master)


class GrimeArtistsAndExceptionsScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)
        #TODO: adjusts to input exceptions and save and load said exceptions from files
        #xml element: pair type = 0-2 base = "..." new = "..."
        #Tkinter Vars
        self.newArtist = TK.StringVar()
        self.file = os.path.join(Screen.baseDirectory, "auxFiles",
                                 "GrimeArtists.xml")
        tree = ET.parse(self.file)
        root = tree.getroot()
        self.grimeArtists = [child.text for child in root]
        self.mode = 0
        #1 - new Grime Artist
        #2 - delete Grime Artist

        #Widget Creation
        self.lbl_title = TK.Label(self.frm_master,
                                  text="Insert New Grime Artist or Remove",
                                  font=DEFAULT_FONT1,
                                  fg="white",
                                  bg=DEFAULT_BGCOLOR)
        self.lbl_auxEntry = TK.Label(self.frm_master,
                                     text="Artist",
                                     font=DEFAULT_FONT2,
                                     fg="white",
                                     bg=DEFAULT_BGCOLOR)
        self.ent_artist = TK.Entry(self.frm_master,
                                   textvariable=self.newArtist,
                                   font=DEFAULT_FONT3,
                                   width=30)
        self.btn_addArtist = TK.Button(self.frm_master,
                                       text="Add New Artist",
                                       font=DEFAULT_FONT3,
                                       command=self.addArtist)
        self.btn_removeArtist = TK.Button(self.frm_master,
                                          text="Remove Artist",
                                          font=DEFAULT_FONT3,
                                          command=self.removeArtist)
        self.btn_confirm = TK.Button(self.frm_master,
                                     text="Confirm",
                                     font=DEFAULT_FONT3,
                                     command=self.nextScreen)
        self.btn_previousScreen = TK.Button(self.frm_master,
                                            text="Go Back",
                                            font=DEFAULT_FONT3,
                                            command=self.backScreen)
        self.txt_artists = TK.Text(self.frm_master,
                                   font=DEFAULT_FONT3,
                                   fg="white",
                                   bg=DEFAULT_BGCOLOR)

        #Widget Placement
        self.lbl_title.grid(row=0, column=2)
        self.btn_addArtist.grid(row=2, column=1)
        self.btn_removeArtist.grid(row=3, column=1)
        self.btn_previousScreen.grid(row=4, column=0)

        #Widget Configuration

    def backScreen(self, event=None):
        tree = ET.parse(self.file)
        root = tree.getroot()
        root.clear()
        for artist in self.grimeArtists:
            child = ET.Element('artist')
            child.text = artist
            root.append(child)
        tree.write(self.file)
        InitialScreen(self.frm_master)

    def nextScreen(self, event=None):
        artist = self.newArtist.get()
        if self.mode == 1:
            self.grimeArtists.append(artist)
        elif self.mode == 2:
            try:
                self.grimeArtists.remove(artist)
            except ValueError:
                pass
        self.newArtist.set("")
        self.btn_addArtist.grid(row=2, column=1)
        self.btn_removeArtist.grid(row=3, column=1)
        self.btn_previousScreen.grid(row=4, column=0)
        self.lbl_auxEntry.grid_forget()
        self.ent_artist.grid_forget()
        self.btn_confirm.grid_forget()
        self.txt_artists.grid_forget()

    def addArtist(self):
        self.mode = 1
        self.lbl_auxEntry.grid(row=1, column=1)
        self.ent_artist.grid(row=1, column=2)
        self.btn_confirm.grid(row=2, column=2)
        self.btn_addArtist.grid_forget()
        self.btn_removeArtist.grid_forget()
        self.btn_previousScreen.grid_forget()

    def removeArtist(self):
        self.mode = 2
        self.txt_artists.config(height=len(self.grimeArtists))
        self.txt_artists.delete("1.0", TK.END)
        self.txt_artists.insert("1.0", "\n".join(self.grimeArtists))
        self.lbl_auxEntry.grid(row=1, column=1)
        self.ent_artist.grid(row=1, column=2)
        self.btn_confirm.grid(row=2, column=2)
        self.txt_artists.grid(row=1, column=3, rowspan=1500)
        self.btn_addArtist.grid_forget()
        self.btn_removeArtist.grid_forget()
        self.btn_previousScreen.grid_forget()


class SchoolScreen(Screen):
    def __init__(self, masterFramePreviousScreen, downloadsDir):
        super().__init__(masterFramePreviousScreen)
        #Tkinter Vars
        self.downloadsDir = downloadsDir
        self.title = TK.StringVar()
        self.numberOfFiles = 0
        self.title.set(str(self.numberOfFiles) + " Files Found")

        #Widget Creation
        self.lbl_title = TK.Label(self.frm_master,
                                  textvariable=self.title,
                                  font=DEFAULT_FONT1,
                                  bg=DEFAULT_BGCOLOR,
                                  fg="white")
        self.txt_filesFound = TK.Text(self.frm_master,
                                      bg=DEFAULT_BGCOLOR,
                                      fg="white",
                                      font=DEFAULT_FONT3)
        self.txt_filesMoved = TK.Text(self.frm_master,
                                      bg=DEFAULT_BGCOLOR,
                                      fg="white",
                                      font=DEFAULT_FONT3)
        self.btn_stopCycle = TK.Button(self.frm_master,
                                       text="Stop",
                                       font=DEFAULT_FONT3,
                                       command=self.stopCheckDownloads)

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=200)
        self.txt_filesFound.grid(row=1, column=0)
        self.txt_filesMoved.grid(row=1, column=1)
        self.btn_stopCycle.grid(row=2, column=0)

        Screen.window.update_idletasks()

        self.cycleCondition = True
        webbrowser.open("https://moodle.cee.uma.pt/login/index.php", new=2)
        webbrowser.open("https://infoalunos.uma.pt", new=2)
        self.txt_filesMoved.tag_config("existed", fg="yellow")
        self.txt_filesMoved.tag_config("notExisted", fg="green")
        self.txt_filesMoved.tag_config("deleted/Skipped", fg="red")
        self.checkDownloads()

    def stopCheckDownloads(self):
        self.cycleCondition = False
        self.btn_stopCycle.destroy()

    def addToOutput(self, fileFound, fileMoved, tag):
        self.numberOfFiles += 1
        self.title.set(str(self.numberOfFiles) + " Files Found")
        self.txt_filesFound.config(state=TK.NORMAL)
        self.txt_filesMoved.config(state=TK.NORMAL)
        self.txt_filesFound.insert(TK.END, fileFound + "\n")
        self.txt_filesMoved.insert(TK.END, fileMoved + "\n", tag)
        self.txt_filesFound.config(state=TK.DISABLED)
        self.txt_filesMoved.config(state=TK.DISABLED)
        Screen.window.update_idletasks()
        self.txt_filesFound.see(TK.END)
        self.txt_filesMoved.see(TK.END)

    def checkDownloads(self):
        #FIXME: need to adapt this to the GUI and the new disciplines when the time comes
        if self.cycleCondition:
            Screen.window.after(1000, self.checkDownloads)
            for filename in os.listdir(self.downloadsDir):
                #try:
                if os.path.getctime(os.path.join(
                        self.downloadsDir,
                        filename)) > Screen.tempoAtual and os.path.getsize(
                            os.path.join(
                                self.downloadsDir,
                                filename)) > 0 and filename.endswith(".pdf"):
                    destino = self.whichFolder(filename)
                    if "False" != destino:
                        count += 1
                        try:
                            os.rename(
                                os.path.join(self.downloadsDir, filename),
                                destino)
                            self.addToOutput(filename, destino, "notExisted")
                            # print("File downloaded succesfully")
                        except FileExistsError:
                            os.remove(destino)
                            os.rename(
                                os.path.join(self.downloadsDir, filename),
                                destino)
                            self.addToOutput(filename, destino, "existed")
                            #print("File replaced succesfully")
                    else:
                        self.addToOutput(filename, "REMOVED/SKIPPED",
                                         "deleted/Skipped")
                        #print("File skipped/deleted")
                # except FileNotFoundError:
                #     if not filename.endswith(".part"):
                #         print(filename + "\nERRO")
                #         break

    def whichFolder(self, filename):
        if filename.startswith("PT_AC_"):
            return os.path.join(ACaulas,
                                filename[len("PT_AC_"):].replace("T_", ""))
        elif filename.startswith("Apresentação") or filename.startswith(
                "Guia"):
            return os.path.join(ACpl, filename)
        elif filename.startswith("Aula_"):
            return os.path.join(ACtp, filename)
        elif filename.startswith("T1") or filename.startswith("T2"):
            if "Frequencia" in filename:
                return os.path.join(
                    ACfreq, 'Normal',
                    filename[len("T1_"):].replace("_AC",
                                                  "").replace("_PT", ""))
            elif "Recurso" in filename:
                return os.path.join(
                    ACfreq, 'Recurso', filename[len("T1_T2_"):].replace(
                        "_AC", "").replace("_PT", "").replace("_20", ""))
            elif "Especial" in filename:
                return os.path.join(
                    ACfreq, 'EpocaEspecial', filename[len("T1_T2_"):].replace(
                        "_AC", "").replace("_PT", "").replace("_20", ""))
        elif filename.startswith("AC_P"):
            return os.path.join(ACgeral,
                                "Enunciado Projeto " + filename[4] + ".pdf")
        elif filename[2] == ".":
            return os.path.join(POOaulas, filename)
        elif filename.startswith("Ficha"):
            diretoria = os.path.join(
                POOpl, filename[:filename.find(".")].replace(" ", ""))
            try:
                os.makedirs(diretoria)
            except FileExistsError:
                print("Directory already existed")
            return os.path.join(diretoria, filename)
        elif filename.startswith("MNIO_FichaExerc"):
            return os.path.join(MNIOtp, filename[len("MNIO_"):])
        elif filename.startswith("MNIO_Formulario"):
            return os.path.join(MNIOformularios_geral, filename[len("MNIO_"):])
        elif filename.startswith("Folha"):
            return os.path.join(TFCtp, filename.replace("TFC1920", ""))
        elif filename.startswith("TFC1920"):
            numero = filename[filename.rfind("Semana") +
                              6:filename.rfind("Handout") - 1]
            return os.path.join(
                TFCaulas,
                filename.replace("TFC1920", "").replace("-", "")[0:12] +
                numero + ".pdf")
        else:
            rename = input(
                "This is the file " + filename +
                "\nDo you want to rename it? (y/n, d to delete, s to skip)\n")
            if rename == "y":
                filename = input("Rename the file: ") + ".pdf"
            elif rename == "d":
                os.remove(os.path.join(self.downloadsDir, filename))
                return "False"
            elif rename == "s":
                return "False"
            op = input(
                "Choose the discipline:\n1.AC\n2.POO\n3.TFC\n4.MNIO\nOption: ")
            if op == "1":
                return os.path.join(ACgeral, filename)
            elif op == "2":
                return os.path.join(POOgeral, filename)
            elif op == "3":
                return os.path.join(TFCgeral, filename)
            elif op == "4":
                return os.path.join(MNIOformularios_geral, filename)


class MusicScreen(Screen):
    def __init__(self, masterFramePreviousScreen, musicOriginDir,
                 musicDestinyDir, firstTime):
        super().__init__(masterFramePreviousScreen)
        if firstTime:
            os.startfile(
                r"C:\Users\ruben\Desktop\deemix\deemix-tools\start.bat")

        #Tkinter Vars
        self.musicOriginDir = musicOriginDir
        self.musicDestinyDir = musicDestinyDir
        self.numberOfFilesFound = 0
        self.numberOfFilesMoved = 0
        self.buffer = []
        self.title = TK.StringVar()
        self.title.set(str(self.numberOfFilesFound) + " Files Found")

        #Widget Creation
        self.lbl_title = TK.Label(self.frm_master,
                                  textvariable=self.title,
                                  font=DEFAULT_FONT1,
                                  bg=DEFAULT_BGCOLOR,
                                  fg="white")
        self.frm_textOutput = TK.Frame(self.frm_master, bg=DEFAULT_BGCOLOR)
        self.lbl_beforeFiles = TK.Label(self.frm_textOutput,
                                        bg=DEFAULT_BGCOLOR,
                                        fg="white",
                                        text="Before",
                                        font=DEFAULT_FONT2)
        self.lbl_afterFiles = TK.Label(self.frm_textOutput,
                                       bg=DEFAULT_BGCOLOR,
                                       fg="white",
                                       text="After",
                                       font=DEFAULT_FONT2)
        self.scb_textOutput = TK.Scrollbar(self.frm_textOutput,
                                           command=self.scrollTextOutput,
                                           orient=TK.VERTICAL)
        self.txt_beforeFiles = TK.Text(self.frm_textOutput,
                                       bg=DEFAULT_BGCOLOR,
                                       fg="white",
                                       font=DEFAULT_FONT3,
                                       yscrollcommand=self.scb_textOutput.set,
                                       state=TK.DISABLED)
        self.txt_afterFiles = TK.Text(self.frm_textOutput,
                                      bg=DEFAULT_BGCOLOR,
                                      fg="white",
                                      font=DEFAULT_FONT3,
                                      yscrollcommand=self.scb_textOutput.set,
                                      state=TK.DISABLED)
        self.btn_moveOutOfBuffer = TK.Button(self.frm_master,
                                             text="Move Files",
                                             command=self.nextScreen,
                                             font=DEFAULT_FONT3)
        self.btn_nextScreen = TK.Button(self.frm_master,
                                        text="Get Album Year and Lyrics",
                                        font=DEFAULT_FONT3,
                                        command=self.nextScreen)

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=200)
        self.frm_textOutput.grid(row=1, column=0)
        self.lbl_beforeFiles.grid(row=0, column=0)
        self.lbl_afterFiles.grid(row=0, column=1)
        self.scb_textOutput.grid(row=1, column=2, sticky=TK.NS)
        self.txt_beforeFiles.grid(row=1, column=0)
        self.txt_afterFiles.grid(row=1, column=1)
        self.btn_moveOutOfBuffer.grid(row=2, column=0)

        #Widget Configuration
        self.txt_afterFiles.bind("<MouseWheel>",
                                 self.scrollTextOutputMouseWheel)
        self.txt_beforeFiles.bind("<MouseWheel>",
                                  self.scrollTextOutputMouseWheel)

        self.checkMusicCondition = True
        self.newFiles = []
        auxFile = os.path.join(Screen.baseDirectory, "auxFiles",
                               "GrimeArtists.xml")
        tree = ET.parse(auxFile)
        root = tree.getroot()
        self.grimeArtists = [child.text for child in root]
        self.checkMusic()

    def nextScreen(self, event=None):
        if self.checkMusicCondition:
            self.checkMusicCondition = False
            self.txt_beforeFiles.delete("end-1c linestart", TK.END)
            self.moveOutOfBuffer()
            self.txt_afterFiles.delete("end-1c linestart", TK.END)
            self.btn_moveOutOfBuffer.destroy()
            self.btn_nextScreen.grid(row=2, column=0)
        else:
            AlbumAndLyricsScreen(self.frm_master, self.newFiles,
                                 self.musicOriginDir, self.musicDestinyDir)

    def scrollTextOutput(self, *args):
        self.txt_beforeFiles.yview(*args)
        self.txt_afterFiles.yview(*args)

    def scrollTextOutputMouseWheel(self, event):
        self.txt_beforeFiles.yview("scroll", -1 * (event.delta // SCROLLSPEED),
                                   "units")
        self.txt_afterFiles.yview("scroll", -1 * (event.delta // SCROLLSPEED),
                                  "units")
        return "break"

    def checkMusic(self):
        for filename in os.listdir(self.musicOriginDir):
            if filename.endswith(".mp3") and filename not in self.buffer:
                self.buffer.append(filename)
                self.txt_beforeFiles.config(state=TK.NORMAL)
                self.txt_beforeFiles.insert(TK.END, filename + "\n")
                self.txt_beforeFiles.config(state=TK.DISABLED)
                self.txt_beforeFiles.see(TK.END)
                self.numberOfFilesFound += 1
                self.title.set(str(self.numberOfFilesFound) + " Files Found")
            elif filename.endswith(".txt"):
                for ficheiro in self.buffer:
                    os.remove(os.path.join(self.musicOriginDir, ficheiro))
                self.buffer.clear()
                self.txt_beforeFiles.config(state=TK.NORMAL)
                self.txt_beforeFiles.delete("1.0", TK.END)
                self.txt_beforeFiles.config(state=TK.DISABLED)
                self.numberOfFilesFound = 0
                self.title.set(str(self.numberOfFilesFound) + " Files Found")
        if self.checkMusicCondition:
            Screen.window.update_idletasks()
            Screen.window.after(1000, self.checkMusic)

    def addToOutput(self, filename):
        self.txt_afterFiles.config(state=TK.NORMAL)
        self.txt_afterFiles.insert(TK.END, filename + "\n")
        self.txt_afterFiles.config(state=TK.DISABLED)

    def moveOutOfBuffer(self):
        if self.buffer != []:
            Screen.window.update_idletasks()
            old = self.buffer[0]
            filename = old.replace("f_ck", "fuck").replace(
                "f___", "fuck").replace("f__k", "fuck").replace(
                    "sh_t", "shit").replace("s__t", "shit").replace(
                        "sh__", "shit").replace("ni__as", "niggas").replace(
                            "F_ck", "Fuck").replace("F__k", "Fuck").replace(
                                "F___",
                                "Fuck").replace("Sh_t", "Shit").replace(
                                    "S__t",
                                    "Shit").replace("Sh__", "Shit").replace(
                                        "Ni__as", "Niggas")
            filename = Screen.removeWordsFromWord(
                ["Remaster", "Album Version", "Stereo"], filename)
            self.slightTagChanges(os.path.join(self.musicOriginDir, old),
                                  filename)
            try:
                os.rename(os.path.join(self.musicOriginDir, old),
                          os.path.join(self.musicDestinyDir, filename))
                self.numberOfFilesMoved += 1
                self.addToOutput(filename)
                self.newFiles.append(
                    os.path.join(self.musicDestinyDir, filename))
            except FileExistsError:
                mp3aEnviar = EasyID3(os.path.join(self.musicOriginDir, old))
                mp3aVerificar = EasyID3(
                    os.path.join(self.musicDestinyDir, filename))
                if mp3aEnviar['albumartist'][0] == mp3aVerificar[
                        'albumartist'][0] and mp3aEnviar['album'][
                            0] == mp3aVerificar['album'][0]:
                    os.remove(os.path.join(self.musicOriginDir, old))
                    self.addToOutput(filename + " already exists, deleted")
                else:
                    acrescenta = "("
                    palavras = mp3aEnviar['albumartist'][0].split()
                    mp3aEnviar.save()
                    if "The" in palavras[0]:
                        del palavras[0]
                    if len(palavras) == 1:
                        acrescenta += palavras[0]
                    else:
                        for w in palavras:
                            acrescenta += w[0].upper()
                    acrescenta += ")"
                    filename = filename[:filename.
                                        rfind(".")] + " " + acrescenta + ".mp3"
                    if os.path.isfile(
                            os.path.join(self.musicDestinyDir, filename)):
                        if mp3aEnviar['albumartist'][0] == mp3aVerificar[
                                'albumartist'][0] and mp3aEnviar['album'][
                                    0] == mp3aVerificar['album'][0]:
                            os.remove(os.path.join(self.musicOriginDir, old))
                            self.addToOutput(filename +
                                             " already exists, deleted")
                        else:
                            os.rename(
                                os.path.join(self.musicOriginDir, old),
                                os.path.join(self.musicDestinyDir, filename))
                            self.numberOfFilesMoved += 1
                            self.addToOutput(filename)
                            self.newFiles.append(
                                os.path.join(self.musicDestinyDir, filename))
                    else:
                        os.rename(os.path.join(self.musicOriginDir, old),
                                  os.path.join(self.musicDestinyDir, filename))
                        self.numberOfFilesMoved += 1
                        self.addToOutput(filename)
                        self.newFiles.append(
                            os.path.join(self.musicDestinyDir, filename))
            self.buffer.remove(old)
            self.txt_afterFiles.see(TK.END)
            self.title.set(str(self.numberOfFilesMoved) + " Files Moved")
            self.moveOutOfBuffer()

    def slightTagChanges(self, filename, newFilename):
        mp3 = EasyID3(filename)
        if "King Gizzard and the Lizard Wizard".lower(
        ) in mp3['albumartist'][0].lower():
            mp3['artist'] = mp3['artist'][0].replace("And", "&")
            mp3['albumartist'] = mp3['albumartist'][0].replace("And", "&")
        elif "&" in mp3['albumartist'][0] and mp3['album'][
                0] != "Without Warning" and " Mayall " not in mp3[
                    'albumartist'][0]:
            mp3['albumartist'] = mp3['albumartist'][0].split(" & ")[0]
        elif mp3['album'][0] == "Without Warning":
            mp3['albumartist'] = "21 Savage, Offset & Metro Boomin"
        if "/" in mp3['albumartist'][0]:
            mp3['albumartist'] = mp3['albumartist'][0].split("/")[0]
        if "Remaster" in mp3['title'][0] or "Album Version" in mp3['title'][
                0] or "Stereo" in mp3['title'][0]:
            mp3['title'] = Screen.removeWordsFromWord([
                "Remaster", "Album Version", "Stereo", "Hidden Track",
                "Explicit", "explicit"
            ], mp3['title'][0])
        if mp3['albumartist'][0] in self.grimeArtists:
            mp3['genre'] = "Grime"
        elif "Electro" in mp3['genre'][0]:
            mp3['genre'] = "Electro"
        elif "Rock" in mp3['genre'][0]:
            mp3['genre'] = "Rock"
        elif "Rap" in mp3['genre'][0]:
            mp3['genre'] = "Rap/Hip Hop"
        elif "Alternativa" in mp3['genre'][0]:
            mp3['genre'] = "Alternative"
        if "f*ck" in mp3['title'][0].lower() or "f***" in mp3['title'][
                0].lower() or "f**k" in mp3['title'][0].lower(
                ) or "sh*t" in mp3['title'][0].lower() or "sh**" in mp3[
                    'title'][0].lower() or "s**t" in mp3['title'][0].lower(
                    ) or "ni**as" in mp3['title'][0].lower():
            mp3['title'] = mp3['title'][0].replace("f*ck", "fuck").replace(
                "f***", "fuck").replace("f**k", "fuck").replace(
                    "sh*t", "shit").replace("s**t", "shit").replace(
                        "sh**", "shit").replace("ni**as", "niggas").replace(
                            "F*ck", "Fuck").replace("F**k", "Fuck").replace(
                                "F***",
                                "Fuck").replace("Sh*t", "Shit").replace(
                                    "S**t",
                                    "Shit").replace("Sh**", "Shit").replace(
                                        "Ni**as", "Niggas")
        mp3.save()


class AlbumAndLyricsScreen(Screen):
    pagesVisited_year = {}
    artistAlbumReplacements = {}

    def __init__(self,
                 masterFramePreviousScreen,
                 newFiles,
                 musicOriginDir=None,
                 musicDestinyDir=None):
        super().__init__(masterFramePreviousScreen)
        Screen.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Tkinter Vars
        self.musicOriginDir = musicOriginDir
        self.musicDestinyDir = musicDestinyDir
        self.numberOfFilesProcessed = 0
        self.newFiles = newFiles
        self.totalNewFiles = len(self.newFiles)
        self.title = TK.StringVar()
        self.title.set(
            str(self.numberOfFilesProcessed) + "/" + str(self.totalNewFiles) +
            " Files Processed")
        self.currentArtist = TK.StringVar()
        self.currentAlbum = TK.StringVar()
        self.currentTitle = TK.StringVar()
        self.currentYear = TK.StringVar()
        self.currentLyrics = ""
        self.trackBeingReviewedDetails = {
            "Artist": self.currentArtist,
            "Album": self.currentAlbum,
            "Title": self.currentTitle,
            "Year": self.currentYear
        }
        self.currentUrl = TK.StringVar()
        self.gettingYear = False
        self.errorHandled = TK.BooleanVar()
        self.errorHandled.set(True)
        self.finished = True
        self.romanNums = [
            " i", " ii", " iii", " iv", " v", " vi", " vii", " viii", " ix",
            " x"
        ]
        self.errorSound = threading.Thread(target=self.thread_function,
                                           daemon=True)
        self.removePtOrPart = False

        #Widget Creation
        self.lbl_title = TK.Label(self.frm_master,
                                  textvariable=self.title,
                                  bg=DEFAULT_BGCOLOR,
                                  fg="white",
                                  font=DEFAULT_FONT1)
        self.frm_textOutput = TK.Frame(self.frm_master, bg=DEFAULT_BGCOLOR)
        self.scb_textOutput = TK.Scrollbar(self.frm_textOutput,
                                           command=self.scrollTextOutput,
                                           orient=TK.VERTICAL)
        self.categories_width = {
            "Artist": 30,
            "Album": 55,
            "Title": 70,
            "Year": 5
        }
        self.textBoxes = []
        i = 0
        for category in self.categories_width:
            if category == "Year":
                break
            lbl_category = TK.Label(self.frm_textOutput,
                                    text=category,
                                    font=DEFAULT_FONT2,
                                    bg=DEFAULT_BGCOLOR,
                                    fg="white")
            txt_category = TK.Text(self.frm_textOutput,
                                   font=DEFAULT_FONT3,
                                   width=self.categories_width[category],
                                   bg=DEFAULT_BGCOLOR,
                                   yscrollcommand=self.scb_textOutput.set)
            txt_category.tag_config("album", foreground="yellow")
            txt_category.tag_config("lyrics", foreground="dark green")
            txt_category.tag_config("success", foreground="green2")
            txt_category.bind("<MouseWheel>", self.scrollTextOutputMouseWheel)
            self.textBoxes.append(txt_category)
            lbl_category.grid(row=0, column=i)
            txt_category.grid(row=1, column=i)
            i += 1
        self.frm_newAAT = TK.Frame(self.frm_master, bg=DEFAULT_BGCOLOR)
        i = 0
        self.entriesTrack = []
        for category in self.trackBeingReviewedDetails:
            label = TK.Label(self.frm_newAAT,
                             font=DEFAULT_FONT2,
                             bg=DEFAULT_BGCOLOR,
                             fg="white",
                             text=category)
            entry = TK.Entry(
                self.frm_newAAT,
                font=DEFAULT_FONT3,
                textvariable=self.trackBeingReviewedDetails[category],
                width=50)
            self.entriesTrack.append(entry)
            label.grid(row=i, column=0)
            entry.grid(row=i, column=1)
            if category == "Year":
                entry.configure(validatecommand=(entry.register(self.testVal),
                                                 '%P'))
            i += 1
        self.lbl_url = TK.Label(self.frm_master,
                                textvariable=self.currentUrl,
                                font=DEFAULT_FONT2,
                                bg=DEFAULT_BGCOLOR,
                                fg="white")
        colors = ["yellow", "dark green", "green2"]
        text = ["Getting Album Year", "Getting Track Lyrics", "File Done"]
        self.cnv_tagsLabel = TK.Canvas(self.frm_master,
                                       bg=DEFAULT_BGCOLOR,
                                       highlightthickness=0,
                                       bd=0,
                                       width=200,
                                       height=len(colors) * 1.5 * 25)
        i = 0
        for index in range(len(colors)):
            self.cnv_tagsLabel.create_rectangle(0,
                                                i * 25,
                                                25,
                                                25 + i * 25,
                                                fill=colors[index])
            self.cnv_tagsLabel.create_text(27,
                                           13 + i * 25,
                                           text=" - " + text[index],
                                           fill="white",
                                           font=DEFAULT_FONT3,
                                           anchor=TK.W)
            i += 1.5
        self.btn_tryAgain = TK.Button(self.frm_newAAT,
                                      text="Try Again",
                                      font=DEFAULT_FONT3,
                                      command=self.nextScreen,
                                      state=TK.DISABLED)
        self.btn_skipLyrics = TK.Button(self.frm_newAAT,
                                        text="Skip Song",
                                        font=DEFAULT_FONT3,
                                        command=self.skipLyrics,
                                        state=TK.DISABLED)
        self.btn_downloadMore = TK.Button(self.frm_master,
                                          text="Download More",
                                          font=DEFAULT_FONT3,
                                          command=self.goBackDownloadMore)
        self.btn_exit = TK.Button(self.frm_master,
                                  text="Exit",
                                  font=DEFAULT_FONT3,
                                  command=self.exitOpenHandler)

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=300)
        self.frm_textOutput.grid(row=1, column=0)
        self.scb_textOutput.grid(row=1, column=3, sticky=TK.NS)
        self.frm_newAAT.grid(row=3, column=0)
        self.lbl_url.grid(row=2, column=0)
        self.cnv_tagsLabel.grid(row=1, column=1)
        self.btn_tryAgain.grid(row=5, column=1)
        self.btn_skipLyrics.grid(row=6, column=1)

        #Widget Configuration
        self.disableEntries()
        Screen.window.update_idletasks()
        self.lyricsAndYear()
        Screen.window.update_idletasks()

    def skipLyrics(self):
        self.currentLyrics = "None"
        self.errorHandled.set(True)

    def nextScreen(self, event=None):
        try:
            if self.btn_tryAgain["state"] == "normal":
                self.errorHandled.set(True)
        except:
            pass

    # restricts entry to only accept digits
    def testVal(self, inStr):
        if not inStr.isdigit():
            return False
        return True

    def on_closing(self):
        self.errorHandled.set(True)
        Screen.window.destroy()

    def goBackDownloadMore(self):
        MusicScreen(self.frm_master, self.musicOriginDir, self.musicDestinyDir,
                    False)

    def exitOpenHandler(self):
        Screen.window.quit()
        os.system(os.path.join(Screen.baseDirectory, "Handler_Music.py"))

    def scrollTextOutput(self, *args):
        for txt in self.textBoxes:
            txt.yview(*args)

    def scrollTextOutputMouseWheel(self, event):
        for txt in self.textBoxes:
            txt.yview("scroll", -1 * (event.delta // SCROLLSPEED), "units")
        return "break"

    def addToOutput(self):
        i = 0
        for category in self.trackBeingReviewedDetails:
            if i == 3:
                break
            self.textBoxes[i].insert(
                TK.END, self.trackBeingReviewedDetails[category].get(),
                "album")
            i += 1
        Screen.window.update_idletasks()

    def disableEntries(self):
        for entry in self.entriesTrack:
            entry.config(state=TK.DISABLED)
        self.btn_tryAgain.config(state=TK.DISABLED)
        self.btn_skipLyrics.config(state=TK.DISABLED)

    def enableEntries(self, whichOnes):
        if whichOnes == 0:
            self.entriesTrack[1].config(state=TK.NORMAL)
            self.entriesTrack[0].config(state=TK.NORMAL)
            self.entriesTrack[2].config(state=TK.NORMAL)
        elif whichOnes == 1:
            self.entriesTrack[2].config(state=TK.NORMAL)
            self.entriesTrack[0].config(state=TK.NORMAL)
            self.btn_skipLyrics.config(state=TK.NORMAL)
        elif whichOnes == 2:
            self.entriesTrack[3].config(state=TK.NORMAL)
        self.btn_tryAgain.config(state=TK.NORMAL)

    def changeTag(self, tag):
        for txt in self.textBoxes:
            txt.tag_add(tag, "end-1c linestart", TK.END)
        Screen.window.update_idletasks()

    """
        Gets the parameter name right, according to the Genius url conventions
    """

    def namingConventions(self, name, version):  #version = True -> title
        replacementsDict = {
            "/": " ",
            ">": " ",
            "<": " ",
            "'": "",
            "*": " ",
            "-": " ",
            "’": "",
            "“": " ",
            "”": " ",
            "\"": " ",
            "…": " ",
            "&": "And",
            ",": " ",
            "|": " ",
            "_": " ",
            "(": " ",
            ")": " ",
            "+": "",
            "=": " ",
            "é": "e",
            "à": "a",
            "ñ": "n",
            "@": "at",
            "...": " ",
            ".": "",
            ":": " ",
            "!": " ",
            "?": " ",
            "#": " ",
            "$": " ",
            "–": " "
        }
        if not version:
            replacementsDict["&"] = " "
        if "pt." in name.lower() or "part." in name.lower(
        ) or "pts." in name.lower() or "mr." in name.lower(
        ) or "vol." in name.lower():
            replacementsDict["."] = " "
        for key in replacementsDict:
            name = name.replace(key, replacementsDict[key])
        return "-".join(name.split()).capitalize()

    """
        Determines the artist and title to be used in the search for lyrics and handles the most common changes
    """

    #TODO: divide function into settings to get year and to get lyrics and save exceptions user has to define
    def ArtistAlbumAndTitle(self, filename):
        artist = EasyID3(filename)['albumartist'][0]
        title = EasyID3(filename)['title'][0]
        album = EasyID3(filename)['album'][0]
        album = Screen.removeWordsFromWord(
            ["Remaster", "Anniversary", "Deluxe", "Expanded"], album)
        # if "OKNOTOK" in album:
        #     album = "OK Computer"
        # elif "Piñata" == album or "Bandana" == album:
        #     artist += " & Madlib"
        # elif "What A Time To Be Alive" == album:
        #     artist += " & Future"
        # elif "Alfredo" == album:
        #     artist += " & The Alchemist"
        # elif "sign of the times" in album.lower():
        #     album = artist
        # elif "UNLOCKED" == album:
        #     artist += " & Kenny Beats"
        # elif "Watch The Throne" == album:
        #     artist += " & Kanye West"
        # elif "Tonight" == album:
        #     album += ": Franz Ferdinand"
        # elif "Bluesbreakers" == album:
        #     album = "Blues Breakers with Eric Clapton"
        # elif "The Beatles" == album:
        #     album = "The Beatles The White Album"
        if (artist, album) in AlbumAndLyricsScreen.artistAlbumReplacements:
            artist = AlbumAndLyricsScreen.artistAlbumReplacements[(artist,
                                                                   album)][0]
            album = AlbumAndLyricsScreen.artistAlbumReplacements[(artist,
                                                                  album)][1]
        if "Tea In China" in album:
            artist += " & The Alchemist"
        if "God's" == album:
            album = album.replace("'", " ")
        elif "Section" in album or "good kid," in album:
            album.replace(".", " ")
        title = Screen.removeWordsFromWord([
            "feat", "Feat", "bonus", "Bonus", "Conclusion", "Hidden Track",
            "Vocal Mix", "Explicit", "explicit", "Extended"
        ], title)
        if "King's Dead" == title:
            artist = "Jay Rock Kendrick Lamar Future & James Blake"
        elif "various" in artist.lower():
            artist = EasyID3(filename)['artist'][0]
            if "," in artist:
                artist = artist[:artist.find(",")]
        elif "wickedskeng" in title.lower():
            title = "wickedskengman part 4"
        elif "Kiss and Tell" == title:
            artist += " & Skepta"
        elif "Short King Anthem" == title:
            artist = "blackbear & " + artist
        elif "Bang (feat." in title:
            title = "Bang (Remix)"
        elif "Psycho" in title and "Curry" in artist:
            artist = "slowthai & Denzel Curry"
        elif "Ripe" in title:
            title = "Ripe & Ruin"
        elif "Life After Death" == title:
            title += " (Intro)"
        elif "Strangiato" in title:
            title += " (An Exercise In Self-Indulgence)"
        elif "Protect Ya Neck" in title:
            title = "Protect Ya Neck"
        elif "Kush & Corinthians" == title:
            title += "(His Pain)"
        elif "P Money" == artist and "Money Over Everyone" == album and "Intro" == title:
            title = album + " " + title
        elif "Punch Up" in title:
            title = title.replace("Punch Up", "Punchup")
        elif "Breaks" == title:
            title = "The " + title
        elif "Packt Like" in title:
            title = title.replace("Crushed", "Crushd")
        elif "Curtains Close" == title:
            title += "(Skit)"
        elif "Paul" in title:
            if "Marshall" in album:
                title = "Paul Skit 2000"
            elif "Eminem" in album:
                title = "Paul Rosenberg Skit 2002"
        elif "Steve Ber" in title:
            if "Marshall" in album:
                title = "Steve Berman Skit 2000"
            elif "Eminem" in album:
                title = "Steve Berman Skit 2002"
        elif "JME" in artist and "Taking Over" in title:
            title += " (It Ain't Working)"
        elif "Denzel Curry" in artist and "Pig Feet" in title:
            artist = "Terrace Martin & Denzel Curry"
        title = title.replace("$hit", "Shit")
        self.currentArtist.set(artist)
        self.currentAlbum.set(album)
        self.currentTitle.set(title)
        self.currentYear.set(EasyID3(filename)['date'][0])
        if "Marc Rebillet" in artist and "Europe" in album and "Malta" not in title:
            return True
        elif "Dizzee Rascal" in artist and "Face" in title:
            return True
        return False

    def thread_function(self):
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        self.errorSound = threading.Thread(target=self.thread_function,
                                           daemon=True)

    def titleContainsRomanNumeral(self):
        for index in range(len(self.romanNums)):
            if self.romanNums[index] in self.currentTitle.get():
                return index
        return -1

    def checkIfWebpageExists(self):
        name = self.namingConventions(
            self.currentArtist.get() + " " + self.currentTitle.get(), True)
        url = "https://genius.com/" + name + "-lyrics"
        self.currentUrl.set(url)
        req = Request(self.currentUrl.get(),
                      headers={'User-Agent': 'Mozilla/5.0'})
        try:
            webpage = urlopen(req).read()
            # Creating a BeautifulSoup object of the html page for easy extraction of data.
            soup = BeautifulSoup(webpage, 'html.parser')
            return soup
        except:
            return None

    def setLyricsCycle(self):
        soup = self.checkIfWebpageExists()
        if soup != None:
            for div in soup.findAll('div', attrs={'class': 'lyrics'}):
                self.currentLyrics += div.text.strip()
            if self.currentLyrics.strip() == "":
                for div in soup.findAll(
                        'div',
                        attrs={
                            'class': 'Lyrics__Container-sc-1ynbvzw-2 iVKelV'
                        }):
                    linha = ''
                    for elem in div.recursiveChildGenerator():
                        if isinstance(elem, str):
                            linha += elem.strip()
                        elif elem.name == 'br':
                            linha += '\n'
                    self.currentLyrics += linha
            if self.currentLyrics.strip() == "":
                self.setLyricsCycle()
        else:
            index = self.titleContainsRomanNumeral()
            if "pt" in self.currentTitle.get().lower(
            ) and not self.removePtOrPart:
                self.currentTitle.set(self.currentTitle.get().replace(
                    "pt", "part").replace("Pt", "Part"))
                self.removePtOrPart = True
            elif "part" in self.currentTitle.get().lower(
            ) and not self.removePtOrPart:
                self.currentTitle.set(self.currentTitle.get().replace(
                    "part", "pt").replace("Part", "Pt"))
                self.removePtOrPart = True
            elif index != -1:
                self.currentTitle.set(self.currentTitle.get().replace(
                    self.romanNums[index], str(index + 1)))
                self.removePtOrPart = False
            else:
                self.errorSound.start()
                self.errorHandled.set(False)
                self.enableEntries(1)
                self.btn_tryAgain.wait_variable(self.errorHandled)
                self.disableEntries()
            if self.currentLyrics.strip() == "":
                self.setLyricsCycle()

    """
        Gets the lyrics of the file passed as parameter, writing them in the metaTags of the file, given it has the metaTags defined correctly
        In case of not finding the page, it asks the user
    """

    def setLyrics(self, filename, skip):
        self.currentLyrics = ""
        if skip:
            return
        self.setLyricsCycle()
        if self.currentLyrics != "None":
            audio = ID3(filename)
            audio.delall("USLT")
            audio.add(USLT(encoding=3, text=self.currentLyrics))
            audio.save()

    """
        Gets the year of release of the file passed as parameter, writing it in the metaTag of the file, given it has the metaTags defined correctly
        In case of not finding the page, it asks the user. If the user writes two empty lines, it skips, leaving the original year
    """

    def getYearCycle(self):
        name = self.namingConventions(self.currentArtist.get(),
                                      True) + "/" + self.namingConventions(
                                          self.currentAlbum.get(), False)
        url = "https://www.genius.com/albums/" + name
        self.currentUrl.set(url)
        if url in AlbumAndLyricsScreen.pagesVisited_year:
            self.currentYear.set(AlbumAndLyricsScreen.pagesVisited_year[url])
            return
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            webpage = urlopen(req).read()
            # Creating a BeautifulSoup object of the html page for easy extraction of data.
            soup = BeautifulSoup(webpage, 'html.parser')
            yearTemp = ""
            #Extract the year of the album
            for div in soup.findAll('div', attrs={'class': 'metadata_unit'}):
                yearTemp += div.text.strip()
                break
            year = yearTemp.split()
            AlbumAndLyricsScreen.pagesVisited_year[url] = year[len(year) - 1]
            self.currentYear.set(year[len(year) - 1])
            return
        except:
            try:
                name = self.namingConventions(
                    self.currentArtist.get() + " " + self.currentTitle.get(),
                    True)
                url = "https://genius.com/" + name + "-lyrics"
                self.currentUrl.set(url)
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, 'html.parser')
                aux = soup.get_text(separator="\n").split(sep="\n")
                aux = [item for item in aux if item.strip() != ""]
                year = [
                    aux[index + 1] for index in range(len(aux))
                    if "release date" in aux[index].lower()
                ][0]
                nonInt = False
                try:
                    int(year[len(year) - 4:])
                except:
                    nonInt = True
                if not nonInt:
                    AlbumAndLyricsScreen.pagesVisited_year[url] = year[len(year
                                                                           ) -
                                                                       4:]
                    self.currentYear.set(year[len(year) - 4:])
                    return
            except:
                self.errorSound.start()
                key = (self.currentArtist.get(), self.currentAlbum.get())
                self.errorHandled.set(False)
                self.enableEntries(0)
                self.btn_tryAgain.wait_variable(self.errorHandled)
                value = [self.currentArtist.get(), self.currentAlbum.get()]
                AlbumAndLyricsScreen.artistAlbumReplacements[key] = value
                self.disableEntries()
        self.getYearCycle()
        return

    def getYear(self, filename):
        self.getYearCycle()
        year = self.currentYear.get()
        audio = ID3(filename)
        audio.delall("TDRC")
        audio.add(TDRC(encoding=3, text=year))
        audio.save()

    def lyricsAndYear(self):
        if self.newFiles != []:
            self.removePtOrPart = False
            filename = self.newFiles[0]
            self.gettingYear = True
            skipLyrics = self.ArtistAlbumAndTitle(filename)
            self.addToOutput()
            self.getYear(filename)
            self.gettingYear = False
            self.changeTag("lyrics")
            self.setLyrics(filename, skipLyrics)
            self.changeTag("success")
            for txt in self.textBoxes:
                txt.insert(TK.END, "\n")
                txt.see(TK.END)
            self.numberOfFilesProcessed += 1
            self.title.set(
                str(self.numberOfFilesProcessed) + "/" +
                str(self.totalNewFiles) + " Files Processed")
            Screen.window.update_idletasks()
            self.newFiles.remove(filename)
            Screen.window.after(50, self.lyricsAndYear)
        else:
            if self.finished:
                for txt in self.textBoxes:
                    txt.delete("end-1c linestart", TK.END)
                self.finished = False
                self.frm_newAAT.destroy()
                self.lbl_url.destroy()
                if self.musicDestinyDir != None and self.musicOriginDir != None:
                    self.btn_downloadMore.grid(row=2, column=0)
                self.btn_exit.grid(row=3, column=0)


if __name__ == "__main__":
# def main():
    # For ignoring SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    Screen.window.title("Downloader")
    Screen.window.configure(bg=DEFAULT_BGCOLOR)
    InitialScreen(TK.Frame())
    Screen.window.mainloop()
    #os.system("cls")
    #url = "https://genius.com/Jpegmafia-bald-lyrics"
    #print(url)
    #webbrowser.open(url)
    # url = "https://www.google.com.tr/search?q={}".format(
    #     "Radiohead".replace(" &", "").replace(" ", "+") + "+" +
    #     "A Punch Up At A Wedding".replace(" &", "").replace(" ", "+") +
    #     "+lyrics+site:Genius.com")
    # req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # webpage = urlopen(req).read()
    # soup = BeautifulSoup(webpage, 'html.parser')
    # links = soup.findAll("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
    # url2 = str(links[0])[str(links[0]).find("https"):str(links[0]).find("&")]
    # print(url2)
    # req2 = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    # webpage2 = urlopen(req2).read()
    # soup2 = BeautifulSoup(webpage2, 'html.parser')
    # aux = soup.get_text(separator="\n").split(sep="\n")
    # aux = [f for f in aux if f.strip() != ""]
    # print(aux)
    # for i in range(len(aux)):
    #     if "release date" in aux[i].lower():
    #         #print(aux[i])
    #         print(aux[i + 1][len(aux[i + 1]) - 4:])
    #         break
    # lyrics = ""
    # while lyrics.strip() == "":
    #     for div in soup2.findAll('div', attrs={'class': 'lyrics'}):
    #         lyrics += div.text.strip()
    #     if lyrics.strip() == "":
    #         for div in soup2.findAll(
    #                 'div',
    #                 attrs={'class': 'Lyrics__Container-sc-1ynbvzw-2 iVKelV'}):
    #             linha = ''
    #             for elem in div.recursiveChildGenerator():
    #                 if isinstance(elem, str):
    #                     linha += elem.strip()
    #                 elif elem.name == 'br':
    #                     linha += '\n'
    #             lyrics += linha
    # print(lyrics)
