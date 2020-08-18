import os
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
import subprocess
from Screen import Screen
from ScrollableWidget import ScrollableWidget

# OneDrive = os.path.join('C:', os.path.sep, 'Users', 'ruben',
#                         'Onedrive - Universidade da Madeira', 'Ano_2',
#                         'Semestre_2')
# ACaulas = os.path.join(OneDrive, 'AC', 'Aulas')
# ACpl = os.path.join(OneDrive, 'AC', 'PL')
# ACtp = os.path.join(OneDrive, 'AC', 'TP')
# ACfreq = os.path.join(OneDrive, 'AC', 'Frequências')
# ACgeral = os.path.join(OneDrive, 'AC')
# MNIOtp = os.path.join(OneDrive, 'MNIO', 'TP')
# MNIOformularios_geral = os.path.join(OneDrive, 'MNIO')
# POOaulas = os.path.join(OneDrive, 'POO', 'Aulas')
# POOpl = os.path.join(OneDrive, 'POO', 'PL')
# POOgeral = os.path.join(OneDrive, 'POO')
# TFCaulas = os.path.join(OneDrive, 'TFC', 'Aulas')
# TFCtp = os.path.join(OneDrive, 'TFC', 'TP')
# TFCgeral = os.path.join(OneDrive, 'TFC')

#TODO: comment the code


class InitialScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)
        Screen.container.getDirectories()
        #Widget Creation
        self.lbl_title = TK.Label(
            self.frm_master,
            text=
            "Welcome to the Download Helper!\nYou want help moving files related to school or music?",
            bg=Screen.DEFAULT_BGCOLOR,
            font=Screen.DEFAULT_FONT1,
            fg="white")
        # self.btn_schoolVersion = TK.Button(self.frm_master,
        #                                    font=Screen.DEFAULT_FONT3,
        #                                    text="School",
        #                                    command=self.schoolScreen)
        self.btn_musicVersion = TK.Button(self.frm_master,
                                          font=Screen.DEFAULT_FONT3,
                                          text="Music (Downloaded)",
                                          command=self.musicScreen)
        self.btn_musicModifiedVersion = TK.Button(
            self.frm_master,
            font=Screen.DEFAULT_FONT3,
            text="Music (Files Modified)",
            command=self.albumLyricsScreen)
        self.btn_grimeArtistsExceptions = TK.Button(
            self.frm_master,
            text="Grime Artists And Exceptions",
            font=Screen.DEFAULT_FONT3,
            command=self.grimeArtistsExceptionsScreen)
        self.frm_whichDirectories = TK.Frame(self.frm_master,
                                             width=750,
                                             bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_whichDirectories = TK.Label(
            self.frm_whichDirectories,
            text="Choose the respective directories",
            font=Screen.DEFAULT_FONT1,
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white")
        self.lbl_downloadsDirectory = TK.Label(self.frm_whichDirectories,
                                               text="Downloads",
                                               font=Screen.DEFAULT_FONT2,
                                               bg=Screen.DEFAULT_BGCOLOR,
                                               fg="white")
        self.ent_downloadsDirectory = TK.Entry(self.frm_whichDirectories,
                                               width=60,
                                               state=TK.NORMAL,
                                               font=Screen.DEFAULT_FONT3)
        self.lbl_musicOriginDirectory = TK.Label(self.frm_whichDirectories,
                                                 text="Origin Music",
                                                 font=Screen.DEFAULT_FONT2,
                                                 bg=Screen.DEFAULT_BGCOLOR,
                                                 fg="white")
        self.ent_musicOriginDirectory = TK.Entry(self.frm_whichDirectories,
                                                 width=60,
                                                 state=TK.NORMAL,
                                                 font=Screen.DEFAULT_FONT3)
        self.lbl_musicDestinyDirectory = TK.Label(self.frm_whichDirectories,
                                                  text="Destiny Music",
                                                  font=Screen.DEFAULT_FONT2,
                                                  bg=Screen.DEFAULT_BGCOLOR,
                                                  fg="white")
        self.ent_musicDestinyDirectory = TK.Entry(self.frm_whichDirectories,
                                                  width=60,
                                                  state=TK.NORMAL,
                                                  font=Screen.DEFAULT_FONT3)
        i = 0
        while i < 3:
            self.btn_chooseDirectory = TK.Button(
                self.frm_whichDirectories,
                text="Open",
                command=lambda i=i: self.chooseDirectory(i),
                font=Screen.DEFAULT_FONT3)
            self.btn_chooseDirectory.grid(row=i + 1, column=2)
            i += 1

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=200)
        # self.btn_schoolVersion.grid(row=2, column=1)
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
        self.ent_downloadsDirectory.insert(
            TK.END, str(Screen.container.downloadsDirectory))
        self.ent_downloadsDirectory.config(state="readonly")
        self.ent_musicOriginDirectory.insert(
            TK.END, str(Screen.container.musicOriginDirectory))
        self.ent_musicOriginDirectory.config(state="readonly")
        self.ent_musicDestinyDirectory.insert(
            TK.END, str(Screen.container.musicDestinyDirectory))
        self.ent_musicDestinyDirectory.config(state="readonly")
        Screen.container.getExceptions()

    def chooseDirectory(self, whichOne):
        aux = filedialog.askdirectory(initialdir=os.path.join(
            "C:", os.path.sep, "Users", "ruben", "Desktop")).replace(
                "/", "\\")
        if aux != "":
            if whichOne == 0:
                Screen.container.downloadsDirectory = aux
            elif whichOne == 1:
                Screen.container.musicOriginDirectory = aux
                ent_Directory = self.ent_musicOriginDirectory
            else:
                Screen.container.musicDestinyDirectory = aux
                ent_Directory = self.ent_musicDestinyDirectory
            Screen.container.saveDirectories()
            ent_Directory.config(state=TK.NORMAL)
            ent_Directory.delete(0, 'end')
            ent_Directory.insert(TK.END, aux)
            ent_Directory.config(state="readonly")

    # def schoolScreen(self):
    #     SchoolScreen(self.frm_master)

    def musicScreen(self):
        MusicScreen(self.frm_master, True)

    def albumLyricsScreen(self):
        AlbumAndLyricsScreen(self.frm_master, [
            os.path.join(Screen.container.musicDestinyDirectory, f)
            for f in os.listdir(Screen.container.musicDestinyDirectory)
            if os.path.join(Screen.container.musicDestinyDirectory, f).
            endswith(".mp3") and os.path.getmtime(
                os.path.join(Screen.container.musicDestinyDirectory,
                             f)) > Screen.container.timeOfLastModifiedFile
        ])

    def grimeArtistsExceptionsScreen(self):
        GrimeArtistsAndExceptionsScreen(self.frm_master)


class GrimeArtistsAndExceptionsScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)
        #Tkinter Vars
        self.newArtistOrOldPair = TK.StringVar()
        self.newPair = TK.StringVar()
        Screen.container.getGrimeArtists()
        self.mode = 0
        #1 - new Grime Artist
        #2 - delete Grime Artist
        #3 - new url replacement pair
        #TODO: down
        #4 - delete url replacement pair
        #5 - add exception
        #6 - delete exception

        #Widget Creation
        self.lbl_title = TK.Label(
            self.frm_master,
            text=
            "Insert New Grime Artist or Remove or create Url Replacement Pair",
            font=Screen.DEFAULT_FONT1,
            fg="white",
            bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_auxEntry = TK.Label(self.frm_master,
                                     font=Screen.DEFAULT_FONT2,
                                     fg="white",
                                     bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_newPair = TK.Label(self.frm_master,
                                    text="New Replacement",
                                    font=Screen.DEFAULT_FONT2,
                                    fg="white",
                                    bg=Screen.DEFAULT_BGCOLOR)
        self.ent_artistOrOldPair = TK.Entry(
            self.frm_master,
            textvariable=self.newArtistOrOldPair,
            font=Screen.DEFAULT_FONT3,
            width=30)
        self.ent_newPair = TK.Entry(self.frm_master,
                                    textvariable=self.newPair,
                                    font=Screen.DEFAULT_FONT3,
                                    width=30)
        self.btn_addArtist = TK.Button(self.frm_master,
                                       text="Add New Artist",
                                       font=Screen.DEFAULT_FONT3,
                                       command=self.addArtist)
        self.btn_removeArtist = TK.Button(self.frm_master,
                                          text="Remove Artist",
                                          font=Screen.DEFAULT_FONT3,
                                          command=self.removeArtist)
        self.btn_addUrlReplacementPair = TK.Button(
            self.frm_master,
            text="Add Url Replacement Pair",
            font=Screen.DEFAULT_FONT3,
            command=self.newReplacementPair)
        self.btn_confirm = TK.Button(self.frm_master,
                                     text="Confirm",
                                     font=Screen.DEFAULT_FONT3,
                                     command=self.nextScreen)
        self.btn_previousScreen = TK.Button(self.frm_master,
                                            text="Go Back",
                                            font=Screen.DEFAULT_FONT3,
                                            command=self.backScreen)
        self.scrollableWidget = ScrollableWidget(self.frm_master, ["Listbox"])
        self.scrollableWidget.boxes[0].config(height=15,width=50)

        #Widget Placement
        self.lbl_title.grid(row=0, column=2)
        self.btn_addArtist.grid(row=2, column=1)
        self.btn_removeArtist.grid(row=3, column=1)
        self.btn_addUrlReplacementPair.grid(row=4, column=1)
        self.btn_previousScreen.grid(row=4, column=0)
        self.scrollableWidget.frame.grid(row=1, column=3, rowspan=1500)
        self.scrollableWidget.boxes[0].grid(row=0, column=0)
        self.scrollableWidget.scrollbar.grid(row=0,column=1,sticky=TK.NS)

    def backScreen(self, event=None):
        Screen.container.saveGrimeArtists()
        InitialScreen(self.frm_master)

    def nextScreen(self, event=None):
        artist = self.newArtistOrOldPair.get()
        if self.mode == 1:
            if artist != "":
                Screen.container.grimeArtists.append(artist)
        elif self.mode == 2:
            if artist != "":
                try:
                    Screen.container.grimeArtists.remove(artist)
                except ValueError:
                    pass
        else:
            newPair = self.newPair.get()
            try:
                old = artist[artist.find("\"") + 1:artist.rfind("\"")]
                new = newPair[newPair.find("\"") + 1:newPair.rfind("\"")]
                if new == "": new = None
                Screen.container.replacementsDict[old] = new
            except:
                pass
        self.newArtistOrOldPair.set("")
        self.newPair.set("")
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        self.lbl_title.config(
            text=
            "Insert New Grime Artist or Remove or create Url Replacement Pair")
        self.btn_addArtist.grid(row=2, column=1)
        self.btn_removeArtist.grid(row=3, column=1)
        self.btn_addUrlReplacementPair.grid(row=4, column=1)
        self.btn_previousScreen.grid(row=4, column=0)
        self.lbl_auxEntry.grid_forget()
        self.ent_artistOrOldPair.grid_forget()
        self.lbl_newPair.grid_forget()
        self.ent_newPair.grid_forget()
        self.btn_confirm.grid_forget()

    def addArtist(self):
        self.mode = 1
        self.lbl_title.config(text="Insert the name of the Artist")
        self.lbl_auxEntry.config(text="Artist")
        self.lbl_auxEntry.grid(row=1, column=1)
        self.ent_artistOrOldPair.grid(row=1, column=2)
        self.btn_confirm.grid(row=2, column=2)
        self.btn_addArtist.grid_forget()
        self.btn_removeArtist.grid_forget()
        self.btn_addUrlReplacementPair.grid_forget()
        self.btn_previousScreen.grid_forget()

    def newReplacementPair(self):
        self.mode = 3
        self.lbl_title.config(
            text="Insert what to replace and what with, in \"\"")
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        for key in Screen.container.replacementsDict:
            self.scrollableWidget.boxes[0].insert(
                TK.END, "\"" + key + "\"\t--->\t\"" +
                Screen.container.replacementsDict[key] + "\"")
        self.lbl_auxEntry.config(text="Old Replacement")
        self.lbl_auxEntry.grid(row=1, column=1)
        self.lbl_newPair.grid(row=2, column=1)
        self.ent_artistOrOldPair.grid(row=1, column=2)
        self.ent_newPair.grid(row=2, column=2)
        self.btn_confirm.grid(row=3, column=2)
        self.btn_addArtist.grid_forget()
        self.btn_removeArtist.grid_forget()
        self.btn_addUrlReplacementPair.grid_forget()
        self.btn_previousScreen.grid_forget()

    def removeArtist(self):
        self.mode = 2
        self.lbl_title.config(text="Insert the name of the Artist")
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        for artist in Screen.container.grimeArtists:
            self.scrollableWidget.boxes[0].insert(0, artist)
        self.lbl_auxEntry.config(text="Artist")
        self.lbl_auxEntry.grid(row=1, column=1)
        self.ent_artistOrOldPair.grid(row=1, column=2)
        self.btn_confirm.grid(row=2, column=2)
        self.btn_addArtist.grid_forget()
        self.btn_removeArtist.grid_forget()
        self.btn_addUrlReplacementPair.grid_forget()
        self.btn_previousScreen.grid_forget()


# class SchoolScreen(Screen):
#     def __init__(self, masterFramePreviousScreen):
#         super().__init__(masterFramePreviousScreen)
#         #Tkinter Vars
#         self.title = TK.StringVar()
#         self.numberOfFiles = 0
#         self.title.set(str(self.numberOfFiles) + " Files Found")

#         #Widget Creation
#         self.lbl_title = TK.Label(self.frm_master,
#                                   textvariable=self.title,
#                                   font=Screen.DEFAULT_FONT1,
#                                   bg=Screen.DEFAULT_BGCOLOR,
#                                   fg="white")
#         self.txt_filesFound = TK.Text(self.frm_master,
#                                       bg=Screen.DEFAULT_BGCOLOR,
#                                       fg="white",
#                                       font=Screen.DEFAULT_FONT3)
#         self.txt_filesMoved = TK.Text(self.frm_master,
#                                       bg=Screen.DEFAULT_BGCOLOR,
#                                       fg="white",
#                                       font=Screen.DEFAULT_FONT3)
#         self.btn_stopCycle = TK.Button(self.frm_master,
#                                        text="Stop",
#                                        font=Screen.DEFAULT_FONT3,
#                                        command=self.stopCheckDownloads)

#         #Widget Placement
#         self.lbl_title.grid(row=0, column=0, padx=200)
#         self.txt_filesFound.grid(row=1, column=0)
#         self.txt_filesMoved.grid(row=1, column=1)
#         self.btn_stopCycle.grid(row=2, column=0)

#         Screen.window.update_idletasks()

#         self.cycleCondition = True
#         webbrowser.open("https://moodle.cee.uma.pt/login/index.php", new=2)
#         webbrowser.open("https://infoalunos.uma.pt", new=2)
#         self.txt_filesMoved.tag_config("existed", fg="yellow")
#         self.txt_filesMoved.tag_config("notExisted", fg="green")
#         self.txt_filesMoved.tag_config("deleted/Skipped", fg="red")
#         self.checkDownloads()

#     def stopCheckDownloads(self):
#         self.cycleCondition = False
#         self.btn_stopCycle.destroy()

#     def addToOutput(self, fileFound, fileMoved, tag):
#         self.numberOfFiles += 1
#         self.title.set(str(self.numberOfFiles) + " Files Found")
#         self.txt_filesFound.config(state=TK.NORMAL)
#         self.txt_filesMoved.config(state=TK.NORMAL)
#         self.txt_filesFound.insert(TK.END, fileFound + "\n")
#         self.txt_filesMoved.insert(TK.END, fileMoved + "\n", tag)
#         self.txt_filesFound.config(state=TK.DISABLED)
#         self.txt_filesMoved.config(state=TK.DISABLED)
#         Screen.window.update_idletasks()
#         self.txt_filesFound.see(TK.END)
#         self.txt_filesMoved.see(TK.END)

#     def checkDownloads(self):
#         #FIXME: need to adapt this to the GUI and the new disciplines when the time comes
#         if self.cycleCondition:
#             Screen.window.after(1000, self.checkDownloads)
#             for filename in os.listdir(Screen.container.downloadsDirectory):
#                 #try:
#                 if os.path.getctime(os.path.join(
#                         Screen.container.downloadsDirectory,
#                         filename)) > Screen.tempoAtual and os.path.getsize(
#                             os.path.join(
#                                 Screen.container.downloadsDirectory,
#                                 filename)) > 0 and filename.endswith(".pdf"):
#                     destino = self.whichFolder(filename)
#                     if "False" != destino:
#                         count += 1
#                         try:
#                             os.rename(
#                                 os.path.join(Screen.container.downloadsDirectory, filename),
#                                 destino)
#                             self.addToOutput(filename, destino, "notExisted")
#                             # print("File downloaded succesfully")
#                         except FileExistsError:
#                             os.remove(destino)
#                             os.rename(
#                                 os.path.join(Screen.container.downloadsDirectory, filename),
#                                 destino)
#                             self.addToOutput(filename, destino, "existed")
#                             #print("File replaced succesfully")
#                     else:
#                         self.addToOutput(filename, "REMOVED/SKIPPED",
#                                          "deleted/Skipped")
#                         #print("File skipped/deleted")
#                 # except FileNotFoundError:
#                 #     if not filename.endswith(".part"):
#                 #         print(filename + "\nERRO")
#                 #         break

#     def whichFolder(self, filename):
#         if filename.startswith("PT_AC_"):
#             return os.path.join(ACaulas,
#                                 filename[len("PT_AC_"):].replace("T_", ""))
#         elif filename.startswith("Apresentação") or filename.startswith(
#                 "Guia"):
#             return os.path.join(ACpl, filename)
#         elif filename.startswith("Aula_"):
#             return os.path.join(ACtp, filename)
#         elif filename.startswith("T1") or filename.startswith("T2"):
#             if "Frequencia" in filename:
#                 return os.path.join(
#                     ACfreq, 'Normal',
#                     filename[len("T1_"):].replace("_AC",
#                                                   "").replace("_PT", ""))
#             elif "Recurso" in filename:
#                 return os.path.join(
#                     ACfreq, 'Recurso', filename[len("T1_T2_"):].replace(
#                         "_AC", "").replace("_PT", "").replace("_20", ""))
#             elif "Especial" in filename:
#                 return os.path.join(
#                     ACfreq, 'EpocaEspecial', filename[len("T1_T2_"):].replace(
#                         "_AC", "").replace("_PT", "").replace("_20", ""))
#         elif filename.startswith("AC_P"):
#             return os.path.join(ACgeral,
#                                 "Enunciado Projeto " + filename[4] + ".pdf")
#         elif filename[2] == ".":
#             return os.path.join(POOaulas, filename)
#         elif filename.startswith("Ficha"):
#             diretoria = os.path.join(
#                 POOpl, filename[:filename.find(".")].replace(" ", ""))
#             try:
#                 os.makedirs(diretoria)
#             except FileExistsError:
#                 print("Directory already existed")
#             return os.path.join(diretoria, filename)
#         elif filename.startswith("MNIO_FichaExerc"):
#             return os.path.join(MNIOtp, filename[len("MNIO_"):])
#         elif filename.startswith("MNIO_Formulario"):
#             return os.path.join(MNIOformularios_geral, filename[len("MNIO_"):])
#         elif filename.startswith("Folha"):
#             return os.path.join(TFCtp, filename.replace("TFC1920", ""))
#         elif filename.startswith("TFC1920"):
#             numero = filename[filename.rfind("Semana") +
#                               6:filename.rfind("Handout") - 1]
#             return os.path.join(
#                 TFCaulas,
#                 filename.replace("TFC1920", "").replace("-", "")[0:12] +
#                 numero + ".pdf")
#         else:
#             rename = input(
#                 "This is the file " + filename +
#                 "\nDo you want to rename it? (y/n, d to delete, s to skip)\n")
#             if rename == "y":
#                 filename = input("Rename the file: ") + ".pdf"
#             elif rename == "d":
#                 os.remove(os.path.join(Screen.container.downloadsDirectory, filename))
#                 return "False"
#             elif rename == "s":
#                 return "False"
#             op = input(
#                 "Choose the discipline:\n1.AC\n2.POO\n3.TFC\n4.MNIO\nOption: ")
#             if op == "1":
#                 return os.path.join(ACgeral, filename)
#             elif op == "2":
#                 return os.path.join(POOgeral, filename)
#             elif op == "3":
#                 return os.path.join(TFCgeral, filename)
#             elif op == "4":
#                 return os.path.join(MNIOformularios_geral, filename)


class MusicScreen(Screen):
    def __init__(self, masterFramePreviousScreen, firstTime):
        super().__init__(masterFramePreviousScreen)
        # if firstTime:
        #     os.startfile(
        #         r"C:\Users\ruben\Desktop\deemix\deemix-tools\start.bat")

        #Tkinter Vars
        self.numberOfFilesFound = 0
        self.numberOfFilesMoved = 0
        self.buffer = []
        self.checkMusicCondition = True
        self.newFiles = []
        self.title = TK.StringVar()
        self.title.set(str(self.numberOfFilesFound) + " Files Found")

        #Widget Creation
        self.lbl_title = TK.Label(self.frm_master,
                                  textvariable=self.title,
                                  font=Screen.DEFAULT_FONT1,
                                  bg=Screen.DEFAULT_BGCOLOR,
                                  fg="white")
        self.scrollableWidget = ScrollableWidget(self.frm_master,
                                                 ["Textbox", "Textbox"])
        self.lbl_beforeFiles = TK.Label(self.scrollableWidget.frame,
                                        bg=Screen.DEFAULT_BGCOLOR,
                                        fg="white",
                                        text="Before",
                                        font=Screen.DEFAULT_FONT2)
        self.lbl_afterFiles = TK.Label(self.scrollableWidget.frame,
                                       bg=Screen.DEFAULT_BGCOLOR,
                                       fg="white",
                                       text="After",
                                       font=Screen.DEFAULT_FONT2)
        self.scrollableWidget.boxes[0].config(state=TK.DISABLED)
        self.scrollableWidget.boxes[1].config(state=TK.DISABLED)
        self.btn_nextScreen = TK.Button(self.frm_master,
                                        text="Move Files",
                                        font=Screen.DEFAULT_FONT3,
                                        command=self.nextScreen)

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=200)
        self.scrollableWidget.frame.grid(row=1, column=0)
        self.lbl_beforeFiles.grid(row=0, column=0)
        self.lbl_afterFiles.grid(row=0, column=1)
        self.scrollableWidget.scrollbar.grid(row=1, column=2, sticky=TK.NS)
        self.scrollableWidget.boxes[0].grid(row=1, column=0)
        self.scrollableWidget.boxes[1].grid(row=1, column=1)
        self.btn_nextScreen.grid(row=2, column=0)

        self.checkMusic()

    def nextScreen(self, event=None):
        if self.checkMusicCondition:
            self.checkMusicCondition = False
            self.scrollableWidget.boxes[0].delete("end-1c linestart", TK.END)
            self.moveOutOfBuffer()
            self.scrollableWidget.boxes[1].delete("end-1c linestart", TK.END)
            self.btn_nextScreen.config(text="Get Album Year and Lyrics")
        else:
            AlbumAndLyricsScreen(self.frm_master, self.newFiles)

    def checkMusic(self):
        for filename in os.listdir(Screen.container.musicOriginDirectory):
            if filename.endswith(".mp3") and filename not in self.buffer:
                self.buffer.append(filename)
                self.scrollableWidget.boxes[0].config(state=TK.NORMAL)
                self.scrollableWidget.boxes[0].insert(TK.END, filename + "\n")
                self.scrollableWidget.boxes[0].config(state=TK.DISABLED)
                self.scrollableWidget.boxes[0].see(TK.END)
                self.numberOfFilesFound += 1
                self.title.set(str(self.numberOfFilesFound) + " Files Found")
            elif filename.endswith(".txt"):
                for ficheiro in self.buffer:
                    os.remove(
                        os.path.join(Screen.container.musicOriginDirectory,
                                     ficheiro))
                self.buffer.clear()
                self.scrollableWidget.boxes[0].config(state=TK.NORMAL)
                self.scrollableWidget.boxes[0].delete("1.0", TK.END)
                self.scrollableWidget.boxes[0].config(state=TK.DISABLED)
                self.numberOfFilesFound = 0
                self.title.set(str(self.numberOfFilesFound) + " Files Found")
        if self.checkMusicCondition:
            Screen.window.update_idletasks()
            Screen.window.after(1000, self.checkMusic)

    def addToOutput(self, filename):
        self.scrollableWidget.boxes[1].config(state=TK.NORMAL)
        self.scrollableWidget.boxes[1].insert(TK.END, filename + "\n")
        self.scrollableWidget.boxes[1].config(state=TK.DISABLED)

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
            self.slightTagChanges(
                os.path.join(Screen.container.musicOriginDirectory, old),
                filename)
            try:
                os.rename(
                    os.path.join(Screen.container.musicOriginDirectory, old),
                    os.path.join(Screen.container.musicDestinyDirectory,
                                 filename))
                self.numberOfFilesMoved += 1
                self.addToOutput(filename)
                self.newFiles.append(
                    os.path.join(Screen.container.musicDestinyDirectory,
                                 filename))
            except FileExistsError:
                mp3aEnviar = EasyID3(
                    os.path.join(Screen.container.musicOriginDirectory, old))
                mp3aVerificar = EasyID3(
                    os.path.join(Screen.container.musicDestinyDirectory,
                                 filename))
                if mp3aEnviar['albumartist'][0] == mp3aVerificar[
                        'albumartist'][0] and mp3aEnviar['album'][
                            0] == mp3aVerificar['album'][0]:
                    os.remove(
                        os.path.join(Screen.container.musicOriginDirectory,
                                     old))
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
                            os.path.join(
                                Screen.container.musicDestinyDirectory,
                                filename)):
                        if mp3aEnviar['albumartist'][0] == mp3aVerificar[
                                'albumartist'][0] and mp3aEnviar['album'][
                                    0] == mp3aVerificar['album'][0]:
                            os.remove(
                                os.path.join(
                                    Screen.container.musicOriginDirectory,
                                    old))
                            self.addToOutput(filename +
                                             " already exists, deleted")
                        else:
                            os.rename(
                                os.path.join(
                                    Screen.container.musicOriginDirectory,
                                    old),
                                os.path.join(
                                    Screen.container.musicDestinyDirectory,
                                    filename))
                            self.numberOfFilesMoved += 1
                            self.addToOutput(filename)
                            self.newFiles.append(
                                os.path.join(
                                    Screen.container.musicDestinyDirectory,
                                    filename))
                    else:
                        os.rename(
                            os.path.join(Screen.container.musicOriginDirectory,
                                         old),
                            os.path.join(
                                Screen.container.musicDestinyDirectory,
                                filename))
                        self.numberOfFilesMoved += 1
                        self.addToOutput(filename)
                        self.newFiles.append(
                            os.path.join(
                                Screen.container.musicDestinyDirectory,
                                filename))
            self.buffer.remove(old)
            self.scrollableWidget.boxes[1].see(TK.END)
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
        if mp3['albumartist'][0] in Screen.container.grimeArtists:
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

    def __init__(self, masterFramePreviousScreen, newFiles):
        super().__init__(masterFramePreviousScreen)
        Screen.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Tkinter Vars
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
        self.exceptionRaised = False
        self.key = None
        self.value = None
        self.categories_width = {
            "Artist": 30,
            "Album": 55,
            "Title": 70,
            "Year": 5
        }
        colors = ["yellow", "dark green", "green2"]
        text = ["Getting Album Year", "Getting Track Lyrics", "File Done"]

        #Widget Creation
        self.lbl_title = TK.Label(self.frm_master,
                                  textvariable=self.title,
                                  bg=Screen.DEFAULT_BGCOLOR,
                                  fg="white",
                                  font=Screen.DEFAULT_FONT1)
        self.scrollableWidget = ScrollableWidget(
            self.frm_master,
            ["Textbox" for i in range(len(self.categories_width) - 1)])
        i = 0
        for category in self.categories_width:
            if category == "Year":
                break
            lbl_category = TK.Label(self.scrollableWidget.frame,
                                    text=category,
                                    font=Screen.DEFAULT_FONT2,
                                    bg=Screen.DEFAULT_BGCOLOR,
                                    fg="white")
            self.scrollableWidget.boxes[i].config(
                width=self.categories_width[category])
            self.scrollableWidget.boxes[i].tag_config("album",
                                                      foreground="yellow")
            self.scrollableWidget.boxes[i].tag_config("lyrics",
                                                      foreground="dark green")
            self.scrollableWidget.boxes[i].tag_config("success",
                                                      foreground="green2")
            lbl_category.grid(row=0, column=i)
            self.scrollableWidget.boxes[i].grid(row=1, column=i)
            i += 1
        self.frm_newAAT = TK.Frame(self.frm_master, bg=Screen.DEFAULT_BGCOLOR)
        g = 0
        self.entriesTrack = []
        for category in self.trackBeingReviewedDetails:
            label = TK.Label(self.frm_newAAT,
                             font=Screen.DEFAULT_FONT2,
                             bg=Screen.DEFAULT_BGCOLOR,
                             fg="white",
                             text=category)
            entry = TK.Entry(
                self.frm_newAAT,
                font=Screen.DEFAULT_FONT3,
                textvariable=self.trackBeingReviewedDetails[category],
                width=50)
            self.entriesTrack.append(entry)
            label.grid(row=g, column=0)
            entry.grid(row=g, column=1)
            if category == "Year":
                entry.configure(validatecommand=(entry.register(self.testVal),
                                                 '%P'))
            g += 1
        self.lbl_url = TK.Label(self.frm_master,
                                textvariable=self.currentUrl,
                                font=Screen.DEFAULT_FONT2,
                                bg=Screen.DEFAULT_BGCOLOR,
                                fg="white")
        self.cnv_tagsLabel = TK.Canvas(self.frm_master,
                                       bg=Screen.DEFAULT_BGCOLOR,
                                       highlightthickness=0,
                                       bd=0,
                                       width=200,
                                       height=len(colors) * 1.5 * 25)
        j = 0
        for index in range(len(colors)):
            self.cnv_tagsLabel.create_rectangle(0,
                                                j * 25,
                                                25,
                                                25 + j * 25,
                                                fill=colors[index])
            self.cnv_tagsLabel.create_text(27,
                                           13 + j * 25,
                                           text=" - " + text[index],
                                           fill="white",
                                           font=Screen.DEFAULT_FONT3,
                                           anchor=TK.W)
            j += 1.5
        self.btn_tryAgain = TK.Button(self.frm_newAAT,
                                      text="Try Again",
                                      font=Screen.DEFAULT_FONT3,
                                      command=self.nextScreen,
                                      state=TK.DISABLED)
        self.btn_skipLyrics = TK.Button(self.frm_newAAT,
                                        text="Skip Song",
                                        font=Screen.DEFAULT_FONT3,
                                        command=self.skipLyrics,
                                        state=TK.DISABLED)
        self.btn_downloadMore = TK.Button(self.frm_master,
                                          text="Download More",
                                          font=Screen.DEFAULT_FONT3,
                                          command=self.goBackDownloadMore)
        self.btn_exit = TK.Button(self.frm_master,
                                  text="Exit",
                                  font=Screen.DEFAULT_FONT3,
                                  command=self.exitOpenHandler)

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=300)
        self.scrollableWidget.frame.grid(row=1, column=0)
        self.scrollableWidget.scrollbar.grid(row=1, column=i, sticky=TK.NS)
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
        Screen.container.songsToSkip.append("\n".join([
            self.currentArtist.get(),
            self.currentAlbum.get(),
            self.currentTitle.get()
        ]))
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
        MusicScreen(self.frm_master, False)

    def exitOpenHandler(self):
        Screen.window.quit()
        # subprocess.run(
        #     ['python',
        #      os.path.join(Screen.container.baseDirectory, "Handler_Music.py")])
        # subprocess.run(
        #     [os.path.join(Screen.container.baseDirectory, "Handler_Music.exe")])

    def addToOutput(self):
        i = 0
        for category in self.trackBeingReviewedDetails:
            if i == 3:
                break
            self.scrollableWidget.boxes[i].insert(
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
        for txt in self.scrollableWidget.boxes:
            txt.tag_add(tag, "end-1c linestart", TK.END)
        Screen.window.update_idletasks()

    """
        Gets the parameter name right, according to the Genius url conventions
    """

    def namingConventions(self, name, version):  #version = True -> title
        if not version:
            Screen.container.replacementsDict["&"] = " "
        if "pt." in name.lower() or "part." in name.lower(
        ) or "pts." in name.lower() or "mr." in name.lower(
        ) or "vol." in name.lower():
            Screen.container.replacementsDict["."] = " "
        for key in Screen.container.replacementsDict:
            name = name.replace(key, Screen.container.replacementsDict[key])
        return "-".join(name.split()).capitalize()

    """
        Determines the artist and title to be used in the search for lyrics and handles the most common changes
    """

    def ArtistAlbumAndTitle(self, filename, forYear):
        artist = EasyID3(filename)['albumartist'][0]
        title = EasyID3(filename)['title'][0]
        album = EasyID3(filename)['album'][0]
        if forYear:
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
            # elif "Tea In China" in album:
            #     artist += " & The Alchemist"
            # elif "God's" == album:
            #     album = album.replace("'", " ")
            # elif "Section" in album or "good kid," in album:
            #     album.replace(".", " ")
            if (artist, album) in Screen.container.artistAlbumReplacements:
                tempArtist = artist
                tempAlbum = album
                artist = Screen.container.artistAlbumReplacements[(
                    tempArtist, tempAlbum)][0]
                album = Screen.container.artistAlbumReplacements[(
                    tempArtist, tempAlbum)][1]
                # title = AlbumAndLyricsScreen.songAttributesReplacements[(artist,
                #                                                     album,title)][2]

        title = Screen.removeWordsFromWord([
            "feat", "Feat", "bonus", "Bonus", "Conclusion", "Hidden Track",
            "Vocal Mix", "Explicit", "explicit", "Extended"
        ], title)

        if (artist, title) in Screen.container.artistTitleReplacements:
            tempArtist = artist
            tempTitle = title
            artist = Screen.container.artistTitleReplacements[(tempArtist,
                                                               tempTitle)][0]
            title = Screen.container.artistTitleReplacements[(tempArtist,
                                                              tempTitle)][1]
        # if "King's Dead" == title:
        #     artist = "Jay Rock Kendrick Lamar Future & James Blake"
        # elif "various" in artist.lower():
        #     artist = EasyID3(filename)['artist'][0]
        #     if "," in artist:
        #         artist = artist[:artist.find(",")]
        # elif "wickedskeng" in title.lower():
        #     title = "wickedskengman part 4"
        # elif "Kiss and Tell" == title:
        #     artist += " & Skepta"
        # elif "Short King Anthem" == title:
        #     artist = "blackbear & " + artist
        # elif "Bang (feat." in title:
        #     title = "Bang (Remix)"
        # elif "Psycho" in title and "Curry" in artist:
        #     artist = "slowthai & Denzel Curry"
        # elif "Ripe" in title:
        #     title = "Ripe & Ruin"
        # elif "Life After Death" == title:
        #     title += " (Intro)"
        # elif "Strangiato" in title:
        #     title += " (An Exercise In Self-Indulgence)"
        # elif "Protect Ya Neck" in title:
        #     title = "Protect Ya Neck"
        # elif "Kush & Corinthians" == title:
        #     title += "(His Pain)"
        # elif "P Money" == artist and "Money Over Everyone" == album and "Intro" == title:
        #     title = album + " " + title
        # elif "Punch Up" in title:
        #     title = title.replace("Punch Up", "Punchup")
        # elif "Breaks" == title:
        #     title = "The " + title
        # elif "Packt Like" in title:
        #     title = title.replace("Crushed", "Crushd")
        # elif "Curtains Close" == title:
        #     title += "(Skit)"
        # elif "Paul" in title:
        #     if "Marshall" in album:
        #         title = "Paul Skit 2000"
        #     elif "Eminem" in album:
        #         title = "Paul Rosenberg Skit 2002"
        # elif "Steve Ber" in title:
        #     if "Marshall" in album:
        #         title = "Steve Berman Skit 2000"
        #     elif "Eminem" in album:
        #         title = "Steve Berman Skit 2002"
        # elif "JME" in artist and "Taking Over" in title:
        #     title += " (It Ain't Working)"
        # elif "Denzel Curry" in artist and "Pig Feet" in title:
        #     artist = "Terrace Martin & Denzel Curry"
        # title = title.replace("$hit", "Shit")
        self.currentArtist.set(artist)
        self.currentAlbum.set(album)
        self.currentTitle.set(title)
        self.currentYear.set(EasyID3(filename)['date'][0])
        # if "Marc Rebillet" in artist and "Europe" in album and "Malta" not in title:
        #     return True
        # elif "Dizzee Rascal" in artist and "Face" in title:
        #     return True

    def thread_function(self):
        self.exceptionRaised = True
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        self.errorSound = threading.Thread(target=self.thread_function,
                                           daemon=True)

    def titleContainsRomanNumeral(self):
        for index in range(len(self.romanNums)):
            if self.romanNums[index] in self.currentTitle.get():
                return index
        return -1

    def checkIfWebpageExists(self, forAlbum):
        skip = False
        if forAlbum:
            name = self.namingConventions(self.currentArtist.get(),
                                          True) + "/" + self.namingConventions(
                                              self.currentAlbum.get(), False)
            url = "https://www.genius.com/albums/" + name
            if url in AlbumAndLyricsScreen.pagesVisited_year:
                self.currentYear.set(
                    AlbumAndLyricsScreen.pagesVisited_year[url])
                skip = True
        else:
            name = self.namingConventions(
                self.currentArtist.get() + " " + self.currentTitle.get(), True)
            url = "https://genius.com/" + name + "-lyrics"
        self.currentUrl.set(url)
        Screen.window.update_idletasks()
        if skip:
            return "Skip"
        req = Request(self.currentUrl.get(),
                      headers={'User-Agent': 'Mozilla/5.0'})
        try:
            webpage = urlopen(req).read()
            # Creating a BeautifulSoup object of the html page for easy extraction of data.
            soup = BeautifulSoup(webpage, 'html.parser')
            return soup
        except:
            return None

    """
        Gets the year of release of the file passed as parameter, writing it in the metaTag of the file, given it has the metaTags defined correctly
        In case of not finding the page, it asks the user. If the user writes two empty lines, it skips, leaving the original year
    """

    def getYearCycle(self):
        soup = self.checkIfWebpageExists(True)
        if soup == "Skip":
            return
        if soup != None:
            yearTemp = ""
            #Extract the year of the album
            for div in soup.findAll('div', attrs={'class': 'metadata_unit'}):
                yearTemp += div.text.strip()
                break
            year = yearTemp.split()
            AlbumAndLyricsScreen.pagesVisited_year[
                self.currentUrl.get()] = year[len(year) - 1]
            self.currentYear.set(year[len(year) - 1])
            return
        else:
            soup = self.checkIfWebpageExists(False)
            if soup != None:
                aux = soup.get_text(separator="\n").split(sep="\n")
                aux = [item for item in aux if item.strip() != ""]
                year = [
                    aux[index + 1] for index in range(len(aux))
                    if "release date" in aux[index].lower()
                ][0]
                try:
                    int(year[len(year) - 4:])
                    self.currentYear.set(year[len(year) - 4:])
                    return
                except Exception as error:
                    print(error)
            else:
                while True:
                    try:
                        self.errorSound.start()
                        break
                    except:
                        pass
                self.errorHandled.set(False)
                self.enableEntries(0)
                self.btn_tryAgain.wait_variable(self.errorHandled)
                self.value = [
                    self.currentArtist.get(),
                    self.currentAlbum.get()
                ]
                self.disableEntries()
        self.getYearCycle()
        return

    def getYear(self, filename):
        self.getYearCycle()
        audio = ID3(filename)
        audio.delall("TDRC")
        audio.add(TDRC(encoding=3, text=self.currentYear.get()))
        audio.save()

    def setLyricsCycle(self):
        soup = self.checkIfWebpageExists(False)
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
                if "\n".join([artist, album,
                              title]) in Screen.container.songsToSkip:
                    self.currentLyrics = "None"
                    return
                while True:
                    try:
                        self.errorSound.start()
                        break
                    except:
                        pass
                self.errorHandled.set(False)
                self.enableEntries(1)
                self.btn_tryAgain.wait_variable(self.errorHandled)
                self.value = [
                    self.currentArtist.get(),
                    self.currentTitle.get()
                ]
                self.disableEntries()
            if self.currentLyrics.strip() == "":
                self.setLyricsCycle()

    """
        Gets the lyrics of the file passed as parameter, writing them in the metaTags of the file, given it has the metaTags defined correctly
        In case of not finding the page, it asks the user
    """

    def setLyrics(self, filename):
        self.currentLyrics = ""
        if skip:
            return
        self.setLyricsCycle()
        if self.currentLyrics != "None":
            audio = ID3(filename)
            audio.delall("USLT")
            audio.add(USLT(encoding=3, text=self.currentLyrics))
            audio.save()

    def lyricsAndYear(self):
        if self.newFiles != []:
            self.removePtOrPart = False
            filename = self.newFiles[0]
            self.ArtistAlbumAndTitle(filename, True)
            self.key = (self.currentArtist.get(), self.currentAlbum.get())
            self.addToOutput()
            self.getYear(filename)
            if self.exceptionRaised:
                Screen.container.artistAlbumReplacements[self.key] = self.value
                self.exceptionRaised = False
            self.changeTag("lyrics")
            self.ArtistAlbumAndTitle(filename, False)
            self.key = (self.currentArtist.get(), self.currentTitle.get())
            self.setLyrics(filename)
            if self.exceptionRaised:
                Screen.container.artistTitleReplacements[self.key] = self.value
                self.exceptionRaised = False
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
                Screen.container.saveExceptions()
                for txt in self.textBoxes:
                    txt.delete("end-1c linestart", TK.END)
                self.finished = False
                self.frm_newAAT.destroy()
                self.lbl_url.destroy()
                self.btn_downloadMore.grid(row=2, column=0)
                self.btn_exit.grid(row=3, column=0)


if __name__ == "__main__":
    # For ignoring SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    Screen.window.title("Downloader")
    Screen.window.iconbitmap(
        os.path.join(Screen.container.baseDirectory, "auxFiles",
                     "icons8-download-32.ico"))
    Screen.window.configure(bg=Screen.DEFAULT_BGCOLOR)
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
