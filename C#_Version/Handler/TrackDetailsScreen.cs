using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using System.IO;
using iTunesLib;

namespace Handler
{
    public partial class TrackDetailsScreen : UserControl
    {
        private HandlerForm Window;
        private List<MusicFile> Tracks;
        private List<string> PreviousValues;
        private List<string> NewValues;
        private int NUMBER_OF_THREADS = 15;
        public TrackDetailsScreen(HandlerForm window, List<MusicFile> tracks)
        {
            InitializeComponent();
            this.Window = window;
            this.Window.CancelButton = this.buttonBack;
            this.Tracks = tracks;
            this.PreviousValues = new List<string>();
            this.NewValues = new List<string>();
            this.textBoxAlbumArtist.Text = this.Tracks[0].AlbumArtist;
            this.textBoxContributingArtist.Text = this.Tracks[0].ContributingArtists;
            this.textBoxAlbum.Text = this.Tracks[0].Album;
            this.textBoxTitle.Text = this.Tracks[0].Title;
            this.textBoxTrackNumber.Text = this.Tracks[0].TrackNumber.ToString();
            this.textBoxDiscNumber.Text = this.Tracks[0].DiscNumber.ToString();
            this.textBoxYear.Text = this.Tracks[0].Year.ToString();
            this.textBoxGenre.Text = this.Tracks[0].Genre;
            this.textBoxGenre.AutoCompleteCustomSource.AddRange(this.Window.LAFContainer.GenresColors.Keys.ToArray());
            this.textBoxPlayCount.Text = this.Tracks[0].PlayCount.ToString();
            foreach (MusicFile musicFile in this.Tracks.Skip(1))
            {
                if (musicFile.AlbumArtist != this.textBoxAlbumArtist.Text)
                {
                    this.textBoxAlbumArtist.Text = "";
                }
                if (musicFile.ContributingArtists != this.textBoxContributingArtist.Text)
                {
                    this.textBoxContributingArtist.Text = "";
                }
                if (musicFile.Album != this.textBoxAlbum.Text)
                {
                    this.textBoxAlbum.Text = "";
                }
                if (musicFile.Title != this.textBoxTitle.Text)
                {
                    this.textBoxTitle.Text = "";
                }
                if (musicFile.TrackNumber.ToString() != this.textBoxTrackNumber.Text)
                {
                    this.textBoxTrackNumber.Text = "";
                }
                if (musicFile.DiscNumber.ToString() != this.textBoxDiscNumber.Text)
                {
                    this.textBoxDiscNumber.Text = "";
                }
                if (musicFile.Year.ToString() != this.textBoxYear.Text)
                {
                    this.textBoxYear.Text = "";
                }
                if (musicFile.Genre != this.textBoxGenre.Text)
                {
                    this.textBoxGenre.Text = "";
                }
                if (musicFile.PlayCount.ToString() != this.textBoxPlayCount.Text)
                {
                    this.textBoxPlayCount.Text = "";
                }
            }
            this.PreviousValues.Add(this.textBoxAlbumArtist.Text);
            this.PreviousValues.Add(this.textBoxContributingArtist.Text);
            this.PreviousValues.Add(this.textBoxAlbum.Text);
            this.PreviousValues.Add(this.textBoxTitle.Text);
            this.PreviousValues.Add(this.textBoxTrackNumber.Text);
            this.PreviousValues.Add(this.textBoxDiscNumber.Text);
            this.PreviousValues.Add(this.textBoxYear.Text);
            this.PreviousValues.Add(this.textBoxGenre.Text);
            this.PreviousValues.Add(this.textBoxPlayCount.Text);
        }

        #region Event Handlers
        private void buttonBack_Click(object sender, EventArgs e)
        {
            this.NewValues.Add(this.textBoxAlbumArtist.Text);
            this.NewValues.Add(this.textBoxContributingArtist.Text);
            this.NewValues.Add(this.textBoxAlbum.Text);
            this.NewValues.Add(this.textBoxTitle.Text);
            this.NewValues.Add(this.textBoxTrackNumber.Text);
            this.NewValues.Add(this.textBoxDiscNumber.Text);
            this.NewValues.Add(this.textBoxYear.Text);
            this.NewValues.Add(this.textBoxGenre.Text);
            this.NewValues.Add(this.textBoxPlayCount.Text);
            this.Dispose();
            this.Window.ActiveControl = this.Window.Controls.OfType<SearchLibraryScreen>().ToList()[0];
            this.Window.Controls.OfType<SearchLibraryScreen>().ToList()[0].Visible = true;
            this.NUMBER_OF_THREADS = Math.Min(this.Tracks.Count, this.NUMBER_OF_THREADS);
            Thread[] threads = new Thread[NUMBER_OF_THREADS+1];
            for (int i = 0; i < threads.Length; i++)
            {
                threads[i] = new Thread(new ParameterizedThreadStart(UpdateFiles));
                threads[i].Start(i);
            }
            for (int i = 0; i < threads.Length; ++i)
            {
                threads[i].Join();
            }
        }
        #endregion

        private void UpdateFiles(object arg)
        {
            int start = (int)arg * (this.Tracks.Count / NUMBER_OF_THREADS);
            int end = Math.Min(((int)arg + 1) * (this.Tracks.Count / NUMBER_OF_THREADS), this.Tracks.Count);
            for (int index = start; index < end; index++)
            {
                MusicFile musicFile = this.Tracks[index];
                using (var mp3 = TagLib.File.Create(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, musicFile.Filename)))
                {
                    IITFileOrCDTrack iTunesTrack = (IITFileOrCDTrack)this.Window.LAFContainer.GetITunesTrack(musicFile.Title, musicFile.Album);
                    if (this.PreviousValues[0] != this.NewValues[0])
                    {
                        mp3.Tag.AlbumArtists = new string[] { this.NewValues[0] };
                        musicFile.AlbumArtist = this.NewValues[0];
                        iTunesTrack.AlbumArtist = musicFile.AlbumArtist;
                    }
                    if (this.PreviousValues[1] != this.NewValues[1])
                    {
                        mp3.Tag.Performers = new string[] { this.NewValues[1] };
                        musicFile.ContributingArtists = this.NewValues[1];
                        iTunesTrack.Artist = musicFile.ContributingArtists;
                    }
                    if (this.PreviousValues[2] != this.NewValues[2])
                    {
                        mp3.Tag.Album = this.NewValues[2];
                        musicFile.Album = mp3.Tag.Album;
                        iTunesTrack.Album = musicFile.Album;
                    }
                    if (this.PreviousValues[3] != this.NewValues[3])
                    {
                        mp3.Tag.Title = this.NewValues[3];
                        musicFile.Title = mp3.Tag.Title;
                        iTunesTrack.Name = musicFile.Title;
                    }
                    if (this.PreviousValues[4] != this.NewValues[4])
                    {
                        bool plus = this.NewValues[4].StartsWith("+");
                        bool minus = this.NewValues[4].StartsWith("-");
                        uint amount = !plus & !minus ? UInt32.Parse(this.NewValues[4]) : UInt32.Parse(this.NewValues[4].Substring(1));
                        if (plus)
                        {
                            mp3.Tag.Track += amount;
                        }
                        else if (minus)
                        {
                            mp3.Tag.Track = Math.Max(0, mp3.Tag.Track - amount);
                        }
                        else
                        {
                            mp3.Tag.Track = amount;
                        }
                        musicFile.TrackNumber = (int)mp3.Tag.Track;
                        iTunesTrack.TrackNumber = musicFile.TrackNumber;
                    }
                    if (this.PreviousValues[5] != this.NewValues[5])
                    {
                        bool plus = this.NewValues[5].StartsWith("+");
                        bool minus = this.NewValues[5].StartsWith("-");
                        uint amount = !plus & !minus ? UInt32.Parse(this.NewValues[5]) : UInt32.Parse(this.NewValues[5].Substring(1));
                        if (plus)
                        {
                            mp3.Tag.Disc += amount;
                        }
                        else if (minus)
                        {
                            mp3.Tag.Disc = Math.Max(0, mp3.Tag.Disc - amount);
                        }
                        else
                        {
                            mp3.Tag.Disc = amount;
                        }
                        musicFile.DiscNumber = (int)mp3.Tag.Disc;
                        iTunesTrack.DiscNumber = musicFile.DiscNumber;
                    }
                    if (this.PreviousValues[6] != this.NewValues[6])
                    {
                        bool plus = this.NewValues[6].StartsWith("+");
                        bool minus = this.NewValues[6].StartsWith("-");
                        uint amount = !plus & !minus ? UInt32.Parse(this.NewValues[6]) : UInt32.Parse(this.NewValues[6].Substring(1));
                        if (plus)
                        {
                            mp3.Tag.Year += amount;
                        }
                        else if (minus)
                        {
                            mp3.Tag.Year = Math.Max(0, mp3.Tag.Year - amount);
                        }
                        else
                        {
                            mp3.Tag.Year = amount;
                        }
                        musicFile.Year = (int)mp3.Tag.Year;
                        iTunesTrack.Year = musicFile.Year;
                    }
                    if (this.PreviousValues[7] != this.NewValues[7])
                    {
                        mp3.Tag.Genres = new string[] { this.NewValues[7] };
                        musicFile.Genre = mp3.Tag.Genres[0];
                        iTunesTrack.Genre = musicFile.Genre;
                    }
                    if (this.PreviousValues[8] != this.NewValues[8])
                    {
                        bool plus = this.NewValues[8].StartsWith("+");
                        bool minus = this.NewValues[8].StartsWith("-");
                        int amount = !plus & !minus ? Int32.Parse(this.NewValues[8]) : Int32.Parse(this.NewValues[8].Substring(1));
                        if (plus)
                        {
                            iTunesTrack.PlayedCount += amount;
                        }
                        else if (minus)
                        {
                            iTunesTrack.PlayedCount = Math.Max(0, iTunesTrack.PlayedCount - amount);
                        }
                        else
                        {
                            iTunesTrack.PlayedCount = amount;
                        }
                        musicFile.PlayCount = iTunesTrack.PlayedCount;
                    }
                    mp3.Save();
                }
            }
        }
    }
}
