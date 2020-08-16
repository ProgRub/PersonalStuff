import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import xml.etree.ElementTree as ET


class ListsAndFiles:
    def __init__(self):
        # Variables
        self.downloadsDirectory = ""
        self.musicOriginDirectory = ""
        self.musicDestinyDirectory = ""
        self.listMusicFile = []
        self.listAlbums = []
        self.listGenres = []
        self.artistAlbumReplacements = {}
        self.artistTitleReplacements = {}
        self.replacementsDict={}
        self.songsToSkip = []
        self.grimeArtists = []
        self.files = []
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
        self.workoutDatabase = {}
        self.alreadyReadFile = False
        self.baseDirectory = os.path.dirname(__file__)
        self.numberOfFiles = 0
        self.timeOfLastModified = 0
        self.numberOfFilesFile = -1
        self.timeOfLastModifiedFile = -1

        # Create files, if necessary
        self.fileDetails = os.path.join(self.baseDirectory, "auxFiles",
                                        "OtherDetails.xml")
        if not os.path.isfile(self.fileDetails):
            root = ET.Element("root")
            tree = ET.ElementTree(root)
            tree.write(self.fileDetails)
        else:
            self.getDirectories()
            self.files = os.listdir(self.musicDirectory)
            self.files = [
                os.path.join(self.musicDirectory, f) for f in self.files
                if f.endswith(".mp3")
            ]
            self.numberOfFiles = len([
                filename for filename in self.files
                if filename.endswith(".mp3")
            ])
            self.timeOfLastModified = self.getLastModified()
            self.getNumFilesLastModifiedFromFile()
            self.generateGenreColorsFromFile()
        self.newFilesFound = self.numberOfFiles > self.numberOfFilesFile or self.timeOfLastModified > self.timeOfLastModifiedFile
        self.fileMusicFiles = os.path.join(self.baseDirectory, "auxFiles",
                                           "MusicFiles.xml")
        if not os.path.isfile(self.fileMusicFiles):
            root = ET.Element("root")
            tree = ET.ElementTree(root)
            tree.write(self.fileMusicFiles)
            self.numberOfFilesFile = -1
            self.timeOfLastModifiedFile = -1
        self.fileExceptions = os.path.join(Screen.baseDirectory, "auxFiles",
                                           "YearLyricsExceptions.xml")
        if not os.path.isfile(self.fileExceptions):
            root = ET.Element("root")
            tree = ET.ElementTree(root)
            tree.write(self.fileExceptions)
        # self.workoutFile = os.path.join(self.baseDirectory, "auxFiles",
        #                                 "WorkoutDatabase.xml")
        # if not os.path.isfile(self.workoutFile):
        #     root = ET.Element("root")
        #     tree = ET.ElementTree(root)
        #     tree.write(self.workoutFile)
        self.loadWorkoutDatabase()

    def getLastModified(self):
        self.files.sort(key=os.path.getmtime, reverse=True)
        return os.path.getmtime(self.files[0])

    # getters from file and file savers

    def getNumFilesLastModified(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        try:
            self.numberOfFilesFile = int(root.find('numberfiles').text)
            self.timeOfLastModifiedFile = float(root.find('lastmodified').text)
        except:
            self.numberOfFilesFile = 0
            self.timeOfLastModifiedFile = 0

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

    def getDirectories(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        try:
            self.downloadsDirectory = root.find('downloaddir').text
        except:
            self.downloadsDirectory = "SET DOWNLOADS DIRECTORY"
        try:
            self.musicOriginDirectory = root.find('musicorigindir').text
        except:
            self.musicOriginDirectory = "SET THE DIRECTORY WHERE MUSIC FILES GO AFTER DOWNLOAD"
        try:
            self.musicDestinyDirectory = root.find('musicdestinydir').text
        except:
            self.musicDestinyDirectory = "SET THE DIRECTORY WHERE YOU STORE THE MUSIC FILES"

    def saveDirectories(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        try:
            root.find('downloaddir').text = self.downloadsDirectory
        except:
            child = ET.Element('downloaddir')
            child.text = self.downloadsDirectory
            root.append(child)
        try:
            root.find('musicorigindir').text = self.musicOriginDirectory
        except:
            child = ET.Element('musicorigindir')
            child.text = self.musicOriginDirectory
            root.append(child)
        try:
            root.find('musicdestinydir').text = self.musicDestinyDirectory
        except:
            child = ET.Element('musicdestinydir')
            child.text = self.musicDestinyDirectory
            root.append(child)
        tree.write(self.fileDetails)

    def getGenreColors(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        genreColors = tree.find('genreColors')
        if genreColors != None:
            for pair in genreColors:
                genre = pair.get('genre')
                colour = pair.get('colour')
                self.genresColors[genre] = colour

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

    def getWorkoutDatabase(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        workouts = root.findall('workout')
        for workout in workouts:
            times = []
            for time in workout:
                times.append(int(time.text))
            self.workoutDatabase[workout.text] = times

    def saveWorkoutDatabase(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        for child in root.findall("workout"):
            root.remove(child)
        for workout in self.workoutDatabase:
            child = ET.Element('workout')
            child.text = workout
            for timeNumber in self.workoutDatabase[workout]:
                time = ET.Element('time')
                time.text = str(timeNumber)
                child.append(time)
            root.append(child)
        tree.write(self.workoutFile)

    def getGrimeArtists(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        self.grimeArtists = [child.text for child in root.findall("artist")]

    def saveGrimeArtists(self):
        tree = ET.parse(self.fileDetails)
        root = tree.getroot()
        for child in root.findall("artist"):
            root.remove(child)
        for artist in self.grimeArtists:
            child = ET.Element("artist")
            child.text = artist
            root.append(child)
        tree.write(self.fileDetails)

    def getExceptions(self):
        tree = ET.parse(self.fileExceptions)
        root = tree.getroot()
        allExceptions = root.findall("exception")
        for exc in allExceptions:
            excType = int(exc.find("type").text)
            if excType == 0:
                oldArtist = exc.find("oldartist").text
                newArtist = exc.find("newartist").text
                oldAlbum = exc.find("oldalbum").text
                newAlbum = exc.find("newalbum").text
                self.artistAlbumReplacements[(oldArtist, oldAlbum)] = [
                    newArtist, newAlbum
                ]
            elif excType == 1:
                oldArtist = exc.find("oldartist").text
                newArtist = exc.find("newartist").text
                oldTitle = exc.find("oldtitle").text
                newTitle = exc.find("newtitle").text
                self.artistTitleReplacements[(oldArtist, oldTitle)] = [
                    newArtist, newTitle
                ]
            else:
                artist = exc.find("artist").text
                album = exc.find("album").text
                title = exc.find("title").text
                self.songsToSkip.append("\n".join([artist, album, title]))
        for replacementPair in root.findall("pair"):
            old = replacementPair.find("old").text
            new = replacementPair.find("new").text
            if new == None:
                new = ""
            self.replacementsDict[old] = new

    def saveExceptions(self):
        filename = os.path.join(Screen.baseDirectory, "auxFiles",
                                "YearLyricsExceptions.xml")
        tree = ET.parse(filename)
        root = tree.getroot()
        root.clear()
        for exc in self.artistAlbumReplacements:
            child = ET.Element("exception")
            mode = ET.Element("type")
            mode.text = str(0)
            oldArtist = ET.Element("oldartist")
            newArtist = ET.Element("newartist")
            oldAlbum = ET.Element("oldalbum")
            newAlbum = ET.Element("newalbum")
            oldArtist.text = exc[0]
            oldAlbum.text = exc[1]
            newArtist.text = self.artistAlbumReplacements[exc][
                0]
            newAlbum.text = self.artistAlbumReplacements[exc][
                1]
            child.append(mode)
            child.append(oldArtist)
            child.append(oldAlbum)
            child.append(newArtist)
            child.append(newAlbum)
            root.append(child)
        for exc in self.artistTitleReplacements:
            child = ET.Element("exception")
            mode = ET.Element("type")
            mode.text = str(1)
            oldArtist = ET.Element("oldartist")
            newArtist = ET.Element("newartist")
            oldTitle = ET.Element("oldtitle")
            newTitle = ET.Element("newtitle")
            oldArtist.text = exc[0]
            oldTitle.text = exc[1]
            newArtist.text = self.artistTitleReplacements[exc][
                0]
            newTitle.text = self.artistTitleReplacements[exc][
                1]
            child.append(mode)
            child.append(oldArtist)
            child.append(oldTitle)
            child.append(newArtist)
            child.append(newTitle)
            root.append(child)
        for exc in self.songsToSkip:
            child = ET.Element("exception")
            mode = ET.Element("type")
            mode.text = str(2)
            artist = ET.Element("artist")
            album = ET.Element("album")
            title = ET.Element("title")
            auxArray = exc.split("\n")
            artist.text = auxArray[0]
            album.text = auxArray[1]
            title.text = auxArray[2]
            child.append(mode)
            child.append(artist)
            child.append(album)
            child.append(title)
            root.append(child)
        for replacementPair in self.replacementsDict:
            child = ET.Element("pair")
            old = ET.Element("old")
            new = ET.Element("new")
            old.text = replacementPair
            new.text = self.replacementsDict[replacementPair]
            child.append(old)
            child.append(new)
            root.append(child)
        tree.write(filename)

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
                    MusicFile(child.text.strip(),
                              child.find('title').text,
                              child.find('artist').text,
                              child.find('album').text,
                              int(child.find('tracknumber').text),
                              int(child.find('numbertracks').text),
                              int(child.find('discnumber').text),
                              int(child.find('numberdiscs').text),
                              child.find('genre').text,
                              int(child.find('year').text),
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
            if os.path.join(self.musicDirectory,
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
