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

        private void DownloaderForm_FormClosed(object sender, FormClosedEventArgs e)
        {
            try
            {
                System.Runtime.InteropServices.Marshal.ReleaseComObject(this.LAFContainer.iTunes);
                GC.Collect();
            }
            catch (NullReferenceException)
            {
                Console.WriteLine("iTunes not opened.");
            }
        }
    }
}
