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

namespace Downloader
{
    public partial class OptionsScreen : UserControl
    {
        public DownloaderForm Window { get; set; }
        private List<List<Control>> ComponentsByLine;
        private bool NeedsConfirm;
        private int Mode;
        public OptionsScreen(DownloaderForm window)
        {
            InitializeComponent();
            this.Window = window;
            this.Window.CancelButton = this.buttonBack;
            this.ComponentsByLine = new List<List<Control>>();
            this.ComponentsByLine.Add(new List<Control>() { this.label1, this.textBox1 });
            this.ComponentsByLine.Add(new List<Control>() { this.label2, this.textBox2 });
            this.ComponentsByLine.Add(new List<Control>() { this.label3, this.textBox3 });
            this.ComponentsByLine.Add(new List<Control>() { this.label4, this.textBox4 });
            this.ComponentsByLine.Add(new List<Control>() { this.label5, this.textBox5 });
            this.ComponentsByLine.Add(new List<Control>() { this.label6, this.textBox6 });
            this.NeedsConfirm = false;
        }
        #region Event Handlers
        private void buttonGrimeArtistConfirm_Click(object sender, EventArgs e)
        {
            if (!this.NeedsConfirm)
            {
                this.NeedsConfirm = !this.NeedsConfirm;
                this.Mode = 0;
                this.AddToListbox();
                this.label1.Text = "New Artist";
                foreach (var line in ComponentsByLine.Skip(1))
                {
                    line[0].Visible = false;
                    line[1].Visible = false;
                }
                this.buttonSongSkipLyrics.Visible = false;
                this.buttonException.Visible = false;
                this.buttonURLReplacement.Visible = false;
                this.buttonGrimeArtistConfirm.Text = "Confirm";
                this.Window.AcceptButton = this.buttonGrimeArtistConfirm;
                return;
            }
            this.Window.AcceptButton = null;
            this.NeedsConfirm = !this.NeedsConfirm;
            this.listBoxToDelete.Items.Clear();
            switch (this.Mode)
            {
                case 0:
                    string grimeArtist = this.textBox1.Text.Trim();
                    if (grimeArtist != "" && !this.Window.LAFContainer.GrimeArtists.Contains(grimeArtist))
                    {
                        this.Window.LAFContainer.GrimeArtists.Add(grimeArtist);
                        this.listBoxToDelete.Items.Add(grimeArtist);
                    }
                    this.Window.LAFContainer.SaveGrimeArtists();
                    break;
                case 1:
                    string artist = this.textBox1.Text.Trim();
                    string album = this.textBox2.Text.Trim();
                    string title = this.textBox3.Text.Trim();
                    if (artist != "" && album != "" && title != "")
                    {
                        bool contains = false;
                        foreach (var item in this.Window.LAFContainer.SongsToSkipLyrics)
                        {
                            if (item[0] == artist && item[1] == album && item[2] == title)
                            {
                                contains = true;
                                break;
                            }
                        }
                        if (!contains)
                        {
                            var list = new List<string>() { artist, album, title };
                            this.Window.LAFContainer.SongsToSkipLyrics.Add(list);
                            this.listBoxToDelete.Items.Add(string.Join(" | ", list));
                        }
                    }
                    this.Window.LAFContainer.SaveExceptions();
                    break;
                case 2:
                    string oldArtist = this.textBox1.Text.Trim();
                    string oldAlbum = this.textBox2.Text.Trim();
                    string oldTitle = this.textBox3.Text.Trim();
                    string newArtist = this.textBox4.Text.Trim();
                    string newAlbum = this.textBox5.Text.Trim();
                    string newTitle = this.textBox6.Text.Trim();
                    if (oldArtist != "" && oldAlbum != "" && newArtist != "" && newAlbum != "")
                    {
                        var oldList = new List<string>() { oldArtist, oldAlbum, oldTitle };
                        var newList = new List<string>() { newArtist, newAlbum, newTitle };
                        this.Window.LAFContainer.ExceptionsReplacements[oldList] = newList;
                        this.listBoxToDelete.Items.Add(string.Join(" | ", oldList) + " ---> " + string.Join(" | ", newList));
                    }
                    this.Window.LAFContainer.SaveExceptions();
                    break;
                case 3:
                    string artistYear = this.textBox1.Text.Trim();
                    string albumYear = this.textBox2.Text.Trim();
                    if (artistYear != "" && albumYear != "")
                    {
                        var songToSkip = new List<string>() { artistYear, albumYear };
                        this.Window.LAFContainer.SongsToSkipYear.Add(songToSkip);
                        this.listBoxToDelete.Items.Add(string.Join(" | ", songToSkip));
                    }
                    this.Window.LAFContainer.SaveExceptions();
                    break;
                case 4:
                    string auxToReplace = this.textBox1.Text.Trim();
                    string auxReplacement = this.textBox2.Text.Trim();
                    if (auxToReplace.StartsWith("\"") && auxToReplace.EndsWith("\"") && auxReplacement.StartsWith("\"") && auxReplacement.EndsWith("\""))
                    {
                        string toReplace = auxToReplace.Substring(1, auxToReplace.LastIndexOf('\"') - 1);
                        string replacement = auxReplacement.Substring(1, auxToReplace.LastIndexOf('\"') - 1);
                        this.Window.LAFContainer.UrlReplacements[toReplace] = replacement;
                        this.listBoxToDelete.Items.Add("\"" + toReplace + "\" ---> \"" + replacement + "\"");
                    }
                    this.Window.LAFContainer.SaveExceptions();
                    break;
                default:
                    break;
            }
            foreach (var line in ComponentsByLine)
            {
                line[0].Visible = true;
                line[0].Text = "Input";
                line[1].Visible = true;
                line[1].Text = "";
            }
            this.buttonSongSkipYear.Visible = true;
            this.buttonSongSkipLyrics.Visible = true;
            this.buttonException.Visible = true;
            this.buttonURLReplacement.Visible = true;
            this.buttonGrimeArtistConfirm.Text = "Grime Artist";
        }

        private void buttonSongSkipYear_Click(object sender, EventArgs e)
        {
            this.NeedsConfirm = !this.NeedsConfirm;
            this.Mode = 3;
            this.AddToListbox();
            this.label1.Text = "Artist";
            this.label2.Text = "Album";
            foreach (var line in ComponentsByLine.Skip(2))
            {
                line[0].Visible = false;
                line[1].Visible = false;
            }
            this.buttonSongSkipYear.Visible = false;
            this.buttonSongSkipLyrics.Visible = false;
            this.buttonException.Visible = false;
            this.buttonURLReplacement.Visible = false;
            this.buttonGrimeArtistConfirm.Text = "Confirm";
        }

        private void buttonSongToSkipLyrics_Click(object sender, EventArgs e)
        {
            this.NeedsConfirm = !this.NeedsConfirm;
            this.Mode = 1;
            this.AddToListbox();
            this.label1.Text = "Artist";
            this.label2.Text = "Album";
            this.label3.Text = "Title";
            foreach (var line in ComponentsByLine.Skip(3))
            {
                line[0].Visible = false;
                line[1].Visible = false;
            }
            this.buttonSongSkipYear.Visible = false;
            this.buttonSongSkipLyrics.Visible = false;
            this.buttonException.Visible = false;
            this.buttonURLReplacement.Visible = false;
            this.buttonGrimeArtistConfirm.Text = "Confirm";
        }

        private void buttonException_Click(object sender, EventArgs e)
        {
            this.NeedsConfirm = !this.NeedsConfirm;
            this.Mode = 2;
            this.AddToListbox();
            this.label1.Text = "Old Artist";
            this.label2.Text = "Old Album";
            this.label3.Text = "Old Title";
            this.label4.Text = "New Artist";
            this.label5.Text = "New Album";
            this.label6.Text = "New Title";
            this.buttonSongSkipYear.Visible = false;
            this.buttonSongSkipLyrics.Visible = false;
            this.buttonException.Visible = false;
            this.buttonURLReplacement.Visible = false;
            this.buttonGrimeArtistConfirm.Text = "Confirm";
        }

        private void buttonURLReplacement_Click(object sender, EventArgs e)
        {
            this.NeedsConfirm = !this.NeedsConfirm;
            this.Mode = 4;
            this.AddToListbox();
            this.label1.Text = "To Replace";
            this.label2.Text = "Replacement";
            foreach (var line in ComponentsByLine.Skip(2))
            {
                line[0].Visible = false;
                line[1].Visible = false;
            }
            this.buttonSongSkipYear.Visible = false;
            this.buttonSongSkipLyrics.Visible = false;
            this.buttonException.Visible = false;
            this.buttonURLReplacement.Visible = false;
            this.buttonGrimeArtistConfirm.Text = "Confirm";
        }

        private void listBoxToDelete_KeyDown(object sender, KeyEventArgs e)
        {
            if (Keys.Delete == e.KeyCode)
            {
                switch (this.Mode)
                {
                    case 0:
                        for (int index = 0; index < this.listBoxToDelete.Items.Count; index++)
                        {
                            if (this.listBoxToDelete.GetSelected(index))
                            {
                                this.Window.LAFContainer.GrimeArtists.Remove(this.listBoxToDelete.Items[index].ToString());
                                this.listBoxToDelete.Items.RemoveAt(index);
                                index--;
                            }
                        }
                        this.Window.LAFContainer.SaveGrimeArtists();
                        break;
                    case 1:
                        for (int index = 0; index < this.listBoxToDelete.Items.Count; index++)
                        {
                            if (this.listBoxToDelete.GetSelected(index))
                            {
                                string[] listItem = this.listBoxToDelete.Items[index].ToString().Split(new string[] { " | " }, StringSplitOptions.None);
                                string artist = listItem[0];
                                string album = listItem[1];
                                string title = listItem[2];
                                foreach (var song in this.Window.LAFContainer.SongsToSkipLyrics)
                                {
                                    if (song[0] == artist && song[1] == album && song[2] == title)
                                    {
                                        this.Window.LAFContainer.SongsToSkipLyrics.Remove(song);
                                    }
                                }
                                this.listBoxToDelete.Items.RemoveAt(index);
                                index--;
                            }
                        }
                        this.Window.LAFContainer.SaveExceptions();
                        break;
                    case 2:
                        for (int index = 0; index < this.listBoxToDelete.Items.Count; index++)
                        {
                            if (this.listBoxToDelete.GetSelected(index))
                            {
                                string[] oldAndNew = this.listBoxToDelete.Items[index].ToString().Split(new string[] { " ---> " }, StringSplitOptions.None);
                                List<string> oldList = oldAndNew[0].Split(new string[] { " | " }, StringSplitOptions.None).ToList();
                                foreach (var key in this.Window.LAFContainer.ExceptionsReplacements.Keys)
                                {
                                    if (key[0] == oldList[0] && key[1] == oldList[1] && key[2] == oldList[2])
                                    {
                                        this.Window.LAFContainer.ExceptionsReplacements.Remove(key);
                                        break;
                                    }
                                }
                                this.listBoxToDelete.Items.RemoveAt(index);
                                index--;
                            }
                        }
                        this.Window.LAFContainer.SaveExceptions();
                        break;
                    case 3:
                        for (int index = 0; index < this.listBoxToDelete.Items.Count; index++)
                        {
                            if (this.listBoxToDelete.GetSelected(index))
                            {
                                List<string> song = this.listBoxToDelete.Items[index].ToString().Split(new string[] { " | " }, StringSplitOptions.None).ToList();
                                foreach (var key in this.Window.LAFContainer.ExceptionsReplacements.Keys)
                                {
                                    if (key[0] == song[0] && key[1] == song[1])
                                    {
                                        this.Window.LAFContainer.SongsToSkipYear.Remove(key);
                                        break;
                                    }
                                }
                                this.listBoxToDelete.Items.RemoveAt(index);
                                index--;
                            }
                        }
                        this.Window.LAFContainer.SaveExceptions();
                        break;
                    case 4:
                        for (int index = 0; index < this.listBoxToDelete.Items.Count; index++)
                        {
                            if (this.listBoxToDelete.GetSelected(index))
                            {
                                string[] auxList = this.listBoxToDelete.Items[index].ToString().Split(new string[] { " ---> " }, StringSplitOptions.None);
                                string auxToReplace = auxList[0];
                                string toReplace = auxToReplace.Substring(1, auxToReplace.LastIndexOf('\"') - 1);
                                this.Window.LAFContainer.UrlReplacements.Remove(toReplace);
                                this.listBoxToDelete.Items.RemoveAt(index);
                                index--;
                            }
                        }
                        this.Window.LAFContainer.SaveExceptions();
                        break;
                    default:
                        break;
                }
            }
        }
        private void buttonBack_Click(object sender, EventArgs e)
        {
            this.Dispose();
            this.Window.Controls.OfType<HomeScreen>().ToList()[0].Visible = true;
            this.Window.ActiveControl = this.Window.Controls.OfType<HomeScreen>().ToList()[0];
        }
        #endregion
        private void AddToListbox()
        {
            switch (this.Mode)
            {
                case 0:
                    this.listBoxToDelete.Items.AddRange(this.Window.LAFContainer.GrimeArtists.ToArray());
                    break;
                case 1:
                    foreach (var song in this.Window.LAFContainer.SongsToSkipLyrics)
                    {
                        this.listBoxToDelete.Items.Add(string.Join(" | ", song));
                    }
                    break;
                case 2:
                    foreach (var old in this.Window.LAFContainer.ExceptionsReplacements.Keys)
                    {
                        this.listBoxToDelete.Items.Add(string.Join(" | ", old) + " ---> " + string.Join(" | ", this.Window.LAFContainer.ExceptionsReplacements[old]));
                    }
                    break;
                case 3:
                    foreach (var song in this.Window.LAFContainer.SongsToSkipYear)
                    {
                        this.listBoxToDelete.Items.Add(string.Join(" | ", song));
                    }
                    break;
                case 4:
                    foreach (var old in this.Window.LAFContainer.UrlReplacements.Keys)
                    {
                        this.listBoxToDelete.Items.Add("\"" + old + "\" ---> \"" + this.Window.LAFContainer.UrlReplacements[old] + "\"");
                    }
                    break;
                default:
                    break;
            }
        }
    }
}
