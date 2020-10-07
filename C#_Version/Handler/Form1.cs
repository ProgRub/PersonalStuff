using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Handler
{
    public partial class HandlerForm : Form
    {
        public ListsAndFiles LAFContainer { get; }
        public HandlerForm()
        {
            InitializeComponent();
            this.LAFContainer = new ListsAndFiles();
        }

        private void HandlerForm_FormClosed(object sender, FormClosedEventArgs e)
        {
            //BackgroundWorker worker = new BackgroundWorker();
            //worker.DoWork += new DoWorkEventHandler(this.LAFContainer.SaveAllToFiles);
            //worker.RunWorkerAsync();
            this.LAFContainer.SaveAllToFiles();
        }
    }
}
