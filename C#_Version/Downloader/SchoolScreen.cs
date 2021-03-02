using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using Microsoft.VisualBasic.FileIO;

namespace Downloader
{
    public partial class SchoolScreen : UserControl
    {
        private DownloaderForm Window;
        private int NumberFiles;
        private string OneDrive, CurrentFile, ChosenDirectory;
        private List<string> PossibleDirectories, CheckedFiles;
        private Timer TimerCheckDownloads;
        public SchoolScreen(DownloaderForm window)
        {
            InitializeComponent();
            this.Window = window;
            this.Window.AcceptButton = this.buttonMoveFile;
            this.OneDrive = Path.Combine(new string[] { "C:", Path.DirectorySeparatorChar.ToString(), "Users", "ruben", "Onedrive - Universidade da Madeira", "Ano_3", "Semestre_2" });
            this.PossibleDirectories = new List<string>();
            this.CheckedFiles = new List<string>();
            foreach (string directory in Directory.EnumerateDirectories(this.OneDrive))
            {
                this.PossibleDirectories.Add(directory.Replace(this.OneDrive + Path.DirectorySeparatorChar.ToString(), ""));
                this.AddDirectories(directory);
            }
            this.dropdownDirectories.Items.AddRange(PossibleDirectories.ToArray());
            this.dropdownDirectories.Items.Add("Skip File");
            this.dropdownDirectories.Items.Add("Delete File");
            this.NumberFiles = 0;
            this.TimerCheckDownloads = new Timer();
            this.TimerCheckDownloads.Tick += new EventHandler(CheckDownloads);
            this.TimerCheckDownloads.Interval = 15;
            this.TimerCheckDownloads.Start();
        }

        private void buttonMoveFile_Click(object sender, EventArgs e)
        {
            this.ChosenDirectory = this.dropdownDirectories.SelectedItem.ToString();
            this.NumberFiles++;
            this.labelFilesFound.Text = this.NumberFiles + " Files Found";
            if (this.ChosenDirectory == "Delete File")
            {
                FileSystem.DeleteFile(this.CurrentFile, UIOption.OnlyErrorDialogs, RecycleOption.SendToRecycleBin);
                this.TextBoxFilesMoved.AppendText(this.CurrentFile + " deleted" + Environment.NewLine);
            }
            else if (this.ChosenDirectory != "Skip File")
            {
                if (this.textBoxFilename.Text.Contains(Path.DirectorySeparatorChar.ToString()))
                {
                    int index = this.dropdownDirectories.Items.IndexOf(this.ChosenDirectory) + 1;
                    this.ChosenDirectory = Path.Combine(this.ChosenDirectory, this.textBoxFilename.Text.Split(Path.DirectorySeparatorChar)[0]);
                    this.dropdownDirectories.Items.Insert(index, this.ChosenDirectory);
                    this.textBoxFilename.Text = this.textBoxFilename.Text.Split(Path.DirectorySeparatorChar)[1];
                    Directory.CreateDirectory(Path.Combine(this.OneDrive, this.ChosenDirectory));
                }
                bool replaced = false;
                while (true)
                {
                    try
                    {
                        File.Move(this.CurrentFile, Path.Combine(this.OneDrive, this.ChosenDirectory, this.textBoxFilename.Text));
                        this.TextBoxFilesMoved.AppendText(Path.Combine(this.ChosenDirectory, this.textBoxFilename.Text) +(replaced?" REPLACED":"")+ Environment.NewLine);
                        break;
                    }
                    catch (IOException)
                    {
                        FileSystem.DeleteFile(Path.Combine(this.OneDrive, this.ChosenDirectory, this.textBoxFilename.Text), UIOption.OnlyErrorDialogs, RecycleOption.SendToRecycleBin);
                        replaced = true;
                    }
                }
            }
            else
            {
                this.TextBoxFilesMoved.AppendText(this.textBoxFilename.Text + " SKIPPED" + Environment.NewLine);
            }
            this.textBoxFilename.Text = "";
            this.TextBoxFilesFound.AppendText(Environment.NewLine);
            this.CheckedFiles.Add(this.CurrentFile);
            this.TimerCheckDownloads.Start();
        }

        private void AddDirectories(string directory)
        {
            if (directory.Replace(this.OneDrive + Path.DirectorySeparatorChar, "").Count(x => x == Path.DirectorySeparatorChar) >= 2)
            {
                return;
            }
            foreach (string dir in Directory.EnumerateDirectories(directory))
            {
                this.PossibleDirectories.Add(dir.Replace(this.OneDrive + Path.DirectorySeparatorChar.ToString(), ""));
                this.AddDirectories(dir);
            }
        }

        private void CheckDownloads(object sender, EventArgs e)
        {
            foreach (string filename in Directory.EnumerateFiles(this.Window.LAFContainer.DownloadsDirectory))
            {
                if (!this.CheckedFiles.Contains(filename) && filename.EndsWith(".pdf"))
                {
                    this.CurrentFile = filename;
                    Console.WriteLine(this.CurrentFile);
                    this.TextBoxFilesFound.AppendText(Path.GetFileName(filename));
                    this.textBoxFilename.Text = Path.GetFileName(filename).Replace(" ", "_");
                    this.TimerCheckDownloads.Stop();
                    break;
                }
            }
        }
    }
}
