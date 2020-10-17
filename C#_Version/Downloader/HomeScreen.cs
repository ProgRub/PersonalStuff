using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Runtime.CompilerServices;
using Microsoft.WindowsAPICodePack.Dialogs;
using System.IO;

namespace Downloader
{
    public partial class HomeScreen : UserControl
    {
        public DownloaderForm Window { get; set; }
        public CommonOpenFileDialog folderDialog { get; set; }
        private BackgroundWorker Worker;
        public HomeScreen()
        {
            InitializeComponent();
            this.folderDialog = new CommonOpenFileDialog();
            this.folderDialog.IsFolderPicker = true;

        }

        private void LoadNextScreens(object sender, DoWorkEventArgs e)
        {
            MusicScreen aux = new MusicScreen();
            aux.Dock = DockStyle.Fill;
            aux.Visible = false;
            this.Window.Invoke((MethodInvoker)delegate { this.Window.Controls.Add(aux); });
            YearLyricsScreen aux2 = new YearLyricsScreen();
            aux2.Dock = DockStyle.Fill;
            aux2.Visible = false;
            this.Window.Invoke((MethodInvoker)delegate { this.Window.Controls.Add(aux2); });
            SchoolScreen aux3 = new SchoolScreen();
            aux3.Dock = DockStyle.Fill;
            aux3.Visible = false;
            this.Window.Invoke((MethodInvoker)delegate { this.Window.Controls.Add(aux3); });
            OptionsScreen aux4 = new OptionsScreen();
            aux4.Dock = DockStyle.Fill;
            aux4.Visible = false;
            this.Window.Invoke((MethodInvoker)delegate { this.Window.Controls.Add(aux4); });
        }

        private void HomeScreen_Enter(object sender, EventArgs e)
        {
            this.Window = this.Parent as DownloaderForm;
            this.textBoxDownloadsDir.Text = this.Window.LAFContainer.DownloadsDirectory;
            this.textBoxMusicOriginDir.Text = this.Window.LAFContainer.MusicOriginDirectory;
            this.textBoxMusicDestinyDir.Text = this.Window.LAFContainer.MusicDestinyDirectory;
            this.Worker = new BackgroundWorker();
            this.Worker.DoWork += new DoWorkEventHandler(this.LoadNextScreens);
            this.Worker.RunWorkerAsync();

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
            if (!this.Worker.IsBusy)
            {
                this.Hide();
                var aux = this.Window.Controls.OfType<MusicScreen>().ToList()[0];
                aux.Visible = true;
                this.Window.ActiveControl =aux;
            }
        }

        private void buttonYLModified_Click(object sender, EventArgs e)
        {
            if (!this.Worker.IsBusy)
            {
                this.Hide();
                long lastModifiedTime = this.Window.LAFContainer.GetLastModifiedTime();
                YearLyricsScreen aux = this.Window.Controls.OfType<YearLyricsScreen>().ToList()[0];
                aux.setAttributes(Directory.EnumerateFiles(this.Window.LAFContainer.MusicDestinyDirectory).Where(x => x.EndsWith(".mp3") && File.GetLastWriteTime(x).ToFileTime() > (lastModifiedTime - 5 * 60)).ToList(), false);
                aux.Visible = true;
                this.Window.ActiveControl = aux;
            }
        }

        private void buttonYLAll_Click(object sender, EventArgs e)
        {
            if (!this.Worker.IsBusy)
            {
                this.Hide();
                YearLyricsScreen aux = this.Window.Controls.OfType<YearLyricsScreen>().ToList()[0];
                aux.setAttributes(Directory.EnumerateFiles(this.Window.LAFContainer.MusicDestinyDirectory).Where(x => x.EndsWith(".mp3")).ToList(), false);
                aux.Visible = true;
                this.Window.ActiveControl = aux;
            }
        }

        private void buttonOptions_Click(object sender, EventArgs e)
        {
            if (!this.Worker.IsBusy)
            {
                this.Hide();
                var aux = this.Window.Controls.OfType<OptionsScreen>().ToList()[0];
                aux.Visible = true;
                this.Window.ActiveControl = aux;
            }
        }

        private void buttonDownloadSchool_Click(object sender, EventArgs e)
        {
            if (!this.Worker.IsBusy)
            {
                this.Hide();
                var aux = this.Window.Controls.OfType<SchoolScreen>().ToList()[0];
                aux.Visible = true;
                this.Window.ActiveControl = aux;
            }
        }
    }
}
