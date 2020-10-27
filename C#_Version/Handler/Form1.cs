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
            System.Runtime.InteropServices.Marshal.ReleaseComObject(this.LAFContainer.iTunes);
            System.GC.Collect();
        }
    }
}
