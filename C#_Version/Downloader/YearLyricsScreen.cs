using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using HtmlAgilityPack;
using System.Media;

namespace Downloader
{
    public partial class YearLyricsScreen : UserControl
    {
        public DownloaderForm Window { get; set; }
        private List<string> NewFiles;
        private Dictionary<string, int> PagesVisited_Year;
        private int NumberFilesProcessed;
        private string CurrentLyrics;
        private bool ExceptionRaised, ErrorHandled, ProgressWorkerDone;
        private List<string> Key;
        private List<string> Value;
        private string Filename;
        private uint TrackCount;
        private BackgroundWorker worker;
        private string CurrentArtist, CurrentAlbum, CurrentTitle, CurrentYear;
        private bool AddFileToList;

        public YearLyricsScreen(DownloaderForm window, List<string> newFiles, bool addFileToList)
        {
            InitializeComponent();
            this.Window = window;
            this.PagesVisited_Year = new Dictionary<string, int>();
            this.NumberFilesProcessed = 0;
            this.ExceptionRaised = false;
            this.Filename = "";
            this.ErrorHandled = true;
            this.ProgressWorkerDone = false;
            this.NewFiles = newFiles;
            this.AddFileToList = addFileToList;
            this.labelFilesProcessed.Text = this.NumberFilesProcessed + "/" + this.NewFiles.Count + " Files Processed";
            this.Window.WindowState = FormWindowState.Maximized;
            this.worker = new BackgroundWorker();
            worker.DoWork += new DoWorkEventHandler(this.GetLyricsAndYear);
            worker.ProgressChanged += new ProgressChangedEventHandler(this.ChangeUI);
            this.worker.WorkerReportsProgress = true;
            this.worker.RunWorkerAsync();
        }
        private void ChangeUI(object sender, ProgressChangedEventArgs e)
        {
            this.ProgressWorkerDone = false;
            switch (e.ProgressPercentage)
            {
                case 0:
                    this.textBoxArtist.Text = this.CurrentArtist;
                    this.textBoxAlbum.Text = this.CurrentAlbum;
                    this.textBoxTitle.Text = this.CurrentTitle;
                    this.textBoxYear.Text = this.CurrentYear;
                    break;
                case 1:
                    this.AddToOutput();
                    break;
                case 2:
                    this.textBoxArtist.Text = this.CurrentArtist;
                    this.textBoxAlbum.Text = this.CurrentAlbum;
                    //this.ChangeOutput(0,true);
                    //this.ChangeOutput(1, true);
                    //self.changeOutput(0, True)
                    //self.changeOutput(1, True)
                    break;
                case 3:
                    this.textBoxArtist.Text = this.CurrentArtist;
                    this.textBoxAlbum.Text = this.CurrentAlbum;
                    this.textBoxTitle.Text = this.CurrentTitle;
                    //this.ChangeOutput(0, false);
                    //this.ChangeOutput(2, false);
                    //self.changeOutput(0, True)
                    //self.changeOutput(2, True)
                    break;
                case 4:
                    this.textBoxArtist.Text = this.CurrentArtist;
                    this.textBoxAlbum.Text = this.CurrentAlbum;
                    break;
                case 5:
                    this.textBoxYear.Text = this.CurrentYear;
                    break;
                case 6:
                    this.labelUrlBeingChecked.Text = e.UserState.ToString();
                    break;
                case 7:
                    this.textBoxYear.Text = this.CurrentYear;
                    break;
                case 8:
                    //this.ChangeOutput(0, true);
                    //this.ChangeOutput(1, true);
                    break;
                case 9:
                    //this.ChangeOutput(0, false);
                    //this.ChangeOutput(2, false);
                    break;
                case 10:
                    this.DisableComponents();
                    break;
                case 11:
                    this.EnableComponents(true);
                    break;
                case 12:
                    this.EnableComponents(false);
                    break;
                case 13:
                    this.ChangeTextColor(false);
                    break;
                case 14:
                    this.ChangeTextColor(true);
                    break;
                case 15:
                    this.labelFilesProcessed.Text = this.NumberFilesProcessed + "/" + this.NewFiles.Count + " Files Processed";
                    break;
                case 16:
                    this.richTextBoxArtist.AppendText(Environment.NewLine);
                    this.richTextBoxAlbum.AppendText(Environment.NewLine);
                    this.richTextBoxTitle.AppendText(Environment.NewLine);
                    break;
                case 17:
                    this.textBoxArtist.Visible = false;
                    this.textBoxTitle.Visible = false;
                    this.textBoxYear.Visible = false;
                    this.textBoxAlbum.Visible = false;
                    this.labelArtist.Visible = false;
                    this.labelAlbum.Visible = false;
                    this.labelTitle.Visible = false;
                    this.labelYear.Visible = false;
                    this.labelUrlBeingChecked.Visible = false;
                    this.buttonSkipSong.Visible = false;
                    this.buttonTryAgain.Visible = false;
                    this.labelFilesProcessed.Text = this.NumberFilesProcessed + "/" + this.NewFiles.Count + " Files Processed. All Done!";
                    break;
                default:
                    break;
            }
            this.ProgressWorkerDone = true;
        }

        private void buttonTryAgain_Click(object sender, EventArgs e)
        {
            if (this.buttonTryAgain.Enabled)
            {
                this.CurrentArtist = this.textBoxArtist.Text;
                this.CurrentAlbum = this.textBoxAlbum.Text;
                this.CurrentTitle = this.textBoxTitle.Text;
                this.Value = new List<string>() { this.CurrentArtist, this.CurrentAlbum, this.CurrentTitle };
                this.DisableComponents();
                this.worker.ReportProgress(10);
                while (!this.ProgressWorkerDone) { }
                if (!this.buttonSkipSong.Enabled)
                {
                    this.worker.ReportProgress(8);
                    while (!this.ProgressWorkerDone) { }
                    this.GetYear();
                }
                else
                {
                    this.worker.ReportProgress(9);
                    while (!this.ProgressWorkerDone) { }
                    this.GetLyrics();
                }
                this.ErrorHandled = true;
            }
        }

        private void buttonSkipSong_Click(object sender, EventArgs e)
        {
            if (this.buttonSkipSong.Enabled)
            {
                this.CurrentLyrics = "None";
                this.Window.LAFContainer.SongsToSkip.Add(new List<string>() { this.textBoxArtist.Text, this.textBoxAlbum.Text, this.textBoxTitle.Text });
                this.ErrorHandled = true;
            }
        }


        private void AddToOutput()
        {
            this.richTextBoxArtist.AppendText(this.CurrentArtist);
            this.richTextBoxAlbum.AppendText(this.CurrentAlbum);
            this.richTextBoxTitle.AppendText(this.CurrentTitle);
            this.richTextBoxArtist.Select(this.richTextBoxArtist.GetFirstCharIndexFromLine(this.NumberFilesProcessed), this.richTextBoxArtist.Lines[this.NumberFilesProcessed].Length);
            this.richTextBoxAlbum.Select(this.richTextBoxAlbum.GetFirstCharIndexFromLine(this.NumberFilesProcessed), this.richTextBoxAlbum.Lines[this.NumberFilesProcessed].Length);
            this.richTextBoxTitle.Select(this.richTextBoxTitle.GetFirstCharIndexFromLine(this.NumberFilesProcessed), this.richTextBoxTitle.Lines[this.NumberFilesProcessed].Length);
            this.richTextBoxArtist.SelectionColor = Color.Yellow;
            this.richTextBoxAlbum.SelectionColor = Color.Yellow;
            this.richTextBoxTitle.SelectionColor = Color.Yellow;
        }

        //private void ChangeOutput(int whichBox,bool gettingYear)
        //{
        //    RichTextBox boxToUpdate= this.richTextBoxArtist;
        //    switch (whichBox)
        //    {
        //        case 0:
        //            boxToUpdate = this.richTextBoxArtist;
        //            break;
        //        case 1:
        //            boxToUpdate = this.richTextBoxAlbum;
        //            break;
        //        case 2:
        //            boxToUpdate = this.richTextBoxTitle;
        //            break;
        //        default:
        //            break;
        //    }
        //    int start_index = boxToUpdate.GetFirstCharIndexFromLine(boxToUpdate.Lines.Length-1);
        //    int count = boxToUpdate.Lines[boxToUpdate.Lines.Length - 1].Length;

        //    // Eat new line chars
        //    //if (a_line < richTextBox.Lines.Length - 1)
        //    //{
        //    //    count += richTextBox.GetFirstCharIndexFromLine(a_line + 1) -
        //    //        ((start_index + count - 1) + 1);
        //    //}

        //    boxToUpdate.Text = boxToUpdate.Text.Remove(start_index, count);
        //    this.AddToOutput();
        //    this.ChangeTextColor(!gettingYear);
        //}

        private void ChangeTextColor(bool fileProcessed)
        {
            if (!fileProcessed)
            {
                this.richTextBoxArtist.Select(this.richTextBoxArtist.GetFirstCharIndexFromLine(this.NumberFilesProcessed), this.richTextBoxArtist.Lines[this.NumberFilesProcessed].Length);
                this.richTextBoxAlbum.Select(this.richTextBoxAlbum.GetFirstCharIndexFromLine(this.NumberFilesProcessed), this.richTextBoxAlbum.Lines[this.NumberFilesProcessed].Length);
                this.richTextBoxTitle.Select(this.richTextBoxTitle.GetFirstCharIndexFromLine(this.NumberFilesProcessed), this.richTextBoxTitle.Lines[this.NumberFilesProcessed].Length);
                this.richTextBoxArtist.SelectionColor = Color.DarkGreen;
                this.richTextBoxAlbum.SelectionColor = Color.DarkGreen;
                this.richTextBoxTitle.SelectionColor = Color.DarkGreen;
            }
            else
            {
                this.richTextBoxArtist.Select(this.richTextBoxArtist.GetFirstCharIndexFromLine(this.NumberFilesProcessed), this.richTextBoxArtist.Lines[this.NumberFilesProcessed].Length);
                this.richTextBoxAlbum.Select(this.richTextBoxAlbum.GetFirstCharIndexFromLine(this.NumberFilesProcessed), this.richTextBoxAlbum.Lines[this.NumberFilesProcessed].Length);
                this.richTextBoxTitle.Select(this.richTextBoxTitle.GetFirstCharIndexFromLine(this.NumberFilesProcessed), this.richTextBoxTitle.Lines[this.NumberFilesProcessed].Length);
                this.richTextBoxArtist.SelectionColor = Color.Lime;
                this.richTextBoxAlbum.SelectionColor = Color.Lime;
                this.richTextBoxTitle.SelectionColor = Color.Lime;
            }
        }

        private void DisableComponents()
        {
            this.Window.AcceptButton = null;
            this.textBoxAlbum.ReadOnly = true;
            this.textBoxArtist.ReadOnly = true;
            this.textBoxTitle.ReadOnly = true;
            this.buttonSkipSong.Enabled = false;
            this.buttonTryAgain.Enabled = false;
        }

        private void EnableComponents(bool forAlbumYear)
        {
            this.Window.AcceptButton = this.buttonTryAgain;
            if (forAlbumYear) { this.textBoxAlbum.ReadOnly = false; }
            else { this.buttonSkipSong.Enabled = true; }
            this.textBoxArtist.ReadOnly = false;
            this.textBoxTitle.ReadOnly = false;
            this.buttonTryAgain.Enabled = true;
        }

        private string NamingConventions(string namePar)
        {
            string name = namePar.ToLower();
            if (name.Contains("pt.") || name.Contains("part.") || name.Contains("pts.") || name.Contains("mr.") || name.Contains("vol."))
            {
                name = name.Replace(".", " ");
            }
            foreach (var key in this.Window.LAFContainer.UrlReplacements.Keys)
            {
                name = name.Replace(key, this.Window.LAFContainer.UrlReplacements[key]);
            }
            var auxList = name.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            for (int index = 0; index < auxList.Length; index++)
            {
                auxList[index] = auxList[index].Trim();
            }
            name = string.Join("-", auxList);
            return char.ToUpper(name[0]) + name.Substring(1).ToLower();
        }

        private void ChangeArtistAlbumTitle(bool forAlbumYear)
        {
            if (forAlbumYear)
            {
                foreach (List<string> key in this.Window.LAFContainer.ExceptionsReplacements.Keys)
                {
                    if (this.Key[0] == key[0] && this.Key[1] == key[1] && key[2] == "")
                    {
                        //this.textBoxArtist.Text = key[0];
                        //this.textBoxAlbum.Text = key[1];
                        //Console.WriteLine("HERE");
                        this.CurrentArtist = this.Window.LAFContainer.ExceptionsReplacements[key][0];
                        this.CurrentAlbum = this.Window.LAFContainer.ExceptionsReplacements[key][1];
                        this.worker.ReportProgress(2);
                        while (!this.ProgressWorkerDone) { }
                        break;
                    }
                }
            }
            else if (!forAlbumYear || this.TrackCount < 5)
            {
                foreach (List<string> key in this.Window.LAFContainer.ExceptionsReplacements.Keys)
                {
                    if (this.Key[0] == key[0] && this.Key[1] == key[1] && key[2] == "")
                    {
                        //this.textBoxArtist.Text = key[0];
                        //this.textBoxAlbum.Text = key[1];
                        this.CurrentArtist = this.Window.LAFContainer.ExceptionsReplacements[key][0];
                        this.CurrentAlbum = this.Window.LAFContainer.ExceptionsReplacements[key][1];
                        this.worker.ReportProgress(4);
                        //this.worker.ReportProgress(4);
                        while (!this.ProgressWorkerDone) { }
                    }
                    else if (this.Key[0] == key[0] && this.Key[1] == key[1] && this.Key[2] == key[2])
                    {
                        //this.textBoxArtist.Text = key[0];
                        //this.textBoxAlbum.Text = key[1];
                        //this.textBoxTitle.Text = key[2];
                        this.CurrentArtist = this.Window.LAFContainer.ExceptionsReplacements[key][0];
                        this.CurrentAlbum = this.Window.LAFContainer.ExceptionsReplacements[key][1];
                        this.CurrentTitle = this.Window.LAFContainer.ExceptionsReplacements[key][2];
                        this.worker.ReportProgress(3);
                        //this.worker.ReportProgress(3);
                        while (!this.ProgressWorkerDone) { }
                        break;
                    }
                }
            }
        }

        private object CheckIfWebpageExists(bool forAlbumYear)
        {
            if (forAlbumYear)
            {
                string name = "https://www.genius.com/albums/" + this.NamingConventions(this.CurrentArtist) + "/" + this.NamingConventions(this.CurrentAlbum);
                //this.labelUrlBeingChecked.Text = "https://www.genius.com/albums/" + name;
                this.worker.ReportProgress(6, name);
                while (!this.ProgressWorkerDone) { }
                if (this.PagesVisited_Year.Keys.Contains(this.CurrentArtist + this.CurrentAlbum))
                {
                    //this.textBoxYear.Text = this.PagesVisited_Year[name].ToString();
                    this.CurrentYear = this.PagesVisited_Year[this.CurrentArtist + this.CurrentAlbum].ToString();
                    this.worker.ReportProgress(5, this.CurrentArtist + this.CurrentAlbum);
                    while (!this.ProgressWorkerDone) { }
                    return "Skip";
                }
            }
            else
            {
                string name = "https://genius.com/" + this.NamingConventions(this.CurrentArtist + " " + this.CurrentTitle) + "-lyrics";
                //this.labelUrlBeingChecked.Text = "https://genius.com/" + name + "-lyrics";
                this.worker.ReportProgress(6, name);
                while (!this.ProgressWorkerDone) { }
            }
            var htmlWeb = new HtmlWeb();
            while (!this.labelUrlBeingChecked.Text.StartsWith("http")) { }
            var htmlDoc = htmlWeb.Load(this.labelUrlBeingChecked.Text);
            var pageTitle = htmlDoc.DocumentNode.Descendants("title").ToList()[0];
            if (pageTitle.InnerText == "Burrr! | Genius")
            {
                return null;
            }
            return htmlDoc;
        }

        private void SetYearInFile()
        {
            using (var mp3 = TagLib.File.Create(this.Filename))
            {
                //var mp3 = TagLib.File.Create(this.Filename);
                mp3.Tag.Year = Convert.ToUInt32(this.CurrentYear);
                mp3.Save();
            }
        }
        private void GetYear()
        {
            while (true)
            {
                var htmlDoc = this.CheckIfWebpageExists(true);
                if (htmlDoc != null && htmlDoc.ToString() == "Skip")
                {
                    this.SetYearInFile();
                    return;
                }
                if (htmlDoc != null)
                {
                    string yearTemp = "";
                    var soup = (HtmlAgilityPack.HtmlDocument)htmlDoc;
                    foreach (var div in soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "metadata_unit").ToList())
                    {
                        yearTemp += div.InnerText.Trim();
                        break;
                    }
                    var year = yearTemp.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                    this.CurrentYear = year.Last();
                    this.worker.ReportProgress(7);
                    while (!this.ProgressWorkerDone) { }
                    if (!this.PagesVisited_Year.ContainsKey(this.CurrentArtist + this.CurrentAlbum))
                    {
                        this.PagesVisited_Year.Add(this.CurrentArtist + this.CurrentAlbum, Int32.Parse(this.CurrentYear));
                    }
                    this.SetYearInFile();
                    this.ErrorHandled = true;
                    return;
                }
                else
                {
                    if (this.TrackCount < 5)
                    {
                        htmlDoc = this.CheckIfWebpageExists(false);
                        if (htmlDoc != null)
                        {
                            var soup = (HtmlAgilityPack.HtmlDocument)htmlDoc;
                            var auxList = soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "HeaderMetadata__Section-sc-1p42fnf-2 hAhJBU").ToList();
                            if (auxList.Count != 0)
                            {
                                foreach (var div in auxList)
                                {
                                    if (div.InnerText.Contains("Release Date"))
                                    {
                                        var aux = div.InnerText.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                                        //foreach (var item in aux)
                                        //{
                                        //    Console.WriteLine(":" + item.Trim() + ":");
                                        //}
                                        this.CurrentYear = aux.Last().Trim();
                                        this.worker.ReportProgress(7);
                                        while (!this.ProgressWorkerDone) { }
                                        //this.textBoxYear.Text = aux.Last();
                                        this.SetYearInFile();
                                        this.ErrorHandled = true;
                                        return;
                                    }
                                }
                            }
                            else
                            {
                                auxList = soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "metadata_unit metadata_unit--table_row").ToList();
                                foreach (var div in auxList)
                                {
                                    if (div.InnerText.Contains("Release Date"))
                                    {
                                        var aux = div.InnerText.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                                        //foreach (var item in aux)
                                        //{
                                        //    Console.WriteLine(":" + item.Trim() + ":");
                                        //}
                                        this.CurrentYear = aux.Last().Trim();
                                        this.worker.ReportProgress(7);
                                        while (!this.ProgressWorkerDone) { }
                                        //this.textBoxYear.Text = aux.Last();
                                        this.SetYearInFile();
                                        this.ErrorHandled = true;
                                        return;
                                    }
                                }
                            }
                        }
                    }
                    else
                    {
                        this.ExceptionRaised = true;
                        SystemSounds.Exclamation.Play();
                        if (this.TrackCount < 5)
                        {
                            System.Diagnostics.Process.Start(string.Format("https://www.google.com.tr/search?q={0}", this.CurrentArtist.Replace(" &", "").Replace(" ", "+") + "+" + this.CurrentTitle.Replace(" &", "").Replace(" ", "+") + "+lyrics+site:Genius.com"));
                        }
                        else
                        {
                            System.Diagnostics.Process.Start(string.Format("https://www.google.com.tr/search?q={0}", this.CurrentArtist.Replace(" &", "").Replace(" ", "+") + "+" + this.CurrentAlbum.Replace(" &", "").Replace(" ", "+") + "+site:Genius.com"));
                        }
                        this.ErrorHandled = false;
                        this.worker.ReportProgress(11);
                        //this.EnableComponents(true);
                        while (!this.ErrorHandled)
                        {
                            Task.Delay(1000);
                        }
                    }
                }

            }
        }
        private void SetLyricsInFile()
        {
            using (var mp3 = TagLib.File.Create(this.Filename))
            {
                //var mp3 = TagLib.File.Create(this.Filename);
                mp3.Tag.Lyrics = this.CurrentLyrics;
                mp3.Save();
            }
        }
        private void GetLyrics()
        {
            while (true)
            {
                var htmlDoc = this.CheckIfWebpageExists(false);
                if (htmlDoc != null)
                {
                    var soup = (HtmlAgilityPack.HtmlDocument)htmlDoc;
                    foreach (var div in soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "lyrics").ToList())
                    {
                        this.CurrentLyrics += div.InnerText.Trim();
                    }
                    if (this.CurrentLyrics != "")
                    {
                        this.SetLyricsInFile();
                        this.ErrorHandled = true;
                        return;
                    }
                }
                else
                {
                    this.ExceptionRaised = true;
                    SystemSounds.Exclamation.Play();
                    System.Diagnostics.Process.Start(string.Format("https://www.google.com.tr/search?q={0}", this.CurrentArtist.Replace(" &", "").Replace(" ", "+") + "+" + this.CurrentTitle.Replace(" &", "").Replace(" ", "+") + "+lyrics+site:Genius.com"));
                    //this.EnableComponents(false);
                    this.ErrorHandled = false;
                    this.worker.ReportProgress(12);
                    while (!this.ProgressWorkerDone) { }
                    while (!this.ErrorHandled)
                    {
                        Task.Delay(1000);
                    }
                }
            }
        }
        private void GetLyricsAndYear(object sender, DoWorkEventArgs e)
        {
            foreach (string filename in this.NewFiles)
            {
                this.Filename = filename;
                this.ErrorHandled = false;
                this.CurrentLyrics = "";
                this.ErrorHandled = true;
                using (var mp3 = TagLib.File.Create(this.Filename))
                {
                    //var mp3 = TagLib.File.Create(filename);
                    this.CurrentArtist = mp3.Tag.AlbumArtists[0];
                    this.CurrentAlbum = mp3.Tag.Album;
                    this.CurrentTitle = this.Window.LAFContainer.RemoveWordsFromWord(new List<string>() { "feat", "Feat", "bonus", "Bonus", "Conclusion", "Hidden Track", "Vocal Mix", "Explicit", "explicit", "Extended" }, mp3.Tag.Title);
                    this.CurrentYear = mp3.Tag.Year.ToString();
                    this.TrackCount = mp3.Tag.TrackCount;
                    mp3.Save();
                }
                this.worker.ReportProgress(0);
                while (!this.ProgressWorkerDone) { }
                this.Key = new List<string>() { this.CurrentArtist, this.CurrentAlbum, this.CurrentTitle };
                //this.AddToOutput();
                this.worker.ReportProgress(1);
                while (!this.ProgressWorkerDone) { }
                this.ChangeArtistAlbumTitle(true);
                this.GetYear();
                this.ErrorHandled = false;
                //this.ChangeTextColor(false);
                this.worker.ReportProgress(13);
                while (!this.ProgressWorkerDone) { }
                if (this.ExceptionRaised && this.Key.SequenceEqual(this.Value))
                {
                    if (this.Key[2] == this.Value[2])
                    {
                        this.Key[2] = this.Value[2] = "";
                    }
                    try
                    {
                        this.Window.LAFContainer.ExceptionsReplacements[this.Key] = this.Value;
                    }
                    catch (ArgumentException)
                    {
                        this.Window.LAFContainer.ExceptionsReplacements[this.Key] = this.Value;
                    }
                    this.ExceptionRaised = false;
                }
                this.ChangeArtistAlbumTitle(false);
                var skipSong = false;
                foreach (var item in this.Window.LAFContainer.SongsToSkip)
                {
                    if (item[0] == this.CurrentArtist && item[1] == this.CurrentAlbum && item[2] == this.CurrentTitle)
                    {
                        skipSong = true;
                        break;
                    }
                }
                if (!skipSong)
                {
                    this.GetLyrics();
                    if (this.ExceptionRaised)
                    {
                        if (this.CurrentLyrics != "None")
                        {
                            this.Window.LAFContainer.ExceptionsReplacements[this.Key] = this.Value;
                        }
                        this.ExceptionRaised = false;
                    }
                }
                //this.ChangeTextColor(true);
                this.worker.ReportProgress(14);
                while (!this.ProgressWorkerDone) { }
                var opStatus = this.Window.LAFContainer.iTunesLibrary.AddFile(this.Filename);
                while (opStatus.InProgress) { }
                var addedTrack = opStatus.Tracks[1];
                if (Int32.Parse(this.CurrentYear) < 1985)
                {
                    addedTrack.VolumeAdjustment = 50;
                }
                this.worker.ReportProgress(16);
                while (!this.ProgressWorkerDone) { }
                this.NumberFilesProcessed++;
                this.worker.ReportProgress(15);
                while (!this.ProgressWorkerDone) { }
                this.Window.LAFContainer.iTunesLibrary.AddFile(this.Filename);
                if (this.AddFileToList)
                {
                    this.Window.LAFContainer.AddMusicFile(this.Filename);
                }
            }
            this.Window.LAFContainer.SaveNumberFilesLastModified();
            this.Window.LAFContainer.SaveMusicFiles();
            this.worker.ReportProgress(17);
        }
    }

}
