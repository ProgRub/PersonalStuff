using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.WindowsAPICodePack.Dialogs;
using System.IO;

namespace Downloader
{
    public partial class HomeScreen : UserControl
    {
        public DownloaderForm Window { get; set; }
        public CommonOpenFileDialog folderDialog { get; set; }
        public HomeScreen()
        {
            InitializeComponent();
			this.folderDialog = new CommonOpenFileDialog
			{
				IsFolderPicker = true
			};
		}

        private void HomeScreen_Enter(object sender, EventArgs e)
        {
            this.Window = this.Parent as DownloaderForm;
            this.textBoxDownloadsDir.Text = this.Window.LAFContainer.DownloadsDirectory;
            this.textBoxMusicOriginDir.Text = this.Window.LAFContainer.MusicOriginDirectory;
            this.textBoxMusicDestinyDir.Text = this.Window.LAFContainer.MusicDestinyDirectory;

        }

        private void buttonChooseDownloadsFolder_Click(object sender, EventArgs e)
        {
            this.folderDialog.InitialDirectory = this.Window.LAFContainer.CurrentDirectory;
            CommonFileDialogResult result = this.folderDialog.ShowDialog();
            if (result == CommonFileDialogResult.Ok && !string.IsNullOrWhiteSpace(this.folderDialog.FileName))
            {
                this.textBoxDownloadsDir.Text = this.folderDialog.FileName;
                this.Window.LAFContainer.DownloadsDirectory = this.folderDialog.FileName;
            }
        }

        private void buttonChooseMusicOriginFolder_Click(object sender, EventArgs e)
        {
            this.folderDialog.InitialDirectory = this.Window.LAFContainer.CurrentDirectory;
            CommonFileDialogResult result = this.folderDialog.ShowDialog();
            if (result == CommonFileDialogResult.Ok && !string.IsNullOrWhiteSpace(this.folderDialog.FileName))
            {
                this.textBoxMusicOriginDir.Text = this.folderDialog.FileName;
                this.Window.LAFContainer.MusicOriginDirectory = this.folderDialog.FileName;
            }
        }

        private void buttonChooseMusicDestinyFolder_Click(object sender, EventArgs e)
        {
            this.folderDialog.InitialDirectory = this.Window.LAFContainer.CurrentDirectory;
            CommonFileDialogResult result = this.folderDialog.ShowDialog();
            if (result == CommonFileDialogResult.Ok && !string.IsNullOrWhiteSpace(this.folderDialog.FileName))
            {
                this.textBoxMusicDestinyDir.Text = this.folderDialog.FileName;
                this.Window.LAFContainer.MusicDestinyDirectory = this.folderDialog.FileName;
            }
        }

        private void buttonDownloadMusic_Click(object sender, EventArgs e)
        {
            this.Window.LAFContainer.SaveDirectories();
            this.Hide();
			MusicScreen aux = new MusicScreen(this.Window)
			{
				Dock = DockStyle.Fill
			};
			this.Window.Controls.Add(aux);
            this.Window.ActiveControl = aux;
        }

        private void buttonYLModified_Click(object sender, EventArgs e)
        {
            this.Window.LAFContainer.SaveDirectories();
            this.Hide();
            long lastModifiedTime = this.Window.LAFContainer.GetLastModifiedTime();
			YearLyricsScreen aux = new YearLyricsScreen(this.Window, Directory.EnumerateFiles(this.Window.LAFContainer.MusicDestinyDirectory).Where(x => x.EndsWith(".mp3") && File.GetLastWriteTime(x).ToFileTime() > (lastModifiedTime - 5 * 60)).ToList())
			{
				Dock = DockStyle.Fill
			};
			this.Window.Controls.Add(aux);
            this.Window.ActiveControl = aux;
        }

        private void buttonYLAll_Click(object sender, EventArgs e)
        {
            this.Window.LAFContainer.SaveDirectories();
            this.Hide();
			YearLyricsScreen aux = new YearLyricsScreen(this.Window, Directory.EnumerateFiles(this.Window.LAFContainer.MusicDestinyDirectory).Where(x => x.EndsWith(".mp3")).ToList())
			{
				Dock = DockStyle.Fill
			};
			this.Window.Controls.Add(aux);
            this.Window.ActiveControl = aux;
        }

        private void buttonOptions_Click(object sender, EventArgs e)
        {
            this.Window.LAFContainer.SaveDirectories();
            this.Hide();
			OptionsScreen aux = new OptionsScreen(this.Window)
			{
				Dock = DockStyle.Fill
			};
			this.Window.Controls.Add(aux);
            this.Window.ActiveControl = aux;
        }

        private void buttonDownloadSchool_Click(object sender, EventArgs e)
        {
            this.Window.LAFContainer.SaveDirectories();
            this.Hide();
			SchoolScreen aux = new SchoolScreen(this.Window)
			{
				Dock = DockStyle.Fill
			};
			this.Window.Controls.Add(aux);
            this.Window.ActiveControl = aux;
        }
    }
}
