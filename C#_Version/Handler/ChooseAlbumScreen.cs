using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Handler
{
    public partial class ChooseAlbumScreen : UserControl
    {
        private HandlerForm Window;
        private int AlbumTime, AlbumLeeway;
        private List<string> AlbumGenres;
        private List<Album> PossibleAlbums, PossibleHalfAlbums;
        private int Over, Under;

        public ChooseAlbumScreen(int albumTime, int albumLeeway, List<string> genresPicked, int leewayMode)
        {
            InitializeComponent();
            this.AlbumTime = albumTime;
            this.AlbumLeeway = albumLeeway;
            this.AlbumGenres = genresPicked;
            this.listBoxPossibleAlbums.DrawMode = DrawMode.OwnerDrawFixed;
            this.listBoxPossibleHalfAlbums.DrawMode = DrawMode.OwnerDrawFixed;
            switch (leewayMode)
            {
                case 0:
                    this.Over = this.Under = 1;
                    break;
                case 1:
                    this.Over = 1;
                    this.Under = 0;
                    break;
                case 2:
                    this.Over = 0;
                    this.Under = 1;
                    break;
                default:
                    break;
            }
            this.labelPossibleAlbums.Text = string.Format("Albums whose length varies between {0} minutes and {1} minutes",this.AlbumTime/60-(this.AlbumLeeway / 60 )* this.Under, this.AlbumTime / 60 + (this.AlbumLeeway / 60) * this.Over);
            this.labelPossibleHalfAlbums.Text = string.Format("Albums where half of their length varies between {0} minutes and {1} minutes", this.AlbumTime / 60 - (this.AlbumLeeway / 60) * this.Under, this.AlbumTime / 60 + (this.AlbumLeeway / 60) * this.Over);
            this.PossibleAlbums = new List<Album>();
            this.PossibleHalfAlbums = new List<Album>();
        }

        private void ChooseAlbumScreen_Load(object sender, EventArgs e)
        {
            this.Window = this.Parent as HandlerForm;
            this.GetAlbums();
            this.PossibleAlbums=this.PossibleAlbums.OrderByDescending(album => album.Length).ToList();
            this.PossibleHalfAlbums = this.PossibleHalfAlbums.OrderByDescending(album => album.Length).ToList();
            foreach (Album album in this.PossibleAlbums)
            {
                this.listBoxPossibleAlbums.Items.Add(album.Artist + " - " + album.Title+"\t\t\t"+this.Window.LAFContainer.StandardFormatTime(album.Length));
            }
            foreach (Album album in this.PossibleHalfAlbums)
            {
                this.listBoxPossibleHalfAlbums.Items.Add(album.Artist + " - " + album.Title + "\t\t\t" + this.Window.LAFContainer.StandardFormatTime(album.Length));
            }
            //this.Window.Controls.OfType<HomeScreen>().ToList()[0].Dispose();
        }

        private void GetAlbums()
        {
            int underTime, overTime = 0;
            foreach (Album album in this.Window.LAFContainer.Albums)
            {
                int leeway = 60;
                int albumLength = album.Length;
                string albumGenre = album.Genre;
                if (this.AlbumGenres.Contains(albumGenre))
                {
                    while (leeway <= this.AlbumLeeway)
                    {
                        underTime = this.AlbumTime - this.AlbumLeeway * this.Under;
                        overTime = this.AlbumTime + this.AlbumLeeway * this.Under;
                        if(albumLength>=underTime && albumLength <= overTime)
                        {
                            this.PossibleAlbums.Add(album);
                            break;
                        }
                        else if (albumLength / 2 >= (this.AlbumTime - this.AlbumLeeway) && albumLength / 2 <= (this.AlbumTime + this.AlbumLeeway))
                        {
                            this.PossibleHalfAlbums.Add(album);
                            break;
                        }
                        leeway += 60;
                    }
                }
            }
        }
        private void listBoxPossibleAlbums_DrawItem(object sender, DrawItemEventArgs e)
        {
            var item = listBoxPossibleAlbums.Items[e.Index];
            //Console.WriteLine(item);

            if (item != null)
            {
                e.Graphics.DrawString(
                    item.ToString(),
                    e.Font,
                    new SolidBrush(this.Window.LAFContainer.GenresColors[this.PossibleAlbums[e.Index].Genre]),
                    e.Bounds);
            }
        }
        private void listBoxPossibleHalfAlbums_DrawItem(object sender, DrawItemEventArgs e)
        {
            var item = listBoxPossibleHalfAlbums.Items[e.Index];
            //Console.WriteLine(item);

            if (item != null)
            {
                e.Graphics.DrawString(
                    item.ToString(),
                    e.Font,
                    new SolidBrush(this.Window.LAFContainer.GenresColors[this.PossibleHalfAlbums[e.Index].Genre]),
                    e.Bounds);
            }
        }
    }
}
