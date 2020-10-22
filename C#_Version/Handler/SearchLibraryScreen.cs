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

namespace Handler
{
    public partial class SearchLibraryScreen : UserControl
    {
        private HandlerForm Window;
        public SearchLibraryScreen(HandlerForm window)
        {
            InitializeComponent();
            this.Window = window;
            this.listBoxResults.Items.AddRange(this.Window.LAFContainer.MusicFiles.Select(x => x.Filename).ToArray());
        }

        private void UpdateResults(int whichOne)
        {
            List<MusicFile> results = new List<MusicFile>(this.Window.LAFContainer.MusicFiles);
            int lenResults = results.Count;
            int index = 0;
            switch (whichOne)
            {
                case 0: //Album Artist
                    while (index < lenResults)
                    {
                        if (!results[index].AlbumArtist.ToLower().Contains(this.textBoxAlbumArtist.Text.ToLower()))
                        {
                            results.RemoveAt(index);
                            index--;
                            lenResults--;
                        }
                        index++;
                    }
                    break;
                case 1: //Contributing Artist
                    while (index < lenResults)
                    {
                        if (!results[index].ContributingArtists.Split(new string[] { ", " }, StringSplitOptions.RemoveEmptyEntries).Select(x => x.ToLower()).Contains(this.textBoxContributingArtist.Text.ToLower()))
                        {
                            results.RemoveAt(index);
                            index--;
                            lenResults--;
                        }
                        index++;
                    }
                    break;
                case 2: //Album
                    while (index < lenResults)
                    {
                        if (!results[index].Album.ToLower().Contains(this.textBoxAlbum.Text.ToLower()))
                        {
                            results.RemoveAt(index);
                            index--;
                            lenResults--;
                        }
                        index++;
                    }
                    break;
                case 3: //Title
                    while (index < lenResults)
                    {
                        if (!results[index].Title.ToLower().Contains(this.textBoxTitle.Text.ToLower()))
                        {
                            results.RemoveAt(index);
                            index--;
                            lenResults--;
                        }
                        index++;
                    }
                    break;
                case 4: //Year
                    bool over = this.textBoxYear.Text.StartsWith(">");
                    bool under = this.textBoxYear.Text.StartsWith("<");
                    try
                    {
                        int year = !over & !under ? Int32.Parse(this.textBoxYear.Text) : Int32.Parse(this.textBoxYear.Text.Substring(1));
                        while (index < lenResults)
                        {
                            if (over)
                            {
                                if (results[index].Year <= year)
                                {
                                    results.RemoveAt(index);
                                    index--;
                                    lenResults--;
                                }
                            }
                            else if (under)
                            {
                                if (results[index].Year >= year)
                                {
                                    results.RemoveAt(index);
                                    index--;
                                    lenResults--;
                                }
                            }
                            else
                            {
                                if (year != results[index].Year)
                                {
                                    results.RemoveAt(index);
                                    index--;
                                    lenResults--;
                                }
                            }
                            index++;
                        }
                    }
                    catch (FormatException)
                    {
                    }
                    break;
                case 5: //Genre
                    while (index < lenResults)
                    {
                        if (!results[index].Genre.ToLower().Contains(this.textBoxGenre.Text.ToLower()))
                        {
                            results.RemoveAt(index);
                            index--;
                            lenResults--;
                        }
                        index++;
                    }
                    break;
                default:
                    break;
            }
            this.listBoxResults.Items.Clear();
            this.listBoxResults.Items.AddRange(results.Select(x => x.Filename).ToArray());
        }

        private void textBoxAlbumArtist_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults(0);
        }

        private void textBoxContributingArtist_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults(1);
        }

        private void textBoxAlbum_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults(2);
        }

        private void textBoxTitle_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults(3);
        }

        private void textBoxYear_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults(4);
        }

        private void textBoxGenre_TextChanged(object sender, EventArgs e)
        {
            this.UpdateResults(5);
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
            this.Window.LAFContainer.SaveNumberFilesLastModified();
            this.Window.LAFContainer.SaveMusicFiles();
            this.Dispose();
            this.Window.Controls.OfType<HomeScreen>().ToList()[0].Visible = true;
            this.Window.ActiveControl = this.Window.Controls.OfType<HomeScreen>().ToList()[0];
        }

        private void buttonTrackDetails_Click(object sender, EventArgs e)
        {
            if (this.listBoxResults.SelectedItems.Count > 0)
            {
                this.Hide();
                TrackDetailsScreen aux = new TrackDetailsScreen(this.Window,this.Window.LAFContainer.MusicFiles.Where(x => this.listBoxResults.SelectedItems.Contains(x.Filename)).ToList());
                aux.Dock = DockStyle.Fill;
                this.Window.Controls.Add(aux);
                this.Window.ActiveControl = aux;
            }
        }
    }
}
