import os
# import threading
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import xml.etree.ElementTree as ET
import win32com.client as win32com
# import pythoncom


#TODO: try and implement threading support for iTunes management
class MusicFile:
    def __init__(self, filename, title, albumArtist, album, trackNumber,
                 numberOfTracks, discNumber, numberOfDiscs, genre, year,
                 length, playCount):
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
        self.playCount = playCount

    def getAttribute(self, whichOne):
        if whichOne == "Artist":
            return self.albumArtist
        elif whichOne == "Album":
            return self.album
        elif whichOne == "Genre":
            return self.genre
        elif whichOne == "Year":
            return self.year
        elif whichOne == "Title":
            return self.title
        elif whichOne == "Track Number":
            return self.trackNumber
        elif whichOne == "Disc Number":
            return self.discNumber

    def attributeToMutagenTag(self, whichOne):
        if whichOne == "Artist":
            return "album" + whichOne.lower()
        elif whichOne == "Album":
            return whichOne.lower()
        elif whichOne == "Genre":
            return whichOne.lower()
        elif whichOne == "Year":
            return "date"
        elif whichOne == "Title":
            return whichOne.lower()
        elif whichOne == "Track Number":
            return "tracknumber"
        elif whichOne == "Disc Number":
            return "discnumber"


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
        self.averagePlayCount=0

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
        self.averagePlayCount+=track.playCount


class ListsAndFiles:
    def __init__(self):
        # Variables
        self.iTunes = win32com.gencache.EnsureDispatch("iTunes.Application")
        self.iTunesLibrary = self.iTunes.LibraryPlaylist
        # self.iTunes_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, self.iTunes)
        self.recycle = os.path.join('C:', os.sep, 'Users', 'ruben', 'Desktop',
                                    'Recycle.exe')
        # self.thread = threading.Thread(target=self.thread_function,
        #                                daemon=True)
        # self.thread.start()
        self.downloadsDirectory = ""
        self.musicOriginDirectory = ""
        self.musicDestinyDirectory = ""
        self.listMusicFile = []
        self.listAlbums = []
        self.listGenres = []
        self.exceptionsReplacements = {}
        self.replacementsDict = {}
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
            self.files = os.listdir(self.musicDestinyDirectory)
            self.files = [
                os.path.join(self.musicDestinyDirectory, f) for f in self.files
                if f.endswith(".mp3")
            ]
            self.numberOfFiles = len([
                filename for filename in self.files
                if filename.endswith(".mp3")
            ])
            self.timeOfLastModified = self.getLastModified()
            self.getNumFilesLastModified()
            self.getGenreColors()
        self.newFilesFound = self.numberOfFiles > self.numberOfFilesFile or self.timeOfLastModified > self.timeOfLastModifiedFile
        self.fileMusicFiles = os.path.join(self.baseDirectory, "auxFiles",
                                           "MusicFiles.xml")
        if not os.path.isfile(self.fileMusicFiles):
            root = ET.Element("root")
            tree = ET.ElementTree(root)
            tree.write(self.fileMusicFiles)
            self.numberOfFilesFile = -1
            self.timeOfLastModifiedFile = -1
        self.fileExceptions = os.path.join(self.baseDirectory, "auxFiles",
                                           "YearLyricsExceptions.xml")
        if not os.path.isfile(self.fileExceptions):
            root = ET.Element("root")
            tree = ET.ElementTree(root)
            tree.write(self.fileExceptions)
        self.getWorkoutDatabase()
        # self.thread.join()

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
            self.workoutDatabase[workout.text.strip()] = times

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
        tree.write(self.fileDetails)

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
        self.exceptionsReplacements.clear()
        self.songsToSkip.clear()
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
                oldTitle = exc.find("oldtitle").text
                newTitle = exc.find("newtitle").text
                self.exceptionsReplacements[(oldArtist, oldAlbum,
                                             oldTitle)] = [
                                                 newArtist, newAlbum, newTitle
                                             ]
            else:
                artist = exc.find("artist").text
                album = exc.find("album").text
                title = exc.find("title").text
                self.songsToSkip.append([artist, album, title])
        for replacementPair in root.findall("pair"):
            old = replacementPair.find("old").text
            new = replacementPair.find("new").text
            if new == None:
                new = ""
            self.replacementsDict[old] = new

    def saveExceptions(self):
        filename = os.path.join(self.baseDirectory, "auxFiles",
                                "YearLyricsExceptions.xml")
        tree = ET.parse(filename)
        root = tree.getroot()
        root.clear()
        for exc in self.exceptionsReplacements:
            child = ET.Element("exception")
            mode = ET.Element("type")
            mode.text = str(0)
            oldArtist = ET.Element("oldartist")
            newArtist = ET.Element("newartist")
            oldAlbum = ET.Element("oldalbum")
            newAlbum = ET.Element("newalbum")
            oldTitle = ET.Element("oldtitle")
            newTitle = ET.Element("newtitle")
            oldArtist.text = exc[0]
            oldAlbum.text = exc[1]
            oldTitle.text = exc[2]
            newArtist.text = self.exceptionsReplacements[exc][0] if self.exceptionsReplacements[exc][0]!=None else ""
            newAlbum.text = self.exceptionsReplacements[exc][1]if self.exceptionsReplacements[exc][1]!=None else ""
            newTitle.text = self.exceptionsReplacements[exc][2]if self.exceptionsReplacements[exc][2]!=None else ""
            child.append(mode)
            child.append(oldArtist)
            child.append(oldAlbum)
            child.append(oldTitle)
            child.append(newArtist)
            child.append(newAlbum)
            child.append(newTitle)
            root.append(child)
        for exc in self.songsToSkip:
            child = ET.Element("exception")
            mode = ET.Element("type")
            mode.text = str(1)
            artist = ET.Element("artist")
            album = ET.Element("album")
            title = ET.Element("title")
            artist.text = exc[0]
            album.text = exc[1]
            title.text = exc[2]
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
                              int(child.find('length').text),
                              int(child.find('playcount').text)))
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
            if os.path.join(self.musicDestinyDirectory,
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
                ET.Element('length'),
                ET.Element('playcount')
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
            elements[10].text = str(musicFile.playCount)
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
        length = 0
        playCount = 0
        # self.thread.join()
        for filename in self.files:
            conta += 1
            if filename.endswith(".mp3") and os.path.getmtime(
                    filename) > self.timeOfLastModified:
                mp3 = EasyID3(filename)
                shortFilename = filename.replace(
                    self.musicDestinyDirectory + os.sep, "")
                genre = mp3["genre"][0]
                album = mp3["album"][0]
                title = mp3["title"][0]
                albumartist = mp3["albumartist"][0]
                year = int(mp3["date"][0])
                tracknumber = mp3["tracknumber"][0]
                discnumber = mp3["discnumber"][0]
                screen.addToOutput(albumartist, album, title, genre, year,
                                   tracknumber, discnumber)
                track = self.findiTunesTrack(title, album)
                length = track.Duration
                playCount = track.PlayedCount
                mp3.save()
                aux = MusicFile(shortFilename, title, albumartist, album,
                                int(tracknumber[:tracknumber.find("/")]),
                                int(tracknumber[tracknumber.find("/") + 1:]),
                                int(discnumber[:discnumber.find("/")]),
                                int(discnumber[discnumber.find("/") + 1:]),
                                genre, year, length, playCount)
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

    def findiTunesTrack(self, title, album):
        tracks = self.iTunesLibrary.Search(title, 5)
        if len(tracks) == 1:
            return tracks.Item(1)
        for track in tracks:
            if track.Album == album:
                return track

    def updatePlayCounts(self):
        for track in self.listMusicFile:
            iTunesPlayCount = self.findiTunesTrack(track.title,
                                                   track.album).PlayedCount
            if track.playCount < iTunesPlayCount:
                track.playCount = iTunesPlayCount

    def correctRapGenre(self, genre):
        return "Rap" if "Rap" in genre else genre

    def inverseCorrectRapGenre(self, genre):
        return "Rap/Hip Hop" if "Rap" in genre else genre

    def standardFormatTime(self, time):
        return str(int(time // 60)) + ":" + ("0" if time % 60 < 10 else
                                             "") + str(int(time % 60))

    def generateAlbums(self):
        for track in self.listMusicFile:
            indexOfAlbum = self.findAlbumByName(track.album)
            if indexOfAlbum == -1:
                self.listAlbums.append(
                    Album(track.album, track.albumArtist, track.numberOfTracks,
                          track.numberOfDiscs, track.genre, track.year))
                if self.correctRapGenre(track.genre) not in self.listGenres:
                    self.listGenres.append(self.correctRapGenre(track.genre))
                    if self.correctRapGenre(
                            track.genre) not in self.genresColors:
                        self.genresColors[self.correctRapGenre(
                            track.genre)] = "white"
            self.listAlbums[indexOfAlbum].addTrack(track)
        for album in self.listAlbums:
            totalTracks = 0
            for disc in album.tracksByDiscs:
                totalTracks+=len(disc)
            album.averagePlayCount=album.averagePlayCount/totalTracks
