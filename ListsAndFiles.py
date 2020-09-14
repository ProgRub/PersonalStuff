#!/usr/bin/env python3.8
import os
import sys
# import threading
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, PCNT
import xml.etree.ElementTree as ET
import win32com.client as win32com
import subprocess
# import pythoncom
"""
    Simple container object that represents a music file
"""


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

    """
        This method allows to get one of the musicFile's properties based on the string whichOne
    """

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
        elif whichOne == "Play Count":
            return self.playCount

    """
        This method allows to set one of the musicFile's properties based on the string whichOne with newAttribute
    """

    def setAttribute(self, whichOne, newAttribute):
        if whichOne == "Artist":
            self.albumArtist = newAttribute
        elif whichOne == "Album":
            self.album = newAttribute
        elif whichOne == "Genre":
            self.genre = newAttribute
        elif whichOne == "Year":
            self.year = newAttribute
        elif whichOne == "Title":
            self.title = newAttribute
        elif whichOne == "Track Number":
            self.trackNumber = newAttribute
        elif whichOne == "Disc Number":
            self.discNumber = newAttribute
        elif whichOne == "Play Count":
            self.playCount = newAttribute

    """
        This method allows to "translate" the string whichOne, that represents the attribute we want, to the correspondent mutagen EasyID3 tag
    """

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


"""
    Simple container object that represents an album
"""


class Album:
    def __init__(self, albumTitle, albumArtist, numberOfTracks, numberOfDiscs,
                 genre, year):
        self.title = albumTitle
        self.artist = albumArtist
        self.numberOfTracks = numberOfTracks
        self.numberOfDiscs = numberOfDiscs
        self.genre = genre
        self.year = year
        self.tracksByDiscs = []  #the track's are divided by their disc number
        for _ in range(self.numberOfDiscs):
            self.tracksByDiscs.append([])
        self.length = 0
        self.averagePlayCount = 0

    """
        Method that allows registering a track to this album and takes care of the reordering based on track number
    """

    def addTrack(self, track: MusicFile):
        self.tracksByDiscs[track.discNumber - 1].append(
            track
        )  #the track's discnumber determines which array of tracks to append to
        for index in range(
                len(self.tracksByDiscs[track.discNumber - 1]) - 1, 0, -1
        ):  #since the appended track is at the end, we start there and make our way backwards, via a sortof bubble sort
            if self.tracksByDiscs[
                    track.discNumber -
                    1][index].trackNumber < self.tracksByDiscs[
                        track.discNumber -
                        1][index -
                           1].trackNumber:  #if the added track's track number is lower than the one on its left, it still isn't in the correct position according to track number we swap it with the one on its left
                aux = self.tracksByDiscs[track.discNumber - 1][index - 1]
                self.tracksByDiscs[track.discNumber -
                                   1][index -
                                      1] = self.tracksByDiscs[track.discNumber
                                                              - 1][index]
                self.tracksByDiscs[track.discNumber - 1][index] = aux
            else:  #if the added track's track number isn't lower than the one on its left, it's (possibly) in the correct position and we don't need to continue going through the list
                break
        self.length += track.length  #add to the length of the album the length of its new track
        self.averagePlayCount += track.playCount  #add to the average play count of the album the new track's play count


class ListsAndFiles:
    def __init__(self):
        # Variables
        self.baseDirectory = os.path.dirname(
            __file__)  #defines the directory in which the file is placed
        if "GitHub" not in self.baseDirectory:
            aux = self.baseDirectory.split(os.sep)
            self.baseDirectory = os.path.join('C:', os.sep,
                                              *aux[1:len(aux) - 1])
        self.recycle = os.path.join(
            self.baseDirectory, "auxFiles", 'Recycle.exe'
        )  #the Recycle utility that recycles a file passed as "parameter"
        while True:
            try:
                self.iTunes = win32com.gencache.EnsureDispatch(
                    "iTunes.Application")  #allows communication with iTunes
                break
            except AttributeError:
                subprocess.run([
                    self.recycle,
                    os.path.join("C:", os.sep, "Users", "ruben", "AppData",
                                 "Local", "Temp", "gen_py", "3.8")
                ]) #weird error, deleting this folder solves the problem with ensure dispatch
        self.iTunesLibrary = self.iTunes.LibraryPlaylist  #the main iTunes Library, where all files are
        # self.thread = threading.Thread(target=self.thread_function,
        #                                daemon=True)
        # self.thread.start()
        self.downloadsDirectory = ""  #the directory where the downloads end up
        self.musicOriginDirectory = ""  # the directory where the download music files end up
        self.musicDestinyDirectory = ""  #the directory where the music is supposed to be stored
        self.listMusicFile = [
        ]  #the list of music files in the musicDestinyDirectory, they're stored to avoid multiple file readings
        self.listAlbums = [
        ]  #the list of all albums based on the music files in listMusicFile
        self.exceptionsReplacements = {
        }  #the dict that represents all "exceptions", this is, files where we need to alter their "properties" (we don't change the tags on the file) to get its year or its lyrics on Genius.com
        self.replacementsDict = {
        }  #the dict that has all the common replacements that need to be made to respect the way genius does its url's
        self.songsToSkip = [
        ]  #a list that represents song's to which Genius doesn't have the lyrics or has them wrong and so we can just skip them
        self.grimeArtists = [
        ]  #a list that represents the grime artists, to change the genre of their music to Grime instead of Rap/Hip-Hop because it's wildly different
        self.files = [
        ]  #a list that represents all mp3 files in the musicDestinyDirectory, different than listMusicFile because it's only used to update the number of files and the date of the last modified file, if we were constantly check the tags of file via mutagen it would be much slower
        self.genresColors = {
        }  # a dict that permits distinguishing the genres by color, the key is the genre and the value is the color with which it should be displayed
        self.workoutDatabase = {
        }  #a dict that permits keeping track of the times of rep based workouts, because the Nike App is no good there and permits getting an approximate time frame to pick an album to listen to while doing said workout
        self.alreadyReadFile = False  #a boolean var that makes sure we're not reading the file constantly
        self.numberOfFiles = 0  #the total number of files in the directory
        self.timeOfLastModified = 0  #the date of last modified file in the directory
        self.numberOfFilesFile = -1  #the total number of files last time this program was run, useful to check if new files have been added
        self.timeOfLastModifiedFile = -1  # the date of last modified file last time this program was run, useful to check if any file's properties have been changed

        # Create directory, if necessary
        if not os.path.isdir(os.path.join(self.baseDirectory, "auxFiles")):
            os.mkdir(os.path.join(self.baseDirectory, "auxFiles"))

        # Create files, if necessary
        self.fileDetails = os.path.join(
            self.baseDirectory, "auxFiles", "OtherDetails.xml"
        )  #the directory of the file in which the minor details like the directories, the workout "database" and the grime artists are
        if not os.path.isfile(
                self.fileDetails
        ):  #this creates the file if it doesn't exist yet
            aux = open(self.fileDetails, "w+")
            aux.close()
            root = ET.Element("root")
            tree = ET.ElementTree(root)
            tree.write(self.fileDetails)
        else:
            self.getDirectories()
            try:
                self.files = os.listdir(
                    self.musicDestinyDirectory
                )  #gets all files in musicDestinyDirectory
                self.files = [
                    os.path.join(self.musicDestinyDirectory, f)
                    for f in self.files if f.endswith(".mp3")
                ]  #reduces to only the mp3's
            except:
                self.files = []
            self.numberOfFiles = len([
                filename for filename in self.files
                if filename.endswith(".mp3")
            ])
            self.timeOfLastModified = self.getLastModified()
            self.getNumFilesLastModified()  #the file versions
            self.getGenreColors()
        self.fileMusicFiles = os.path.join(
            self.baseDirectory, "auxFiles", "MusicFiles.xml"
        )  #the file that contains the details of all music files
        if not os.path.isfile(
                self.fileMusicFiles
        ):  #this creates the file if it doesn't exist yet
            aux = open(self.fileMusicFiles, "w+")
            aux.close()
            root = ET.Element("root")
            tree = ET.ElementTree(root)
            tree.write(self.fileMusicFiles)
            self.numberOfFilesFile = -1
            self.timeOfLastModifiedFile = -1
        self.newFilesFound = self.timeOfLastModified > self.timeOfLastModifiedFile
        self.fileExceptions = os.path.join(
            self.baseDirectory, "auxFiles", "YearLyricsExceptions.xml"
        )  #the file that contains all the "exceptions"
        if not os.path.isfile(
                self.fileExceptions
        ):  #this creates the file if it doesn't exist yet
            aux = open(self.fileExceptions, "w+")
            aux.close()
            root = ET.Element("root")
            tree = ET.ElementTree(root)
            tree.write(self.fileExceptions)
        self.getWorkoutDatabase()
        # self.thread.join()

    """
        Method that returns the date of last modification of the most recently changed file
    """

    def getLastModified(self):
        self.files.sort(key=os.path.getmtime, reverse=True)
        try:
            return os.path.getmtime(self.files[0])
        except:
            return -1

    # methods that gets stuff from files and saves said stuff to the files

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
        self.genresColors.clear()
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
        self.workoutDatabase.clear()
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
        self.grimeArtists.clear()
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
        self.replacementsDict.clear()
        tree = ET.parse(self.fileExceptions)
        root = tree.getroot()
        allExceptions = root.findall("exception")
        for exc in allExceptions:
            excType = int(exc.find("type").text)
            if excType == 0:  #type of exception that changes the attributes of the file to get the year or the lyrics correctly
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
            else:  #type of "exception" that indicates that we don't need to check Genius for the lyrics, either because it doesn't have them or they're working
                artist = exc.find("artist").text
                album = exc.find("album").text
                title = exc.find("title").text
                self.songsToSkip.append([artist, album, title])
        for replacementPair in root.findall(
                "pair"
        ):  #find all the common url replacements and save them to the dictionary
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
            newArtist.text = self.exceptionsReplacements[exc][
                0] if self.exceptionsReplacements[exc][0] != None else ""
            newAlbum.text = self.exceptionsReplacements[exc][
                1] if self.exceptionsReplacements[exc][1] != None else ""
            newTitle.text = self.exceptionsReplacements[exc][
                2] if self.exceptionsReplacements[exc][2] != None else ""
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

    """
        Method that returns the index of the music file with the param filename as their filename, or return -1 if there is none
    """

    def indexOf(self, filename: str):
        for index in range(len(self.listMusicFile)):
            if self.listMusicFile[index].filename == filename:
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
            if self.numberOfFilesFile > self.numberOfFiles:
                self.deleteFilesFromList()
        else:
            self.timeOfLastModified = self.timeOfLastModifiedFile
            self.recalibrateList(screen)
        self.generateAlbums()
        self.timeOfLastModified = self.getLastModified()
        self.reWriteFiles()
        self.alreadyReadFile = True

    """
        Method that removes music files from the list of music files if they're no longer in the directory
    """

    def deleteFilesFromList(self):
        toDelete = []
        for obj in self.listMusicFile:
            if os.path.join(self.musicDestinyDirectory,
                            obj.filename) not in self.files:
                toDelete.append(obj)
        for obj in toDelete:
            self.listMusicFile.remove(obj)

    """
        Method that, as the name indicates, rewrites the files, saving the updated information, the info related to the number of files, the date of last modification, the genre colors and the whole list of music Files
    """

    def reWriteFiles(self):
        self.saveNumFilesLastModified()
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

    """
        Method that takes care of adding the new files to the list or updating the information about recently modificated files
    """

    def recalibrateList(self, screen):
        genre = ""
        album = ""
        title = ""
        albumartist = ""
        year = 0
        tracknumber = 0
        discnumber = 0
        length = 0
        playCount = 0
        for filename in self.files:
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
                mp3.save()
                screen.addToOutput(albumartist, album, title, genre, year,
                                   tracknumber, discnumber)
                track = self.findiTunesTrack(title, album)
                length = track.Duration
                playCount = track.PlayedCount
                if self.indexOf(
                        shortFilename) == -1:  #if it's a new file we create it
                    self.listMusicFile.append(
                        MusicFile(shortFilename, title, albumartist, album,
                                  int(tracknumber[:tracknumber.find("/")]),
                                  int(tracknumber[tracknumber.find("/") + 1:]),
                                  int(discnumber[:discnumber.find("/")]),
                                  int(discnumber[discnumber.find("/") + 1:]),
                                  genre, year, length, playCount))
                else:  #if it isn't a new file, we modify the one in the list to match the updated tags
                    index = self.indexOf(shortFilename)
                    self.listMusicFile[index].title = title
                    self.listMusicFile[index].albumArtist = albumartist
                    self.listMusicFile[index].album = album
                    self.listMusicFile[index].trackNumber = int(
                        tracknumber[:tracknumber.find("/")])
                    self.listMusicFile[index].numberOfTracks = int(
                        tracknumber[tracknumber.find("/") + 1:])
                    self.listMusicFile[index].discNumber = int(
                        discnumber[:discnumber.find("/")])
                    self.listMusicFile[index].numberOfDiscs = int(
                        discnumber[discnumber.find("/") + 1:])
                    self.listMusicFile[index].genre = genre
                    self.listMusicFile[index].year = year
                    self.listMusicFile[index].length = length
                    self.listMusicFile[index].playCount = playCount
            else:
                break
        screen.endOfCheckFiles()

    """
        Simple method that, as the name indicates, allows finding the index of an album by its name
    """

    def findAlbumByName(self, name: str):
        for index in range(len(self.listAlbums)):
            if name == self.listAlbums[index].title:
                return index
        return -1

    """
        Method that allows to find the iTunes version of a track by its title and we pass the album to especify even further the track if there are multiple tracks with said title
    """

    def findiTunesTrack(self, title: str, album: str):
        tracks = self.iTunesLibrary.Search(title, 5)
        try:
            if len(tracks) == 1:
                return tracks.Item(1)
            for track in tracks:
                if track.Album == album:
                    return track
        except:
            pass

    """
        Method that allows updating the play count of file according to its play count on iTunes
    """

    #FIXME: Not updating the file's play count
    def updatePlayCounts(self, screen):
        for track in self.listMusicFile:
            iTunesPlayCount = int(
                self.findiTunesTrack(track.title, track.album).PlayedCount)
            track.playCount = iTunesPlayCount
            screen.addToOutput(track.albumArtist, track.album, track.title,
                               track.playCount)
            audio = ID3(
                os.path.join(self.musicDestinyDirectory, track.filename))
            audio.delall("PCNT")
            audio.add(PCNT(encoding=3, text=str(track.playCount)))
            audio.save()
            # self.iTunesLibrary.AddFile(
            #     os.path.join(self.musicDestinyDirectory, track.filename))
        screen.btn_backScreen.config(state="normal")

    """
        Method that transforms "Rap/Hip Hop" into just "Rap" because it was messing up with the color coding of the genres
    """

    def correctRapGenre(self, genre: str):
        return "Rap" if "Rap" in genre else genre

    """
        Method that does the opposite of the above method, for visual purposes
    """

    def inverseCorrectRapGenre(self, genre: str):
        return "Rap/Hip Hop" if "Rap" in genre else genre

    """
        Utility method that transforms the parameter time (in seconds) to a minutes:seconds format, for visual purposes
    """

    def standardFormatTime(self, time: int):
        return str(int(time // 60)) + ":" + ("0" if time % 60 < 10 else
                                             "") + str(int(time % 60))

    """
        Method that goes through the list of music files and creates the albums, grouping tracks with the same albums and also creates a pair for the genresColors dict, with the default color being white.
        After generating all the albums, we determine their average play count, dividing the play count they have by the number of tracks in the album
    """

    def generateAlbums(self):
        self.listAlbums.clear()
        for track in self.listMusicFile:
            indexOfAlbum = self.findAlbumByName(track.album)
            if indexOfAlbum == -1:
                self.listAlbums.append(
                    Album(track.album, track.albumArtist, track.numberOfTracks,
                          track.numberOfDiscs, track.genre, track.year))
                if self.correctRapGenre(track.genre) not in self.genresColors:
                    self.genresColors[self.correctRapGenre(
                        track.genre)] = "white"
            self.listAlbums[indexOfAlbum].addTrack(track)
        for album in self.listAlbums:
            totalTracks = 0
            for disc in album.tracksByDiscs:
                totalTracks += len(disc)
            album.averagePlayCount = album.averagePlayCount / totalTracks
