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
            for (int index = 0; index < form.LAFContainer.workingThreads.Count; index++)
            {
                form.LAFContainer.workingThreads[index].Join();
            }
            form.LAFContainer.SaveMusicFiles();
            System.Runtime.InteropServices.Marshal.ReleaseComObject(form.LAFContainer.iTunes);
            GC.Collect();
        }
    }
}
