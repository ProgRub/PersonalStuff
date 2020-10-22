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

namespace Handler
{
    public partial class TracklistScreen : UserControl
    {
        private HandlerForm Window;
        private Album Album;
        public TracklistScreen(HandlerForm window,Album album)
        {
            InitializeComponent();
            this.Window = window;
            this.Album = album;
            this.labelAlbum.Text = this.labelAlbum.Text + this.Album.Title;
            this.labelLength.Text = this.labelLength.Text + this.Window.LAFContainer.StandardFormatTime(this.Album.Length);
            bool imageGot = false;
            int maxPreviousDisc = 0;
            int numberTracks = 0;
            foreach (List<MusicFile> disc in this.Album.TracksByDiscs)
            {
                foreach (MusicFile track in disc)
                {
                    numberTracks++;
                    this.textBoxTrackList.AppendText(track.TrackNumber + maxPreviousDisc + ". " + track.Title + Environment.NewLine);
                    if (!imageGot)
                    {
                        using (var mp3 = TagLib.File.Create(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, track.Filename)))
                        {
                            this.pictureBox1.Image = Image.FromStream(new MemoryStream((byte[])(mp3.Tag.Pictures[0].Data.Data)));
                        }
                        imageGot = true;
                    }
                }
                maxPreviousDisc = disc.Count;
            }
            this.textBoxTrackList.Text = this.textBoxTrackList.Text.Trim();
            this.textBoxTrackList.Height = this.textBoxTrackList.Font.Height * numberTracks+3+(this.textBoxTrackList.Height - this.textBoxTrackList.ClientSize.Height);
            this.labelLength.Location = new Point(this.textBoxTrackList.Location.X, this.textBoxTrackList.Location.Y + this.textBoxTrackList.Size.Height);
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            this.Dispose();
            this.Window.Controls.OfType<ChooseAlbumScreen>().ToList()[0].Visible = true;
            this.Window.ActiveControl = this.Window.Controls.OfType<ChooseAlbumScreen>().ToList()[0];
        }
    }
}
