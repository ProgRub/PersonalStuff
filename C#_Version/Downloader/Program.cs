using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Downloader
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
            DownloaderForm form = new DownloaderForm();
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
