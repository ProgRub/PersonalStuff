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

namespace Handler
{
    public partial class HomeScreen : UserControl
    {
        private HandlerForm Window;
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
            AlbumPropertiesScreen aux = new AlbumPropertiesScreen();
            aux.Dock = DockStyle.Fill;
            aux.Visible = false;
            this.Window.Invoke((MethodInvoker)delegate { this.Window.Controls.Add(aux); });
            GenresColorsScreen aux2 = new GenresColorsScreen();
            aux2.Dock = DockStyle.Fill;
            aux2.Visible = false;
            this.Window.Invoke((MethodInvoker)delegate { this.Window.Controls.Add(aux2); });
            SearchLibraryScreen aux3 = new SearchLibraryScreen();
            aux3.Dock = DockStyle.Fill;
            aux3.Visible = false;
            this.Window.Invoke((MethodInvoker)delegate { this.Window.Controls.Add(aux3); });
        }

        private void HomeScreen_Enter(object sender, EventArgs e)
        {
            this.Window = this.Parent as HandlerForm;
            this.textBoxMusicDestinyDir.Text = this.Window.LAFContainer.MusicDestinyDirectory;
            this.Worker = new BackgroundWorker();
            this.Worker.DoWork += new DoWorkEventHandler(this.LoadNextScreens);
            this.Worker.RunWorkerAsync();
        }

        private void buttonChooseAlbum_Click(object sender, EventArgs e)
        {
            this.Hide();
            var aux = this.Window.Controls.OfType<AlbumPropertiesScreen>().ToList()[0];
            aux.Visible = true;
            this.Window.ActiveControl = aux;
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

        private void buttonGenresColors_Click(object sender, EventArgs e)
        {
            this.Hide();
            var aux = this.Window.Controls.OfType<GenresColorsScreen>().ToList()[0];
            aux.Visible = true;
            this.Window.ActiveControl = aux;
        }

        private void buttonSearchLibrary_Click(object sender, EventArgs e)
        {
            this.Hide();
            var aux = this.Window.Controls.OfType<SearchLibraryScreen>().ToList()[0];
            aux.Visible = true;
            this.Window.ActiveControl = aux;
        }
    }
}
