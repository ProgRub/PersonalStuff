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
    }
}
