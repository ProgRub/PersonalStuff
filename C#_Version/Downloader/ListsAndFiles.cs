using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;
using HtmlAgilityPack;
using iTunesLib;

namespace Downloader
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
        public Dictionary<string, string> GenresColors;
        public Dictionary<string, List<int>> WorkoutDatabase;
        private string DetailsFile, SongsFile, ExceptionsFile;
        private int NumberOfFilesFromFile;
        private double LastModifiedTimeFromFile;
        public iTunesApp iTunes { get; }
        public IITLibraryPlaylist iTunesLibrary { get; }

        public ListsAndFiles()
        {
            this.CurrentDirectory = Directory.GetCurrentDirectory();
            this.DetailsFile = Path.Combine(this.CurrentDirectory, "auxFiles", "OtherDetails.xml");
            this.SongsFile = Path.Combine(this.CurrentDirectory, "auxFiles", "MusicFiles.xml");
            this.ExceptionsFile = Path.Combine(this.CurrentDirectory, "auxFiles", "YearLyricsExceptions.xml");
            this.DownloadsDirectory = null;
            this.MusicOriginDirectory = null;
            this.MusicDestinyDirectory = null;
            this.GetDirectories();
            this.MusicFiles = new List<MusicFile>();
            this.Albums = new List<Album>();
            this.ExceptionsReplacements = new Dictionary<List<string>, List<string>>();
            this.UrlReplacements = new Dictionary<string, string>();
            this.SongsToSkip = new List<List<string>>();
            this.GrimeArtists = new List<string>();
            this.Files = new List<string>();
            this.Files = Directory.EnumerateFiles(this.MusicDestinyDirectory).ToList();
            this.GenresColors = new Dictionary<string, string>();
            this.WorkoutDatabase = new Dictionary<string, List<int>>();
            this.iTunes = new iTunesApp();
            this.iTunesLibrary = this.iTunes.LibraryPlaylist;
            this.GetAllFromFiles();
            //var html = new HtmlWeb();
            //var soup = html.Load("https://genius.com/Tiny-meat-gang-sofia-lyrics");

            //foreach (var div in soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "metadata_unit").ToList())
            //{
            //    yearTemp += div.InnerText.Trim();
            //    break;
            //}
            //var year = yearTemp.Split(' ');
            //foreach (var item in year)
            //{
            //Console.WriteLine(item);
            //}
            //var auxList = soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "HeaderMetadata__Section-sc-1p42fnf-2 hAhJBU").ToList();
            //if (auxList.Count != 0)
            //{
            //    foreach (var div in auxList)
            //    {
            //        if (div.InnerText.Contains("Release Date"))
            //        {
            //            var aux = div.InnerText.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            //            foreach (var item in aux)
            //            {
            //                Console.WriteLine(":" + item + ":");
            //            }
            //        }
            //    }
            //    Console.WriteLine("HERE");
            //}
            //else
            //{
            //    auxList = soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "metadata_unit metadata_unit--table_row").ToList();
            //    foreach (var div in auxList)
            //    {
            //        var aux = div.InnerText.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            //        foreach (var item in aux)
            //        {
            //            Console.WriteLine(":" + item.Trim() + ":");
            //        }
            //    }
            //}
        }

        public string RemoveWordsFromWord(List<string> setOfWords, string wordPar)
        {
            string word = wordPar;
            if (word.Contains("(") || word.Contains("["))
            {
                for (int index = 0; index < setOfWords.Count; index++)
                {
                    bool inRoundParenthesis = true;
                    string wordToRemove = setOfWords[index];
                    int startParenthesisPosition = -1;
                    int endParenthesisPosition = -1;
                    while (word.Contains(wordToRemove))
                    {
                        if (inRoundParenthesis)
                        {
                            startParenthesisPosition = word.IndexOf("(");
                            endParenthesisPosition = word.IndexOf(")");
                        }
                        if (!inRoundParenthesis || startParenthesisPosition == -1)
                        {
                            startParenthesisPosition = word.IndexOf("[");
                            endParenthesisPosition = word.IndexOf("]");
                        }
                        Console.WriteLine(word.Substring(startParenthesisPosition, endParenthesisPosition - startParenthesisPosition + 1));
                        if (word.Substring(startParenthesisPosition, endParenthesisPosition - startParenthesisPosition + 1).Contains(wordToRemove))
                        {
                            word = this.RemoveWordsFromWord(setOfWords, word.Remove(startParenthesisPosition - 1, endParenthesisPosition - startParenthesisPosition + 2));
                        }
                        else
                        {
                            if (!inRoundParenthesis)
                            {
                                if (word.Contains("("))
                                {
                                    word = word.Replace(word.Substring(word.IndexOf(")") + 1), this.RemoveWordsFromWord(setOfWords, word.Substring(word.IndexOf(")") + 1)));
                                }
                                if (word.Contains("["))
                                {
                                    word = word.Replace(word.Substring(word.IndexOf("]") + 1), this.RemoveWordsFromWord(setOfWords, word.Substring(word.IndexOf("]") + 1)));
                                }
                            }
                            inRoundParenthesis = false;
                        }
                    }
                }
            }
            return word.Trim();
        }

        public void TagChanges(string filename)
        {
            using (var mp3 = TagLib.File.Create(filename))
            {
                //var mp3 = TagLib.File.Create(filename);
                //Console.WriteLine("[{0}]",string.Join(", ", mp3.Tag.Performers));
                mp3.Tag.Album = this.RemoveWordsFromWord(new List<string>() { "Remaster", "Anniversary", "Deluxe", "Expanded" }, mp3.Tag.Album);
                mp3.Tag.Title = this.RemoveWordsFromWord(new List<string>() { "Remaster", "Album Version", "Stereo", "Hidden Track", "Explicit",
            "explicit" }, mp3.Tag.Title);
                mp3.Tag.Title = mp3.Tag.Title.Replace("f*ck", "fuck").Replace(
                "f***",
                "fuck").Replace("f**k", "fuck").Replace("sh*t", "shit").Replace(
                    "s**t", "shit").Replace("sh**", "shit").Replace(
                        "ni**as", "niggas").Replace("F*ck", "Fuck").Replace(
                            "F**k", "Fuck").Replace("F***", "Fuck").Replace(
                                "Sh*t", "Shit").Replace("S**t", "Shit").Replace(
                                    "Sh**", "Shit").Replace("Ni**as", "Niggas");
                if (mp3.Tag.AlbumArtists[0].Contains("King Gizzard"))
                {
                    mp3.Tag.Performers[0] = mp3.Tag.Performers[0].Replace("And", "&");
                    mp3.Tag.AlbumArtists[0] = mp3.Tag.AlbumArtists[0].Replace("And", "&");
                }
                else if (mp3.Tag.AlbumArtists[0].Contains("&") && mp3.Tag.Album != "Without Warning" && !mp3.Tag.AlbumArtists[0].Contains(" Mayall "))
                {
                    mp3.Tag.AlbumArtists[0] = mp3.Tag.AlbumArtists[0].Split(new string[] { " & " }, StringSplitOptions.None)[0];
                }
                else if (mp3.Tag.Album == "Without Warning")
                {
                    mp3.Tag.AlbumArtists[0] = "21 Savage, Offset & Metro Boomin";
                }
                if (mp3.Tag.AlbumArtists.Length > 1)
                {
                    mp3.Tag.AlbumArtists = new string[] { mp3.Tag.AlbumArtists[0] };
                }
                else if (mp3.Tag.AlbumArtists[0].Contains("/"))
                {
                    mp3.Tag.AlbumArtists[0] = mp3.Tag.AlbumArtists[0].Substring(0, mp3.Tag.AlbumArtists[0].IndexOf("/"));
                }
                if (mp3.Tag.Performers.Length > 1)
                {
                    mp3.Tag.Performers = new string[] { string.Join(", ", mp3.Tag.Performers) };
                }
                else if (mp3.Tag.Performers[0].Contains("/"))
                {
                    mp3.Tag.Performers[0] = mp3.Tag.Performers[0].Substring(0, mp3.Tag.Performers[0].IndexOf("/"));
                }
                if (this.GrimeArtists.Contains(mp3.Tag.AlbumArtists[0]))
                {
                    mp3.Tag.Genres[0] = "Grime";
                }
                else if (mp3.Tag.Genres[0].Contains("Electro"))
                {
                    mp3.Tag.Genres[0] = "Electro";
                }
                else if (mp3.Tag.Genres[0].Contains("Rock"))
                {
                    mp3.Tag.Genres[0] = "Rock";
                }
                else if (mp3.Tag.Genres[0].Contains("Rap"))
                {
                    mp3.Tag.Genres = new string[] { "Hip Hop" };
                }
                else if (mp3.Tag.Genres[0].Contains("Alternativa"))
                {
                    mp3.Tag.Genres[0] = "Alternative";
                }
                mp3.Save();
            }
        }

        public double GetLastModifiedTime()
        {
            this.Files = this.Files.OrderBy(x => File.GetLastWriteTime(x)).ToList();
            try
            {
                return File.GetLastWriteTime(this.Files[0]).ToOADate();
            }
            catch (ArgumentOutOfRangeException)
            {
                return -1;
            }
        }

        private void GetMusicFiles()
        {
            //XDocument xmlDocument = XDocument.Load(this.SongsFile);
            //foreach (var musicFile in xmlDocument.Root.Elements("MusicFile"))
            //{
            //    Console.WriteLine(musicFile.Value);
            //    //musicFile.Attribute("title").Value;
            //    //musicFile.Attribute("albumArtist").Value;
            //    //musicFile.Attribute("contributingArtists").Value;
            //    //musicFile.Attribute("album").Value;
            //    //musicFile.Attribute("tracknumber").Value;
            //    //musicFile.Attribute("numbertracks").Value;
            //    //musicFile.Attribute("discnumber").Value;
            //    //musicFile.Attribute("numberdiscs").Value;
            //    //musicFile.Attribute("genre").Value;
            //    //musicFile.Attribute("year").Value;
            //    //musicFile.Attribute("length").Value;
            //    //musicFile.Attribute("playcount").Value;
            //}
        }

        public void AddMusicFile(string filename)
        {
            using (var mp3 = TagLib.File.Create(filename))
            {
                this.MusicFiles.Add(new MusicFile(filename, mp3.Tag.Title, string.Join("*", mp3.Tag.Performers), mp3.Tag.AlbumArtists[0], mp3.Tag.Album, (int)mp3.Tag.Track, (int)mp3.Tag.TrackCount, (int)mp3.Tag.Disc, (int)mp3.Tag.DiscCount, mp3.Tag.Genres[0], (int)mp3.Tag.Year, Int32.Parse(mp3.Properties.Duration.TotalSeconds.ToString())));
                mp3.Save();            
            }
        }

        public void SaveMusicFiles()
        {
            XDocument xmlDocument = XDocument.Load(this.SongsFile);
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
                this.GenresColors[genre] = color;
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
                    this.ExceptionsReplacements[new List<string>() { oldArtist, oldAlbum, oldTitle }]= new List<string>() { newArtist, newAlbum, newTitle };
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
                this.UrlReplacements[old]= replacement;
            }

        }
        #endregion


        #region Methods that save to files
        public void SaveAllToFiles()
        {
            this.SaveDirectories();
            this.SaveNumberFilesLastModified();
            this.SaveGenreColors();
            this.SaveWorkoutDatabase();
            this.SaveGrimeArtists();
            this.SaveExceptions();
        }
        public void SaveDirectories()
        {
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            xmlDocument.Root.Descendants("Directory").Remove();
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
            double lastModifiedTime = this.GetLastModifiedTime();
            int numberFiles = this.Files.Count;
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
                newPair.SetAttributeValue("colour", this.GenresColors[genre]);
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

        public void SaveGrimeArtists()
        {
            XDocument xmlDocument = XDocument.Load(this.DetailsFile);
            xmlDocument.Root.Elements("Artist").Remove();
            foreach (string artist in this.GrimeArtists)
            {
                xmlDocument.Root.Add(new XElement("Artist", artist));
            }
            xmlDocument.Save(this.DetailsFile);
        }

        public void SaveExceptions()
        {
            XDocument xmlDocument = XDocument.Load(this.ExceptionsFile);
            xmlDocument.Root.Elements().Remove();
            foreach (List<string> key in this.ExceptionsReplacements.Keys)
            {
                XElement child = new XElement("Exception");
                child.SetAttributeValue("type", 0.ToString());
                XElement oldArtist = new XElement("OldArtist", key[0]);
                XElement oldAlbum = new XElement("OldAlbum", key[1]);
                XElement oldTitle = new XElement("OldTitle", key[2]);
                XElement newArtist = new XElement("NewArtist", this.ExceptionsReplacements[key][0]);
                XElement newAlbum = new XElement("NewAlbum", this.ExceptionsReplacements[key][1]);
                XElement newTitle = new XElement("NewTitle", this.ExceptionsReplacements[key][2]);
                child.Add(oldArtist);
                child.Add(oldAlbum);
                child.Add(oldTitle);
                child.Add(newArtist);
                child.Add(newAlbum);
                child.Add(newTitle);
                xmlDocument.Root.Add(child);
            }
            foreach (List<string> song in this.SongsToSkip)
            {
                XElement child = new XElement("Exception");
                child.SetAttributeValue("type", 1.ToString());
                XElement artist = new XElement("Artist", song[0]);
                XElement album = new XElement("Album", song[1]);
                XElement title = new XElement("Title", song[2]);
                child.Add(artist);
                child.Add(album);
                child.Add(title);
                xmlDocument.Root.Add(child);
            }
            foreach (string old in this.UrlReplacements.Keys)
            {
                XElement pair = new XElement("Pair");
                XElement oldChild = new XElement("Old", String.Format("\"{0}\"", old));
                XElement newChild = new XElement("New", String.Format("\"{0}\"", this.UrlReplacements[old]));
                pair.Add(oldChild);
                pair.Add(newChild);
                xmlDocument.Root.Add(pair);
            }
            xmlDocument.Save(this.ExceptionsFile);
        }
        #endregion
    }
}
