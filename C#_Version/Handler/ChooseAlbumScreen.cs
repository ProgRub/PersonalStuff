using System;
using System.Collections.Generic;
using System.Collections;
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
        private int PreviousColumnPA, PreviousColumnPHA;
        private bool ReversePA, ReversePHA;

        public ChooseAlbumScreen(HandlerForm window,int albumTime, int albumLeeway, List<string> genresPicked, int leewayMode)
        {
            InitializeComponent();
            this.Window = window;
            this.AlbumTime = albumTime;
            this.AlbumLeeway = albumLeeway;
            this.AlbumGenres = genresPicked;
            this.PreviousColumnPA = this.PreviousColumnPHA = 2;
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
            this.labelPossibleAlbums.Text = string.Format("Albums whose length varies between {0} minutes and {1} minutes", this.AlbumTime / 60 - (this.AlbumLeeway / 60) * this.Under, this.AlbumTime / 60 + (this.AlbumLeeway / 60) * this.Over);
            this.labelPossibleHalfAlbums.Text = string.Format("Albums where half of their length varies between {0} minutes and {1} minutes", this.AlbumTime / 60 - (this.AlbumLeeway / 60) * this.Under, this.AlbumTime / 60 + (this.AlbumLeeway / 60) * this.Over);
            this.PossibleAlbums = new List<Album>();
            this.PossibleHalfAlbums = new List<Album>();
            this.GetAlbums();
            this.PossibleAlbums = this.PossibleAlbums.OrderByDescending(album => album.Length).ToList();
            this.PossibleHalfAlbums = this.PossibleHalfAlbums.OrderByDescending(album => album.Length).ToList();
            foreach (Album album in this.PossibleAlbums)
            {
                var item = new ListViewItem(album.Artist);
                item.ForeColor = this.Window.LAFContainer.GenresColors[album.Genre];
                item.SubItems.Add(album.Title);
                item.SubItems.Add(this.Window.LAFContainer.StandardFormatTime(album.Length));
                item.SubItems.Add(album.AveragePlayCount.ToString());
                this.listViewPossibleAlbums.Items.Add(item);
            }
            foreach (Album album in this.PossibleHalfAlbums)
            {
                var item = new ListViewItem(album.Artist);
                item.ForeColor = this.Window.LAFContainer.GenresColors[album.Genre];
                item.SubItems.Add(album.Title);
                item.SubItems.Add(this.Window.LAFContainer.StandardFormatTime(album.Length));
                item.SubItems.Add(album.AveragePlayCount.ToString());
                this.listViewPossibleHalfAlbums.Items.Add(item);
            }
        }
        #region Event Handlers
        private void listViewPossibleAlbums_DoubleClick(object sender, EventArgs e)
        {
            //Console.WriteLine(this.listViewPossibleAlbums.SelectedItems[0].SubItems[1].Text);
            Album albumSelected = this.Window.LAFContainer.Albums[this.Window.LAFContainer.IndexOfAlbumByName(this.listViewPossibleAlbums.SelectedItems[0].SubItems[1].Text)];
            this.Hide();
            TracklistScreen aux = new TracklistScreen(this.Window,albumSelected);
            aux.Dock = DockStyle.Fill;
            this.Window.Controls.Add(aux);
            this.Window.ActiveControl = aux;
        }

        private void listViewPossibleAlbums_KeyDown(object sender, KeyEventArgs e)
        {
            if (Keys.Enter == e.KeyCode)
            {
                Album albumSelected = this.Window.LAFContainer.Albums[this.Window.LAFContainer.IndexOfAlbumByName(this.listViewPossibleAlbums.SelectedItems[0].SubItems[1].Text)];
                this.Hide();
                TracklistScreen aux = new TracklistScreen(this.Window, albumSelected);
                aux.Dock = DockStyle.Fill;
                this.Window.Controls.Add(aux);
                this.Window.ActiveControl = aux;
            }
        }

        private void listViewPossibleHalfAlbums_KeyDown(object sender, KeyEventArgs e)
        {
            if (Keys.Enter == e.KeyCode)
            {
                Album albumSelected = this.Window.LAFContainer.Albums[this.Window.LAFContainer.IndexOfAlbumByName(this.listViewPossibleAlbums.SelectedItems[0].SubItems[1].Text)];
                this.Hide();
                TracklistScreen aux = new TracklistScreen(this.Window, albumSelected);
                aux.Dock = DockStyle.Fill;
                this.Window.Controls.Add(aux);
                this.Window.ActiveControl = aux;
            }
        }

        private void listViewPossibleAlbums_ColumnClick(object sender, ColumnClickEventArgs e)
        {
            this.ReversePA = !this.ReversePA & this.PreviousColumnPA == e.Column;
            this.listViewPossibleAlbums.ListViewItemSorter = new ListViewItemComparer(e.Column, this.ReversePA);
            this.PreviousColumnPA = e.Column;
        }
        private void buttonBack_Click(object sender, EventArgs e)
        {
            this.Dispose();
            this.Window.Controls.OfType<AlbumPropertiesScreen>().ToList()[0].Visible = true;
            this.Window.ActiveControl = this.Window.Controls.OfType<AlbumPropertiesScreen>().ToList()[0];
        }

        private void listViewPossibleHalfAlbums_DoubleClick(object sender, EventArgs e)
        {
            Album albumSelected = this.Window.LAFContainer.Albums[this.Window.LAFContainer.IndexOfAlbumByName(this.listViewPossibleHalfAlbums.SelectedItems[0].SubItems[1].Text)];
            this.Hide();
            TracklistScreen aux = new TracklistScreen(this.Window, albumSelected);
            aux.Dock = DockStyle.Fill;
            this.Window.Controls.Add(aux);
            this.Window.ActiveControl = aux;
        }

        private void listViewPossibleHalfAlbums_ColumnClick(object sender, ColumnClickEventArgs e)
        {
            this.ReversePHA = !this.ReversePHA & this.PreviousColumnPHA == e.Column;
            this.listViewPossibleHalfAlbums.ListViewItemSorter = new ListViewItemComparer(e.Column, this.ReversePHA);
            this.PreviousColumnPHA = e.Column;
        }
        #endregion

        private void GetAlbums()
        {
            int underTime, overTime;
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
                        overTime = this.AlbumTime + this.AlbumLeeway * this.Over;
                        if (albumLength >= underTime && albumLength <= overTime)
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
    }

    // Implements the manual sorting of items by columns.
    class ListViewItemComparer : IComparer
    {
        private int col;
        private int reverse;
        public ListViewItemComparer()
        {
            col = 0;
        }
        public ListViewItemComparer(int column, bool reverse)
        {
            col = column;
            this.reverse = reverse ? -1 : 1;
        }
        public int Compare(object x, object y)
        {
            if (this.col == 2)
            {
                string[] timeX = ((ListViewItem)x).SubItems[col].Text.Split(':');
                string[] timeY = ((ListViewItem)y).SubItems[col].Text.Split(':');
                if ((Int32.Parse(timeX[0]) * 60 + Int32.Parse(timeX[1])) == (Int32.Parse(timeY[0]) * 60 + Int32.Parse(timeY[1])))
                {
                    return 0;
                }
                else if ((Int32.Parse(timeX[0]) * 60 + Int32.Parse(timeX[1])) < (Int32.Parse(timeY[0]) * 60 + Int32.Parse(timeY[1])))
                {
                    return 1 * reverse;
                }
                return -1 * reverse;
            }
            else if (this.col == 3)
            {
                if (float.Parse(((ListViewItem)x).SubItems[col].Text) == float.Parse(((ListViewItem)y).SubItems[col].Text))
                {
                    return 0;
                }
                else if (float.Parse(((ListViewItem)x).SubItems[col].Text) < float.Parse(((ListViewItem)y).SubItems[col].Text))
                {
                    return -1 * reverse;
                }
                return 1 * reverse;
            }
            return String.Compare(((ListViewItem)x).SubItems[col].Text, ((ListViewItem)y).SubItems[col].Text) * reverse;
        }
    }
}
