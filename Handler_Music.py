import sys
import os
import tkinter as TK
import tkinter.filedialog as filedialog
import tkinter.colorchooser as colorchooser
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import xml.etree.ElementTree as ET

DEFAULT_FONT1 = ("Times New Roman", 16)
DEFAULT_FONT2 = ("Times New Roman", 14)
DEFAULT_FONT3 = ("Times New Roman", 12)
DEFAULT_BGCOLOR = "#061130"
SCROLLSPEED = 30  #less=faster

#TODO: create search screen, with key listeners
#TODO: comment the code

class MusicFile:
    def __init__(self, filename, title, albumArtist, album, trackNumber,
                 numberOfTracks, discNumber, numberOfDiscs, genre, year,
                 length):
        self.filename = filename
        self.title = title
        self.albumArtist = albumArtist
        self.album = album
        self.trackNumber = trackNumber
        self.numberOfTracks = numberOfTracks
        self.discNumber = discNumber
        self.numberOfDiscs = numberOfDiscs
        self.genre = genre
        self.year = year
        self.length = length


class Album:
    def __init__(self, albumTitle, albumArtist, numberOfTracks, numberOfDiscs,
                 genre, year):
        self.title = albumTitle
        self.artist = albumArtist
        self.numberOfTracks = numberOfTracks
        self.numberOfDiscs = numberOfDiscs
        self.genre = genre
        self.year = year
        self.tracksByDiscs = []
        for _ in range(numberOfDiscs):
            self.tracksByDiscs.append([])
        self.length = 0.0

    def addTrack(self, track: MusicFile):
        self.tracksByDiscs[track.discNumber - 1].append(track)
        for index in range(
                len(self.tracksByDiscs[track.discNumber - 1]) - 1, 0, -1):
            if self.tracksByDiscs[track.discNumber -
                                  1][index].trackNumber < self.tracksByDiscs[
                                      track.discNumber - 1][index -
                                                            1].trackNumber:
                aux = self.tracksByDiscs[track.discNumber - 1][index - 1]
                self.tracksByDiscs[track.discNumber -
                                   1][index -
                                      1] = self.tracksByDiscs[track.discNumber
                                                              - 1][index]
                self.tracksByDiscs[track.discNumber - 1][index] = aux
            else:
                break
        self.length += track.length


class ListsAndFiles:
    def __init__(self):
        self.listMusicFile = []
        self.listAlbums = []
        self.listGenres = []
        self.fileMusicFiles = os.path.join(os.path.dirname(__file__), "auxFiles",
                                           "MusicFiles.xml")
        if not os.path.isfile(self.fileMusicFiles):
            aux = open(self.fileMusicFiles, "w", encoding="utf-8")
            aux.close()
        self.fileDetails = os.path.join(os.path.dirname(__file__), "auxFiles",
                                        "DetailsMusic.xml")
        if not os.path.isfile(self.fileDetails):
            aux = open(self.fileDetails, "w", encoding="utf-8")
            aux.close()
        self.workoutFile = os.path.join(os.path.dirname(__file__), "auxFiles",
                                        "WorkoutDatabase.xml")
        if not os.path.isfile(self.workoutFile):
            aux = open(self.workoutFile, "w", encoding="utf-8")
            aux.close()
        self.musicDirectory = self.getMusicDirectory()
        self.files = os.listdir(self.musicDirectory)
        self.files = [
            os.path.join(self.musicDirectory, f) for f in self.files
            if f.endswith(".mp3")
        ]
        self.genresColors = {}
        # self.genresColors = {
        #     "Grime": "red",
        #     "Rock": "yellow",
        #     "Rap": "blue",  #/Hip Hop
        #     "Alternative": "dark green",
        #     "Pop": "pink",
        #     "Electro": "ivory4",
        #     "Metal": "black",
        #     "R&B": "purple"
        # }
        self.generateGenreColorsFromFile()
        self.alreadyReadFile = False
        self.numberOfFiles = self.getNumFiles()
        self.timeOfLastModified = self.getLastModified()
        self.numberOfFilesFile = -1
        self.timeOfLastModifiedFile = -1
        self.getNumFilesLastModifiedFromFile()
        self.newFilesFound = self.numberOfFiles > self.numberOfFilesFile or self.timeOfLastModified > self.timeOfLastModifiedFile
        self.workoutDatabase = {}
        self.loadWorkoutDatabase()

    def getNumFiles(self):
        return len(
            [filename for filename in self.files if filename.endswith(".mp3")])

    def getLastModified(self):
        self.files.sort(key=os.path.getmtime, reverse=True)
        return os.path.getmtime(self.files[0])

    def getNumFilesLastModifiedFromFile(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        self.numberOfFilesFile = int(root.find('numberfiles').text)
        self.timeOfLastModifiedFile = float(root.find('lastmodified').text)

    def saveNumFilesLastModified(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        try:
            root.find('numberfiles').text = str(self.numberOfFiles)
            root.find('lastmodified').text = str(self.timeOfLastModified)
        except:
            child = ET.Element('numberfiles')
            child.text = str(self.numberOfFiles)
            root.append(child)
            child = ET.Element('lastmodified')
            child.text = str(self.timeOfLastModified)
            root.append(child)
        tree.write(self.fileDetails)

    def getMusicDirectory(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        return root.find('directory').text

    def saveMusicDirectory(self, newDirectory):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        try:
            root.find('directory').text = newDirectory
        except:
            child = ET.Element('directory')
            child.text = newDirectory
            root.append(child)
        tree.write(self.fileDetails)

    def generateGenreColorsFromFile(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        genreColors = tree.find('genreColors')
        for pair in genreColors:
            genre = pair.get('genre')
            colour = pair.get('colour')
            self.genresColors[genre] = colour
        tree.write(self.fileDetails)

    def saveGenreColors(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        try:
            genreColors = tree.find('genreColors')
            genreColors.clear()
        except:
            genreColors = ET.Element('genreColors')
            root.append(genreColors)
        for genre in self.genresColors:
            pair = ET.Element("pair")
            pair.set('genre', genre)
            pair.set('colour', self.genresColors[genre])
            genreColors.append(pair)
        tree.write(self.fileDetails)

    def loadWorkoutDatabase(self):
        tree = ET.parse(self.workoutFile)
        root = tree.getroot()
        workouts = root.findall('workout')
        for workout in workouts:
            times = []
            for time in workout:
                times.append(int(time.text))
            self.workoutDatabase[workout.text] = times
    def saveWorkoutDatabase(self):
        tree = ET.parse(self.workoutFile)
        root = tree.getroot()
        root.clear()
        for workout in self.workoutDatabase:
            child = ET.Element('workout')
            child.text = workout
            for timeNumber in self.workoutDatabase[workout]:
                time = ET.Element('time')
                time.text = str(timeNumber)
                child.append(time)
            root.append(child)
        tree.write(self.workoutFile)

    def indexOf(self, obj):
        for index in range(len(self.listMusicFile)):
            if self.listMusicFile[index].filename == obj.filename:
                return index
        return -1

    def checkFiles(self, screen=None):
        if not self.alreadyReadFile and self.timeOfLastModifiedFile > 0:
            tree = ET.parse(self.fileMusicFiles)
            root = tree.getroot()
            for child in root:
                self.listMusicFile.append(
                    MusicFile(
                        child.text,
                        child.find('title').text,
                        child.find('artist').text,
                        child.find('album').text,
                        int(child.find('tracknumber').text),
                        int(child.find('numbertracks').text),
                        int(child.find('discnumber').text),
                        int(child.find('numberdiscs').text),
                        child.find('genre').text, int(child.find('year').text),
                        float(child.find('length').text)))
            if screen != None:
                self.timeOfLastModified = self.timeOfLastModifiedFile
                self.recalibrateList(screen)
            elif self.numberOfFilesFile > self.numberOfFiles:
                self.deleteFilesFromList()
        else:
            self.timeOfLastModified = self.timeOfLastModifiedFile
            self.recalibrateList(screen)
        self.generateAlbums()
        self.timeOfLastModified = self.getLastModified()
        self.reWriteFiles()
        self.alreadyReadFile = True

    def deleteFilesFromList(self):
        toDelete = []
        for obj in self.listMusicFile:
            if os.path.join(self.musicDirectory +
                            obj.filename) not in self.files:
                toDelete.append(obj)
        for obj in toDelete:
            self.listMusicFile.remove(obj)

    def reWriteFiles(self):
        self.saveNumFilesLastModified()
        self.saveGenreColors()
        tree = ET.parse(self.fileMusicFiles)
        root = tree.getroot()
        root.clear()
        for musicFile in self.listMusicFile:
            child = ET.Element('musicfile')
            elements = [
                ET.Element('title'),
                ET.Element('artist'),
                ET.Element('album'),
                ET.Element('tracknumber'),
                ET.Element('numbertracks'),
                ET.Element('discnumber'),
                ET.Element('numberdiscs'),
                ET.Element('genre'),
                ET.Element('year'),
                ET.Element('length')
            ]
            child.text = musicFile.filename
            elements[0].text = musicFile.title
            elements[1].text = musicFile.albumArtist
            elements[2].text = musicFile.album
            elements[3].text = str(musicFile.trackNumber)
            elements[4].text = str(musicFile.numberOfTracks)
            elements[5].text = str(musicFile.discNumber)
            elements[6].text = str(musicFile.numberOfDiscs)
            elements[7].text = musicFile.genre
            elements[8].text = str(musicFile.year)
            elements[9].text = str(musicFile.length)
            for el in elements:
                child.append(el)
            root.append(child)
        tree.write(self.fileMusicFiles)

    def recalibrateList(self, screen):
        conta = 0
        genre = ""
        album = ""
        title = ""
        albumartist = ""
        year = 0
        tracknumber = 0
        discnumber = 0
        length = 0.0
        for filename in self.files:
            conta += 1
            if filename.endswith(".mp3") and os.path.getmtime(
                    filename) > self.timeOfLastModified:
                mp3 = EasyID3(filename)
                shortFilename = filename.replace(self.musicDirectory + os.sep,
                                                 "")
                genre = mp3["genre"][0]
                album = mp3["album"][0]
                title = mp3["title"][0]
                albumartist = mp3["albumartist"][0]
                year = int(mp3["date"][0])
                tracknumber = mp3["tracknumber"][0]
                discnumber = mp3["discnumber"][0]
                screen.addToOutput(albumartist, album, title, genre, year,
                                   tracknumber, discnumber)
                size = MP3(filename)
                length = float(size.info.length)
                size.save()
                mp3.save()
                aux = MusicFile(shortFilename, title, albumartist, album,
                                int(tracknumber[:tracknumber.find("/")]),
                                int(tracknumber[tracknumber.find("/") + 1:]),
                                int(discnumber[:discnumber.find("/")]),
                                int(discnumber[discnumber.find("/") + 1:]),
                                genre, year, length)
                if self.indexOf(aux) == -1:  # aux not in listMusicFile:
                    self.listMusicFile.append(aux)
                else:
                    self.listMusicFile[self.indexOf(aux)] = aux
            else:
                break

    def findAlbumByName(self, name):
        for index in range(len(self.listAlbums)):
            if name == self.listAlbums[index].title:
                return index
        return -1

    def generateAlbums(self):
        for track in self.listMusicFile:
            indexOfAlbum = self.findAlbumByName(track.album)
            if indexOfAlbum == -1:
                self.listAlbums.append(
                    Album(track.album, track.albumArtist, track.numberOfTracks,
                          track.numberOfDiscs, track.genre, track.year))
                if Screen.correctRapGenre(track.genre) not in self.listGenres:
                    self.listGenres.append(Screen.correctRapGenre(track.genre))
                    if Screen.correctRapGenre(
                            track.genre) not in self.genresColors:
                        self.genresColors[Screen.correctRapGenre(
                            track.genre)] = "black"
            self.listAlbums[indexOfAlbum].addTrack(track)


class Screen:
    container = ListsAndFiles()
    window = TK.Tk()

    def __init__(self, masterFramePreviousScreen):
        masterFramePreviousScreen.destroy()

        #Widget Creation
        self.frm_master = TK.Frame(Screen.window, bg=DEFAULT_BGCOLOR)
        self.btn_backScreen = TK.Button(self.frm_master,
                                        text="Go Back",
                                        command=self.backScreen,
                                        font=DEFAULT_FONT3)

        #Widget Placement
        self.frm_master.grid(row=0, column=0)

        Screen.window.bind("<Return>", self.nextScreen)
        Screen.window.bind('<KP_Enter>', self.nextScreen)
        Screen.window.bind("<Escape>", self.backScreen)

    @staticmethod
    def correctRapGenre(genre):
        return "Rap" if "Rap" in genre else genre

    @staticmethod
    def inverseCorrectRapGenre(genre):
        return "Rap/Hip Hop" if "Rap" in genre else genre

    @staticmethod
    def standardFormatTime(time):
        return str(int(time // 60)) + ":" + ("0" if time % 60 < 10 else
                                             "") + str(int(time % 60))

    @staticmethod
    def generateGenreTags(textBox):
        for genre in Screen.container.genresColors:
            textBox.tag_config(Screen.correctRapGenre(genre),
                               foreground=Screen.container.genresColors[
                                   Screen.correctRapGenre(genre)])

    def backScreen(self, event=None):
        pass

    def nextScreen(self, event=None):
        pass


class InitialScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)

        #Widget Creation
        self.lbl_title = TK.Label(
            self.frm_master,
            text=
            "Welcome to the Music Handler Program!\nYou can search your library for a certain file\nOr choose an album to listen to!",
            font=DEFAULT_FONT1,
            bg=DEFAULT_BGCOLOR,
            fg="white")
        self.frm_whichDirectory = TK.Frame(self.frm_master,
                                           width=750,
                                           height=250,
                                           bg=DEFAULT_BGCOLOR)
        self.lbl_whichDirectory = TK.Label(
            self.frm_whichDirectory,
            text="In which directory do you have your music files?",
            font=DEFAULT_FONT1,
            bg=DEFAULT_BGCOLOR,
            fg="white")
        self.ent_Directory = TK.Entry(self.frm_whichDirectory,
                                      width=60,
                                      state=TK.NORMAL,
                                      font=DEFAULT_FONT3)
        self.ent_Directory.insert(TK.END, str(Screen.container.musicDirectory))
        self.ent_Directory.config(state="readonly")
        self.btn_chooseDirectory = TK.Button(self.frm_whichDirectory,
                                             text="Open",
                                             command=self.chooseDirectory,
                                             font=DEFAULT_FONT3)
        self.btn_advanceScreen = TK.Button(self.frm_master,
                                           text="Choose Album",
                                           command=self.nextScreen,
                                           font=DEFAULT_FONT3)
        self.btn_recalibrateAll = TK.Button(self.frm_master,
                                            text="Recalibrate All Files",
                                            command=self.recalibrateALL,
                                            font=DEFAULT_FONT3)
        self.btn_chooseGenreColors = TK.Button(
            self.frm_master,
            text="Genre Colors",
            command=self.chooseGenreColorsScreen,
            font=DEFAULT_FONT3)
        self.btn_registerWorkout = TK.Button(
            self.frm_master,
            text="Register Workout",
            command=self.registerWorkoutScreen,
            font=DEFAULT_FONT3)

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

    def chooseDirectory(self):
        aux = filedialog.askdirectory(initialdir=os.path.join(
            "C:", os.sep, "Users", "ruben", "Desktop")).replace("/", "\\")
        if aux != "":
            Screen.container.musicDirectory = aux
            Screen.container.saveMusicDirectory(
                Screen.container.musicDirectory)
        self.ent_Directory.config(state=TK.NORMAL)
        self.ent_Directory.delete(0, 'end')
        self.ent_Directory.insert(TK.END, str(Screen.container.musicDirectory))
        self.ent_Directory.config(state="readonly")

    def nextScreen(self, event=None):
        if not Screen.container.newFilesFound:
            Screen.container.checkFiles()
        ChooseAlbumScreen(self.frm_master)

    def recalibrateALL(self):
        Screen.container.timeOfLastModified = Screen.container.timeOfLastModifiedFile = 0
        newFilesFoundScreen(self.frm_master)

    def chooseGenreColorsScreen(self):
        ChooseColorsScreen(self.frm_master)

    def registerWorkoutScreen(self):
        WorkoutRegistryScreen(self.frm_master)


class ChooseColorsScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)

        #Widget Creation
        self.lbl_title = TK.Label(
            self.frm_master,
            text="Click the button of the Genre which color you want to change",
            font=DEFAULT_FONT1,
            bg=DEFAULT_BGCOLOR,
            fg="white")
        i = 1
        Screen.container.generateGenreColorsFromFile()
        self.genreButtons = {}
        self.exampleLabels = {}
        for genre in Screen.container.genresColors:
            btn_genre = TK.Button(
                self.frm_master,
                text=Screen.inverseCorrectRapGenre(genre),
                font=DEFAULT_FONT3,
                command=lambda genre=genre: self.changeColor(genre),
                fg=Screen.container.genresColors[genre])
            lbl_example = TK.Label(self.frm_master,
                                   text="This is an example.",
                                   font=DEFAULT_FONT3,
                                   fg=Screen.container.genresColors[genre],
                                   bg=DEFAULT_BGCOLOR)
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
        InitialScreen(self.frm_master)


class WorkoutRegistryScreen(Screen):
    def __init__(self, masterFramePreviousScreen):
        super().__init__(masterFramePreviousScreen)

        #Tkinter Vars
        self.workoutName = TK.StringVar()
        self.time = TK.StringVar()

        #Widget Creation
        self.lbl_title = TK.Label(
            self.frm_master,
            text=
            "Input the name of the workout and how long it took (format MM:SS)",
            bg=DEFAULT_BGCOLOR,
            fg="white",
            font=DEFAULT_FONT1)
        self.lbl_workoutName = TK.Label(self.frm_master,
                                        text="Name of the Workout",
                                        bg=DEFAULT_BGCOLOR,
                                        fg="white",
                                        font=DEFAULT_FONT2)
        self.lbl_time = TK.Label(self.frm_master,
                                 text="Time to Complete",
                                 bg=DEFAULT_BGCOLOR,
                                 fg="white",
                                 font=DEFAULT_FONT2)
        self.ent_workoutName = TK.Entry(self.frm_master,
                                        textvariable=self.workoutName,
                                        font=DEFAULT_FONT3,
                                        width=30)
        self.ent_time = TK.Entry(self.frm_master,
                                 textvariable=self.time,
                                 font=DEFAULT_FONT3,
                                 width=6)
        self.btn_confirm = TK.Button(self.frm_master,
                                     text="Confirm",
                                     font=DEFAULT_FONT3,
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
        InitialScreen(self.frm_master)
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

        #Widget Creation
        self.lbl_title = TK.Label(self.frm_master,
                                  textvariable=self.auxVar,
                                  font=DEFAULT_FONT1,
                                  bg=DEFAULT_BGCOLOR,
                                  fg="white")
        self.frm_textOutput = TK.Frame(self.frm_master, bg=DEFAULT_BGCOLOR)
        self.scb_textOutput = TK.Scrollbar(self.frm_textOutput,
                                           command=self.scrollTextOutput,
                                           orient=TK.VERTICAL)
        HEIGHT = 35
        categories_width = {
            "Artist": 30,
            "Album": 55,
            "Title": 70,
            "Genre": 12,
            "Year": 5,
            "Track\nN.": 6,
            "Disc\nN.": 6
        }
        self.textBoxes = []
        i = 0
        for category in categories_width:
            lbl_category = TK.Label(self.frm_textOutput,
                                    text=category,
                                    font=DEFAULT_FONT2,
                                    bg=DEFAULT_BGCOLOR,
                                    fg="white")
            txt_category = TK.Text(self.frm_textOutput,
                                   font=DEFAULT_FONT3,
                                   width=categories_width[category],
                                   height=HEIGHT,
                                   bg=DEFAULT_BGCOLOR,
                                   yscrollcommand=self.scb_textOutput.set)
            self.textBoxes.append(txt_category)
            lbl_category.grid(row=0, column=i)
            txt_category.grid(row=1, column=i)
            i += 1
        self.btn_advanceScreen = TK.Button(
            self.frm_master,
            text=("Choose Album"
                  if not Screen.container.newFilesFound else "Exit"),
            font=DEFAULT_FONT3,
            command=self.nextScreen,
            state=TK.DISABLED)

        #Widget Placement
        self.lbl_title.grid(row=0, column=0, padx=200)
        self.frm_textOutput.grid(row=1, column=0)
        self.scb_textOutput.grid(row=1, column=7, sticky=TK.NS)
        self.btn_advanceScreen.grid(row=2, column=0, padx=200)

        #Widget Configuration
        for txt in self.textBoxes:
            txt.bind("<MouseWheel>", self.scrollTextOutputMouseWheel)
            Screen.generateGenreTags(txt)
        Screen.window.update_idletasks()
        Screen.container.checkFiles(self)

        #Delete last newline
        for txt in self.textBoxes:
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

    def scrollTextOutput(self, *args):
        for txt in self.textBoxes:
            txt.yview(*args)

    def scrollTextOutputMouseWheel(self, event):
        for txt in self.textBoxes:
            txt.yview("scroll", -1 * (event.delta // SCROLLSPEED), "units")
        return "break"

    def addToOutput(self, artist, album, title, genre, year, trackNumber,
                    discNumber):
        self.numberOfFilesFound += 1
        self.auxVar.set(
            str(self.numberOfFilesFound) + "/" + str(self.totalNewFiles) +
            " Files Found")
        aux = [artist, album, title, genre, year, trackNumber, discNumber]
        i = 0
        for txt in self.textBoxes:
            txt.config(state=TK.NORMAL)
            txt.insert(TK.END,
                       str(aux[i]) + "\n", Screen.correctRapGenre(genre))
            txt.config(state=TK.DISABLED)
            i += 1
        Screen.window.update_idletasks()
        for txt in self.textBoxes:
            txt.see(TK.END)


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
            bg=DEFAULT_BGCOLOR,
            fg="white",
            font=DEFAULT_FONT1)
        self.lbl_chooseTime = TK.Label(self.frm_master,
                                       text="Time",
                                       bg=DEFAULT_BGCOLOR,
                                       fg="white",
                                       font=DEFAULT_FONT3)
        self.lbl_chooseLeeway = TK.Label(self.frm_master,
                                         text="Leeway",
                                         bg=DEFAULT_BGCOLOR,
                                         fg="white",
                                         font=DEFAULT_FONT3)
        self.ent_chooseTime = TK.Entry(self.frm_master,
                                       textvariable=self.time,
                                       width=30,
                                       font=DEFAULT_FONT3,
                                       validate="key")
        self.ent_chooseLeeway = TK.Entry(self.frm_master,
                                         textvariable=self.leeway,
                                         width=30,
                                         font=DEFAULT_FONT3,
                                         validate="key")
        self.lbl_missingTime = TK.Label(self.frm_master,
                                        text="Insert the time!",
                                        bg=DEFAULT_BGCOLOR,
                                        fg="red",
                                        font=DEFAULT_FONT3)
        self.lbl_missingLeeway = TK.Label(self.frm_master,
                                          text="Insert the leeway!",
                                          bg=DEFAULT_BGCOLOR,
                                          fg="red",
                                          font=DEFAULT_FONT3)
        aux = ["Both", "Over", "Under"]
        for i in range(len(aux)):
            radioButton = TK.Radiobutton(self.frm_master,
                                         text=aux[i],
                                         padx=20,
                                         variable=self.overUnderLeeway,
                                         value=i,
                                         bg=DEFAULT_BGCOLOR,
                                         fg="white",
                                         activebackground=DEFAULT_BGCOLOR,
                                         activeforeground="white",
                                         selectcolor=DEFAULT_BGCOLOR,
                                         font=DEFAULT_FONT3)
            radioButton.grid(row=i + 3, column=1)
        self.btn_selectAllAlbums = TK.Button(self.frm_master,
                                             text="All Albums",
                                             font=DEFAULT_FONT3,
                                             command=self.selectAllAlbums)
        self.btn_forWorkout = TK.Button(self.frm_master,
                                        text="Album For Workout",
                                        font=DEFAULT_FONT3,
                                        command=self.forWorkout)
        self.lbl_chooseWorkout = TK.Label(self.frm_master,
                                          text="Workout Name",
                                          font=DEFAULT_FONT2,
                                          bg=DEFAULT_BGCOLOR,
                                          fg="white")
        self.ent_workoutName = TK.Entry(self.frm_master,
                                        textvariable=self.workoutName,
                                        font=DEFAULT_FONT3,
                                        width=30)
        self.btn_confirmWorkout = TK.Button(self.frm_master,
                                            text="Confirm Workout",
                                            command=self.workoutChosen,
                                            font=DEFAULT_FONT3)
        self.btn_forCar = TK.Button(self.frm_master,
                                    text="Album For Car",
                                    font=DEFAULT_FONT3,
                                    command=self.forCar)
        self.btn_allGenres = TK.Checkbutton(self.frm_master,
                                            text="All genres",
                                            font=DEFAULT_FONT3,
                                            fg="white",
                                            bg=DEFAULT_BGCOLOR,
                                            activebackground=DEFAULT_BGCOLOR,
                                            activeforeground="white",
                                            selectcolor=DEFAULT_BGCOLOR,
                                            command=self.tickAllCheckButtons,
                                            variable=self.selectAllGenres)
        self.btn_listAlbums = TK.Button(self.frm_master,
                                        text="Advance",
                                        font=DEFAULT_FONT3,
                                        command=self.nextScreen)
        i = 8
        self.booleanValsGenres = []
        self.checkButtons = []
        for genre in Screen.container.listGenres:
            var = TK.BooleanVar()
            btn_checkGenre = TK.Checkbutton(
                self.frm_master,
                text=Screen.inverseCorrectRapGenre(genre),
                variable=var,
                fg=Screen.container.genresColors[genre],
                bg=DEFAULT_BGCOLOR,
                activebackground=DEFAULT_BGCOLOR,
                activeforeground=Screen.container.genresColors[genre],
                selectcolor=DEFAULT_BGCOLOR,
                font=DEFAULT_FONT3)
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
        self.lbl_chooseWorkout.grid(row=1, column=2)
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
            leewayMin = average - Screen.container.workoutDatabase[
                workoutName][0] // 60
            leewayMax = average - Screen.container.workoutDatabase[workoutName][
                len(Screen.container.workoutDatabase[workoutName]) - 1] // 60
            self.leeway.set(max(leewayMin, leewayMax))
            self.time.set(average)
        self.workoutName.set("")
        self.lbl_chooseWorkout.grid_forget()
        self.ent_workoutName.grid_forget()
        self.btn_confirmWorkout.grid_forget()
        self.btn_forCar.grid(row=2, column=2)
        self.btn_forWorkout.grid(row=1, column=2)

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

    def nextScreen(self, event=None):
        advance = True
        try:
            self.time.get()
            self.lbl_missingTime.grid_forget()
        except ValueError:
            advance = False
            self.lbl_missingTime.grid(row=1, column=2, padx=25)
        try:
            self.leeway.get()
            self.lbl_missingLeeway.grid_forget()
        except ValueError:
            advance = False
            self.lbl_missingLeeway.grid(row=2, column=2, padx=25)
        if advance:
            ListAlbumScreen(self.frm_master,
                            self.time.get(), self.leeway.get(),
                            self.overUnderLeeway.get(), self)

    def backScreen(self, event=None):
        InitialScreen(self.frm_master)


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
        self.lists[0].sort(key=lambda album: album.length, reverse=True)
        self.lists[1].sort(key=lambda album: album.length, reverse=True)

        #Widget Creation
        self.lbl_titleAlbumsScreen = TK.Label(
            self.frm_master,
            text=("These are the albums whose length varies between " +
                  str(int(self.time -
                          (self.leeway * int(self.under)))) + " and " +
                  str(int(self.time +
                          (self.leeway * int(self.over)))) + " minutes."),
            bg=DEFAULT_BGCOLOR,
            fg="white",
            font=DEFAULT_FONT1)
        self.scb_possibleAlbums = TK.Scrollbar(
            self.frm_master,
            command=self.bothScrollPossibleAlbums,
            orient=TK.VERTICAL)
        self.frm_possibleAlbums = TK.Frame(self.frm_master,
                                           width=600,
                                           height=305,
                                           bd=0)
        self.lbx_possibleAlbums = TK.Listbox(
            self.frm_possibleAlbums,
            font=DEFAULT_FONT3,
            bd=0,
            bg=DEFAULT_BGCOLOR,
            highlightthickness=0,
            selectborderwidth=0,
            yscrollcommand=self.scb_possibleAlbums.set)
        self.txt_possibleAlbumsLengths = TK.Text(
            self.frm_possibleAlbums,
            font=DEFAULT_FONT3,
            width=10,
            spacing3=1,
            bg=DEFAULT_BGCOLOR,
            borderwidth=0,
            yscrollcommand=self.scb_possibleAlbums.set)
        self.lbl_titleHalfAlbumsScreen = TK.Label(
            self.frm_master,
            text=
            ("These are the albums where half of their length varies between "
             + str(int(self.time - (self.leeway * int(self.under)))) +
             " and " + str(int(self.time +
                               (self.leeway * int(self.over)))) + " minutes."),
            bg=DEFAULT_BGCOLOR,
            fg="white",
            font=DEFAULT_FONT1)
        self.frm_PossibleHalfAlbums = TK.Frame(self.frm_master,
                                               width=600,
                                               height=305,
                                               bd=0)
        self.scb_PossibleHalfAlbums = TK.Scrollbar(
            self.frm_master, command=self.bothScrollPossibleHalfAlbums)
        self.lbx_PossibleHalfAlbums = TK.Listbox(
            self.frm_PossibleHalfAlbums,
            font=DEFAULT_FONT3,
            bd=0,
            bg=DEFAULT_BGCOLOR,
            highlightthickness=0,
            selectborderwidth=0,
            yscrollcommand=self.scb_PossibleHalfAlbums.set)
        self.txt_PossibleHalfAlbumsLengths = TK.Text(
            self.frm_PossibleHalfAlbums,
            width=10,
            font=DEFAULT_FONT3,
            spacing3=1,
            bg=DEFAULT_BGCOLOR,
            borderwidth=0,
            yscrollcommand=self.scb_PossibleHalfAlbums.set)
        self.btn_showTracklist = TK.Button(self.frm_master,
                                           text="Show Tracklist",
                                           font=DEFAULT_FONT3,
                                           command=self.nextScreen)
        self.lbl_colorsLabel = TK.Label(self.frm_master,
                                        bg=DEFAULT_BGCOLOR,
                                        fg="white",
                                        text="Colors Label",
                                        font=DEFAULT_FONT1)
        self.cnv_colorsLabel = TK.Canvas(
            self.frm_master,
            bg=DEFAULT_BGCOLOR,
            highlightthickness=0,
            bd=0,
            height=len(Screen.container.genresColors) * 1.5 * 25)
        i = 0
        for genre in Screen.container.genresColors:
            self.cnv_colorsLabel.create_rectangle(
                0,
                i * 25,
                25,
                25 + i * 25,
                fill=Screen.container.genresColors[Screen.correctRapGenre(
                    genre)])
            self.cnv_colorsLabel.create_text(
                35,
                13 + i * 25,
                text=" - " + Screen.inverseCorrectRapGenre(genre),
                fill="white",
                font=DEFAULT_FONT3,
                anchor=TK.W)
            i += 1.5

        #Widget Placement
        self.lbl_titleAlbumsScreen.grid(row=0, column=1)
        self.frm_possibleAlbums.grid(row=1, column=1)
        self.frm_possibleAlbums.grid_propagate(False)
        self.frm_possibleAlbums.rowconfigure(0, weight=2)
        self.frm_possibleAlbums.columnconfigure(0, weight=2)
        self.scb_possibleAlbums.grid(row=1, column=2, sticky=TK.NS)
        self.lbx_possibleAlbums.grid(row=0, column=0, sticky=TK.NSEW)
        self.txt_possibleAlbumsLengths.grid(row=0, column=1, sticky=TK.E)
        self.lbl_titleHalfAlbumsScreen.grid(row=2, column=1)
        self.frm_PossibleHalfAlbums.grid(row=3, column=1)
        self.frm_PossibleHalfAlbums.grid_propagate(False)
        self.frm_PossibleHalfAlbums.rowconfigure(0, weight=1)
        self.frm_PossibleHalfAlbums.columnconfigure(0, weight=1)
        self.scb_PossibleHalfAlbums.grid(sticky=TK.NS, row=3, column=2)
        self.lbx_PossibleHalfAlbums.grid(row=0, column=0, sticky=TK.NSEW)
        self.txt_PossibleHalfAlbumsLengths.grid(row=0, column=1, sticky=TK.E)
        self.btn_showTracklist.grid(row=4, column=4)
        self.lbl_colorsLabel.grid(row=0, column=5)
        self.cnv_colorsLabel.grid(row=1, column=5, rowspan=2)
        self.btn_backScreen.grid(row=4, column=0)

        #Widget Configuration
        Screen.generateGenreTags(self.txt_possibleAlbumsLengths)
        Screen.generateGenreTags(self.txt_PossibleHalfAlbumsLengths)
        for index in range(len(self.lists[0])):
            album = self.lists[0][index]
            self.lbx_possibleAlbums.insert(
                TK.END, album.artist + " - " + album.title + "\n")
            self.txt_possibleAlbumsLengths.insert(
                TK.END,
                Screen.standardFormatTime(album.length) +
                ("\n" if self.lists[0].index(album) != len(self.lists[0]) - 1
                 else ""), Screen.correctRapGenre(album.genre))
            self.lbx_possibleAlbums.itemconfig(
                index,
                fg=Screen.container.genresColors[Screen.correctRapGenre(
                    album.genre)],
                selectbackground=Screen.container.genresColors[
                    Screen.correctRapGenre(album.genre)])
        for index in range(len(self.lists[1])):
            album = self.lists[1][index]
            self.lbx_PossibleHalfAlbums.insert(
                TK.END, album.artist + " - " + album.title + "\n")
            self.txt_PossibleHalfAlbumsLengths.insert(
                TK.END,
                Screen.standardFormatTime(album.length) + "\n",
                Screen.correctRapGenre(album.genre))
            self.lbx_PossibleHalfAlbums.itemconfig(
                index,
                fg=Screen.container.genresColors[Screen.correctRapGenre(
                    album.genre)],
                selectbackground=Screen.container.genresColors[
                    Screen.correctRapGenre(album.genre)])
        self.lbx_possibleAlbums.bind("<MouseWheel>",
                                     self.bothScrollPossibleAlbumsMouseWheel)
        self.txt_possibleAlbumsLengths.bind(
            "<MouseWheel>", self.bothScrollPossibleAlbumsMouseWheel)
        self.lbx_PossibleHalfAlbums.bind(
            "<MouseWheel>", self.bothScrollPossibleHalfAlbumsMouseWheel)
        self.txt_PossibleHalfAlbumsLengths.bind(
            "<MouseWheel>", self.bothScrollPossibleHalfAlbumsMouseWheel)
        self.txt_possibleAlbumsLengths.delete("end-1c linestart", TK.END)
        self.txt_PossibleHalfAlbumsLengths.delete("end-1c linestart", TK.END)
        self.txt_possibleAlbumsLengths.config(state=TK.DISABLED)
        self.txt_PossibleHalfAlbumsLengths.config(state=TK.DISABLED)

    def bothScrollPossibleAlbums(self, *args):
        self.lbx_possibleAlbums.yview(*args)
        self.txt_possibleAlbumsLengths.yview(*args)

    def bothScrollPossibleAlbumsMouseWheel(self, event):
        self.lbx_possibleAlbums.yview("scroll",
                                      -1 * (event.delta // SCROLLSPEED),
                                      "units")
        self.txt_possibleAlbumsLengths.yview("scroll",
                                             -1 * (event.delta // SCROLLSPEED),
                                             "units")
        return "break"

    def bothScrollPossibleHalfAlbums(self, *args):
        self.lbx_PossibleHalfAlbums.yview(*args)
        self.txt_PossibleHalfAlbumsLengths.yview(*args)

    def bothScrollPossibleHalfAlbumsMouseWheel(self, event):
        self.lbx_PossibleHalfAlbums.yview("scroll",
                                          -1 * (event.delta // SCROLLSPEED),
                                          "units")
        self.txt_PossibleHalfAlbumsLengths.yview(
            "scroll", -1 * (event.delta // SCROLLSPEED), "units")
        return "break"

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
                genreOfAlbum = Screen.correctRapGenre(album.genre)
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
            albumSelected = self.lbx_possibleAlbums.get(
                self.lbx_possibleAlbums.curselection())
            ShowAlbumTracklistScreen(albumSelected, self.frm_master, self)
        except TK.TclError:
            try:
                albumSelected = self.lbx_PossibleHalfAlbums.get(
                    self.lbx_PossibleHalfAlbums.curselection())
                ShowAlbumTracklistScreen(albumSelected, self.frm_master, self)
            except TK.TclError:
                pass  #make TK.Label warning informing user

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

        #Widget Creation
        self.lbl_title = TK.Label(self.frm_master,
                                  text=("This is the tracklist of " +
                                        self.albumTitle),
                                  bg=DEFAULT_BGCOLOR,
                                  fg="white",
                                  font=DEFAULT_FONT1)
        self.frm_showTracklist = TK.Frame(self.frm_master,
                                          width=500,
                                          height=300,
                                          bg=DEFAULT_BGCOLOR)
        self.txt_tracklist = TK.Text(self.frm_showTracklist,
                                     fg="white",
                                     bg=DEFAULT_BGCOLOR,
                                     font=DEFAULT_FONT3)
        self.lbl_length = TK.Label(
            self.frm_master,
            text=("Length: " + Screen.standardFormatTime(album.length) +
                  " minutes"),
            bg=DEFAULT_BGCOLOR,
            fg="white",
            font=DEFAULT_FONT1)

        #Widget Placement
        self.lbl_title.grid(row=0, column=1)
        self.btn_backScreen.grid(row=2, column=0)
        self.frm_showTracklist.grid(row=1, column=1)
        self.txt_tracklist.grid(row=0, column=0, sticky=TK.NSEW)
        self.txt_tracklist.rowconfigure(0, weight=1)
        self.txt_tracklist.columnconfigure(0, weight=1)
        self.lbl_length.grid(row=2, column=1)

        #Display Album's Tracklist
        maxPreviousDisc = 0
        for disc in self.albumSelected.tracksByDiscs:
            for track in disc:
                self.txt_tracklist.insert(
                    TK.END,
                    str(track.trackNumber + maxPreviousDisc) + ". " +
                    track.title + "\n")
            maxPreviousDisc += disc[len(disc) - 1].trackNumber

    def backScreen(self, event=None):
        ListAlbumScreen(self.frm_master, self.previousScreen.time,
                        self.previousScreen.leeway,
                        self.previousScreen.overUnderLeeway,
                        self.previousScreen.previousScreen)


if __name__ == "__main__":
    Screen.window.title("Handler")
    Screen.window.iconbitmap(
        os.path.join(os.path.dirname(__file__),
                     "auxFiles", "icons8-music-32.ico"))
    Screen.window.configure(bg=DEFAULT_BGCOLOR)
    if Screen.container.newFilesFound:
        Screen.window.after(50, lambda x=TK.Frame(): newFilesFoundScreen(x))
    else:
        InitialScreen(TK.Frame())
    Screen.window.mainloop()