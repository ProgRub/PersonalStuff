using System;
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
    }
}
