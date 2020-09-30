#!/usr/bin/env python3.8
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
        self.btn_schoolVersion = TK.Button(self.frm_master,
                                           font=Screen.DEFAULT_FONT3,
                                           text="School",
                                           command=self.schoolScreen)
        self.btn_musicVersion = TK.Button(self.frm_master,
                                          font=Screen.DEFAULT_FONT3,
                                          text="Music (Downloaded)",
                                          command=self.musicScreen)
        self.btn_musicModifiedVersion = TK.Button(
            self.frm_master,
            font=Screen.DEFAULT_FONT3,
            text="Music (Files Modified)",
            command=self.albumLyricsOnlyModified)
        self.btn_allMusicFiles = TK.Button(self.frm_master,
                                           font=Screen.DEFAULT_FONT3,
                                           text="Music (All Files)",
                                           command=self.albumLyricsAllFiles)
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
        self.btn_schoolVersion.grid(row=2, column=1)
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

    """
        Method that prompts the dialog to the user to change the directory he chose to change and changes it in the file (and variable)
    """

    def chooseDirectory(self, whichOne):
        aux = filedialog.askdirectory(
            initialdir=Screen.container.baseDirectory.replace("/", "\\"))
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

    def schoolScreen(self):
        SchoolScreen(self.frm_master)

    def musicScreen(self):
        MusicScreen(self.frm_master, True)

    def albumLyricsOnlyModified(self):
        AlbumAndLyricsScreen(self.frm_master, [
            f for f in Screen.container.files
            if os.path.getmtime(f) > Screen.container.timeOfLastModifiedFile
        ])

    def albumLyricsAllFiles(self):
        AlbumAndLyricsScreen(self.frm_master, Screen.container.files)

    def grimeArtistsExceptionsScreen(self):
        GrimeArtistsAndExceptionsScreen(self.frm_master)


class GrimeArtistsAndExceptionsScreen(Screen):
    def __init__(self, masterFramePreviousScreen: TK.Frame):
        super().__init__(masterFramePreviousScreen)
        #Tkinter Vars
        self.widgetGroupsDict = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: []
        }  #0 - label, 1 - stringVar, 2 - entry
        Screen.container.getGrimeArtists()
        self.mode = 0
        #1 - Grime Artist
        #2 - Url replacement pair
        #3 - exception

        #Widget Creation
        self.lbl_title.config(
            text=
            "Alter Grime Artists, Url Replacement Pairs or add new Exception")
        for key in self.widgetGroupsDict:
            label = TK.Label(self.frm_master,
                             font=Screen.DEFAULT_FONT2,
                             fg="white",
                             bg=Screen.DEFAULT_BGCOLOR)
            self.widgetGroupsDict[key].append(label)
            stringVar = TK.StringVar()
            self.widgetGroupsDict[key].append(stringVar)
            entry = TK.Entry(self.frm_master,
                             textvariable=stringVar,
                             font=Screen.DEFAULT_FONT3,
                             width=50)
            self.widgetGroupsDict[key].append(entry)
        self.widgetGroupsDict[2][0].config(text="Old Title")
        self.widgetGroupsDict[3][0].config(text="New Artist")
        self.widgetGroupsDict[4][0].config(text="New Album")
        self.widgetGroupsDict[5][0].config(text="New Title")
        self.scrollableWidget = ScrollableWidget(self.frm_master, ["Listbox"])
        self.scrollableWidget.boxes[0].config(height=15, width=100)
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
                                     command=self.nextScreen,
                                     state=TK.DISABLED)
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
            else:
                key = selected.split(", ")
            if excType == 0:
                artist = key[:key.find(", ")]
                album = key[key.find(", ") + len(", "):key.find(" - ")]
                title = key[key.find(" - ") + len(" - "):]
                if title == "None": title = None
                Screen.container.exceptionsReplacements.pop(
                    (artist, album, title))
            else:
                artist = key[0]
                album = key[1]
                title = key[2]
                Screen.container.songsToSkip.remove([artist, album, title])
        self.scrollableWidget.boxes[0].delete(
            self.scrollableWidget.boxes[0].curselection())

    """
        Method that doesn't really go to a different "Screen" but it's called when the user presses the confirm button (or hits enter) and takes care of adding what the user inputted to the correct colection
    """

    def nextScreen(self, event=None):
        if self.btn_confirm["state"] == TK.NORMAL:
            if self.mode == 1:
                artist = self.widgetGroupsDict[0][1].get().strip()
                if artist != "":
                    Screen.container.grimeArtists.append(artist)
            elif self.mode == 2:
                oldPair = self.widgetGroupsDict[0][1].get()
                newPair = self.widgetGroupsDict[1][1].get()
                try:
                    old = oldPair[oldPair.find("\"") + 1:oldPair.rfind("\"")]
                    new = newPair[newPair.find("\"") + 1:newPair.rfind("\"")]
                    Screen.container.replacementsDict[old] = new
                except:
                    pass
            else:
                oldArtist = self.widgetGroupsDict[0][1].get().strip()
                oldAlbum = self.widgetGroupsDict[1][1].get().strip()
                oldTitle = self.widgetGroupsDict[2][1].get().strip()
                newArtist = self.widgetGroupsDict[3][1].get().strip()
                newAlbum = self.widgetGroupsDict[4][1].get().strip()
                newTitle = self.widgetGroupsDict[5][1].get().strip()
                if newArtist == "" and newAlbum == "" and newTitle == "":
                    if oldArtist != "" and oldAlbum != "" and oldTitle != "":
                        Screen.container.songsToSkip.append(
                            [oldArtist, oldAlbum, oldTitle])
                else:
                    Screen.container.exceptionsReplacements[(oldArtist,
                                                             oldAlbum,
                                                             oldTitle)] = [
                                                                 newArtist,
                                                                 newAlbum,
                                                                 newTitle
                                                             ]
            for key in self.widgetGroupsDict:
                self.widgetGroupsDict[key][1].set("")
                self.widgetGroupsDict[key][0].grid_forget()
                self.widgetGroupsDict[key][2].grid_forget()
            self.scrollableWidget.boxes[0].delete(0, TK.END)
            self.lbl_title.config(
                text=
                "Alter Grime Artists, Url Replacement Pairs or add new Exception"
            )
            self.btn_grimeArtist.grid(row=2, column=1)
            self.btn_urlReplacementPair.grid(row=3, column=1)
            self.btn_exceptions.grid(row=4, column=1)
            self.btn_previousScreen.grid(row=5, column=0)
            self.btn_confirm.config(state=TK.DISABLED)
            self.btn_confirm.grid_forget()

    """
        Method that sets the screen so the user can add or remove a grime artist
    """

    def alterGrimeArtists(self):
        self.mode = 1
        self.lbl_title.config(text="Insert the name of the Artist")
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        for artist in Screen.container.grimeArtists:
            self.scrollableWidget.boxes[0].insert(0, artist)
        self.widgetGroupsDict[0][0].config(text="Artist")
        self.widgetGroupsDict[0][0].grid(row=1, column=1)
        self.widgetGroupsDict[0][2].grid(row=1, column=2)
        self.btn_confirm.grid(row=2, column=2)
        self.btn_confirm.config(state=TK.NORMAL)
        self.btn_grimeArtist.grid_forget()
        self.btn_urlReplacementPair.grid_forget()
        self.btn_exceptions.grid_forget()
        self.btn_previousScreen.grid_forget()

    """
        Method that sets the screen so the user can add or remove a replacement url pair
    """

    def alterReplacementPair(self):
        self.mode = 2
        self.lbl_title.config(
            text="Insert what to replace and what with, in \"\"")
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        for key in Screen.container.replacementsDict:
            self.scrollableWidget.boxes[0].insert(
                TK.END, "\"" + key + "\"\t--->\t\"" +
                Screen.container.replacementsDict[key] + "\"")
        self.widgetGroupsDict[0][0].config(text="Old Replacement")
        self.widgetGroupsDict[1][0].config(text="New Replacement")
        self.widgetGroupsDict[0][0].grid(row=1, column=1)
        self.widgetGroupsDict[1][0].grid(row=2, column=1)
        self.widgetGroupsDict[0][2].grid(row=1, column=2)
        self.widgetGroupsDict[1][2].grid(row=2, column=2)
        self.btn_confirm.grid(row=3, column=2)
        self.btn_confirm.config(state=TK.NORMAL)
        self.btn_grimeArtist.grid_forget()
        self.btn_urlReplacementPair.grid_forget()
        self.btn_exceptions.grid_forget()
        self.btn_previousScreen.grid_forget()

    """
        Method that sets the screen so the user can add or remove an exception
    """

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
        self.widgetGroupsDict[0][0].config(text="Old Artist")
        self.widgetGroupsDict[1][0].config(text="Old Album")
        self.widgetGroupsDict[2][0].config(text="Old Title")
        self.widgetGroupsDict[3][0].config(text="New Artist")
        self.widgetGroupsDict[4][0].config(text="New Album")
        self.widgetGroupsDict[5][0].config(text="New Title")
        for key in self.widgetGroupsDict:
            self.widgetGroupsDict[key][0].grid(row=key + 1, column=1)
            self.widgetGroupsDict[key][2].grid(row=key + 1, column=2)
        self.btn_confirm.grid(row=len(self.widgetGroupsDict) + 1, column=2)
        self.btn_confirm.config(state=TK.NORMAL)
        self.btn_grimeArtist.grid_forget()
        self.btn_urlReplacementPair.grid_forget()
        self.btn_exceptions.grid_forget()
        self.btn_previousScreen.grid_forget()


class SchoolScreen(Screen):
    def __init__(self, masterFramePreviousScreen: TK.Frame):
        super().__init__(masterFramePreviousScreen)
        #Tkinter Vars
        self.tempoAtual = time.time()
        self.OneDrive = os.path.join('C:', os.path.sep, 'Users', 'ruben',
                                     'Onedrive - Universidade da Madeira',
                                     'Ano_3', 'Semestre_1')
        self.title = TK.StringVar()
        self.pathSelected = TK.StringVar()
        self.possibleDirs = []
        for direc in os.listdir(self.OneDrive):
            if os.path.isdir(os.path.join(self.OneDrive, direc)):
                self.possibleDirs.append(direc)
                self.addDirectories(os.path.join(self.OneDrive, direc))
        self.pathSelected.set(self.possibleDirs[0])
        self.possibleDirs.append("Delete File")
        self.possibleDirs.append("Skip File")
        self.fileFound = TK.BooleanVar()
        self.fileFound.set(False)

        self.numberOfFiles = 0
        self.title.set(str(self.numberOfFiles) + " Files Found")

        #Widget Creation
        self.lbl_title.config(textvariable=self.title)
        self.scrollWidget = ScrollableWidget(self.frm_master,
                                             ["Textbox", "Textbox"])
        self.btn_stopCycle = TK.Button(self.frm_master,
                                       text="Stop",
                                       font=Screen.DEFAULT_FONT3,
                                       command=self.stopCheckDownloads)
        self.frm_choosePath = TK.Frame(self.frm_master,
                                       bg=Screen.DEFAULT_BGCOLOR)
        self.dropdownMenu = TK.OptionMenu(self.frm_choosePath,
                                          self.pathSelected,
                                          *self.possibleDirs)
        self.dropdownMenu.config(font=Screen.DEFAULT_FONT3,
                                 bg=Screen.DEFAULT_BGCOLOR,
                                 fg="white",
                                 state=TK.DISABLED)
        self.ent_newFilename = TK.Entry(self.frm_choosePath,
                                        width=50,
                                        font=Screen.DEFAULT_FONT3,
                                        state=TK.DISABLED)
        self.btn_confirm = TK.Button(self.frm_choosePath,
                                     text="Confirm",
                                     state=TK.DISABLED,
                                     font=Screen.DEFAULT_FONT3)

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=200)
        self.scrollWidget.frame.grid(row=1, column=0)
        self.scrollWidget.boxes[0].grid(row=0, column=0)
        self.scrollWidget.boxes[1].grid(row=0, column=1)
        self.scrollWidget.scrollbar.grid(row=0, column=2, sticky=TK.NS)
        self.frm_choosePath.grid(row=2, column=0)
        self.ent_newFilename.grid(row=0, column=0)
        self.dropdownMenu.grid(row=1, column=0)
        self.btn_confirm.grid(row=2, column=0)
        self.btn_stopCycle.grid(row=3, column=0)

        Screen.window.update_idletasks()

        self.cycleCondition = True
        # webbrowser.open("https://moodle.cee.uma.pt/login/index.php", new=2)
        # webbrowser.open("https://infoalunos.uma.pt", new=2)
        self.checkDownloads()

    def nextScreen(self, event=None):
        if self.btn_confirm["state"] == TK.NORMAL:
            self.fileFound.set(True)

    def addDirectories(self, directory):
        if directory.replace(self.OneDrive + os.sep, "").count(os.sep) >= 2:
            return
        for direc in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, direc)):
                self.possibleDirs.append(
                    os.path.join(directory.replace(self.OneDrive + os.sep, ""),
                                 direc))
                self.addDirectories(os.path.join(directory, direc))

    def stopCheckDownloads(self):
        self.cycleCondition = False
        self.btn_stopCycle.destroy()

    def addToOutput(self, fileFound, fileMoved):
        self.numberOfFiles += 1
        self.title.set(str(self.numberOfFiles) + " Files Found")
        self.scrollWidget.boxes[0].config(state=TK.NORMAL)
        self.scrollWidget.boxes[1].config(state=TK.NORMAL)
        self.scrollWidget.boxes[0].insert(TK.END, fileFound + "\n")
        self.scrollWidget.boxes[1].insert(TK.END, fileMoved + "\n")
        self.scrollWidget.boxes[0].config(state=TK.DISABLED)
        self.scrollWidget.boxes[1].config(state=TK.DISABLED)
        Screen.window.update_idletasks()
        self.scrollWidget.boxes[0].see(TK.END)
        self.scrollWidget.boxes[1].see(TK.END)

    def checkDownloads(self):
        #FIXME: need to adapt this to the new disciplines when the time comes and test it
        if self.cycleCondition:
            Screen.window.after(1000, self.checkDownloads)
            for filename in os.listdir(Screen.container.downloadsDirectory):
                if os.path.getctime(
                        os.path.join(Screen.container.downloadsDirectory,
                                     filename)
                ) > self.tempoAtual and os.path.getsize(
                        os.path.join(
                            Screen.container.downloadsDirectory,
                            filename)) > 0 and filename.endswith(".pdf"):
                    self.ent_newFilename.config(state=TK.NORMAL)
                    self.ent_newFilename.insert(0, filename)
                    self.dropdownMenu.config(state=TK.NORMAL)
                    self.btn_confirm.config(state=TK.NORMAL)
                    self.btn_confirm.wait_variable(self.fileFound)
                    self.ent_newFilename.config(state=TK.DISABLED)
                    self.dropdownMenu.config(state=TK.DISABLED)
                    self.btn_confirm.config(state=TK.DISABLED)
                    self.fileFound.set(False)
                    oldFile = os.path.join(Screen.container.downloadsDirectory,
                                           filename)
                    newFile = os.path.join(self.OneDrive, self.pathSelected,
                                           self.ent_newFilename.get())
                    if self.pathSelected.get(
                    ) != "Delete" and self.pathSelected.get() != "Skip":
                        while True:
                            try:
                                os.rename(oldFile, newFile)
                                self.addToOutput(oldFile, newFile)
                                break
                            except FileExistsError:
                                os.remove(newFile)
                    else:
                        if self.pathSelected.get() == "Delete":
                            subprocess.run([Screen.container.recycle, oldFile])
                            self.addToOutput(
                                oldFile, newFile[newFile.rfind(os.sep) + 1:] +
                                " deleted")
                        else:
                            self.addToOutput(oldFile, oldFile)
                    # destino = self.whichFolder(filename)
                    # if "False" != destino:
                    #     try:
                    #         os.rename(
                    #             os.path.join(Screen.container.downloadsDirectory, filename),
                    #             destino)
                    #         self.addToOutput(filename, destino, "notExisted")
                    #     except FileExistsError:
                    #         os.remove(destino)
                    #         os.rename(
                    #             os.path.join(Screen.container.downloadsDirectory, filename),
                    #             destino)
                    #         self.addToOutput(filename, destino, "existed")
                    # else:
                    #     self.addToOutput(filename, "REMOVED/SKIPPED",
                    #                      "deleted/Skipped")

    # def whichFolder(self, filename):
    #     if filename.startswith("PT_AC_"):
    #         return os.path.join(self.ACaulas,
    #                             filename[len("PT_AC_"):].replace("T_", ""))
    #     elif filename.startswith("Apresentação") or filename.startswith(
    #             "Guia"):
    #         return os.path.join(self.ACpl, filename)
    #     elif filename.startswith("Aula_"):
    #         return os.path.join(self.ACtp, filename)
    #     elif filename.startswith("T1") or filename.startswith("T2"):
    #         if "Frequencia" in filename:
    #             return os.path.join(
    #                 self.ACfreq, 'Normal',
    #                 filename[len("T1_"):].replace("_AC",
    #                                               "").replace("_PT", ""))
    #         elif "Recurso" in filename:
    #             return os.path.join(
    #                 self.ACfreq, 'Recurso', filename[len("T1_T2_"):].replace(
    #                     "_AC", "").replace("_PT", "").replace("_20", ""))
    #         elif "Especial" in filename:
    #             return os.path.join(
    #                 self.ACfreq, 'EpocaEspecial', filename[len("T1_T2_"):].replace(
    #                     "_AC", "").replace("_PT", "").replace("_20", ""))
    #     elif filename.startswith("AC_P"):
    #         return os.path.join(self.ACgeral,
    #                             "Enunciado Projeto " + filename[4] + ".pdf")
    #     elif filename[2] == ".":
    #         return os.path.join(self.POOaulas, filename)
    #     elif filename.startswith("Ficha"):
    #         diretoria = os.path.join(
    #             self.POOpl, filename[:filename.find(".")].replace(" ", ""))
    #         try:
    #             os.makedirs(diretoria)
    #         except FileExistsError:
    #             pass
    #             # print("Directory already existed")
    #         return os.path.join(diretoria, filename)
    #     elif filename.startswith("MNIO_FichaExerc"):
    #         return os.path.join(self.MNIOtp, filename[len("MNIO_"):])
    #     elif filename.startswith("MNIO_Formulario"):
    #         return os.path.join(self.MNIOformularios_geral, filename[len("MNIO_"):])
    #     elif filename.startswith("Folha"):
    #         return os.path.join(self.TFCtp, filename.replace("TFC1920", ""))
    #     elif filename.startswith("TFC1920"):
    #         numero = filename[filename.rfind("Semana") +
    #                           6:filename.rfind("Handout") - 1]
    #         return os.path.join(
    #             self.TFCaulas,
    #             filename.replace("TFC1920", "").replace("-", "")[0:12] +
    #             numero + ".pdf")
    #     else:
    #         rename = input(
    #             "This is the file " + filename +
    #             "\nDo you want to rename it? (y/n, d to delete, s to skip)\n")
    #         if rename == "y":
    #             filename = input("Rename the file: ") + ".pdf"
    #         elif rename == "d":
    #             os.remove(os.path.join(Screen.container.downloadsDirectory, filename))
    #             return "False"
    #         elif rename == "s":
    #             return "False"
    #         op = input(
    #             "Choose the discipline:\n1.AC\n2.POO\n3.TFC\n4.MNIO\nOption: ")
    #         if op == "1":
    #             return os.path.join(self.ACgeral, filename)
    #         elif op == "2":
    #             return os.path.join(self.POOgeral, filename)
    #         elif op == "3":
    #             return os.path.join(self.TFCgeral, filename)
    #         elif op == "4":
    #             return os.path.join(self.MNIOformularios_geral, filename)


class MusicScreen(Screen):
    def __init__(self, masterFramePreviousScreen: TK.Frame, firstTime):
        super().__init__(masterFramePreviousScreen)
        if firstTime:
            openThread = threading.Thread(target=lambda: os.startfile(
                os.path.join(Screen.container.baseDirectory, "auxFiles",
                             "deemix", "start.bat")),
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

    """
        Method that stops the cycle first and then, if called again (by button click or Enter), advances to the next Screen
    """

    def nextScreen(self, event=None):
        if self.checkMusicCondition:
            self.checkMusicCondition = False
            self.scrollableWidget.boxes[0].config(state=TK.NORMAL)
            self.scrollableWidget.boxes[0].delete("end-1c linestart", TK.END)
            self.scrollableWidget.boxes[0].config(state=TK.DISABLED)
            self.btn_nextScreen.config(text="Get Album Year and Lyrics",
                                       state=TK.DISABLED)
            self.moveOutOfBuffer()
        else:
            if self.canAdvance:
                AlbumAndLyricsScreen(self.frm_master, self.newFiles)

    """
        Method that checks, while self.checkMusicCondition is true, for new files and adds them to the output and buffer
    """

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

    """
        Method that takes care of moving the downloaded files to the correct directory and renames them if necessary
    """

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
        else:
            self.canAdvance = True
            self.btn_nextScreen.config(state=TK.NORMAL)
            self.scrollableWidget.boxes[1].config(state=TK.NORMAL)
            self.scrollableWidget.boxes[1].delete("end-1c linestart", TK.END)
            self.scrollableWidget.boxes[1].config(state=TK.DISABLED)

    """
        Method that takes care of making some slight changes to the file's tags
    """

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
        Screen.window.state('zoomed')  #maximizes the window
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
        self.trackBeingReviewedTrackCount = 0

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
                width=70,
                state=TK.DISABLED)
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

        Screen.window.update_idletasks()
        self.lyricsAndYear()

    """
        Method called when user decides to skip a song, most likely Genius doesn't have the lyrics
        Saves it in the list of songs to skip
    """

    def skipLyrics(self):
        self.currentLyrics = "None"
        Screen.container.songsToSkip.append([
            self.currentArtist.get(),
            self.currentAlbum.get(),
            self.currentTitle.get()
        ])
        self.errorHandled.set(True)

    """
        Method that doesn't advance to a different screen but takes care of notifying that user thinks he has handled the error
    """

    def nextScreen(self, event=None):
        if self.btn_tryAgain["state"] == TK.NORMAL:
            self.errorHandled.set(True)

    # restricts entry to only accept digits
    def testVal(self, inStr):
        if not inStr.isdigit():
            return False
        return True

    """
        Method called when the user closes the window, maybe after an error or between files, saves the "exceptions" to the files
    """

    def on_closing(self):
        self.errorHandled.set(True)
        Screen.container.saveExceptions()
        Screen.window.destroy()

    def goBackDownloadMore(self):
        Screen.window.state('normal')
        MusicScreen(self.frm_master, False)

    """
        Method called when the Exit button is pressed, quits the window and opens the Handler
    """

    def exitOpenHandler(self):
        Screen.container.saveExceptions()
        Screen.window.quit()
        # os.system("taskkill /f /im  deemix-pyweb.exe")
        if "GitHub" in Screen.container.baseDirectory:
            threading.Thread(target=subprocess.run([
                'python',
                os.path.join(Screen.container.baseDirectory,
                             "Handler_Music.py")
            ]),daemon=False).start()
        else:
            threading.Thread(target=subprocess.run([
                os.path.join(Screen.container.baseDirectory, "Handler_Music",
                             "Handler_Music.exe")
            ]),daemon=False).start()


    """
        Method that changes the last line if an error ocurred and the user had to change something
    """

    def changeOutput(self, index, inYear):
        self.scrollableWidget.boxes[index].delete("end-1c linestart", TK.END)
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

    """
        Method that plays the windows "error" sound, and resets the thread, because these cannot be restarted, need to be a new instance
    """

    def thread_function(self):
        self.exceptionRaised = True
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        self.errorSound = threading.Thread(target=self.thread_function,
                                           daemon=True)

    """
        Method that adds the output to the textboxes
    """

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

    """
        Method that takes care of disabling the entries, after a user has confirmed he might have fixed the error
    """

    def disableEntries(self):
        for entry in self.entriesTrack:
            entry.config(state=TK.DISABLED)
        self.btn_tryAgain.config(state=TK.DISABLED)
        self.btn_skipLyrics.config(state=TK.DISABLED)

    """
        Method that takes care of enabling the entries so the user can correct the attributes and continue
    """

    def enableEntries(self, whichOnes):
        if whichOnes == 0:  #error when getting year
            self.entriesTrack[1].config(state=TK.NORMAL)
        elif whichOnes == 1:  #error when getting lyrics
            self.btn_skipLyrics.config(state=TK.NORMAL)
        self.entriesTrack[0].config(state=TK.NORMAL)
        self.entriesTrack[2].config(state=TK.NORMAL)
        self.btn_tryAgain.config(state=TK.NORMAL)

    """
        Method that changes the tag (the color) of the last line, simbolizes change in phases
    """

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
        Determines the artist and title to be used in the search for lyrics and year, changing them if they are in the dictionary
    """

    def ArtistAlbumAndTitle(self, forYear):
        if forYear:
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
        if not forYear or self.trackBeingReviewedTrackCount < 5:
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

    """
        Method that returns the index in the title of the roman numeral, if there is one
    """

    def titleContainsRomanNumeral(self):
        for index in range(len(self.romanNums)):
            if self.romanNums[index] in self.currentTitle.get():
                return index
        return -1

    """
        Method that returns the BeautifulSoup of the html of the page, if it exists, otherwise returns None
        If it's to get the year and we have already visited the page, we return "Skip" so we know we don't need to scrape the html again
    """

    def checkIfWebpageExists(self, forAlbum):
        if forAlbum:
            name = self.namingConventions(
                self.currentArtist.get()) + "/" + self.namingConventions(
                    self.currentAlbum.get())
            url = "https://www.genius.com/albums/" + name
            if name in AlbumAndLyricsScreen.pagesVisited_year:
                self.currentYear.set(
                    AlbumAndLyricsScreen.pagesVisited_year[name])
                self.currentUrl.set(url)
                Screen.window.update_idletasks()
                return "Skip"
        else:
            name = self.namingConventions(self.currentArtist.get() + " " +
                                          self.currentTitle.get())
            url = "https://genius.com/" + name + "-lyrics"
        self.currentUrl.set(url)
        Screen.window.update_idletasks()
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
        Gets the year of release of the current file, writing it in the metaTag of the file, given it has the metaTags defined correctly
        In case of not finding the page, it asks the user. If the user corrects it succesfully, we save it in the exceptionsReplacements dict
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
            if self.trackBeingReviewedTrackCount < 5:  #for getting the year of singles, which don't have an albums page created on Genius
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
            while True:  #if the errorSound is started while it's still playing it throws an exception
                try:
                    self.errorSound.start()
                    break
                except:
                    pass
            #In case of an error we pop up a google search to help the user
            if self.trackBeingReviewedTrackCount < 5:
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
            self.btn_tryAgain.wait_variable(
                self.errorHandled
            )  #waits for the user to confirm he has corrected it
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

    """
        Gets the lyrics of the current file, writing them in the metaTags of the file, given it has the metaTags defined correctly
        In case of not finding the page, it asks the user to correct the attributes so we can search again
    """

    def setLyricsCycle(self):
        soup = self.checkIfWebpageExists(False)
        if soup != None:
            for div in soup.findAll('div', attrs={'class': 'lyrics'}):
                self.currentLyrics += div.text.strip()
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
                while True:  #if the errorSound is started while it's still playing it throws an exception
                    try:
                        self.errorSound.start()
                        break
                    except:
                        pass
                self.errorHandled.set(False)
                self.enableEntries(1)
                #In case of an error we pop up a google search to help the user
                webbrowser.open("https://www.google.com.tr/search?q={}".format(
                    self.currentArtist.get().replace(" &", "").replace(
                        " ", "+") + "+" + self.currentTitle.get().replace(
                            " &", "").replace(" ", "+") +
                    "+lyrics+site:Genius.com"))
                self.btn_tryAgain.wait_variable(
                    self.errorHandled
                )  #waits for the user to confirm he has corrected it
                self.value = [
                    self.currentArtist.get(),
                    self.currentAlbum.get(),
                    self.currentTitle.get()
                ]
                self.changeOutput(0, False)
                self.changeOutput(2, False)
                self.disableEntries()
                self.setLyricsCycle()
        return

    def setLyrics(self, filename):
        self.currentLyrics = ""
        self.setLyricsCycle()
        if self.currentLyrics != "None":
            audio = ID3(filename)
            audio.delall("USLT")
            audio.add(USLT(encoding=3, text=self.currentLyrics))
            audio.save()

    """
        Method that goes through all the files in self.newFiles and gets their correct release year (not the year they were remastered) and their lyrics, if we don't skip the file
    """

    def lyricsAndYear(self):
        if self.newFiles != []:
            self.removePtOrPart = False
            filename = self.newFiles[0]
            id3 = EasyID3(filename)
            artist = id3['albumartist'][0]
            title = id3['title'][0]
            album = id3['album'][0]
            self.currentYear.set(int(id3["date"][0]))
            aux = id3["tracknumber"][0]
            self.trackBeingReviewedTrackCount = int(aux[aux.find("/") + 1:])
            id3.save()
            title = Screen.removeWordsFromWord([
                "feat", "Feat", "bonus", "Bonus", "Conclusion", "Hidden Track",
                "Vocal Mix", "Explicit", "explicit", "Extended"
            ], title)
            self.currentArtist.set(artist)
            self.currentAlbum.set(album)
            self.currentTitle.set(title)
            self.key = [artist, album, title]
            self.addToOutput()
            self.ArtistAlbumAndTitle(True)
            self.getYear(filename)
            inYear = False
            if self.exceptionRaised and self.key != self.value:
                if self.key[2] == self.value[2]:
                    self.key[2] = None
                    self.value[2] = None
                Screen.container.exceptionsReplacements[tuple(
                    self.key)] = self.value
                self.exceptionRaised = False
            self.changeTag("lyrics")
            self.ArtistAlbumAndTitle(False)
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
            opStatus = Screen.container.iTunesLibrary.AddFile(filename)
            while opStatus.InProgress:
                pass
            iTunesTrack = opStatus.Tracks.Item(1)
            if self.currentYear.get() < 1985:
                iTunesTrack.VolumeAdjustment = 50
            for txt in self.scrollableWidget.boxes:
                txt.insert(TK.END, "\n")
                txt.see(TK.END)
            self.numberOfFilesProcessed += 1
            self.title.set(
                str(self.numberOfFilesProcessed) + "/" +
                str(self.totalNewFiles) + " Files Processed")
            Screen.container.iTunesLibrary.AddFile(filename)
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
    # url ="https://www.genius.com/Wu-tang-clan-wu-tang-7th-chamber-lyrics"
    # req = Request(url,
    #                 headers={'User-Agent': 'Mozilla/5.0'})
    # webpage = urlopen(req).read()
    # # Creating a BeautifulSoup object of the html page for easy extraction of data.
    # soup = BeautifulSoup(webpage, 'html.parser')
    # aux = []
    # for div in soup.findAll(
    #         'div',
    #         attrs={
    #             'class':
    #             lambda x: x and x.startswith("Lyrics__Container")
    #         }):
    #     for elem in div.contents:
    #         try:
    #             if str(elem) != "<br/>":
    #                 aux.append(elem.text)
    #             else:
    #                 aux.append("")
    #         except:
    #             aux.append(str(elem))
    #     aux.append("")
    # for index in range(len(aux)):
    #     if aux[index].startswith("[") and aux[index - 1] != "":
    #         aux.insert(index, "")
    # index = 0
    # while index < len(aux):
    #     try:
    #         if aux[index] == "" and aux[index + 1] != "":
    #             aux.pop(index)
    #         elif aux[index] == "" and aux[index + 1] == "":
    #             aux.pop(index)
    #             index += 1
    #     except:
    #         pass
    #     index += 1
    # print("\n".join(aux).strip())