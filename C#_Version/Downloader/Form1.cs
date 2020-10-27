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

        private void DownloaderForm_FormClosed(object sender, FormClosedEventArgs e)
        {
            System.Runtime.InteropServices.Marshal.ReleaseComObject(this.LAFContainer.iTunes);
            System.GC.Collect();
        }
    }
}
