using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.IO;
using Microsoft.VisualBasic.FileIO;

namespace Downloader
{
    public partial class MusicScreen : UserControl
    {
        public DownloaderForm Window { get; set; }
        private int NumberFilesFound;
        private int NumberFilesMoved;
        private List<string> FileBuffer;
        private bool CanAdvance;
        private List<string> NewFiles;
        private Timer TimerCheckMusic;

        public MusicScreen()
        {
            InitializeComponent();
            this.NumberFilesFound = 0;
            this.NumberFilesMoved = 0;
            this.FileBuffer = new List<string>();
            this.CanAdvance = false;
            this.NewFiles = new List<string>();
            this.labelFilesFound.Text = "0 Files Found";
        }
        private void CheckMusic(object sender, EventArgs e)
        {
            var files = Directory.EnumerateFiles(Path.Combine(this.Window.LAFContainer.MusicOriginDirectory)).ToList();
            foreach (string filename in files)
            {
                if (filename.EndsWith(".mp3") && !this.FileBuffer.Contains(filename))
                {
                    this.FileBuffer.Add(filename);
                    this.NumberFilesFound++;
                    this.labelFilesFound.Text = this.NumberFilesFound + " Files Found";
                    this.TextBoxFilesFound.AppendText(Path.GetFileName(filename) + Environment.NewLine);
                }
            }
        }

        private void MoveOutOfBuffer()
        {
            foreach (string oldFilename in this.FileBuffer)
            {
                string newFilename = Path.GetFileName(oldFilename);
                newFilename.Replace("f_ck", "fuck").Replace("f___", "fuck").Replace("f__k", "fuck").Replace("sh_t", "shit").Replace("s__t", "shit").Replace("sh__", "shit").Replace("ni__as", "niggas").Replace(
                            "F_ck", "Fuck").Replace("F__k", "Fuck").Replace("F___", "Fuck").Replace("Sh_t", "Shit").Replace("S__t", "Shit").Replace("Sh__", "Shit").Replace("Ni__as", "Niggas");
                newFilename = this.Window.LAFContainer.RemoveWordsFromWord(new List<string>() { "Remaster", "Album Version", "Stereo" }, newFilename);
                this.Window.LAFContainer.TagChanges(oldFilename);
                try
                {
                    File.Move(oldFilename, Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename));
                    this.NumberFilesMoved++;
                    this.TextBoxFilesMoved.AppendText(Path.GetFileName(newFilename) + Environment.NewLine);
                    this.NewFiles.Add(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename));
                }
                catch (IOException)
                {
                    string oldArtist = "";
                    string oldAlbum = "";
                    string newArtist = "";
                    string newAlbum = "";
                    using (var mp3ToSend = TagLib.File.Create(oldFilename))
                    {
                        oldArtist = mp3ToSend.Tag.AlbumArtists[0];
                        oldAlbum = mp3ToSend.Tag.Album;
                        mp3ToSend.Save();
                    }
                    using (var mp3ToCheck = TagLib.File.Create(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename)))
                    {
                        newArtist = mp3ToCheck.Tag.AlbumArtists[0];
                        newAlbum = mp3ToCheck.Tag.Album;
                        mp3ToCheck.Save();
                    }
                    //var mp3ToSend = TagLib.File.Create(oldFilename);
                    //var mp3ToCheck = TagLib.File.Create(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename));
                    if (oldArtist == newArtist && oldAlbum == newAlbum)
                    {
                        FileSystem.DeleteFile(oldFilename, UIOption.OnlyErrorDialogs, RecycleOption.SendToRecycleBin);
                        this.TextBoxFilesMoved.AppendText(Path.GetFileName(oldFilename) + " already exists, DELETED" + Environment.NewLine);
                    }
                    else
                    {
                        string toAdd = " (";
                        List<string> artistSplit = oldArtist.Split(new char[0], StringSplitOptions.RemoveEmptyEntries).ToList();
                        if ("The" == artistSplit[0])
                        {
                            artistSplit.Remove("The");
                        }
                        if (artistSplit.Count == 1) { toAdd += artistSplit[0]; }
                        else
                        {
                            foreach (string item in artistSplit)
                            {
                                toAdd += item.ToUpper()[0];
                            }
                        }
                        toAdd += ").mp3";
                        newFilename = newFilename.Substring(0, newFilename.LastIndexOf('.')) + toAdd;
                        try
                        {
                            File.Move(oldFilename, Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename));
                            this.NumberFilesMoved++;
                            this.TextBoxFilesMoved.AppendText(Path.GetFileName(newFilename) + Environment.NewLine);
                            this.NewFiles.Add(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename));
                        }
                        catch (IOException)
                        {
                            using (var mp3ToCheck = TagLib.File.Create(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename)))
                            {
                                newArtist = mp3ToCheck.Tag.AlbumArtists[0];
                                newAlbum = mp3ToCheck.Tag.Album;
                                mp3ToCheck.Save();
                            }
                            if (oldArtist == newArtist&& oldAlbum == newAlbum)
                            {
                                FileSystem.DeleteFile(oldFilename, UIOption.OnlyErrorDialogs, RecycleOption.SendToRecycleBin);
                                this.TextBoxFilesMoved.AppendText(Path.GetFileName(oldFilename) + " already exists, DELETED" + Environment.NewLine);
                            }
                            else
                            {
                                File.Move(oldFilename, Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename));
                                this.NumberFilesMoved++;
                                this.TextBoxFilesMoved.AppendText(Path.GetFileName(newFilename) + Environment.NewLine);
                                this.NewFiles.Add(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename));
                            }
                        }
                    }
                }
                this.labelFilesFound.Text = this.NumberFilesFound + " Files Found";
            }
            this.CanAdvance = true;
            this.buttonEndCycleAdvance.Enabled = true;
        }

        private void MusicScreen_Load(object sender, EventArgs e)
        {
            this.Window = this.Parent as DownloaderForm;
            Process deemix = new Process();
            deemix.StartInfo.WorkingDirectory = Path.Combine(this.Window.LAFContainer.CurrentDirectory, "auxFiles", "deemix");
            deemix.StartInfo.FileName = "start.bat";
            deemix.Start();
            this.TimerCheckMusic = new Timer();
            this.TimerCheckMusic.Tick += new EventHandler(CheckMusic);
            this.TimerCheckMusic.Interval = 15;
            this.TimerCheckMusic.Start();
        }

        private void buttonEndCycleAdvance_Click(object sender, EventArgs e)
        {
            if (!this.CanAdvance)
            {
                this.CanAdvance = true;
                this.TimerCheckMusic.Stop();
                this.buttonEndCycleAdvance.Text = "Get Album Year And Lyrics";
                this.buttonEndCycleAdvance.Enabled = false;
                this.MoveOutOfBuffer();
            }
            else
            {
                this.Hide();
                YearLyricsScreen aux = new YearLyricsScreen(this.NewFiles);
                aux.Dock = DockStyle.Fill;
                this.Window.Controls.Add(aux);
                this.Window.ActiveControl = aux;
            }
        }
    }
}
