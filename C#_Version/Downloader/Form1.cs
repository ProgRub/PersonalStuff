using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Downloader
{
    public partial class DownloaderForm : Form
    {
        public ListsAndFiles LAFContainer { get; }
        public DownloaderForm()
        {
            InitializeComponent();
            this.LAFContainer = new ListsAndFiles();
        }

        private void Downloader_FormClosed(object sender, FormClosedEventArgs e)
        {
            //BackgroundWorker worker = new BackgroundWorker();
            //worker.DoWork += new DoWorkEventHandler(this.LAFContainer.SaveAllToFiles);
            //worker.RunWorkerAsync();
            this.LAFContainer.SaveAllToFiles();
        }
    }
}
