using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.IO;
using Microsoft.VisualBasic.FileIO;

namespace Downloader
{
	public partial class MusicScreen : UserControl
	{
		public DownloaderForm Window { get; set; }
		private int NumberFilesFound;
		private readonly List<string> FileBuffer;
		private bool CanAdvance;
		private readonly List<string> NewFiles;
		private readonly Timer TimerCheckMusic;

		public MusicScreen(DownloaderForm window)
		{
			InitializeComponent();
			this.Window = window;
			this.Window.LAFContainer.OpenITunes();
			this.Window.AcceptButton = this.buttonEndCycleAdvance;
			this.NumberFilesFound = 0;
			this.FileBuffer = new List<string>();
			this.CanAdvance = false;
			this.NewFiles = new List<string>();
			this.labelFilesFound.Text = "0 Files Found";
			Process deemix = new Process();
			deemix.StartInfo.WorkingDirectory = Path.Combine(this.Window.LAFContainer.CurrentDirectory, "auxFiles", "deemix-pyweb-main");
			deemix.StartInfo.FileName = "deemix-pyweb.py";
            deemix.Start();
            this.TimerCheckMusic = new Timer();
			this.TimerCheckMusic.Tick += new EventHandler(CheckMusic);
			this.TimerCheckMusic.Interval = 150;
			this.TimerCheckMusic.Start();
		}
		private void CheckMusic(object sender, EventArgs e)
		{
			var files = Directory.EnumerateFiles(Path.Combine(this.Window.LAFContainer.MusicOriginDirectory)).ToList();
			foreach (string filename in files)
			{
				if (filename.EndsWith(".mp3") && !this.FileBuffer.Contains(filename))
				{
					this.FileBuffer.Add(filename);
					this.TextBoxFilesFound.AppendText((this.NumberFilesFound>0 ? Environment.NewLine:"")+ Path.GetFileName(filename) );
					this.NumberFilesFound++;
					this.labelFilesFound.Text = this.NumberFilesFound + " Files Found";
				}
			}
		}

		private void MoveOutOfBuffer()
		{
			this.NumberFilesFound = 0;
			foreach (string oldFilename in this.FileBuffer)
			{
				string newFilename = Path.GetFileName(oldFilename);
				newFilename.Replace("f_ck", "fuck").Replace("f___", "fuck").Replace("f__k", "fuck").Replace("sh_t", "shit").Replace("s__t", "shit").Replace("sh__", "shit").Replace("ni__as", "niggas").Replace(
							"F_ck", "Fuck").Replace("F__k", "Fuck").Replace("F___", "Fuck").Replace("Sh_t", "Shit").Replace("S__t", "Shit").Replace("Sh__", "Shit").Replace("Ni__as", "Niggas");
				newFilename = this.Window.LAFContainer.RemoveWordsFromWord(new List<string>() { "Remaster", "Album Version", "Stereo" }, newFilename);
				newFilename = Path.Combine(this.Window.LAFContainer.MusicDestinyDirectory, newFilename);
				this.Window.LAFContainer.TagChanges(oldFilename);
				if (!File.Exists(newFilename) && File.Exists(oldFilename))
				{
					File.Move(oldFilename, newFilename);
					this.TextBoxFilesMoved.AppendText((this.NumberFilesFound > 0 ? Environment.NewLine : "") + Path.GetFileName(newFilename));
					this.NumberFilesFound++;
					this.NewFiles.Add(newFilename);
				}
				else
				{
					string oldArtist = "";
					string oldAlbum = "";
					string newTitle = "";
					string newArtist = "";
					string newAlbum = "";
					using (var mp3ToSend = TagLib.File.Create(oldFilename))
					{
						oldArtist = mp3ToSend.Tag.AlbumArtists[0];
						oldAlbum = mp3ToSend.Tag.Album;
						mp3ToSend.Save();
					}
					using (var mp3ToCheck = TagLib.File.Create(newFilename))
					{
						newArtist = mp3ToCheck.Tag.AlbumArtists[0];
						newAlbum = mp3ToCheck.Tag.Album;
						newTitle = mp3ToCheck.Tag.Title;
						mp3ToCheck.Save();
					}
					if (oldArtist == newArtist && oldAlbum != newAlbum)
					{
						if (!File.Exists(newFilename) && File.Exists(oldFilename))
						{
							FileSystem.DeleteFile(newFilename, UIOption.OnlyErrorDialogs, RecycleOption.SendToRecycleBin);
							this.Window.LAFContainer.GetITunesTrack(newTitle, newAlbum).Delete();
							File.Move(oldFilename, newFilename);
							this.TextBoxFilesMoved.AppendText((this.NumberFilesFound > 0 ? Environment.NewLine : "") + Path.GetFileName(oldFilename) + " REPLACED");
							this.NumberFilesFound++;
							this.NewFiles.Add(newFilename);
						}
					}
					else if (oldArtist == newArtist && oldAlbum == newAlbum)
					{
						if (File.Exists(oldFilename))
						{
							FileSystem.DeleteFile(oldFilename, UIOption.OnlyErrorDialogs, RecycleOption.SendToRecycleBin);
							this.TextBoxFilesMoved.AppendText((this.NumberFilesFound > 0 ? Environment.NewLine : "") + Path.GetFileName(oldFilename) + " already exists, DELETED");
						}
					}
					else
					{
						string toAdd = " (";
						List<string> artistSplit = oldArtist.Split(new char[0], StringSplitOptions.RemoveEmptyEntries).ToList();
						if ("The" == artistSplit[0])
						{
							artistSplit.Remove("The");
						}
						if (artistSplit.Count == 1) { toAdd += artistSplit[0]; }
						else
						{
							foreach (string item in artistSplit)
							{
								toAdd += item.ToUpper()[0];
							}
						}
						toAdd += ").mp3";
						newFilename = newFilename.Substring(0, newFilename.LastIndexOf('.')) + toAdd;
						if (!File.Exists(newFilename) && File.Exists(oldFilename))
						{
							File.Move(oldFilename, newFilename);
							this.TextBoxFilesMoved.AppendText((this.NumberFilesFound > 0 ? Environment.NewLine : "") + Path.GetFileName(newFilename));
							this.NumberFilesFound++;
							this.NewFiles.Add(newFilename);
						}
						else
						{
							int fileNumber = 2;
							while (true)
							{
								using (var mp3ToCheck = TagLib.File.Create(newFilename))
								{
									newArtist = mp3ToCheck.Tag.AlbumArtists[0];
									newAlbum = mp3ToCheck.Tag.Album;
									mp3ToCheck.Save();
								}
								if (oldArtist == newArtist && oldAlbum == newAlbum)
								{
									if (File.Exists(oldFilename))
									{
										FileSystem.DeleteFile(oldFilename, UIOption.OnlyErrorDialogs, RecycleOption.SendToRecycleBin);
										this.TextBoxFilesMoved.AppendText((this.NumberFilesFound > 0 ? Environment.NewLine : "") + Path.GetFileName(oldFilename) + " already exists, DELETED");
									}
									break;
								}
								else
								{
									toAdd = " (" + fileNumber + ").mp3";
									newFilename = newFilename.Substring(0, newFilename.LastIndexOf('.')) + toAdd;
									if (!File.Exists(newFilename) && File.Exists(oldFilename))
									{
										File.Move(oldFilename, newFilename);
										this.TextBoxFilesMoved.AppendText((this.NumberFilesFound > 0 ? Environment.NewLine : "") + Path.GetFileName(newFilename));
										this.NumberFilesFound++;
										this.NewFiles.Add(newFilename);
										break;
									}
								}
								fileNumber++;
							}
						}
					}
				}
				this.labelFilesFound.Text = this.NumberFilesFound + " Files Moved";
			}
			this.CanAdvance = true;
			this.buttonEndCycleAdvance.Enabled = true;
		}

		private void buttonEndCycleAdvance_Click(object sender, EventArgs e)
		{
			if (!this.CanAdvance)
			{
				this.CanAdvance = true;
				this.TimerCheckMusic.Stop();
				this.buttonEndCycleAdvance.Text = "Get Album Year And Lyrics";
				this.buttonEndCycleAdvance.Enabled = false;
				this.MoveOutOfBuffer();
			}
			else
			{
				this.Hide();
				YearLyricsScreen aux = new YearLyricsScreen(this.Window, this.NewFiles);
				aux.Dock = DockStyle.Fill;
				this.Window.Controls.Add(aux);
				this.Window.ActiveControl = aux;
			}
		}
	}
}
