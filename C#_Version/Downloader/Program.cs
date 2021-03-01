using System;
using System.Security.Permissions;
using System.Windows.Forms;

namespace Downloader
{
    static class Program
    {
        static DownloaderForm form = null;
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Program.form = new DownloaderForm();
            Application.Run(form);
            try
            {
                System.Runtime.InteropServices.Marshal.ReleaseComObject(form.LAFContainer.iTunes);
                GC.Collect();
            }
            catch (NullReferenceException)
            {
                Console.WriteLine("iTunes not opened.");
            }
        }
        
    }
}
