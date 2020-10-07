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
        public HomeScreen()
        {
            InitializeComponent();
            this.folderDialog = new CommonOpenFileDialog();
            this.folderDialog.IsFolderPicker = true;
        }

        private void HomeScreen_Load(object sender, EventArgs e)
        {
            this.Window = this.Parent as HandlerForm;
            this.textBoxMusicDestinyDir.Text = this.Window.LAFContainer.MusicDestinyDirectory;
        }

        private void buttonChooseAlbum_Click(object sender, EventArgs e)
        {
            this.Hide();
            AlbumPropertiesScreen aux = new AlbumPropertiesScreen();
            aux.Dock = DockStyle.Fill;
            this.Window.Controls.Add(aux);
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
            GenresColorsScreen aux = new GenresColorsScreen();
            aux.Dock = DockStyle.Fill;
            this.Window.Controls.Add(aux);
            this.Window.ActiveControl = aux;
        }
    }
}
