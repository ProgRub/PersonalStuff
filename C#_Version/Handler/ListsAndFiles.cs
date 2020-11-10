using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
using System.Xml;
using System.Xml.Linq;
using iTunesLib;
using Microsoft.VisualBasic.FileIO;

namespace Handler
{
    public class ListsAndFiles
    {
        public string DownloadsDirectory { get; set; }
        public string MusicOriginDirectory { get; set; }
        public string MusicDestinyDirectory { get; set; }
        public string CurrentDirectory { get; }

        public List<MusicFile> MusicFiles;
        public List<List<string>> SongsToSkip;
        public List<Album> Albums;
        public Dictionary<List<string>, List<string>> ExceptionsReplacements;
        public Dictionary<string, string> UrlReplacements;
        public List<string> GrimeArtists, Files;
        public Dictionary<string, Color> GenresColors;
        public Dictionary<string, List<int>> WorkoutDatabase;
        private readonly string DetailsFile, SongsFile, ExceptionsFile;
        private int NumberOfFilesFromFile;
        private double LastModifiedTimeFromFile;
        private long LastModifiedTime;
        public iTunesApp iTunes { get; }
        public IITLibraryPlaylist iTunesLibrary { get; }
        private const int NUMBER_OF_THREADS = 15;

        public ListsAndFiles()
        {
            this.CurrentDirectory = Directory.GetCurrentDirectory();
            this.DetailsFile = Path.Combine(this.CurrentDirectory, "auxFiles", "OtherDetails.xml");
            this.SongsFile = Path.Combine(this.CurrentDirectory, "auxFiles", "MusicFiles.xml");
            this.ExceptionsFile = Path.Combine(this.CurrentDirectory, "auxFiles", "YearLyricsExceptions.xml");
            this.DownloadsDirectory = null;
            this.MusicOriginDirectory = null;
            this.MusicDestinyDirectory = null;
            this.ExceptionsReplacements = new Dictionary<List<string>, List<string>>();
            this.UrlReplacements = new Dictionary<string, string>();
            this.SongsToSkip = new List<List<string>>();
            this.GrimeArtists = new List<string>();
            this.GenresColors = new Dictionary<string, Color>();
            this.WorkoutDatabase = new Dictionary<string, List<int>>();
            this.MusicFiles = new List<MusicFile>();
            this.Albums = new List<Album>();
            this.GetAllFromFiles();
            this.iTunes = new iTunesApp();
            this.iTunesLibrary = this.iTunes.LibraryPlaylist;
            BackgroundWorker worker = new BackgroundWorker();
            worker.DoWork += new DoWorkEventHandler(this.CheckMusicFilesAndUpdatePlayCounts);
            worker.RunWorkerAsync();
            //BackgroundWorker updatePC = new BackgroundWorker();
            //updatePC.DoWork += new DoWorkEventHandler(this.UpdatePlayCounts);
            //updatePC.RunWorkerAsync();
        }

        //public string RemoveWordsFromWord(List<string> setOfWords, string wordPar)
        //{
        //    string word = wordPar;
        //    if (word.Contains("(") || word.Contains("["))
        //    {
        //        for (int index = 0; index < setOfWords.Count; index++)
        //        {
        //            bool inRoundParenthesis = true;
        //            string wordToRemove = setOfWords[index];
        //            int startParenthesisPosition = -1;
        //            int endParenthesisPosition = -1;
        //            while (word.Contains(wordToRemove))
        //            {
        //                if (inRoundParenthesis)
        //                {
        //                    startParenthesisPosition = word.IndexOf("(");
        //                    endParenthesisPosition = word.IndexOf(")");
        //                }
        //                if (!inRoundParenthesis || startParenthesisPosition == -1)
        //                {
        //                    startParenthesisPosition = word.IndexOf("[");
        //                    endParenthesisPosition = word.IndexOf("]");
        //                }
        //                Console.WriteLine(word.Substring(startParenthesisPosition, endParenthesisPosition - startParenthesisPosition + 1));
        //                if (word.Substring(startParenthesisPosition, endParenthesisPosition - startParenthesisPosition + 1).Contains(wordToRemove))
        //                {
        //                    word = this.RemoveWordsFromWord(setOfWords, word.Remove(startParenthesisPosition - 1, endParenthesisPosition - startParenthesisPosition + 2));
        //                }
        //                else
        //                {
        //                    if (!inRoundParenthesis)
        //                    {
        //                        if (word.Contains("("))
        //                        {
        //                            word = word.Replace(word.Substring(word.IndexOf(")") + 1), this.RemoveWordsFromWord(setOfWords, word.Substring(word.IndexOf(")") + 1)));
        //                        }
        //                        if (word.Contains("["))
        //                        {
        //                            word = word.Replace(word.Substring(word.IndexOf("]") + 1), this.RemoveWordsFromWord(setOfWords, word.Substring(word.IndexOf("]") + 1)));
        //                        }
        //                    }
        //                    inRoundParenthesis = false;
        //                }
        //            }
        //        }
        //    }
        //    return word.Trim();
        //}

        //public void TagChanges(string filename)
        //{
        //    using (var mp3 = TagLib.File.Create(filename))
        //    {
        //        mp3.Tag.Album = this.RemoveWordsFromWord(new List<string>() { "Remaster", "Anniversary", "Deluxe", "Expanded" }, mp3.Tag.Album);
        //        mp3.Tag.Title = this.RemoveWordsFromWord(new List<string>() { "Remaster", "Album Version", "Stereo", "Hidden Track", "Explicit",
        //    "explicit" }, mp3.Tag.Title);
        //        mp3.Tag.Title = mp3.Tag.Title.Replace("f*ck", "fuck").Replace(
        //        "f***",
        //        "fuck").Replace("f**k", "fuck").Replace("sh*t", "shit").Replace(
        //            "s**t", "shit").Replace("sh**", "shit").Replace(
        //                "ni**as", "niggas").Replace("F*ck", "Fuck").Replace(
        //                    "F**k", "Fuck").Replace("F***", "Fuck").Replace(
        //                        "Sh*t", "Shit").Replace("S**t", "Shit").Replace(
        //                            "Sh**", "Shit").Replace("Ni**as", "Niggas");
        //        if (mp3.Tag.AlbumArtists[0].Contains("King Gizzard"))
        //        {
        //            mp3.Tag.Performers[0] = mp3.Tag.Performers[0].Replace("And", "&");
        //            mp3.Tag.AlbumArtists[0] = mp3.Tag.AlbumArtists[0].Replace("And", "&");
        //        }
        //        else if (mp3.Tag.AlbumArtists[0].Contains("&") && mp3.Tag.Album != "Without Warning" && !mp3.Tag.AlbumArtists[0].Contains(" Mayall "))
        //        {
        //            mp3.Tag.AlbumArtists[0] = mp3.Tag.AlbumArtists[0].Split(new string[] { " & " }, StringSplitOptions.None)[0];
        //        }
        //        else if (mp3.Tag.Album == "Without Warning")
        //        {
        //            mp3.Tag.AlbumArtists[0] = "21 Savage, Offset & Metro Boomin";
        //        }
        //        if (mp3.Tag.AlbumArtists.Length > 1)
        //        {
        //            mp3.Tag.AlbumArtists = new string[] { mp3.Tag.AlbumArtists[0] };
        //        }
        //        else if (mp3.Tag.AlbumArtists[0].Contains("/"))
        //        {
        //            mp3.Tag.AlbumArtists[0] = mp3.Tag.AlbumArtists[0].Substring(0, mp3.Tag.AlbumArtists[0].IndexOf("/"));
        //        }
        //        if (mp3.Tag.Performers.Length > 1)
        //        {
        //            mp3.Tag.Performers = new string[] { string.Join(", ", mp3.Tag.Performers) };
        //        }
        //        else if (mp3.Tag.Performers[0].Contains("/"))
        //        {
        //            mp3.Tag.Performers[0] = mp3.Tag.Performers[0].Substring(0, mp3.Tag.Performers[0].IndexOf("/"));
        //        }
        //        if (this.GrimeArtists.Contains(mp3.Tag.AlbumArtists[0]))
        //        {
        //            mp3.Tag.Genres[0] = "Grime";
        //        }
        //        else if (mp3.Tag.Genres[0].Contains("Electro"))
        //        {
        //            mp3.Tag.Genres[0] = "Electro";
        //        }
        //        else if (mp3.Tag.Genres[0].Contains("Rock"))
        //        {
        //            mp3.Tag.Genres[0] = "Rock";
        //        }
        //        else if (mp3.Tag.Genres[0].Contains("Rap"))
        //        {
        //            mp3.Tag.Genres = new string[] { "Hip Hop" };
        //        }
        //        else if (mp3.Tag.Genres[0].Contains("Alternativa"))
        //        {
        //            mp3.Tag.Genres[0] = "Alternative";
        //        }
        //        mp3.Save();
        //    }
        //}

        public long GetLastModifiedTime()
        {
            var files = Directory.EnumerateFiles(this.MusicDestinyDirectory).Where(file => file.EndsWith(".mp3")).ToList();
            files = files.OrderBy(x => File.GetLastWriteTime(x).ToFileTime()).ToList();
            try
            {
                return File.GetLastWriteTime(files[0]).ToFileTime();
            }
            catch (ArgumentOutOfRangeException)
            {
                return -1;
            }
        }

        #region Methods that get from files
        private void GetAllFromFiles()
        {
            this.GetDirectories();
            this.GetNumberFilesLastModified();
            this.GetGenreColors();
            this.GetWorkoutDatabase();
            this.GetGrimeArtists();
            this.GetExceptions();
            this.GetMusicFiles();
        }

        private void GetDirectories()
        {
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            try { this.DownloadsDirectory = xmlDocument.Root.Descendants("Directory").Where(element => element.Attribute("type").Value == "0").ToList()[0].Value; }
            catch (System.ArgumentOutOfRangeException) { this.DownloadsDirectory = null; }
            try { this.MusicOriginDirectory = xmlDocument.Root.Descendants("Directory").Where(element => element.Attribute("type").Value == "1").ToList()[0].Value; }
            catch (System.ArgumentOutOfRangeException) { this.MusicOriginDirectory = null; }
            try { this.MusicDestinyDirectory = xmlDocument.Root.Descendants("Directory").Where(element => element.Attribute("type").Value == "2").ToList()[0].Value; }
            catch (System.ArgumentOutOfRangeException) { this.MusicDestinyDirectory = null; }
        }

        private void GetNumberFilesLastModified()
        {
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            try
            {
                this.NumberOfFilesFromFile = Int32.Parse(xmlDocument.Root.Element("NumberFiles").Value);
                this.LastModifiedTimeFromFile = float.Parse(xmlDocument.Root.Element("LastModified").Value);
            }
            catch (ArgumentOutOfRangeException)
            {
                this.NumberOfFilesFromFile = 0;
                this.LastModifiedTimeFromFile = 0;
            }
        }

        private void GetGenreColors()
        {
            this.GenresColors.Clear();
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            var genreColors = xmlDocument.Root.Element("GenresColors").Elements("Pair").ToList();
            foreach (XElement item in genreColors)
            {
                string genre = item.Attribute("genre").Value;
                string color = item.Attribute("colour").Value;
                this.GenresColors[genre] = Color.FromArgb(Int32.Parse(color));
            }
        }

        private void GetWorkoutDatabase()
        {
            this.WorkoutDatabase.Clear();
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            var workouts = xmlDocument.Root.Elements("Workout").ToList();
            foreach (XElement item in workouts)
            {
                string workoutName = item.Attribute("name").Value;
                var times = new List<int>();
                var timesFile = item.Elements("Time").ToList();
                foreach (XElement timeElement in timesFile)
                {
                    times.Add(Int32.Parse(timeElement.Value));
                }
                this.WorkoutDatabase.Add(workoutName, times);
            }
        }

        private void GetGrimeArtists()
        {
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            var aux = xmlDocument.Root.Elements("Artist").ToList();
            this.GrimeArtists = new List<string>(from artist in aux select artist.Value);
        }

        private void GetExceptions()
        {
            this.UrlReplacements.Clear();
            this.ExceptionsReplacements.Clear();
            this.SongsToSkip.Clear();
            XDocument xmlDocument = XDocument.Load(this.ExceptionsFile);
            var exceptions = xmlDocument.Root.Elements("Exception").ToList();
            foreach (XElement item in exceptions)
            {
                int typeOfException = Int32.Parse(item.Attribute("type").Value);
                if (typeOfException == 0)
                {
                    string oldArtist = item.Element("OldArtist").Value;
                    string oldAlbum = item.Element("OldAlbum").Value;
                    string oldTitle = item.Element("OldTitle").Value;
                    string newArtist = item.Element("NewArtist").Value;
                    string newAlbum = item.Element("NewAlbum").Value;
                    string newTitle = item.Element("NewTitle").Value;
                    this.ExceptionsReplacements[new List<string>() { oldArtist, oldAlbum, oldTitle }] = new List<string>() { newArtist, newAlbum, newTitle };
                }
                else
                {
                    string artist = item.Element("Artist").Value;
                    string album = item.Element("Album").Value;
                    string title = item.Element("Title").Value;
                    this.SongsToSkip.Add(new List<string>() { artist, album, title });
                }
            }
            var urlReplacementsPairs = xmlDocument.Root.Elements("Pair").ToList();
            foreach (XElement item in urlReplacementsPairs)
            {
                string auxOld = item.Element("Old").Value;
                string old = auxOld.Substring(auxOld.IndexOf("\"") + 1, auxOld.LastIndexOf("\"") - auxOld.IndexOf("\"") - 1);
                string auxNew = item.Element("New").Value;
                string replacement = auxNew.Substring(auxNew.IndexOf("\"") + 1, auxNew.LastIndexOf("\"") - auxNew.IndexOf("\"") - 1);
                this.UrlReplacements[old] = replacement;
            }

        }

        private void GetMusicFiles()
        {
            XDocument xmlDocument = XDocument.Load(this.SongsFile);
            foreach (var musicFile in xmlDocument.Root.Elements("MusicFile"))
            {
                MusicFile newSong = new MusicFile(musicFile.Value, musicFile.Attribute("Title").Value,
                musicFile.Attribute("ContributingArtists").Value,
                musicFile.Attribute("AlbumArtist").Value,
                musicFile.Attribute("Album").Value,
                Int32.Parse(musicFile.Attribute("TrackNumber").Value),
                Int32.Parse(musicFile.Attribute("NumberOfTracks").Value),
                Int32.Parse(musicFile.Attribute("DiscNumber").Value),
                Int32.Parse(musicFile.Attribute("NumberOfDiscs").Value),
                musicFile.Attribute("Genre").Value,
                Int32.Parse(musicFile.Attribute("Year").Value),
                Int32.Parse(musicFile.Attribute("Length").Value),
                Int32.Parse(musicFile.Attribute("PlayCount").Value));
                this.MusicFiles.Add(newSong);
            }
        }
        #endregion


        #region Methods that save to files

        public void SaveDirectories()
        {
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            xmlDocument.Root.Elements("Directory").Remove();
            XElement aux = new XElement("Directory", this.DownloadsDirectory);
            aux.SetAttributeValue("type", "0");
            xmlDocument.Root.Add(aux);
            aux = new XElement("Directory", this.MusicOriginDirectory);
            aux.SetAttributeValue("type", "1");
            xmlDocument.Root.Add(aux);
            aux = new XElement("Directory", this.MusicDestinyDirectory);
            aux.SetAttributeValue("type", "2");
            xmlDocument.Root.Add(aux);
            xmlDocument.Save(this.DetailsFile);
        }

        public void SaveNumberFilesLastModified()
        {
            long lastModifiedTime = this.GetLastModifiedTime();
            var files = Directory.EnumerateFiles(this.MusicDestinyDirectory).Where(file => file.EndsWith(".mp3")).ToList();
            int numberFiles = files.Count;
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            try
            {
                xmlDocument.Root.Element("NumberFiles").Value = numberFiles.ToString();
                xmlDocument.Root.Element("LastModified").Value = lastModifiedTime.ToString();
            }
            catch (ArgumentNullException)
            {
                xmlDocument.Root.Add(new XElement("NumberFiles", numberFiles.ToString()));
                xmlDocument.Root.Add(new XElement("LastModified", lastModifiedTime.ToString()));
            }
            xmlDocument.Save(this.DetailsFile);
        }

        public void SaveGenreColors()
        {
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            xmlDocument.Root.Element("GenresColors").Elements().Remove();
            foreach (string genre in this.GenresColors.Keys)
            {
                XElement newPair = new XElement("Pair");
                newPair.SetAttributeValue("genre", genre);
                newPair.SetAttributeValue("colour", this.GenresColors[genre].ToArgb());
                xmlDocument.Root.Element("GenresColors").Add(newPair);
            }
            xmlDocument.Save(this.DetailsFile);
        }

        public void SaveWorkoutDatabase()
        {
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            xmlDocument.Root.Elements("Workout").Remove();
            foreach (string workout in this.WorkoutDatabase.Keys)
            {
                XElement workoutChild = new XElement("Workout");
                workoutChild.SetAttributeValue("name", workout);
                foreach (int time in this.WorkoutDatabase[workout])
                {
                    XElement timeChild = new XElement("Time", time);
                    workoutChild.Add(timeChild);
                }
                xmlDocument.Root.Add(workoutChild);
            }
            xmlDocument.Save(this.DetailsFile);
        }

        public void SaveMusicFiles()
        {
            XDocument xmlDocument = XDocument.Load(this.SongsFile);
            xmlDocument.Root.Elements().Remove();
            foreach (MusicFile musicFile in this.MusicFiles)
            {
                //this.AddMusicFile(filename);
                XElement child = new XElement("MusicFile", musicFile.Filename);
                child.SetAttributeValue("Title", musicFile.Title);
                child.SetAttributeValue("AlbumArtist", musicFile.AlbumArtist);
                child.SetAttributeValue("ContributingArtists", musicFile.ContributingArtists);
                child.SetAttributeValue("Album", musicFile.Album);
                child.SetAttributeValue("TrackNumber", musicFile.TrackNumber);
                child.SetAttributeValue("NumberOfTracks", musicFile.NumberOfTracks);
                child.SetAttributeValue("DiscNumber", musicFile.DiscNumber);
                child.SetAttributeValue("NumberOfDiscs", musicFile.NumberOfDiscs);
                child.SetAttributeValue("Genre", musicFile.Genre);
                child.SetAttributeValue("Year", musicFile.Year);
                child.SetAttributeValue("Length", musicFile.Length);
                child.SetAttributeValue("PlayCount", musicFile.PlayCount);
                xmlDocument.Root.Add(child);
            }
            xmlDocument.Save(this.SongsFile);
        }
        #endregion

        public int IndexOfMusicFile(string filename)
        {
            for (int index = 0; index < this.MusicFiles.Count; index++)
            {
                if (this.MusicFiles[index].Filename == filename)
                {
                    return index;
                }
            }
            return -1;
        }

        private void CheckMusicFilesAndUpdatePlayCounts(object sender, DoWorkEventArgs e)
        {
            var auxList = this.MusicFiles.Select(x => x.Filename).ToList();
            var files = Directory.EnumerateFiles(this.MusicDestinyDirectory).Where(file => file.EndsWith(".mp3")).ToList();
            files = files.Where(x => !auxList.Contains(Path.GetFileName(x))).ToList();
            foreach (string filename in files)
            {
                using (var mp3 = TagLib.File.Create(filename))
                {
                    this.MusicFiles.Add(new MusicFile(Path.GetFileName(filename), mp3.Tag.Title, mp3.Tag.Performers[0], mp3.Tag.AlbumArtists[0], mp3.Tag.Album, (int)mp3.Tag.Track, (int)mp3.Tag.TrackCount, (int)mp3.Tag.Disc, (int)mp3.Tag.DiscCount, mp3.Tag.Genres[0], (int)mp3.Tag.Year, Convert.ToInt32(mp3.Properties.Duration.TotalSeconds), 0));
                    mp3.Save();

                }
            }
            files = Directory.EnumerateFiles(this.MusicDestinyDirectory).Where(file => file.EndsWith(".mp3")).ToList();
            auxList = auxList.Where(x => !files.Contains(Path.Combine(this.MusicDestinyDirectory, x))).ToList();
            foreach (string filename in auxList)
            {
                this.MusicFiles.RemoveAt(this.IndexOfMusicFile(filename));
            }
            this.Files = Directory.EnumerateFiles(this.MusicDestinyDirectory).Where(file => file.EndsWith(".mp3")).ToList();
            this.LastModifiedTime = this.GetLastModifiedTime();
            this.Files = this.Files.Where(x => File.GetLastWriteTime(x).ToFileTime() > this.LastModifiedTime).ToList();
            int filesPerThread = this.Files.Count / NUMBER_OF_THREADS;
            Thread[] threads = new Thread[NUMBER_OF_THREADS + 1];
            for (int i = 0; i < threads.Length; i++)
            {
                threads[i] = new Thread(new ParameterizedThreadStart(UpdateModifiedFiles));
                threads[i].Start(i);
            }
            for (int i = 0; i < threads.Length; ++i)
            {
                threads[i].Join();
            }
            filesPerThread = this.MusicFiles.Count / NUMBER_OF_THREADS;
            threads = new Thread[NUMBER_OF_THREADS + 1];
            for (int i = 0; i < threads.Length; i++)
            {
                threads[i] = new Thread(new ParameterizedThreadStart(UpdatePlayCounts));
                threads[i].Start(i);
            }
            for (int i = 0; i < threads.Length; ++i)
            {
                threads[i].Join();
            }
            this.SaveMusicFiles();
        }

        public int IndexOfAlbumByName(string albumName)
        {
            for (int index = 0; index < this.Albums.Count; index++)
            {
                if (this.Albums[index].Title == albumName)
                {
                    return index;
                }
            }
            return -1;
        }

        public string StandardFormatTime(int time)
        {
            return (time / 60).ToString() + ":" + (time % 60 < 10 ? "0" : "") + (time % 60).ToString();
        }

        public void GenerateAlbums(object sender, DoWorkEventArgs e)
        {
            this.Albums.Clear();
            foreach (MusicFile musicFile in this.MusicFiles)
            {
                int albumIndex = this.IndexOfAlbumByName(musicFile.Album);
                if (albumIndex == -1)
                {
                    if (!this.GenresColors.Keys.Contains(musicFile.Genre))
                    {
                        this.GenresColors[musicFile.Genre] = Color.White;
                    }
                    this.Albums.Add(new Album(musicFile.Album, musicFile.AlbumArtist, musicFile.NumberOfTracks, musicFile.NumberOfDiscs, musicFile.Genre, musicFile.Year));
                    albumIndex = this.Albums.Count - 1;
                }
                this.Albums[albumIndex].AddTrack(musicFile);
            }
            foreach (Album album in this.Albums)
            {
                int totalTracks = 0;
                foreach (var disc in album.TracksByDiscs)
                {
                    totalTracks += disc.Count;
                }
                album.AveragePlayCount = album.AveragePlayCount / totalTracks;
            }
        }

        public IITTrack GetITunesTrack(string title, string album)
        {
            var tracks = this.iTunesLibrary.Search(title, ITPlaylistSearchField.ITPlaylistSearchFieldSongNames);
            if (tracks != null)
            {
                for (int index = 1; index <= tracks.Count; index++)
                {
                    if (tracks[index].Album == album)
                    {
                        return tracks[index];
                    }
                }
            }
            return null;
        }

        private void UpdateModifiedFiles(object arg)
        {
            int start = (int)arg * (this.Files.Count / NUMBER_OF_THREADS);
            int end = Math.Min(((int)arg + 1) * (this.Files.Count / NUMBER_OF_THREADS), this.Files.Count);
            Console.WriteLine(start + " " + end);
            for (int index = start; index < end; index++)
            {
                string filename = this.Files[index];
                using (var mp3 = TagLib.File.Create(filename))
                {
                    int indexMF = this.IndexOfMusicFile(Path.GetFileName(filename));
                    this.MusicFiles[indexMF] = new MusicFile(Path.GetFileName(filename), mp3.Tag.Title, mp3.Tag.Performers[0], mp3.Tag.AlbumArtists[0], mp3.Tag.Album, (int)mp3.Tag.Track, (int)mp3.Tag.TrackCount, (int)mp3.Tag.Disc, (int)mp3.Tag.DiscCount, mp3.Tag.Genres[0], (int)mp3.Tag.Year, (int)mp3.Properties.Duration.TotalSeconds, this.MusicFiles[indexMF].PlayCount);
                    mp3.Save();
                }
            }
        }


        private void UpdatePlayCounts(object arg)
        {
            int start = (int)arg * (this.MusicFiles.Count / NUMBER_OF_THREADS);
            int end = Math.Min(((int)arg + 1) * (this.MusicFiles.Count / NUMBER_OF_THREADS), this.MusicFiles.Count);
            for (int index = start; index < end; index++)
            {
                var track = this.GetITunesTrack(this.MusicFiles[index].Title, this.MusicFiles[index].Album);
                if (track != null)
                {
                    this.MusicFiles[index].PlayCount = track.PlayedCount;
                }
            }
        }

    }
}
