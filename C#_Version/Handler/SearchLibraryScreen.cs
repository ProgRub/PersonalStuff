using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.VisualBasic.FileIO;
using System.IO;
using System.Threading;

namespace Handler
{
    public partial class SearchLibraryScreen : UserControl
    {
        private readonly HandlerForm Window;
        public SearchLibraryScreen(HandlerForm window)
        {
            InitializeComponent();
            this.Window = window;
            this.Window.AcceptButton = this.buttonTrackDetails;
            this.Window.CancelButton = this.buttonBack;
            this.textBoxAlbum.AutoCompleteCustomSource.AddRange(this.Window.LAFContainer.MusicFiles.Select(track => track.Album).ToArray());
            this.textBoxAlbumArtist.AutoCompleteCustomSource.AddRange(this.Window.LAFContainer.MusicFiles.Select(track => track.AlbumArtist).ToArray());
            this.textBoxContributingArtist.AutoCompleteCustomSource.AddRange(this.Window.LAFContainer.MusicFiles.Select(track => track.ContributingArtists).ToArray());
            this.textBoxGenre.AutoCompleteCustomSource.AddRange(this.Window.LAFContainer.GenresColors.Keys.ToArray());
            this.textBoxTitle.AutoCompleteCustomSource.AddRange(this.Window.LAFContainer.MusicFiles.Select(track => track.Title).ToArray());
            this.textBoxYear.AutoCompleteCustomSource.AddRange(this.Window.LAFContainer.MusicFiles.Select(track => track.Year.ToString()).ToArray());
            this.listBoxResults.Items.AddRange(this.Window.LAFContainer.MusicFiles.Select(x => x.Filename).ToArray());
        }

        #region Event Handlers

        private void textBoxAlbumArtist_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults();
        }

        private void textBoxContributingArtist_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults();
        }

        private void textBoxAlbum_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults();
        }

        private void textBoxTitle_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults();
        }

        private void textBoxYear_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults();
        }

        private void textBoxGenre_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults();
        }

        private void listBoxResults_KeyDown(object sender, KeyEventArgs e)
        {
            if (Keys.Delete == e.KeyCode)
            {
                for (int index = 0; index < this.listBoxResults.Items.Count; index++)
                {
                    if (this.listBoxResults.GetSelected(index))
                    {
                        int musicFileIndex = this.Window.LAFContainer.IndexOfMusicFile(this.listBoxResults.Items[index].ToString());
                        FileSystem.DeleteFile(Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, this.Window.LAFContainer.MusicFiles[musicFileIndex].Filename), UIOption.OnlyErrorDialogs, RecycleOption.SendToRecycleBin);
                        this.Window.LAFContainer.GetITunesTrack(this.Window.LAFContainer.MusicFiles[musicFileIndex].Title, this.Window.LAFContainer.MusicFiles[musicFileIndex].Album).Delete();
                        this.Window.LAFContainer.MusicFiles.RemoveAt(musicFileIndex);
                        this.listBoxResults.Items.RemoveAt(index);
                        index--;
                    }
                }
            }
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            this.Dispose();
            this.Window.Controls.OfType<HomeScreen>().ToList()[0].Visible = true;
            this.Window.ActiveControl = this.Window.Controls.OfType<HomeScreen>().ToList()[0];
        }

        private void buttonTrackDetails_Click(object sender, EventArgs e)
        {
            if (this.listBoxResults.SelectedItems.Count > 0)
            {
                this.Hide();
				TrackDetailsScreen aux = new TrackDetailsScreen(this.Window, this.Window.LAFContainer.MusicFiles.Where(x => this.listBoxResults.SelectedItems.Contains(x.Filename)).ToList())
				{
					Dock = DockStyle.Fill
				};
				this.Window.Controls.Add(aux);
                this.Window.ActiveControl = aux;
            }
        }
        #endregion

        private void UpdateResults()
        {
            List<MusicFile> results = new List<MusicFile>(this.Window.LAFContainer.MusicFiles);
            int lenResults = results.Count;
            int index = 0;
            bool removedItem = false;
            bool over;
            bool under;
            while (index < lenResults)
            {
                removedItem = false;
                if (this.textBoxAlbumArtist.Text != "" && !results[index].AlbumArtist.ToLower().Contains(this.textBoxAlbumArtist.Text.ToLower()))
                {
                    results.RemoveAt(index);
                    index--;
                    lenResults--;
                    removedItem = true;
                }
                if (!removedItem && this.textBoxContributingArtist.Text != "" && !results[index].ContributingArtists.Split(new string[] { ", " }, StringSplitOptions.RemoveEmptyEntries).Select(x => x.ToLower()).Contains(this.textBoxContributingArtist.Text.ToLower()))
                {
                    results.RemoveAt(index);
                    index--;
                    lenResults--;
                    removedItem = true;
                }
                if (!removedItem && this.textBoxAlbum.Text != "" && !results[index].Album.ToLower().Contains(this.textBoxAlbum.Text.ToLower()))
                {
                    results.RemoveAt(index);
                    index--;
                    lenResults--;
                    removedItem = true;
                }
                if (!removedItem && this.textBoxTitle.Text != "" && !results[index].Title.ToLower().Contains(this.textBoxTitle.Text.ToLower()))
                {
                    results.RemoveAt(index);
                    index--;
                    lenResults--;
                    removedItem = true;
                }
                if (!removedItem && this.textBoxYear.Text != "")
                {
                    over = this.textBoxYear.Text.StartsWith(">");
                    under = this.textBoxYear.Text.StartsWith("<");
                    try
                    {
                        int year = !over & !under ? Int32.Parse(this.textBoxYear.Text) : Int32.Parse(this.textBoxYear.Text.Substring(1));
                        if (over)
                        {
                            if (results[index].Year <= year)
                            {
                                results.RemoveAt(index);
                                index--;
                                lenResults--;
                                removedItem = true;
                            }
                        }
                        else if (under)
                        {
                            if (results[index].Year >= year)
                            {
                                results.RemoveAt(index);
                                index--;
                                lenResults--;
                                removedItem = true;
                            }
                        }
                        else
                        {
                            if ( year != results[index].Year)
                            {
                                results.RemoveAt(index);
                                index--;
                                lenResults--;
                                removedItem = true;
                            }
                        }
                    }
                    catch (FormatException) { }
                }
                if (!removedItem && this.textBoxGenre.Text != "" && !results[index].Genre.ToLower().Contains(this.textBoxGenre.Text.ToLower()))
                {
                    results.RemoveAt(index);
                    index--;
                    lenResults--;
                    removedItem = true;
                }
                index++;
            }
            this.listBoxResults.Items.Clear();
            this.listBoxResults.Items.AddRange(results.Select(x => x.Filename).ToArray());
        }
    }
}
