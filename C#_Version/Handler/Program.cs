using System;
using System.Windows.Forms;

namespace Handler
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            HandlerForm form = new HandlerForm();
            Application.Run(form);
            form.LAFContainer.backgroundWork.Join();
            System.Runtime.InteropServices.Marshal.ReleaseComObject(form.LAFContainer.iTunes);
            GC.Collect();
        }
    }
}
