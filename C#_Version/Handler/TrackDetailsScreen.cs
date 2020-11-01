using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
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
        public TrackDetailsScreen(HandlerForm window,List<MusicFile> tracks)
        {
            InitializeComponent();
            this.Window = window;
            this.Window.CancelButton = this.buttonBack;
            this.Tracks = tracks;
            this.PreviousValues = new List<string>();
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

        private void buttonBack_Click(object sender, EventArgs e)
        {
            foreach (MusicFile musicFile in this.Tracks)
            {
                using (var mp3 = TagLib.File.Create(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, musicFile.Filename)))
                {
                    Console.WriteLine("HERE");
                    IITFileOrCDTrack iTunesTrack = (IITFileOrCDTrack)this.Window.LAFContainer.GetITunesTrack(musicFile.Title,musicFile.Album);
                    if (this.PreviousValues[0] != this.textBoxAlbumArtist.Text)
                    {
                        mp3.Tag.AlbumArtists = new string[] { this.textBoxAlbumArtist.Text };
                        musicFile.AlbumArtist = this.textBoxAlbumArtist.Text;
                        iTunesTrack.AlbumArtist = musicFile.AlbumArtist;
                    }
                    if (this.PreviousValues[1] != this.textBoxContributingArtist.Text)
                    {
                        mp3.Tag.Performers = new string[] { this.textBoxContributingArtist.Text };
                        musicFile.ContributingArtists = this.textBoxContributingArtist.Text;
                        iTunesTrack.Artist = musicFile.ContributingArtists;
                    }
                    if (this.PreviousValues[2] != this.textBoxAlbum.Text)
                    {
                        mp3.Tag.Album = this.textBoxAlbum.Text;
                        musicFile.Album = this.textBoxAlbum.Text;
                        iTunesTrack.Album = musicFile.Album;
                    }
                    if (this.PreviousValues[3] != this.textBoxTitle.Text)
                    {
                        mp3.Tag.Title = this.textBoxTitle.Text;
                        musicFile.Title = this.textBoxTitle.Text;
                        iTunesTrack.Name = musicFile.Title;
                    }
                    if (this.PreviousValues[4] != this.textBoxTrackNumber.Text)
                    {
                        bool plus = this.textBoxTrackNumber.Text.StartsWith("+");
                        bool minus = this.textBoxTrackNumber.Text.StartsWith("-");
                        uint amount = !plus & !minus ? UInt32.Parse(this.textBoxTrackNumber.Text) : UInt32.Parse(this.textBoxTrackNumber.Text.Substring(1));
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
                            mp3.Tag.Track =amount;
                        }
                        musicFile.TrackNumber = (int)mp3.Tag.Track;
                        iTunesTrack.TrackNumber = musicFile.TrackNumber;
                    }
                    if (this.PreviousValues[5] != this.textBoxDiscNumber.Text)
                    {
                        bool plus = this.textBoxDiscNumber.Text.StartsWith("+");
                        bool minus = this.textBoxDiscNumber.Text.StartsWith("-");
                        uint amount = !plus & !minus ? UInt32.Parse(this.textBoxDiscNumber.Text) : UInt32.Parse(this.textBoxDiscNumber.Text.Substring(1));
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
                    if (this.PreviousValues[6] != this.textBoxYear.Text)
                    {
                        bool plus = this.textBoxYear.Text.StartsWith("+");
                        bool minus = this.textBoxYear.Text.StartsWith("-");
                        uint amount = !plus & !minus ? UInt32.Parse(this.textBoxYear.Text) : UInt32.Parse(this.textBoxYear.Text.Substring(1));
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
                    if (this.PreviousValues[7] != this.textBoxGenre.Text)
                    {
                        mp3.Tag.Genres = new string[] { this.textBoxGenre.Text };
                        musicFile.Genre = mp3.Tag.Genres[0];
                        iTunesTrack.Genre = musicFile.Genre;
                    }
                    if (this.PreviousValues[8] != this.textBoxPlayCount.Text)
                    {
                        bool plus = this.textBoxYear.Text.StartsWith("+");
                        bool minus = this.textBoxYear.Text.StartsWith("-");
                        int amount = !plus & !minus ? Int32.Parse(this.textBoxYear.Text) : Int32.Parse(this.textBoxYear.Text.Substring(1));
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
                    this.Window.LAFContainer.iTunesLibrary.AddFile(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, musicFile.Filename));
                }
            }
            this.Dispose();
            this.Window.ActiveControl = this.Window.Controls.OfType<SearchLibraryScreen>().ToList()[0];
            this.Window.Controls.OfType<SearchLibraryScreen>().ToList()[0].Visible = true;
        }
    }
}
