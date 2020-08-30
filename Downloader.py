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
    def __init__(self, masterFramePreviousScreen: TK.Frame):
        super().__init__(masterFramePreviousScreen)
        Screen.container.getDirectories()
        #Widget Creation
        self.lbl_title.config(
            text=
            "Welcome to the Download Helper!\nYou want help moving files related to school or music?"
        )
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
        self.btn_allMusicFiles = TK.Button(self.frm_master,
                                           font=Screen.DEFAULT_FONT3,
                                           text="Music (All Files)",
                                           command=self.allFiles)
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
        self.btn_allMusicFiles.grid(row=5, column=1)
        self.btn_grimeArtistsExceptions.grid(row=6, column=1)
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
                ent_Directory = self.ent_downloadsDirectory
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
            f for f in Screen.container.files
            if os.path.getmtime(f) > Screen.container.timeOfLastModifiedFile
        ])

    def allFiles(self):
        AlbumAndLyricsScreen(self.frm_master, Screen.container.files)

    def grimeArtistsExceptionsScreen(self):
        GrimeArtistsAndExceptionsScreen(self.frm_master)


class GrimeArtistsAndExceptionsScreen(Screen):
    def __init__(self, masterFramePreviousScreen: TK.Frame):
        super().__init__(masterFramePreviousScreen)
        #Tkinter Vars
        self.firstEntryVar = TK.StringVar()
        self.secondEntryVar = TK.StringVar()
        self.thirdEntryVar = TK.StringVar()
        self.fourthEntryVar = TK.StringVar()
        self.fifthEntryVar = TK.StringVar()
        self.sixthEntryVar = TK.StringVar()
        Screen.container.getGrimeArtists()
        self.mode = 0
        #1 -  Grime Artist
        #2 -  Url replacement pair
        #3 - exception

        #Widget Creation
        self.lbl_title.config(
            text=
            "Insert New Grime Artist or Remove or create Url Replacement Pair")
        self.lbl_1st = TK.Label(self.frm_master,
                                font=Screen.DEFAULT_FONT2,
                                fg="white",
                                bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_2nd = TK.Label(self.frm_master,
                                text="New Replacement",
                                font=Screen.DEFAULT_FONT2,
                                fg="white",
                                bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_3rd = TK.Label(self.frm_master,
                                text="Old Title",
                                font=Screen.DEFAULT_FONT2,
                                fg="white",
                                bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_4th = TK.Label(self.frm_master,
                                text="New Artist",
                                font=Screen.DEFAULT_FONT2,
                                fg="white",
                                bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_5th = TK.Label(self.frm_master,
                                text="New Album",
                                font=Screen.DEFAULT_FONT2,
                                fg="white",
                                bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_6th = TK.Label(self.frm_master,
                                text="New Title",
                                font=Screen.DEFAULT_FONT2,
                                fg="white",
                                bg=Screen.DEFAULT_BGCOLOR)
        self.scrollableWidget = ScrollableWidget(self.frm_master, ["Listbox"])
        self.scrollableWidget.boxes[0].config(height=15, width=100)
        self.ent_1st = TK.Entry(self.frm_master,
                                textvariable=self.firstEntryVar,
                                font=Screen.DEFAULT_FONT3,
                                width=50)
        self.ent_2nd = TK.Entry(self.frm_master,
                                textvariable=self.secondEntryVar,
                                font=Screen.DEFAULT_FONT3,
                                width=50)
        self.ent_3rd = TK.Entry(self.frm_master,
                                textvariable=self.thirdEntryVar,
                                font=Screen.DEFAULT_FONT3,
                                width=50)
        self.ent_4th = TK.Entry(self.frm_master,
                                textvariable=self.fourthEntryVar,
                                font=Screen.DEFAULT_FONT3,
                                width=50)
        self.ent_5th = TK.Entry(self.frm_master,
                                textvariable=self.fifthEntryVar,
                                font=Screen.DEFAULT_FONT3,
                                width=50)
        self.ent_6th = TK.Entry(self.frm_master,
                                textvariable=self.sixthEntryVar,
                                font=Screen.DEFAULT_FONT3,
                                width=50)
        self.btn_grimeArtist = TK.Button(self.frm_master,
                                         text="Grime Artist",
                                         font=Screen.DEFAULT_FONT3,
                                         command=self.alterGrimeArtists)
        self.btn_urlReplacementPair = TK.Button(
            self.frm_master,
            text="Url Replacement Pair",
            font=Screen.DEFAULT_FONT3,
            command=self.alterReplacementPair)
        self.btn_exceptions = TK.Button(self.frm_master,
                                        text="Exception",
                                        font=Screen.DEFAULT_FONT3,
                                        command=self.alterExceptions)
        self.btn_confirm = TK.Button(self.frm_master,
                                     text="Add New One",
                                     font=Screen.DEFAULT_FONT3,
                                     command=self.nextScreen)
        self.btn_previousScreen = TK.Button(self.frm_master,
                                            text="Go Back",
                                            font=Screen.DEFAULT_FONT3,
                                            command=self.backScreen)

        #Widget Placement
        self.lbl_title.grid(row=0, column=2)
        self.btn_grimeArtist.grid(row=2, column=1)
        self.btn_urlReplacementPair.grid(row=3, column=1)
        self.btn_exceptions.grid(row=4, column=1)
        self.btn_previousScreen.grid(row=5, column=0)
        self.scrollableWidget.frame.grid(row=1, column=3, rowspan=1500)
        self.scrollableWidget.boxes[0].grid(row=0, column=0)
        self.scrollableWidget.scrollbar.grid(row=0, column=1, sticky=TK.NS)

        #Widget Configuration
        self.scrollableWidget.boxes[0].bind("<Delete>", self.deleteSelected)

    def backScreen(self, event=None):
        Screen.container.saveGrimeArtists()
        Screen.container.saveExceptions()
        InitialScreen(self.frm_master)

    def deleteSelected(self, event=None):
        if self.mode == 1:
            selected = self.scrollableWidget.boxes[0].get(
                self.scrollableWidget.boxes[0].curselection())
            Screen.container.grimeArtists.remove(selected)
        elif self.mode == 2:
            selected = self.scrollableWidget.boxes[0].get(
                self.scrollableWidget.boxes[0].curselection())
            key = selected[selected.find("\"") +
                           1:selected.find("\"",
                                           selected.find("\"") + 1,
                                           len(selected) - 1)]
            Screen.container.replacementsDict.pop(key)
        else:
            selected = self.scrollableWidget.boxes[0].get(
                self.scrollableWidget.boxes[0].curselection())
            excType = int(selected[6])
            selected = selected[8:]
            if " ---> " in selected:
                key = selected[:selected.find(" ---> ")]
                # value = selected[selected.find(" ---> ") + len(" ---> "):]
            else:
                key = selected.split(", ")
            if excType == 0:
                # self.scrollableWidget.boxes[0].insert(
                #     TK.END, "Type: 0 " + key[0] + ", " + key[1] + " - " + key[2] +
                #     " ---> " + Screen.container.exceptionsReplacements[key][0] +
                #     ", " + Screen.container.exceptionsReplacements[key][1] +
                #     " - " + Screen.container.exceptionsReplacements[key][2])
                artist = key[:key.find(", ")]
                album = key[key.find(", ") + len(", "):key.find(" - ")]
                title = key[key.find(" - ") + len(" - "):]
                if title == "None": title = None
                Screen.container.exceptionsReplacements.pop(
                    (artist, album, title))
                # newArtist = value[:value.find(" - ")]
                # newAlbum = value[value.find(" - ") + len(" - "):]
            # elif excType == 1:
            #     artist = key[:key.find(" - ")]
            #     title = key[key.find(" - ") + len(" - "):]
            #     Screen.container.artistTitleReplacements.pop((artist, title))
            #     # newArtist = value[:value.find(" - ")]
            #     # newTitle = value[value.find(" - ") + len(" - "):]
            else:
                artist = key[0]
                album = key[1]
                title = key[2]
                Screen.container.songsToSkip.remove([artist, album, title])
        self.scrollableWidget.boxes[0].delete(
            self.scrollableWidget.boxes[0].curselection())

    def nextScreen(self, event=None):
        if self.mode == 1:
            artist = self.firstEntryVar.get().strip()
            if artist != "":
                Screen.container.grimeArtists.append(artist)
        elif self.mode == 2:
            oldPair = self.firstEntryVar.get()
            newPair = self.secondEntryVar.get()
            try:
                old = oldPair[oldPair.find("\"") + 1:oldPair.rfind("\"")]
                new = newPair[newPair.find("\"") + 1:newPair.rfind("\"")]
                Screen.container.replacementsDict[old] = new
            except:
                print("ERROR")
        else:
            oldArtist = self.firstEntryVar.get().strip()
            oldAlbum = self.secondEntryVar.get().strip()
            oldTitle = self.thirdEntryVar.get().strip()
            newArtist = self.fourthEntryVar.get().strip()
            newAlbum = self.fifthEntryVar.get().strip()
            newTitle = self.sixthEntryVar.get().strip()
            if newArtist == "" and newAlbum == "" and newTitle == "":
                if oldArtist != "" and oldAlbum != "" and oldTitle != "":
                    Screen.container.songsToSkip.append(
                        [oldArtist, oldAlbum, oldTitle])
            else:
                Screen.container.exceptionsReplacements[(oldArtist, oldAlbum,
                                                         oldTitle)] = [
                                                             newArtist,
                                                             newAlbum, newTitle
                                                         ]
        self.firstEntryVar.set("")
        self.secondEntryVar.set("")
        self.thirdEntryVar.set("")
        self.fourthEntryVar.set("")
        self.fifthEntryVar.set("")
        self.sixthEntryVar.set("")
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        self.lbl_title.config(
            text=
            "Alter Grime Artists, Url Replacement Pairs or add new Exception")
        self.btn_grimeArtist.grid(row=2, column=1)
        self.btn_urlReplacementPair.grid(row=3, column=1)
        self.btn_exceptions.grid(row=4, column=1)
        self.btn_previousScreen.grid(row=5, column=0)
        self.lbl_1st.grid_forget()
        self.lbl_2nd.grid_forget()
        self.lbl_3rd.grid_forget()
        self.lbl_4th.grid_forget()
        self.lbl_5th.grid_forget()
        self.lbl_6th.grid_forget()
        self.ent_1st.grid_forget()
        self.ent_2nd.grid_forget()
        self.ent_3rd.grid_forget()
        self.ent_4th.grid_forget()
        self.ent_5th.grid_forget()
        self.ent_6th.grid_forget()
        self.btn_confirm.grid_forget()

    def alterGrimeArtists(self):
        self.mode = 1
        self.lbl_title.config(text="Insert the name of the Artist")
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        for artist in Screen.container.grimeArtists:
            self.scrollableWidget.boxes[0].insert(0, artist)
        self.lbl_1st.config(text="Artist")
        self.lbl_1st.grid(row=1, column=1)
        self.ent_1st.grid(row=1, column=2)
        self.btn_confirm.grid(row=2, column=2)
        self.btn_grimeArtist.grid_forget()
        self.btn_urlReplacementPair.grid_forget()
        self.btn_exceptions.grid_forget()
        self.btn_previousScreen.grid_forget()

    def alterReplacementPair(self):
        self.mode = 2
        self.lbl_title.config(
            text="Insert what to replace and what with, in \"\"")
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        for key in Screen.container.replacementsDict:
            self.scrollableWidget.boxes[0].insert(
                TK.END, "\"" + key + "\"\t--->\t\"" +
                Screen.container.replacementsDict[key] + "\"")
        self.lbl_1st.config(text="Old Replacement")
        self.lbl_2nd.config(text="New Replacement")
        self.lbl_1st.grid(row=1, column=1)
        self.lbl_2nd.grid(row=2, column=1)
        self.ent_1st.grid(row=1, column=2)
        self.ent_2nd.grid(row=2, column=2)
        self.btn_confirm.grid(row=3, column=2)
        self.btn_grimeArtist.grid_forget()
        self.btn_urlReplacementPair.grid_forget()
        self.btn_exceptions.grid_forget()
        self.btn_previousScreen.grid_forget()

    def alterExceptions(self):
        self.mode = 3
        self.lbl_title.config(text="Insert the exception")
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        for key in Screen.container.exceptionsReplacements:
            self.scrollableWidget.boxes[0].insert(
                TK.END, "Type: 0 " + str(key[0]) + ", " + str(key[1]) + " - " +
                str(key[2]) + " ---> " +
                str(Screen.container.exceptionsReplacements[key][0]) + ", " +
                str(Screen.container.exceptionsReplacements[key][1]) + " - " +
                str(Screen.container.exceptionsReplacements[key][2]))
        for key in Screen.container.songsToSkip:
            self.scrollableWidget.boxes[0].insert(TK.END,
                                                  "Type: 1 " + ", ".join(key))
        self.lbl_1st.config(text="Old Artist")
        self.lbl_2nd.config(text="Old Album")
        self.lbl_3rd.config(text="Old Title")
        self.lbl_4th.config(text="New Artist")
        self.lbl_5th.config(text="New Album")
        self.lbl_6th.config(text="New Title")
        self.lbl_1st.grid(row=1, column=1)
        self.lbl_2nd.grid(row=2, column=1)
        self.lbl_3rd.grid(row=3, column=1)
        self.lbl_4th.grid(row=4, column=1)
        self.lbl_5th.grid(row=5, column=1)
        self.lbl_6th.grid(row=6, column=1)
        self.ent_1st.grid(row=1, column=2)
        self.ent_2nd.grid(row=2, column=2)
        self.ent_3rd.grid(row=3, column=2)
        self.ent_4th.grid(row=4, column=2)
        self.ent_5th.grid(row=5, column=2)
        self.ent_6th.grid(row=6, column=2)
        self.btn_confirm.grid(row=7, column=2)
        self.btn_grimeArtist.grid_forget()
        self.btn_urlReplacementPair.grid_forget()
        self.btn_exceptions.grid_forget()
        self.btn_previousScreen.grid_forget()

    # def removeArtist(self):
    #     self.mode = 2
    #     self.lbl_title.config(text="Insert the name of the Artist")
    #     self.scrollableWidget.boxes[0].delete(0, TK.END)
    #     for artist in Screen.container.grimeArtists:
    #         self.scrollableWidget.boxes[0].insert(0, artist)
    #     self.lbl_1st.config(text="Artist")
    #     self.lbl_1st.grid(row=1, column=1)
    #     self.ent_1st.grid(row=1, column=2)
    #     self.btn_confirm.grid(row=2, column=2)
    #     self.btn_addArtist.grid_forget()
    #     self.btn_removeArtist.grid_forget()
    #     self.btn_addUrlReplacementPair.grid_forget()
    #     self.btn_previousScreen.grid_forget()


# class SchoolScreen(Screen):
#     def __init__(self, masterFramePreviousScreen: TK.Frame):
#         super().__init__(masterFramePreviousScreen)
#         #Tkinter Vars
#         self.title = TK.StringVar()
#         self.numberOfFiles = 0
#         self.title.set(str(self.numberOfFiles) + " Files Found")

#         #Widget Creation
#         self.lbl_title.config(textvariable=self.title)
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
    def __init__(self, masterFramePreviousScreen: TK.Frame, firstTime):
        super().__init__(masterFramePreviousScreen)
        if firstTime:
            openThread = threading.Thread(target=lambda: os.startfile(
                os.path.join(Screen.container.baseDirectory, "auxFiles",
                             "deemix.lnk")),
                                          daemon=True)
            openThread.start()

        #Tkinter Vars
        self.numberOfFilesFound = 0
        self.numberOfFilesMoved = 0
        self.buffer = []
        self.checkMusicCondition = True
        self.canAdvance = False
        self.newFiles = []
        self.title = TK.StringVar()
        self.title.set(str(self.numberOfFilesFound) + " Files Found")

        #Widget Creation
        self.lbl_title.config(textvariable=self.title)
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
            self.scrollableWidget.boxes[0].config(state=TK.NORMAL)
            self.scrollableWidget.boxes[0].delete("end-1c linestart", TK.END)
            self.scrollableWidget.boxes[0].config(state=TK.DISABLED)
            self.moveOutOfBuffer()
            self.btn_nextScreen.config(text="Get Album Year and Lyrics",
                                       state=TK.DISABLED)
        else:
            if self.canAdvance:
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
                    subprocess.run([
                        Screen.container.recycle,
                        os.path.join(Screen.container.musicOriginDirectory,
                                     ficheiro)
                    ])
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
                    subprocess.run([
                        Screen.container.recycle,
                        os.path.join(Screen.container.musicOriginDirectory,
                                     old)
                    ])
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
                            subprocess.run([
                                Screen.container.recycle,
                                os.path.join(
                                    Screen.container.musicOriginDirectory, old)
                            ])
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
            Screen.window.update_idletasks()
            self.scrollableWidget.boxes[1].see(TK.END)
            self.title.set(str(self.numberOfFilesMoved) + " Files Moved")
            Screen.window.after(10, self.moveOutOfBuffer)
            # self.moveOutOfBuffer()
        else:
            self.canAdvance = True
            self.btn_nextScreen.config(state=TK.NORMAL)
            self.scrollableWidget.boxes[1].config(state=TK.NORMAL)
            self.scrollableWidget.boxes[1].delete("end-1c linestart", TK.END)
            self.scrollableWidget.boxes[1].config(state=TK.DISABLED)

    def slightTagChanges(self, filename, newFilename):
        mp3 = EasyID3(filename)
        mp3['album'] = Screen.removeWordsFromWord(
            ["Remaster", "Anniversary", "Deluxe", "Expanded"], mp3['album'][0])
        mp3['title'] = Screen.removeWordsFromWord([
            "Remaster", "Album Version", "Stereo", "Hidden Track", "Explicit",
            "explicit"
        ], mp3['title'][0])
        mp3['title'] = mp3['title'][0].replace("f*ck", "fuck").replace(
            "f***",
            "fuck").replace("f**k", "fuck").replace("sh*t", "shit").replace(
                "s**t", "shit").replace("sh**", "shit").replace(
                    "ni**as", "niggas").replace("F*ck", "Fuck").replace(
                        "F**k", "Fuck").replace("F***", "Fuck").replace(
                            "Sh*t", "Shit").replace("S**t", "Shit").replace(
                                "Sh**", "Shit").replace("Ni**as", "Niggas")
        if "King Gizzard and the Lizard Wizard".lower(
        ) in mp3['albumartist'][0].lower():
            mp3['artist'] = mp3['artist'][0].replace("And", "&")
            mp3['albumartist'] = mp3['albumartist'][0].replace("And", "&")
        elif "&" in mp3['albumartist'][0] and mp3['album'][
                0] != "Without Warning" and " Mayall " not in mp3[
                    'albumartist'][0] and "King Gizzard" not in mp3[
                        'albumartist'][0]:
            mp3['albumartist'] = mp3['albumartist'][0].split(" & ")[0]
        elif mp3['album'][0] == "Without Warning":
            mp3['albumartist'] = "21 Savage, Offset & Metro Boomin"
        if "/" in mp3['albumartist'][0]:
            mp3['albumartist'] = mp3['albumartist'][0].split("/")[0]
        if "/" in mp3['artist'][0]:
            mp3['artist'] = mp3['artist'][0].replace("/", ", ")
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
        mp3.save()


class AlbumAndLyricsScreen(Screen):
    pagesVisited_year = {}

    def __init__(self, masterFramePreviousScreen: TK.Frame, newFiles: list):
        super().__init__(masterFramePreviousScreen)
        Screen.window.state('zoomed')
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
        self.currentYear = TK.IntVar()
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
            "Artist": 45,
            "Album": 70,
            "Title": 85,
            "Year": 5
        }
        colors = ["yellow", "dark green", "green2"]
        text = ["Getting Album Year", "Getting Track Lyrics", "File Done"]
        self.iTunesTrack = None

        #Widget Creation
        self.lbl_title.config(textvariable=self.title)
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
                width=self.categories_width[category], height=35)
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
                width=70)
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
        Screen.container.songsToSkip.append([
            self.currentArtist.get(),
            self.currentAlbum.get(),
            self.currentTitle.get()
        ])
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
        Screen.container.saveExceptions()
        Screen.window.destroy()

    def goBackDownloadMore(self):
        MusicScreen(self.frm_master, False)

    def exitOpenHandler(self):
        Screen.container.saveExceptions()
        Screen.window.quit()
        os.system("taskkill /f /im  deemix-pyweb.exe")
        if "GitHub" in Screen.container.baseDirectory:
            subprocess.run(
            ['python',
             os.path.join(Screen.container.baseDirectory, "Handler_Music.py")])
        else:
            subprocess.run(
            [os.path.join(Screen.container.baseDirectory, "Handler_Music","Handler_Music.exe")])

    def changeOutput(self, index, inYear):
        self.scrollableWidget.boxes[index].delete("end-1c linestart", TK.END)
        Screen.window.update_idletasks()
        if index == 0:
            toAdd = self.currentArtist.get()
        elif index == 1:
            toAdd = self.currentAlbum.get()
        else:
            toAdd = self.currentTitle.get()
        if self.numberOfFilesProcessed != 0:
            self.scrollableWidget.boxes[index].insert(TK.END, "\n")
        self.scrollableWidget.boxes[index].insert(TK.END, toAdd)
        self.scrollableWidget.boxes[index].see(TK.END)
        if inYear:
            self.changeTag("album")
        else:
            self.changeTag("lyrics")
        Screen.window.update_idletasks()

    def thread_function(self):
        self.exceptionRaised = True
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        self.errorSound = threading.Thread(target=self.thread_function,
                                           daemon=True)

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

    def namingConventions(self, name):
        if "pt." in name.lower() or "part." in name.lower(
        ) or "pts." in name.lower() or "mr." in name.lower(
        ) or "vol." in name.lower():
            name = name.replace(".", " ")
        for key in Screen.container.replacementsDict:
            name = name.replace(key, Screen.container.replacementsDict[key])
        return "-".join(name.split()).capitalize()

    """
        Determines the artist and title to be used in the search for lyrics and handles the most common changes
    """

    def ArtistAlbumAndTitle(self, artist, album, title, forYear):
        if forYear:
            self.currentYear.set(self.iTunesTrack.Year)
            for key in Screen.container.exceptionsReplacements:
                if self.key[0] == key[0] and self.key[1] == key[1] and key[
                        2] == None:
                    self.currentArtist.set(
                        Screen.container.exceptionsReplacements[key][0])
                    self.currentAlbum.set(
                        Screen.container.exceptionsReplacements[key][1])
                    self.changeOutput(0, True)
                    self.changeOutput(1, True)
                    break
        if not forYear or self.iTunesTrack.TrackCount < 5:  #and self.iTunesTrack.Year > 1985
            for key in Screen.container.exceptionsReplacements:
                if self.key[0] == key[0] and self.key[1] == key[1] and key[
                        2] == None:
                    self.currentArtist.set(
                        Screen.container.exceptionsReplacements[key][0])
                    self.currentAlbum.set(
                        Screen.container.exceptionsReplacements[key][1])
                elif self.key[0] == key[0] and self.key[1] == key[
                        1] and key[2] != None and self.key[2] == key[2]:
                    self.currentArtist.set(
                        Screen.container.exceptionsReplacements[key][0])
                    self.currentAlbum.set(
                        Screen.container.exceptionsReplacements[key][1])
                    self.currentTitle.set(
                        Screen.container.exceptionsReplacements[key][2])
                    self.changeOutput(0, False)
                    self.changeOutput(2, False)
                    break

    def titleContainsRomanNumeral(self):
        for index in range(len(self.romanNums)):
            if self.romanNums[index] in self.currentTitle.get():
                return index
        return -1

    def checkIfWebpageExists(self, forAlbum):
        skip = False
        if forAlbum:
            name = self.namingConventions(
                self.currentArtist.get()) + "/" + self.namingConventions(
                    self.currentAlbum.get())
            url = "https://www.genius.com/albums/" + name
            if name in AlbumAndLyricsScreen.pagesVisited_year:
                self.currentYear.set(
                    AlbumAndLyricsScreen.pagesVisited_year[name])
                skip = True
        else:
            name = self.namingConventions(self.currentArtist.get() + " " +
                                          self.currentTitle.get())
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
            year = int(year[len(year) - 1])
            self.currentYear.set(year)
            AlbumAndLyricsScreen.pagesVisited_year[
                self.currentUrl.get().replace("https://www.genius.com/albums/",
                                              "")] = year
            return
        else:
            if self.iTunesTrack.TrackCount < 5:
                # print(self.currentArtist.get())  and self.iTunesTrack.Year > 1985
                soup = self.checkIfWebpageExists(False)
                if soup != None:
                    auxList = soup.findAll(
                        'div',
                        attrs={
                            'class':
                            'HeaderMetadata__Section-sc-1p42fnf-2 hAhJBU'
                        })
                    if auxList != []:
                        for div in auxList:
                            if "Release Date" in div.text:
                                aux = div.text.split()
                                year = int(aux[len(aux) - 1])
                                self.currentYear.set(year)
                                return
                    else:
                        auxList = soup.findAll(
                            'div',
                            attrs={
                                'class':
                                'metadata_unit metadata_unit--table_row'
                            })
                        for div in auxList:
                            if "Release Date" in div.text:
                                aux = div.text.split()
                                year = int(aux[len(aux) - 1])
                                self.currentYear.set(year)
                                return
            while True:
                try:
                    self.errorSound.start()
                    break
                except:
                    pass
            if self.iTunesTrack.TrackCount < 5:
                webbrowser.open("https://www.google.com.tr/search?q={}".format(
                    self.currentArtist.get().replace(" &", "").replace(
                        " ", "+") + "+" + self.currentTitle.get().replace(
                            " &", "").replace(" ", "+") +
                    "+lyrics+site:Genius.com"))
            else:
                webbrowser.open("https://www.google.com.tr/search?q={}".format(
                    self.currentArtist.get().replace(" &", "").replace(
                        " ", "+") + "+" + self.currentAlbum.get().replace(
                            " &", "").replace(" ", "+") + "+site:Genius.com"))
            self.errorHandled.set(False)
            self.enableEntries(0)
            self.btn_tryAgain.wait_variable(self.errorHandled)
            self.value = [
                self.currentArtist.get(),
                self.currentAlbum.get(),
                self.currentTitle.get()
            ]
            self.changeOutput(0, True)
            self.changeOutput(1, True)
            self.disableEntries()
        self.getYearCycle()
        return

    def getYear(self, filename):
        self.getYearCycle()
        audio = ID3(filename)
        audio.delall("TDRC")
        audio.add(TDRC(encoding=3, text=str(self.currentYear.get())))
        audio.save()

    def setLyricsCycle(self):
        soup = self.checkIfWebpageExists(False)
        if soup != None:
            for div in soup.findAll('div', attrs={'class': 'lyrics'}):
                self.currentLyrics += div.text.strip()
            if self.currentLyrics.strip() == "":
                aux = []
                for div in soup.findAll(
                        'div',
                        attrs={
                            'class':
                            lambda x: x and x.startswith("Lyrics__Container")
                        }):
                    for elem in div.contents:
                        try:
                            if str(elem) != "<br/>":
                                aux.append(elem.text)
                        except:
                            aux.append(str(elem))
                for index in range(len(aux)):
                    if aux[index].startswith("[") and aux[index - 1] != "":
                        aux.insert(index, "")
                self.currentLyrics = "\n".join(aux).strip()
                # for div in soup.findAll(
                #         'div',
                #         attrs={
                #             'class':
                #             lambda x: x and x.startswith("Lyrics__Container")
                #         }):
                #     linha = ''
                #     for elem in div.recursiveChildGenerator():
                #         if isinstance(elem, str):
                #             linha += elem.strip()
                #         elif elem.name == 'br':
                #             linha += '\n'
                #     self.currentLyrics += linha
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
                while True:
                    try:
                        self.errorSound.start()
                        break
                    except:
                        pass
                self.errorHandled.set(False)
                self.enableEntries(1)
                webbrowser.open("https://www.google.com.tr/search?q={}".format(
                    self.currentArtist.get().replace(" &", "").replace(
                        " ", "+") + "+" + self.currentTitle.get().replace(
                            " &", "").replace(" ", "+") +
                    "+lyrics+site:Genius.com"))
                self.btn_tryAgain.wait_variable(self.errorHandled)
                self.value = [
                    self.currentArtist.get(),
                    self.currentAlbum.get(),
                    self.currentTitle.get()
                ]
                self.changeOutput(0, False)
                self.changeOutput(2, False)
                self.disableEntries()
            if self.currentLyrics.strip() == "":
                self.setLyricsCycle()
        return

    """
        Gets the lyrics of the file passed as parameter, writing them in the metaTags of the file, given it has the metaTags defined correctly
        In case of not finding the page, it asks the user
    """

    def setLyrics(self, filename):
        self.currentLyrics = ""
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
            opStatus = Screen.container.iTunesLibrary.AddFile(filename)
            while opStatus.InProgress:
                pass
            self.iTunesTrack = opStatus.Tracks.Item(1)
            artist = EasyID3(filename)['albumartist'][0]
            title = self.iTunesTrack.Name
            album = self.iTunesTrack.Album
            title = Screen.removeWordsFromWord([
                "feat", "Feat", "bonus", "Bonus", "Conclusion", "Hidden Track",
                "Vocal Mix", "Explicit", "explicit", "Extended"
            ], title)
            self.currentArtist.set(artist)
            self.currentAlbum.set(album)
            self.currentTitle.set(title)
            self.key = [artist, album, title]
            self.addToOutput()
            self.ArtistAlbumAndTitle(artist, album, title, True)
            self.getYear(filename)
            while True:
                try:
                    self.iTunesTrack.Year = self.currentYear.get()
                    break
                except:
                    pass
            if self.iTunesTrack.Year < 1985:
                self.iTunesTrack.VolumeAdjustment = 50
            inYear = False
            if self.exceptionRaised and self.key != self.value:
                if self.key[2] == self.value[2]:
                    self.key[2] = None
                    self.value[2] = None
                Screen.container.exceptionsReplacements[tuple(
                    self.key)] = self.value
                self.exceptionRaised = False
            self.changeTag("lyrics")
            self.ArtistAlbumAndTitle(artist, album, title, False)
            if [
                    self.currentArtist.get(),
                    self.currentAlbum.get(),
                    self.currentTitle.get()
            ] not in Screen.container.songsToSkip:
                self.setLyrics(filename)
                if self.exceptionRaised:
                    if self.currentLyrics != "None":
                        Screen.container.exceptionsReplacements[tuple(
                            self.key)] = self.value
                    self.exceptionRaised = False
            self.changeTag("success")
            for txt in self.scrollableWidget.boxes:
                txt.insert(TK.END, "\n")
                txt.see(TK.END)
            self.numberOfFilesProcessed += 1
            self.title.set(
                str(self.numberOfFilesProcessed) + "/" +
                str(self.totalNewFiles) + " Files Processed")
            Screen.window.update_idletasks()
            self.newFiles.remove(filename)
            Screen.window.after(10, self.lyricsAndYear)
        else:
            if self.finished:
                for txt in self.scrollableWidget.boxes:
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
    # os.system("cls")
    # url = "https://genius.com/albums/Travis-scott/astroworld"
    # req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # webpage = urlopen(req).read()
    # soup = BeautifulSoup(webpage, 'html.parser')
    # yearTemp = ""
    #         #Extract the year of the album
    # for div in soup.findAll('div', attrs={'class': 'metadata_unit'}):
    #     yearTemp += div.text.strip()
    #     break
    # year = yearTemp.split()
    # year = int(year[len(year) - 1])
    # print(year)