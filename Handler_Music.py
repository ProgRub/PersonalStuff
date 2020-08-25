import os
import threading
import tkinter as TK
import tkinter.filedialog as filedialog
import tkinter.colorchooser as colorchooser
from mutagen.easyid3 import EasyID3
import subprocess
from Screen import Screen
from ScrollableWidget import ScrollableWidget

#TODO: comment the code


class InitialScreen(Screen):
    def __init__(self, masterFramePreviousScreen, firstTime=True):
        super().__init__(masterFramePreviousScreen)
        #Thread to check files in the background
        self.firstTime = firstTime and os.path.isdir(
            Screen.container.musicDestinyDirectory)
        self.checkFilesThread = threading.Thread(
            target=Screen.container.checkFiles, daemon=True)
        if self.firstTime:
            self.checkFilesThread.start()

        #Widget Creation
        self.lbl_title.config(
            text=
            "Welcome to the Music Handler Program!\nYou can search your library for a certain file\nOr choose an album to listen to!"
        )
        self.frm_whichDirectory = TK.Frame(self.frm_master,
                                           width=750,
                                           height=250,
                                           bg=Screen.DEFAULT_BGCOLOR)
        self.lbl_whichDirectory = TK.Label(
            self.frm_whichDirectory,
            text="In which directory do you have your music files?",
            font=Screen.DEFAULT_FONT1,
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white")
        self.ent_Directory = TK.Entry(self.frm_whichDirectory,
                                      width=60,
                                      state=TK.NORMAL,
                                      font=Screen.DEFAULT_FONT3)
        self.ent_Directory.insert(TK.END,
                                  str(Screen.container.musicDestinyDirectory))
        self.ent_Directory.config(state="readonly")
        self.btn_chooseDirectory = TK.Button(self.frm_whichDirectory,
                                             text="Open",
                                             command=self.chooseDirectory,
                                             font=Screen.DEFAULT_FONT3)
        self.btn_advanceScreen = TK.Button(self.frm_master,
                                           text="Choose Album",
                                           command=self.nextScreen,
                                           font=Screen.DEFAULT_FONT3)
        self.btn_recalibrateAll = TK.Button(self.frm_master,
                                            text="Recalibrate All Files",
                                            command=self.recalibrateAll,
                                            font=Screen.DEFAULT_FONT3)
        self.btn_chooseGenreColors = TK.Button(
            self.frm_master,
            text="Genre Colors",
            command=self.chooseGenreColorsScreen,
            font=Screen.DEFAULT_FONT3)
        self.btn_registerWorkout = TK.Button(
            self.frm_master,
            text="Register Workout",
            command=self.registerWorkoutScreen,
            font=Screen.DEFAULT_FONT3)
        self.btn_searchLibrary = TK.Button(self.frm_master,
                                           text="Search Library",
                                           command=self.searchLibraryScreen,
                                           font=Screen.DEFAULT_FONT3)

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=200)
        self.frm_whichDirectory.grid(row=1, column=0)
        self.lbl_whichDirectory.grid(row=1, column=0)
        self.ent_Directory.grid(row=2, column=0, padx=50)
        self.btn_chooseDirectory.grid(row=2, column=1)
        self.btn_advanceScreen.grid(row=3, column=2)
        self.btn_recalibrateAll.grid(row=4, column=2)
        self.btn_chooseGenreColors.grid(row=5, column=2)
        self.btn_registerWorkout.grid(row=6, column=2)
        self.btn_searchLibrary.grid(row=7, column=2)

    def chooseDirectory(self):
        aux = filedialog.askdirectory(initialdir=os.path.join(
            "C:", os.sep, "Users", "ruben", "Desktop")).replace("/", "\\")
        if aux != "":
            Screen.container.musicDestinyDirectory = aux
            Screen.container.saveDirectories()
            self.checkFilesThread.start()
        self.ent_Directory.config(state=TK.NORMAL)
        self.ent_Directory.delete(0, 'end')
        self.ent_Directory.insert(TK.END,
                                  str(Screen.container.musicDestinyDirectory))
        self.ent_Directory.config(state="readonly")

    def nextScreen(self, event=None):
        if self.firstTime:
            self.checkFilesThread.join()
        ChooseAlbumScreen(self.frm_master)

    def recalibrateAll(self):
        if self.firstTime:
            self.checkFilesThread.join()
        Screen.container.listMusicFile.clear()
        Screen.container.listAlbums.clear()
        Screen.container.timeOfLastModified = Screen.container.timeOfLastModifiedFile = 0
        newFilesFoundScreen(self.frm_master)

    def chooseGenreColorsScreen(self):
        if self.firstTime:
            self.checkFilesThread.join()
        ChooseColorsScreen(self.frm_master)

    def registerWorkoutScreen(self):
        if self.firstTime:
            self.checkFilesThread.join()
        WorkoutRegistryScreen(self.frm_master)

    def searchLibraryScreen(self):
        if self.firstTime:
            self.checkFilesThread.join()
            Screen.container.updatePlayCounts()
        SearchLibraryScreen(self.frm_master)


class SearchLibraryScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)
        # Possible attributes to search
        self.searchableAttrs = {
            "Artist": None,
            "Album": None,
            "Genre": None,
            "Year": None,
            "Title": None
        }
        self.listOfResults = []

        #Widget Creation
        self.lbl_title.config(text="Search the Library")
        i = 1
        for attribute in self.searchableAttrs:
            stringVar = TK.StringVar()
            stringVar.trace("w", self.updateResults)
            lbl_field = TK.Label(self.frm_master,
                                 text=attribute,
                                 font=Screen.DEFAULT_FONT2,
                                 bg=Screen.DEFAULT_BGCOLOR,
                                 fg="white")
            ent_field = TK.Entry(self.frm_master,
                                 textvariable=stringVar,
                                 width=80,
                                 font=Screen.DEFAULT_FONT3)
            lbl_field.grid(row=i, column=1)
            ent_field.grid(row=i, column=2)
            self.searchableAttrs[attribute] = stringVar
            i += 1
        self.scrollableWidget = ScrollableWidget(self.frm_master, ["Listbox"])
        self.scrollableWidget.boxes[0].config(state=TK.DISABLED,
                                              width=100,
                                              height=25,
                                              selectmode=TK.EXTENDED)
        self.btn_trackDetails = TK.Button(self.frm_master,
                                          text="Show Track Details",
                                          font=Screen.DEFAULT_FONT3,
                                          command=self.nextScreen)

        #Widget Placement
        self.lbl_title.grid(row=0, column=3)
        self.scrollableWidget.frame.grid(row=1,
                                         column=3,
                                         rowspan=len(self.searchableAttrs) *
                                         15)
        self.scrollableWidget.boxes[0].grid(row=0, column=0)
        self.scrollableWidget.scrollbar.grid(row=0, column=1, sticky=TK.NS)
        self.btn_backScreen.grid(row=i, column=0)
        self.btn_trackDetails.grid(row=i, column=2)

        #Widget Configuration
        self.scrollableWidget.boxes[0].bind("<Delete>", self.deleteTracks)

    def backScreen(self, event=None):
        Screen.container.generateAlbums()
        Screen.container.reWriteFiles()
        InitialScreen(self.frm_master, False)

    def nextScreen(self, event=None):
        aux = [
            self.scrollableWidget.boxes[0].get(index)
            for index in self.scrollableWidget.boxes[0].curselection()
        ]
        if len(aux) != 0:
            TrackDetailsScreen(self.frm_master, [
                musicFile for musicFile in self.listOfResults
                if musicFile.filename in aux
            ])

    def updateResults(self, *args):
        self.listOfResults = Screen.container.listMusicFile.copy()
        lenPossHits = len(self.listOfResults)
        for attr in self.searchableAttrs:
            index = 0
            if self.searchableAttrs[attr].get().strip() != "":
                while index < lenPossHits:
                    musicFile = self.listOfResults[index]
                    if self.searchableAttrs[attr].get().lower(
                    ) not in musicFile.getAttribute(attr).lower():
                        self.listOfResults.remove(musicFile)
                        index -= 1
                        lenPossHits -= 1
                    index += 1
        self.writeResults()

    def writeResults(self):
        self.scrollableWidget.boxes[0].config(state=TK.NORMAL)
        self.scrollableWidget.boxes[0].delete(0, TK.END)
        self.listOfResults.sort(key=lambda x: x.filename)
        for obj in self.listOfResults:
            self.scrollableWidget.boxes[0].insert(TK.END, obj.filename)

    def deleteTracks(self, event=None):
        #TODO: also remove from iTunes
        numFilesDeleted = 0
        for index in self.scrollableWidget.boxes[0].curselection():
            Screen.container.findiTunesTrack()
            subprocess.run([
                Screen.container.recycle,
                os.path.join(
                    Screen.container.musicDestinyDirectory,
                    self.scrollableWidget.boxes[0].get(index -
                                                       numFilesDeleted))
            ])
            self.scrollableWidget.boxes[0].delete(index - numFilesDeleted)
            numFilesDeleted += 1


class TrackDetailsScreen(Screen):
    def __init__(self, masterFramePreviousScreen, listOfFiles):
        super().__init__(masterFramePreviousScreen)
        #Attributes
        self.attributes = {
            "Title": [],
            "Artist": [],
            "Album": [],
            "Track Number": [],
            "Disc Number": [],
            "Genre": [],
            "Year": [],
            "Play Count":[]
        }
        self.listOfFiles = listOfFiles

        #Widget Creation
        self.lbl_title.config(text="Track Details")
        i = 1
        for attr in self.attributes:
            label = TK.Label(self.frm_master,
                             text=attr,
                             font=Screen.DEFAULT_FONT2,
                             bg=Screen.DEFAULT_BGCOLOR,
                             fg="white")
            entry = TK.Entry(self.frm_master,
                             font=Screen.DEFAULT_FONT3,
                             width=80)
            attribute = self.listOfFiles[0].getAttribute(attr)
            entry.insert(TK.END, str(attribute))
            for musicFile in self.listOfFiles:
                if musicFile.getAttribute(attr) != attribute:
                    entry.delete(0, TK.END)
                    break
            self.attributes[attr].append(entry.get())
            self.attributes[attr].append(entry)
            label.grid(row=i, column=1)
            entry.grid(row=i, column=2)
            i += 1

        #Widget Placement
        self.lbl_title.grid(row=0, column=2)
        self.btn_backScreen.grid(row=i, column=0)

    def backScreen(self, event=None):
        if not all([
                self.attributes[attr][0] == self.attributes[attr][1].get()
                for attr in self.attributes
        ]):
            for musicFile in self.listOfFiles:
                audio = EasyID3(
                    os.path.join(Screen.container.musicDestinyDirectory,
                                 musicFile.filename))
                for attr in self.attributes:
                    newAttribute = self.attributes[attr][1].get()
                    if self.attributes[attr][0] != newAttribute:
                        audio[musicFile.attributeToMutagenTag(
                            attr)] = newAttribute
                        musicFile.setAttribute(attr,newAttribute)
                audio.save()
        SearchLibraryScreen(self.frm_master)


class ChooseColorsScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)

        #Widget Creation
        self.lbl_title.config(
            text="Click the button of the Genre which color you want to change"
        )
        i = 1
        Screen.container.getGenreColors()
        self.genreButtons = {}
        self.exampleLabels = {}
        for genre in Screen.container.genresColors:
            btn_genre = TK.Button(
                self.frm_master,
                text=Screen.container.inverseCorrectRapGenre(genre),
                font=Screen.DEFAULT_FONT3,
                command=lambda genre=genre: self.changeColor(genre),
                fg=Screen.container.genresColors[genre])
            lbl_example = TK.Label(self.frm_master,
                                   text="This is an example.",
                                   font=Screen.DEFAULT_FONT3,
                                   fg=Screen.container.genresColors[genre],
                                   bg=Screen.DEFAULT_BGCOLOR)
            self.genreButtons[genre] = btn_genre
            self.exampleLabels[genre] = lbl_example
            btn_genre.grid(row=i, column=0)
            lbl_example.grid(row=i, column=1)
            i += 1

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=100)
        self.btn_backScreen.grid(row=i, column=1)

    def changeColor(self, genre):
        color = colorchooser.askcolor()[1]
        Screen.container.genresColors[genre] = color
        self.genreButtons[genre].configure(
            fg=Screen.container.genresColors[genre])
        self.exampleLabels[genre].configure(
            fg=Screen.container.genresColors[genre])

    def backScreen(self, event=None):
        Screen.container.saveGenreColors()
        InitialScreen(self.frm_master, False)


class WorkoutRegistryScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)

        #Tkinter Vars
        self.workoutName = TK.StringVar()
        self.time = TK.StringVar()

        #Widget Creation
        self.lbl_title.config(
            text=
            "Input the name of the workout and how long it took (format MM:SS)"
        )
        self.lbl_workoutName = TK.Label(self.frm_master,
                                        text="Name of the Workout",
                                        bg=Screen.DEFAULT_BGCOLOR,
                                        fg="white",
                                        font=Screen.DEFAULT_FONT2)
        self.lbl_time = TK.Label(self.frm_master,
                                 text="Time to Complete",
                                 bg=Screen.DEFAULT_BGCOLOR,
                                 fg="white",
                                 font=Screen.DEFAULT_FONT2)
        self.ent_workoutName = TK.Entry(self.frm_master,
                                        textvariable=self.workoutName,
                                        font=Screen.DEFAULT_FONT3,
                                        width=30)
        self.ent_time = TK.Entry(self.frm_master,
                                 textvariable=self.time,
                                 font=Screen.DEFAULT_FONT3,
                                 width=6)
        self.btn_confirm = TK.Button(self.frm_master,
                                     text="Confirm",
                                     font=Screen.DEFAULT_FONT3,
                                     command=self.nextScreen)

        #Widget Placement
        self.lbl_title.grid(row=0, column=1)
        self.lbl_workoutName.grid(row=1, column=0)
        self.lbl_time.grid(row=2, column=0)
        self.ent_workoutName.grid(row=1, column=1, sticky=TK.W)
        self.ent_time.grid(row=2, column=1, sticky=TK.W)
        self.btn_confirm.grid(row=3, column=1)
        self.btn_backScreen.grid(row=3, column=0)

    def convertStrTimeToFloat(self, time):
        try:
            minutes = time.split(":")[0]
            seconds = time.split(":")[1]
            if (len(minutes) == 2 and len(seconds) == 2):
                return ((int(minutes[0]) * 10 + int(minutes[1])) *
                        60) + (int(seconds[0]) * 10 + int(seconds[1]))
            else:
                return -1
        except (ValueError, IndexError) as e:
            return -1

    def nextScreen(self, event=None):
        time = int(self.convertStrTimeToFloat(self.time.get()))
        workoutName = self.workoutName.get().strip()
        if time != -1:
            if workoutName in Screen.container.workoutDatabase:
                Screen.container.workoutDatabase[workoutName].append(time)
            else:
                Screen.container.workoutDatabase[workoutName] = [time]
            self.time.set("")
        else:
            self.workoutName.set("")
            self.ent_workoutName.focus()

    def backScreen(self, event=None):
        Screen.container.saveWorkoutDatabase()
        InitialScreen(self.frm_master, False)
        pass


class newFilesFoundScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)
        #Tkinter Vars
        self.numberOfFilesFound = 0
        self.totalNewFiles = len([
            f for f in Screen.container.files
            if os.path.getmtime(f) > Screen.container.timeOfLastModifiedFile
        ])
        self.auxVar = TK.StringVar()
        self.auxVar.set(
            str(self.numberOfFilesFound) + "/" + str(self.totalNewFiles) +
            " Files Found")
        HEIGHT = 40
        categories_width = {
            "Artist": 35,
            "Album": 60,
            "Title": 75,
            "Genre": 15,
            "Year": 5,
            "Track\nN.": 6,
            "Disc\nN.": 6
        }

        #Widget Creation
        self.lbl_title.config(textvariable=self.auxVar)
        self.scrollWidget = ScrollableWidget(
            self.frm_master, ["Textbox" for i in range(len(categories_width))])
        # self.textBoxes = []
        i = 0
        for category in categories_width:
            lbl_category = TK.Label(self.scrollWidget.frame,
                                    text=category,
                                    font=Screen.DEFAULT_FONT2,
                                    bg=Screen.DEFAULT_BGCOLOR,
                                    fg="white")
            self.scrollWidget.boxes[i].config(width=categories_width[category],
                                              height=HEIGHT)
            lbl_category.grid(row=0, column=i)
            self.scrollWidget.boxes[i].grid(row=1, column=i)
            Screen.generateGenreTags(self.scrollWidget.boxes[i])
            i += 1
        self.btn_advanceScreen = TK.Button(
            self.frm_master,
            text=("Choose Album"
                  if not Screen.container.newFilesFound else "Exit"),
            font=Screen.DEFAULT_FONT3,
            command=self.nextScreen,
            state=TK.DISABLED)

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=200)
        self.scrollWidget.frame.grid(row=1, column=0)
        self.scrollWidget.scrollbar.grid(row=1, column=i, sticky=TK.NS)
        self.btn_advanceScreen.grid(row=2, column=0, padx=200)

        Screen.window.update_idletasks()
        Screen.container.checkFiles(self)

        #Delete last newline
        for txt in self.scrollWidget.boxes:
            txt.config(state=TK.NORMAL)
            txt.delete("end-1c linestart", TK.END)
            txt.config(state=TK.DISABLED)
            Screen.generateGenreTags(txt)

        #TK.Button only enabled once all files are found
        self.btn_advanceScreen.config(state=TK.NORMAL)

    def nextScreen(self, event=None):
        if not Screen.container.newFilesFound:
            ChooseAlbumScreen(self.frm_master)
        else:
            Screen.window.quit()

    def addToOutput(self, artist, album, title, genre, year, trackNumber,
                    discNumber):
        self.numberOfFilesFound += 1
        self.auxVar.set(
            str(self.numberOfFilesFound) + "/" + str(self.totalNewFiles) +
            " Files Found")
        aux = [artist, album, title, genre, year, trackNumber, discNumber]
        i = 0
        for txt in self.scrollWidget.boxes:
            txt.config(state=TK.NORMAL)
            txt.insert(TK.END,
                       str(aux[i]) + "\n",
                       Screen.container.correctRapGenre(genre))
            txt.config(state=TK.DISABLED)
            txt.see(TK.END)
            i += 1
        Screen.window.update_idletasks()


class ChooseAlbumScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)
        #Tkinter Vars
        self.overUnderLeeway = TK.IntVar()
        self.overUnderLeeway.set(0)
        self.selectAllGenres = TK.BooleanVar()
        self.time = TK.IntVar()
        self.leeway = TK.IntVar()
        self.workoutName = TK.StringVar()
        #Widget Creation
        self.lbl_infoChooseAlbum = TK.Label(
            self.frm_master,
            text="Choose the time and leeway of the album",
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white",
            font=Screen.DEFAULT_FONT1)
        self.lbl_chooseTime = TK.Label(self.frm_master,
                                       text="Time",
                                       bg=Screen.DEFAULT_BGCOLOR,
                                       fg="white",
                                       font=Screen.DEFAULT_FONT3)
        self.lbl_chooseLeeway = TK.Label(self.frm_master,
                                         text="Leeway",
                                         bg=Screen.DEFAULT_BGCOLOR,
                                         fg="white",
                                         font=Screen.DEFAULT_FONT3)
        self.ent_chooseTime = TK.Entry(self.frm_master,
                                       textvariable=self.time,
                                       width=30,
                                       font=Screen.DEFAULT_FONT3,
                                       validate="key")
        self.ent_chooseLeeway = TK.Entry(self.frm_master,
                                         textvariable=self.leeway,
                                         width=30,
                                         font=Screen.DEFAULT_FONT3,
                                         validate="key")
        self.lbl_missingTime = TK.Label(self.frm_master,
                                        text="Insert the time!",
                                        bg=Screen.DEFAULT_BGCOLOR,
                                        fg="red",
                                        font=Screen.DEFAULT_FONT3)
        self.lbl_missingLeeway = TK.Label(self.frm_master,
                                          text="Insert the leeway!",
                                          bg=Screen.DEFAULT_BGCOLOR,
                                          fg="red",
                                          font=Screen.DEFAULT_FONT3)
        aux = ["Both", "Over", "Under"]
        for i in range(len(aux)):
            radioButton = TK.Radiobutton(
                self.frm_master,
                text=aux[i],
                padx=20,
                variable=self.overUnderLeeway,
                value=i,
                bg=Screen.DEFAULT_BGCOLOR,
                fg="white",
                activebackground=Screen.DEFAULT_BGCOLOR,
                activeforeground="white",
                selectcolor=Screen.DEFAULT_BGCOLOR,
                font=Screen.DEFAULT_FONT3)
            radioButton.grid(row=i + 3, column=1)
        self.btn_selectAllAlbums = TK.Button(self.frm_master,
                                             text="All Albums",
                                             font=Screen.DEFAULT_FONT3,
                                             command=self.selectAllAlbums)
        self.btn_forWorkout = TK.Button(self.frm_master,
                                        text="Album For Workout",
                                        font=Screen.DEFAULT_FONT3,
                                        command=self.forWorkout)
        self.lbl_chooseWorkout = TK.Label(self.frm_master,
                                          text="Workout Name",
                                          font=Screen.DEFAULT_FONT2,
                                          bg=Screen.DEFAULT_BGCOLOR,
                                          fg="white")
        self.ent_workoutName = TK.Entry(self.frm_master,
                                        textvariable=self.workoutName,
                                        font=Screen.DEFAULT_FONT3,
                                        width=30)
        self.btn_confirmWorkout = TK.Button(self.frm_master,
                                            text="Confirm Workout",
                                            command=self.workoutChosen,
                                            font=Screen.DEFAULT_FONT3)
        self.btn_forCar = TK.Button(self.frm_master,
                                    text="Album For Car",
                                    font=Screen.DEFAULT_FONT3,
                                    command=self.forCar)
        self.btn_allGenres = TK.Checkbutton(
            self.frm_master,
            text="All genres",
            font=Screen.DEFAULT_FONT3,
            fg="white",
            bg=Screen.DEFAULT_BGCOLOR,
            activebackground=Screen.DEFAULT_BGCOLOR,
            activeforeground="white",
            selectcolor=Screen.DEFAULT_BGCOLOR,
            command=self.tickAllCheckButtons,
            variable=self.selectAllGenres)
        self.btn_listAlbums = TK.Button(self.frm_master,
                                        text="Advance",
                                        font=Screen.DEFAULT_FONT3,
                                        command=self.nextScreen)
        i = 8
        self.booleanValsGenres = []
        self.checkButtons = []
        for genre in Screen.container.listGenres:
            var = TK.BooleanVar()
            btn_checkGenre = TK.Checkbutton(
                self.frm_master,
                text=Screen.container.inverseCorrectRapGenre(genre),
                variable=var,
                fg=Screen.container.genresColors[genre],
                bg=Screen.DEFAULT_BGCOLOR,
                activebackground=Screen.DEFAULT_BGCOLOR,
                activeforeground=Screen.container.genresColors[genre],
                selectcolor=Screen.DEFAULT_BGCOLOR,
                font=Screen.DEFAULT_FONT3)
            btn_checkGenre.grid(row=i, column=1, sticky=TK.W)
            self.checkButtons.append(btn_checkGenre)
            self.booleanValsGenres.append(var)
            i += 1

        #Widget Placement
        self.lbl_infoChooseAlbum.grid(row=0, column=2)
        self.lbl_chooseTime.grid(row=1, column=1)
        self.lbl_chooseLeeway.grid(row=2, column=1)
        self.ent_chooseTime.grid(row=1, column=2)
        self.ent_chooseLeeway.grid(row=2, column=2)
        self.lbl_missingTime.grid_forget()
        self.lbl_missingLeeway.grid_forget()
        self.btn_selectAllAlbums.grid(row=6, column=1)
        self.btn_allGenres.grid(row=7, column=1, sticky=TK.W)
        self.btn_forWorkout.grid(row=1, column=3)
        self.btn_forCar.grid(row=2, column=3)
        self.btn_listAlbums.grid(row=6, column=3)
        self.btn_backScreen.grid(row=6, column=0)

        #Widget Configuration (Entries only taking digits)
        self.ent_chooseTime.configure(
            validatecommand=(self.ent_chooseTime.register(self.testVal), '%P',
                             '%d'))
        self.ent_chooseLeeway.configure(
            validatecommand=(self.ent_chooseLeeway.register(self.testVal),
                             '%P', '%d'))
        self.ent_chooseTime.delete(0, TK.END)
        self.ent_chooseLeeway.delete(0, TK.END)
        self.ent_chooseTime.bind("<1>",self.hideMissingLabels)
        self.ent_chooseLeeway.bind("<1>",self.hideMissingLabels)

    # restricts entry to only accept digits
    def testVal(self, inStr, acttyp):
        if acttyp == '1':  #insert
            if not inStr.isdigit():
                return False
        return True

    def selectAllAlbums(self):
        if not self.selectAllGenres.get():
            self.btn_allGenres.invoke()
        self.time.set(240)
        self.leeway.set(240)

    def forWorkout(self):
        self.lbl_chooseWorkout.grid(row=0, column=3)
        self.ent_workoutName.grid(row=1, column=3)
        self.btn_confirmWorkout.grid(row=2, column=3)
        self.btn_forCar.grid_forget()
        self.btn_forWorkout.grid_forget()
        pass

    def workoutChosen(self):
        workoutName = self.workoutName.get()
        if workoutName in Screen.container.workoutDatabase:
            timesSum = sum(Screen.container.workoutDatabase[workoutName])
            average = (timesSum // len(
                Screen.container.workoutDatabase[workoutName])) // 60
            if len(Screen.container.workoutDatabase[workoutName]) == 1:
                self.leeway.set(5)
            else:
                leewayMin = average - Screen.container.workoutDatabase[
                    workoutName][0] // 60
                leewayMax = average - Screen.container.workoutDatabase[
                    workoutName][len(Screen.container.
                                     workoutDatabase[workoutName]) - 1] // 60
                self.leeway.set(max(leewayMin, leewayMax))
            self.time.set(average)
        self.workoutName.set("")
        self.lbl_chooseWorkout.grid_forget()
        self.ent_workoutName.grid_forget()
        self.btn_confirmWorkout.grid_forget()
        self.btn_forWorkout.grid(row=1, column=3)
        self.btn_forCar.grid(row=2, column=3)

    def forCar(self):
        self.time.set(25)
        self.leeway.set(5)

    def tickAllCheckButtons(self):
        for val in self.booleanValsGenres:
            val.set(self.selectAllGenres.get())

    def genresPicked(self):
        genresOfAlbums = []
        for i in range(len(Screen.container.listGenres)):
            if self.booleanValsGenres[i].get():
                genresOfAlbums.append(Screen.container.listGenres[i])
        return genresOfAlbums

    def hideMissingLabels(self,event=None):
        self.lbl_missingTime.grid_forget()
        self.lbl_missingLeeway.grid_forget()

    def nextScreen(self, event=None):
        advance = True
        try:
            self.time.get()
            self.lbl_missingTime.grid_forget()
        except TK.TclError:
            advance = False
            self.lbl_missingTime.grid(row=1, column=2, padx=25)
        try:
            self.leeway.get()
            self.lbl_missingLeeway.grid_forget()
        except TK.TclError:
            advance = False
            self.lbl_missingLeeway.grid(row=2, column=2, padx=25)
        if advance:
            ListAlbumScreen(self.frm_master,
                            self.time.get(), self.leeway.get(),
                            self.overUnderLeeway.get(), self)

    def backScreen(self, event=None):
        InitialScreen(self.frm_master, False)


class ListAlbumScreen(Screen):
    def __init__(self, masterFramePreviousScreen, time, leeway,
                 overUnderLeeway, previousScreen):
        super().__init__(masterFramePreviousScreen)
        #Getting albums to display
        self.previousScreen = previousScreen
        self.genresOfAlbums = self.previousScreen.genresPicked()
        self.overUnderLeeway = overUnderLeeway
        self.time = float(time)
        self.leeway = float(leeway)
        self.over = self.overUnderLeeway <= 1
        self.under = self.overUnderLeeway <= 2 and self.overUnderLeeway != 1
        self.lists = self.getAlbum(self.time * 60, self.leeway * 60, self.over,
                                   self.under)
        self.possibleAlbums = self.lists[0]
        self.possibleHalfAlbums = self.lists[1]
        self.sortTimeMostToLeastPA = True
        self.sortPlayCountMostToLeastPA = False
        self.sortTimeMostToLeastPHA = True
        self.sortPlayCountMostToLeastPHA = False
        self.possibleAlbums.sort(key=lambda album: album.length,
                                 reverse=self.sortTimeMostToLeastPA)
        self.possibleHalfAlbums.sort(key=lambda album: album.length,
                                     reverse=self.sortTimeMostToLeastPHA)
        HEIGHT = 20

        #Widget Creation
        self.lbl_titleAlbumsScreen = TK.Label(
            self.frm_master,
            text=("These are the albums whose length varies between " +
                  str(int(self.time -
                          (self.leeway * int(self.under)))) + " and " +
                  str(int(self.time +
                          (self.leeway * int(self.over)))) + " minutes."),
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white",
            font=Screen.DEFAULT_FONT1)
        self.scrollWidgetPossibleAlbums = ScrollableWidget(
            self.frm_master, ["Listbox", "Textbox", "Textbox"])
        self.scrollWidgetPossibleAlbums.boxes[0].config(bd=0,
                                                        highlightthickness=0,
                                                        selectborderwidth=0,
                                                        width=70,
                                                        height=HEIGHT)
        self.scrollWidgetPossibleAlbums.boxes[1].config(width=10,
                                                        spacing3=1,
                                                        borderwidth=0,
                                                        height=HEIGHT)
        self.scrollWidgetPossibleAlbums.boxes[2].config(width=10,
                                                        spacing3=1,
                                                        borderwidth=0,
                                                        height=HEIGHT)
        self.btn_sortByTimePossibleAlbums = TK.Button(
            self.scrollWidgetPossibleAlbums.frame,
            text="Time",
            font=Screen.DEFAULT_FONT3,
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white",
            command=lambda: self.sortAlbums(0, 0))
        self.btn_sortByPlayCountPossibleAlbums = TK.Button(
            self.scrollWidgetPossibleAlbums.frame,
            text="Play Count",
            font=Screen.DEFAULT_FONT3,
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white",
            command=lambda: self.sortAlbums(0, 1))
        self.lbl_titleHalfAlbumsScreen = TK.Label(
            self.frm_master,
            text=
            ("These are the albums where half of their length varies between "
             + str(int(self.time - (self.leeway * int(self.under)))) +
             " and " + str(int(self.time +
                               (self.leeway * int(self.over)))) + " minutes."),
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white",
            font=Screen.DEFAULT_FONT1)
        self.scrollWidgetPossibleHalfAlbums = ScrollableWidget(
            self.frm_master, ["Listbox", "Textbox", "Textbox"])
        self.scrollWidgetPossibleHalfAlbums.boxes[0].config(
            bd=0,
            highlightthickness=0,
            selectborderwidth=0,
            width=70,
            height=HEIGHT)
        self.scrollWidgetPossibleHalfAlbums.boxes[1].config(width=10,
                                                            spacing3=1,
                                                            borderwidth=0,
                                                            height=HEIGHT)
        self.scrollWidgetPossibleHalfAlbums.boxes[2].config(width=10,
                                                            spacing3=1,
                                                            borderwidth=0,
                                                            height=HEIGHT)
        self.btn_sortByTimePossibleHalfAlbums = TK.Button(
            self.scrollWidgetPossibleHalfAlbums.frame,
            text="Time",
            font=Screen.DEFAULT_FONT3,
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white",
            command=lambda: self.sortAlbums(1, 0))
        self.btn_sortByPlayCountPossibleHalfAlbums = TK.Button(
            self.scrollWidgetPossibleHalfAlbums.frame,
            text="Play Count",
            font=Screen.DEFAULT_FONT3,
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white",
            command=lambda: self.sortAlbums(1, 1))
        self.btn_showTracklist = TK.Button(self.frm_master,
                                           text="Show Tracklist",
                                           font=Screen.DEFAULT_FONT3,
                                           command=self.nextScreen)
        self.lbl_colorsLabel = TK.Label(self.frm_master,
                                        bg=Screen.DEFAULT_BGCOLOR,
                                        fg="white",
                                        text="Colors Label",
                                        font=Screen.DEFAULT_FONT1)
        self.cnv_colorsLabel = TK.Canvas(
            self.frm_master,
            bg=Screen.DEFAULT_BGCOLOR,
            highlightthickness=0,
            bd=0,
            height=len(Screen.container.genresColors) * 1.5 * 25)

        #Widget Placement
        self.lbl_titleAlbumsScreen.grid(row=0, column=1)
        self.scrollWidgetPossibleAlbums.frame.grid(row=1, column=1)
        self.btn_sortByTimePossibleAlbums.grid(row=0, column=1)
        self.btn_sortByPlayCountPossibleAlbums.grid(row=0, column=2)
        self.scrollWidgetPossibleAlbums.boxes[0].grid(row=1,
                                                      column=0,
                                                      sticky=TK.NSEW)
        self.scrollWidgetPossibleAlbums.boxes[1].grid(row=1,
                                                      column=1,
                                                      sticky=TK.E)
        self.scrollWidgetPossibleAlbums.boxes[2].grid(row=1,
                                                      column=2,
                                                      sticky=TK.E)
        self.scrollWidgetPossibleAlbums.scrollbar.grid(row=1,
                                                       column=3,
                                                       sticky=TK.NS)
        self.lbl_titleHalfAlbumsScreen.grid(row=2, column=1)
        self.scrollWidgetPossibleHalfAlbums.frame.grid(row=3, column=1)
        self.btn_sortByTimePossibleHalfAlbums.grid(row=0, column=1)
        self.btn_sortByPlayCountPossibleHalfAlbums.grid(row=0, column=2)
        self.scrollWidgetPossibleHalfAlbums.boxes[0].grid(row=1,
                                                          column=0,
                                                          sticky=TK.NSEW)
        self.scrollWidgetPossibleHalfAlbums.boxes[1].grid(row=1,
                                                          column=1,
                                                          sticky=TK.E)
        self.scrollWidgetPossibleHalfAlbums.boxes[2].grid(row=1,
                                                          column=2,
                                                          sticky=TK.E)
        self.scrollWidgetPossibleHalfAlbums.scrollbar.grid(row=1,
                                                           column=3,
                                                           sticky=TK.NS)
        self.btn_showTracklist.grid(row=4, column=4)
        self.lbl_colorsLabel.grid(row=0, column=5)
        self.cnv_colorsLabel.grid(row=1, column=5, rowspan=2)
        self.btn_backScreen.grid(row=4, column=0)

        #Widget Configuration
        Screen.generateGenreTags(self.scrollWidgetPossibleAlbums.boxes[1])
        Screen.generateGenreTags(self.scrollWidgetPossibleHalfAlbums.boxes[1])
        Screen.generateGenreTags(self.scrollWidgetPossibleAlbums.boxes[2])
        Screen.generateGenreTags(self.scrollWidgetPossibleHalfAlbums.boxes[2])
        self.writePossibleAlbums()
        self.writePossibleHalfAlbums()
        i = 0
        for genre in Screen.container.genresColors:
            self.cnv_colorsLabel.create_rectangle(
                0,
                i * 25,
                25,
                25 + i * 25,
                fill=Screen.container.genresColors[
                    Screen.container.correctRapGenre(genre)])
            self.cnv_colorsLabel.create_text(
                35,
                13 + i * 25,
                text=" - " + Screen.container.inverseCorrectRapGenre(genre),
                fill="white",
                font=Screen.DEFAULT_FONT3,
                anchor=TK.W)
            i += 1.5

    def sortAlbums(self, boxIndex, whatSort):  #whatSort=0 -> by Time
        if boxIndex == 0:
            if whatSort == 0:
                self.sortTimeMostToLeastPA = not self.sortTimeMostToLeastPA
                self.possibleAlbums.sort(key=lambda album: album.length,
                                         reverse=self.sortTimeMostToLeastPA)
            else:
                self.sortPlayCountMostToLeastPA = not self.sortPlayCountMostToLeastPA
                self.possibleAlbums.sort(
                    key=lambda album: album.averagePlayCount,
                    reverse=self.sortPlayCountMostToLeastPA)
            self.writePossibleAlbums()
        else:
            if whatSort == 0:
                self.sortTimeMostToLeastPHA = not self.sortTimeMostToLeastPHA
                self.possibleHalfAlbums.sort(
                    key=lambda album: album.length,
                    reverse=self.sortTimeMostToLeastPHA)
            else:
                self.sortPlayCountMostToLeastPHA = not self.sortPlayCountMostToLeastPHA
                self.possibleHalfAlbums.sort(
                    key=lambda album: album.averagePlayCount,
                    reverse=self.sortPlayCountMostToLeastPHA)
            self.writePossibleHalfAlbums()

    def writePossibleAlbums(self):
        self.scrollWidgetPossibleAlbums.boxes[1].config(state=TK.NORMAL)
        self.scrollWidgetPossibleAlbums.boxes[2].config(state=TK.NORMAL)
        self.scrollWidgetPossibleAlbums.boxes[0].delete(0, TK.END)
        self.scrollWidgetPossibleAlbums.boxes[1].delete("1.0", TK.END)
        self.scrollWidgetPossibleAlbums.boxes[2].delete("1.0", TK.END)
        for index in range(len(self.possibleAlbums)):
            album = self.possibleAlbums[index]
            self.scrollWidgetPossibleAlbums.boxes[0].insert(
                TK.END, album.artist + " - " + album.title)
            self.scrollWidgetPossibleAlbums.boxes[0].itemconfig(
                index,
                fg=Screen.container.genresColors[
                    Screen.container.correctRapGenre(album.genre)],
                selectbackground=Screen.container.genresColors[
                    Screen.container.correctRapGenre(album.genre)])
            self.scrollWidgetPossibleAlbums.boxes[1].insert(
                TK.END,
                Screen.container.standardFormatTime(album.length) + "\n",
                Screen.container.correctRapGenre(album.genre))
            self.scrollWidgetPossibleAlbums.boxes[2].insert(
                TK.END,
                str(round(album.averagePlayCount, 3)) + "\n",
                Screen.container.correctRapGenre(album.genre))
        self.scrollWidgetPossibleAlbums.boxes[1].delete(
            "end-1c linestart", TK.END)
        self.scrollWidgetPossibleAlbums.boxes[1].config(state=TK.DISABLED)
        self.scrollWidgetPossibleAlbums.boxes[2].delete(
            "end-1c linestart", TK.END)
        self.scrollWidgetPossibleAlbums.boxes[2].config(state=TK.DISABLED)

    def writePossibleHalfAlbums(self):
        self.scrollWidgetPossibleHalfAlbums.boxes[1].config(state=TK.NORMAL)
        self.scrollWidgetPossibleHalfAlbums.boxes[2].config(state=TK.NORMAL)
        self.scrollWidgetPossibleHalfAlbums.boxes[0].delete(0, TK.END)
        self.scrollWidgetPossibleHalfAlbums.boxes[1].delete("1.0", TK.END)
        self.scrollWidgetPossibleHalfAlbums.boxes[2].delete("1.0", TK.END)
        for index in range(len(self.possibleHalfAlbums)):
            album = self.possibleHalfAlbums[index]
            self.scrollWidgetPossibleHalfAlbums.boxes[0].insert(
                TK.END, album.artist + " - " + album.title)
            self.scrollWidgetPossibleHalfAlbums.boxes[0].itemconfig(
                index,
                fg=Screen.container.genresColors[
                    Screen.container.correctRapGenre(album.genre)],
                selectbackground=Screen.container.genresColors[
                    Screen.container.correctRapGenre(album.genre)])
            self.scrollWidgetPossibleHalfAlbums.boxes[1].insert(
                TK.END,
                Screen.container.standardFormatTime(album.length) + "\n",
                Screen.container.correctRapGenre(album.genre))
            self.scrollWidgetPossibleHalfAlbums.boxes[2].insert(
                TK.END,
                str(round(album.averagePlayCount, 3)) + "\n",
                Screen.container.correctRapGenre(album.genre))
        self.scrollWidgetPossibleHalfAlbums.boxes[1].delete(
            "end-1c linestart", TK.END)
        self.scrollWidgetPossibleHalfAlbums.boxes[1].config(state=TK.DISABLED)
        self.scrollWidgetPossibleHalfAlbums.boxes[2].delete(
            "end-1c linestart", TK.END)
        self.scrollWidgetPossibleHalfAlbums.boxes[2].config(state=TK.DISABLED)

    def getAlbum(self, time, maxLeeway, over, under):
        listPossibleAlbums = []
        listPossibleHalfAlbums = []
        leeway = 60
        underTime = 0
        overTime = 0
        while leeway <= maxLeeway:
            underTime = time - leeway * int(under)
            overTime = time + leeway * int(over)
            for album in Screen.container.listAlbums:
                lengthOfAlbum = album.length
                genreOfAlbum = Screen.container.correctRapGenre(album.genre)
                if genreOfAlbum in self.genresOfAlbums:
                    if lengthOfAlbum >= underTime and lengthOfAlbum <= overTime and album not in listPossibleAlbums:
                        listPossibleAlbums.append(album)
                        if album in listPossibleHalfAlbums:
                            listPossibleHalfAlbums.remove(album)
                    elif lengthOfAlbum / 2 >= underTime and lengthOfAlbum / 2 <= overTime and album not in listPossibleHalfAlbums and album not in listPossibleAlbums:
                        listPossibleHalfAlbums.append(album)
            leeway += 60
        return [listPossibleAlbums, listPossibleHalfAlbums]

    def nextScreen(self, event=None):
        try:
            albumSelected = self.scrollWidgetPossibleAlbums.boxes[0].get(
                self.scrollWidgetPossibleAlbums.boxes[0].curselection())
            ShowAlbumTracklistScreen(albumSelected, self.frm_master, self)
        except TK.TclError:
            try:
                albumSelected = self.scrollWidgetPossibleHalfAlbums.boxes[
                    0].get(self.scrollWidgetPossibleHalfAlbums.boxes[0].
                           curselection())
                ShowAlbumTracklistScreen(albumSelected, self.frm_master, self)
            except TK.TclError:
                pass  #TODO: make TK.Label warning informing user

    def backScreen(self, event=None):
        ChooseAlbumScreen(self.frm_master)


class ShowAlbumTracklistScreen(Screen):
    def __init__(self, albumSelected, masterFramePreviousScreen,
                 previousScreen):
        super().__init__(masterFramePreviousScreen)
        #Determine selected Album
        self.previousScreen = previousScreen
        self.albumArtist = albumSelected[:albumSelected.find(" - ")]
        self.albumTitle = albumSelected[albumSelected.find(" - ") + 3:].strip()
        for album in Screen.container.listAlbums:
            if album.artist == self.albumArtist and album.title == self.albumTitle:
                self.albumSelected = album
                break
        lenAlbum = 0
        for disc in self.albumSelected.tracksByDiscs:
            lenAlbum += len(disc)

        #Widget Creation
        self.lbl_title.config(text="This is the tracklist of " +
                              self.albumTitle)
        #NO SCROLLABLE WIDGET
        self.txt_tracklist = TK.Text(self.frm_master,
                                     fg="white",
                                     bg=Screen.DEFAULT_BGCOLOR,
                                     font=Screen.DEFAULT_FONT3,
                                     height=lenAlbum)
        self.lbl_length = TK.Label(
            self.frm_master,
            text=("Length: " +
                  Screen.container.standardFormatTime(album.length) +
                  " minutes"),
            bg=Screen.DEFAULT_BGCOLOR,
            fg="white",
            font=Screen.DEFAULT_FONT1)

        #Widget Placement
        self.lbl_title.grid(row=0, column=1)
        self.btn_backScreen.grid(row=2, column=0)
        self.txt_tracklist.grid(row=1, column=1)
        self.lbl_length.grid(row=2, column=1)

        #Display Album's Tracklist
        maxPreviousDisc = 0
        for disc in self.albumSelected.tracksByDiscs:
            for track in disc:
                self.txt_tracklist.insert(
                    TK.END,
                    str(track.trackNumber + maxPreviousDisc) + ". " +
                    track.title + "\n")
            if len(disc) > 0:
                maxPreviousDisc += disc[len(disc) - 1].trackNumber
        self.txt_tracklist.delete("end-1c linestart", TK.END)
        self.txt_tracklist.config(state=TK.DISABLED)

    def backScreen(self, event=None):
        ListAlbumScreen(self.frm_master, self.previousScreen.time,
                        self.previousScreen.leeway,
                        self.previousScreen.overUnderLeeway,
                        self.previousScreen.previousScreen)


if __name__ == "__main__":
    Screen.window.title("Handler")
    Screen.window.iconbitmap(
        os.path.join(Screen.container.baseDirectory, "auxFiles",
                     "icons8-music-32.ico"))
    Screen.window.configure(bg=Screen.DEFAULT_BGCOLOR)
    if Screen.container.newFilesFound:
        Screen.window.after(50, lambda x=TK.Frame(): newFilesFoundScreen(x))
    else:
        InitialScreen(TK.Frame())
    Screen.window.mainloop()