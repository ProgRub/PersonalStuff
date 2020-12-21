using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Diagnostics;
using System.Data;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using HtmlAgilityPack;
using System.Media;
using System.Net;

namespace Downloader
{
	public partial class YearLyricsScreen : UserControl
	{
		public DownloaderForm Window { get; set; }
		public List<string> NewFiles;
		public Dictionary<string, int> PagesVisited_Year;
		public int NumberFilesProcessed;
		private bool ErrorOcurred, SkipYear, SkipLyrics;
		private int NUMBER_OF_THREADS = 5;
		private List<int> WorkersLineIndex;
		public Semaphore SemError, SemErrorHandled, SemAllFiles;
		private int WorkerIndexError;
		private System.Windows.Forms.Timer Clock;
		private static object Mutex = new object();
		private DateTime StartTime;
		private int CurrentLine;
		private int Hours, Minutes;

		public YearLyricsScreen(DownloaderForm window, List<string> newFiles)
		{
			InitializeComponent();
			this.Window = window;
			this.Window.LAFContainer.OpenITunes();
			this.StartTime = DateTime.Now;
			this.Clock = new System.Windows.Forms.Timer
			{
				Interval =  1000*60
			};
			this.Clock.Tick += new EventHandler(this.Clock_Tick);
			this.Minutes = 0;
			this.Hours = 0;
			this.Clock.Start();
			this.SkipLyrics = this.SkipYear = false;
			this.PagesVisited_Year = new Dictionary<string, int>();
			this.NumberFilesProcessed = 0;
			this.ErrorOcurred = false;
			this.NewFiles = newFiles;
			this.SemAllFiles = new Semaphore(0, 1);
			this.SemError = new Semaphore(1, 1);
			this.SemErrorHandled = new Semaphore(0, 1);
			this.WorkerIndexError = -1;
			this.Window.WindowState = FormWindowState.Maximized;
			this.CurrentLine = 0;
			try
			{
				Process.GetProcessesByName("python")[0].Kill();
			}
			catch (IndexOutOfRangeException)
			{
			}
		}
#warning TODO: When one thread finishes, rearrange files per threads

		private void Clock_Tick(object sender, EventArgs e)
		{
			Console.WriteLine("HERE");
			this.Minutes++;
			if (this.Minutes == 60) { 
				this.Hours++;
			}
			this.Minutes %= 60;
			this.labelClock.Text = String.Format("Time Elapsed: {0}:{1}", this.Hours.ToString("D2"), this.Minutes.ToString("D2"));
		}

		#region EventHandlers
		private void buttonTryAgain_Click(object sender, EventArgs e)
		{
			if (this.buttonTryAgain.Enabled)
			{
				this.SemErrorHandled.Release();
			}
		}

		private void buttonSkipYear_Click(object sender, EventArgs e)
		{
			if (this.buttonSkipYear.Enabled)
			{
				this.SkipYear = true;
				this.SemErrorHandled.Release();
			}
		}

		private void buttonSkipLyrics_Click(object sender, EventArgs e)
		{
			if (this.buttonSkipLyrics.Enabled)
			{
				this.SkipLyrics = true;
				this.SemErrorHandled.Release();
			}
		}

		private void YearLyricsScreen_Enter(object sender, EventArgs e)
		{
			Task.Delay(250).ContinueWith(t => this.StartThreads());
		}
		#endregion

		private void StartThreads()
		{
			this.NUMBER_OF_THREADS = Math.Min(this.NewFiles.Count, this.NUMBER_OF_THREADS);
			Action update;
			for (int index = 0; index < NUMBER_OF_THREADS; index++)
			{
				update = () => this.textBoxThreadStatus.AppendText("Thread " + index + Environment.NewLine);
				this.textBoxThreadStatus.Invoke(update);
			}
			update = () => this.textBoxThreadStatus.AppendText(String.Format("All Files: {0}/{1} Files Processed" + Environment.NewLine, this.NumberFilesProcessed, this.NewFiles.Count));
			this.textBoxThreadStatus.Invoke(update);
			Thread aux;
			this.WorkersLineIndex = new List<int>();
			int filesPerThread = this.NewFiles.Count / this.NUMBER_OF_THREADS;
			List<int> filesPerThreadList = new List<int>();
			for (int index = 0; index < NUMBER_OF_THREADS; index++)
			{
				filesPerThreadList.Add(filesPerThread);
			}
			int indexThreads = 0;
			int totalFiles = this.NewFiles.Count - filesPerThread * NUMBER_OF_THREADS;
			while (totalFiles > 0)
			{
				filesPerThreadList[indexThreads]++;
				totalFiles--;
				indexThreads = (indexThreads + 1) % NUMBER_OF_THREADS;
			}
			int previousFiles = 0;
			for (int index = 0; index < NUMBER_OF_THREADS; index++)
			{
				aux = new Thread(this.GetLyricsAndYear)
				{
					IsBackground = true
				};
				this.WorkersLineIndex.Add(0);
				if (index != 0)
				{
					previousFiles += filesPerThreadList[index - 1];
				}
				aux.Start(new object[2] { index, this.NewFiles.Skip(previousFiles).Take(filesPerThreadList[index]).ToList() });
			}
			this.SemAllFiles.WaitOne();
			this.FinishedAllFiles();
			Thread saveExceptions = new Thread(this.Window.LAFContainer.SaveExceptions);
			Thread saveMFs = new Thread(this.Window.LAFContainer.SaveMusicFiles);
			saveExceptions.Start();
			saveMFs.Start();
		}

		public void DisableComponents()
		{
			lock (Mutex)
			{
				Action update = () => this.Window.AcceptButton = null;
				this.Window.Invoke(update);
				update = () => { this.textBoxAlbum.ReadOnly = true; this.textBoxAlbum.Text = ""; };
				this.textBoxAlbum.Invoke(update);
				update = () => { this.textBoxArtist.ReadOnly = true; this.textBoxArtist.Text = ""; };
				this.textBoxArtist.Invoke(update);
				update = () => { this.textBoxTitle.ReadOnly = true; this.textBoxTitle.Text = ""; };
				this.textBoxTitle.Invoke(update);
				update = () => { this.textBoxYear.ReadOnly = true; this.textBoxYear.Text = ""; };
				this.textBoxYear.Invoke(update);
				update = () => this.labelUrlBeingChecked.Text = "Genius URL";
				this.labelUrlBeingChecked.Invoke(update);
				update = () => this.buttonSkipYear.Enabled = false;
				this.buttonSkipYear.Invoke(update);
				update = () => this.buttonTryAgain.Enabled = false;
				this.buttonTryAgain.Invoke(update);
				update = () => this.buttonSkipLyrics.Enabled = false;
				this.buttonSkipLyrics.Invoke(update);
			}
		}

		public void EnableComponents(bool forAlbumYear, string artist, string album, string title, string year, string url)
		{
			lock (Mutex)
			{
				Action update = () => this.Window.AcceptButton = this.buttonTryAgain;
				this.Window.Invoke(update);
				update = () => { this.textBoxArtist.Text = artist; this.textBoxArtist.ReadOnly = false; };
				this.textBoxArtist.Invoke(update);
				update = () => this.textBoxAlbum.Text = album;
				this.textBoxAlbum.Invoke(update);
				update = () => { this.textBoxTitle.Text = title; this.textBoxTitle.ReadOnly = false; };
				this.textBoxTitle.Invoke(update);
				update = () => this.labelUrlBeingChecked.Text = url;
				this.labelUrlBeingChecked.Invoke(update);
				if (forAlbumYear)
				{
					update = () => this.textBoxYear.Text = year;
					this.textBoxYear.Invoke(update);
					update = () => this.textBoxAlbum.ReadOnly = false;
					this.textBoxAlbum.Invoke(update);
					update = () => this.buttonSkipYear.Enabled = true;
					this.buttonSkipYear.Invoke(update);
				}
				else
				{
					update = () => this.buttonSkipLyrics.Enabled = true;
					this.buttonSkipLyrics.Invoke(update);
				}
				update = () => this.buttonTryAgain.Enabled = true;
				this.buttonTryAgain.Invoke(update);
			}
		}

		private void FinishedAllFiles()
		{
			Action update = () => this.textBoxArtist.Visible = false;
			this.textBoxArtist.Invoke(update);
			TimeSpan elapsedTime = DateTime.Now - this.StartTime;
			update = () => this.labelClock.Text = "Time Elapsed: " + elapsedTime.ToString(@"hh\:mm\:ss");
			this.labelClock.Invoke(update);
			update = () => this.textBoxTitle.Visible = false;
			this.textBoxTitle.Invoke(update);
			update = () => this.textBoxYear.Visible = false;
			this.textBoxYear.Invoke(update);
			update = () => this.textBoxAlbum.Visible = false;
			this.textBoxAlbum.Invoke(update);
			update = () => this.labelArtist.Visible = false;
			this.labelArtist.Invoke(update);
			update = () => this.labelAlbum.Visible = false;
			this.labelAlbum.Invoke(update);
			update = () => this.labelTitle.Visible = false;
			this.labelTitle.Invoke(update);
			update = () => this.labelYear.Visible = false;
			this.labelYear.Invoke(update);
			update = () => this.labelUrlBeingChecked.Visible = false;
			this.labelUrlBeingChecked.Invoke(update);
			update = () => this.buttonSkipYear.Visible = false;
			this.buttonSkipYear.Invoke(update);
			update = () => this.buttonSkipLyrics.Visible = false;
			this.buttonSkipLyrics.Invoke(update);
			update = () => this.buttonTryAgain.Visible = false;
			this.buttonTryAgain.Invoke(update);
			update = () =>
			{
				this.textBoxThreadStatus.Select(this.textBoxThreadStatus.GetFirstCharIndexFromLine(NUMBER_OF_THREADS), this.textBoxThreadStatus.Lines[NUMBER_OF_THREADS].Length);
				this.textBoxThreadStatus.SelectedText = String.Format("All Files: {0}/{1} Files Processed. All Done!", this.NumberFilesProcessed, this.NewFiles.Count);
			};
			this.textBoxThreadStatus.Invoke(update);
		}

		private void AddToOutput(string artist, string album, string title, int threadIndex)
		{
			lock (Mutex)
			{
				int line = this.CurrentLine;
				this.CurrentLine++;
				this.WorkersLineIndex[threadIndex] = line;
				Action update = () =>
				{
					this.richTextBoxArtist.AppendText(artist + Environment.NewLine);
					this.richTextBoxArtist.Select(this.richTextBoxArtist.GetFirstCharIndexFromLine(line), this.richTextBoxArtist.Lines[line].Length);
					this.richTextBoxArtist.SelectionColor = Color.Yellow;
					this.richTextBoxArtist.ScrollToCaret();
				};
				this.richTextBoxArtist.BeginInvoke(update);
				update = () =>
				{
					this.richTextBoxAlbum.AppendText(album + Environment.NewLine);
					this.richTextBoxAlbum.Select(this.richTextBoxAlbum.GetFirstCharIndexFromLine(line), this.richTextBoxAlbum.Lines[line].Length);
					this.richTextBoxAlbum.SelectionColor = Color.Yellow;
					this.richTextBoxAlbum.ScrollToCaret();
				};
				this.richTextBoxAlbum.BeginInvoke(update);
				update = () =>
				{
					this.richTextBoxTitle.AppendText(title + Environment.NewLine);
					this.richTextBoxTitle.Select(this.richTextBoxTitle.GetFirstCharIndexFromLine(line), this.richTextBoxTitle.Lines[line].Length);
					this.richTextBoxTitle.SelectionColor = Color.Yellow;
					this.richTextBoxTitle.ScrollToCaret();
				};
				this.richTextBoxTitle.BeginInvoke(update);
			}
		}

		//private void ChangeOutput(int whichBox,bool gettingYear)
		//{
		//    RichTextBox boxToUpdate= this.richTextBoxArtist;
		//    switch (whichBox)
		//    {
		//        case 0:
		//            boxToUpdate = this.richTextBoxArtist;
		//            break;
		//        case 1:
		//            boxToUpdate = this.richTextBoxAlbum;
		//            break;
		//        case 2:
		//            boxToUpdate = this.richTextBoxTitle;
		//            break;
		//        default:
		//            break;
		//    }
		//    int start_index = boxToUpdate.GetFirstCharIndexFromLine(boxToUpdate.Lines.Length-1);
		//    int count = boxToUpdate.Lines[boxToUpdate.Lines.Length - 1].Length;

		//    // Eat new line chars
		//    //if (a_line < richTextBox.Lines.Length - 1)
		//    //{
		//    //    count += richTextBox.GetFirstCharIndexFromLine(a_line + 1) -
		//    //        ((start_index + count - 1) + 1);
		//    //}

		//    boxToUpdate.Text = boxToUpdate.Text.Remove(start_index, count);
		//    this.AddToOutput();
		//    this.ChangeTextColor(!gettingYear);
		//}

		private void ChangeTextColor(int mode, int threadIndex, int filesProcessed, int totalFiles)
		{
			lock (Mutex)
			{
				Action update;
				int lineIndex = this.WorkersLineIndex[threadIndex];
				if (mode==0)
				{
					update = () =>
					{
						this.richTextBoxArtist.Select(this.richTextBoxArtist.GetFirstCharIndexFromLine(lineIndex), this.richTextBoxArtist.Lines[lineIndex].Length);
						this.richTextBoxArtist.SelectionColor = Color.DarkGreen;
					};
					this.richTextBoxArtist.BeginInvoke(update);
					update = () =>
					{
						this.richTextBoxAlbum.Select(this.richTextBoxAlbum.GetFirstCharIndexFromLine(lineIndex), this.richTextBoxAlbum.Lines[lineIndex].Length);
						this.richTextBoxAlbum.SelectionColor = Color.DarkGreen;
					};
					this.richTextBoxAlbum.BeginInvoke(update);
					update = () =>
					{
						this.richTextBoxTitle.Select(this.richTextBoxTitle.GetFirstCharIndexFromLine(lineIndex), this.richTextBoxTitle.Lines[lineIndex].Length);
						this.richTextBoxTitle.SelectionColor = Color.DarkGreen;
					};
					this.richTextBoxTitle.BeginInvoke(update);
				}
				else if (mode == 1)
				{
					update = () =>
					{
						this.richTextBoxArtist.Select(this.richTextBoxArtist.GetFirstCharIndexFromLine(lineIndex), this.richTextBoxArtist.Lines[lineIndex].Length);
						this.richTextBoxArtist.SelectionColor = Color.Aquamarine;
					};
					this.richTextBoxArtist.BeginInvoke(update);
					update = () =>
					{
						this.richTextBoxAlbum.Select(this.richTextBoxAlbum.GetFirstCharIndexFromLine(lineIndex), this.richTextBoxAlbum.Lines[lineIndex].Length);
						this.richTextBoxAlbum.SelectionColor = Color.Aquamarine;
					};
					this.richTextBoxAlbum.BeginInvoke(update);
					update = () =>
					{
						this.richTextBoxTitle.Select(this.richTextBoxTitle.GetFirstCharIndexFromLine(lineIndex), this.richTextBoxTitle.Lines[lineIndex].Length);
						this.richTextBoxTitle.SelectionColor = Color.Aquamarine;
					};
					this.richTextBoxTitle.BeginInvoke(update);
				}
				else
				{
					update = () =>
					{
						this.richTextBoxArtist.Select(this.richTextBoxArtist.GetFirstCharIndexFromLine(lineIndex), this.richTextBoxArtist.Lines[lineIndex].Length);
						this.richTextBoxArtist.SelectionColor = Color.Lime;
					};
					this.richTextBoxArtist.BeginInvoke(update);
					update = () =>
					{
						this.richTextBoxAlbum.Select(this.richTextBoxAlbum.GetFirstCharIndexFromLine(lineIndex), this.richTextBoxAlbum.Lines[lineIndex].Length);
						this.richTextBoxAlbum.SelectionColor = Color.Lime;
					};
					this.richTextBoxAlbum.BeginInvoke(update);
					update = () =>
					{
						this.richTextBoxTitle.Select(this.richTextBoxTitle.GetFirstCharIndexFromLine(lineIndex), this.richTextBoxTitle.Lines[lineIndex].Length);
						this.richTextBoxTitle.SelectionColor = Color.Lime;
					};
					this.richTextBoxTitle.BeginInvoke(update);
					update = () =>
					{
						this.textBoxThreadStatus.Select(this.textBoxThreadStatus.GetFirstCharIndexFromLine(threadIndex), this.textBoxThreadStatus.Lines[threadIndex].Length);
						this.textBoxThreadStatus.SelectedText = "Thread " + threadIndex + ": " + filesProcessed + "/" + totalFiles + " Files Processed";
						this.textBoxThreadStatus.Select(this.textBoxThreadStatus.GetFirstCharIndexFromLine(NUMBER_OF_THREADS), this.textBoxThreadStatus.Lines[NUMBER_OF_THREADS].Length);
						this.textBoxThreadStatus.SelectedText = String.Format("All Files: {0}/{1} Files Processed", this.NumberFilesProcessed, this.NewFiles.Count);
					};
					this.textBoxThreadStatus.BeginInvoke(update);
				}
			}
		}

		private string NamingConventions(string namePar)
		{
			string name = namePar.ToLower();
			if (name.Contains("pt.") || name.Contains("part.") || name.Contains("pts.") || name.Contains("mr.") || name.Contains("vol."))
			{
				name = name.Replace(".", " ");
			}
			foreach (var key in this.Window.LAFContainer.UrlReplacements.Keys)
			{
				name = name.Replace(key, this.Window.LAFContainer.UrlReplacements[key]);
			}
			var auxList = name.Split(null as char[], StringSplitOptions.RemoveEmptyEntries);
			for (int index = 0; index < auxList.Length; index++)
			{
				auxList[index] = auxList[index].Trim();
			}
			name = string.Join("-", auxList);
			return char.ToUpper(name[0]) + name.Substring(1).ToLower();
		}

		private void ChangeArtistAlbumTitle(bool forAlbumYear, ref string artist, ref string album, ref string title, uint trackCount)
		{
			List<string> CurrentKey = new List<string>() { artist, album, title };
			if (!forAlbumYear || trackCount < 5)
			{
				foreach (List<string> key in this.Window.LAFContainer.ExceptionsReplacements.Keys)
				{
					if (CurrentKey[0] == key[0] && CurrentKey[1] == key[1] && key[2] == "")
					{
						artist = this.Window.LAFContainer.ExceptionsReplacements[key][0];
						album = this.Window.LAFContainer.ExceptionsReplacements[key][1];
					}
					else if (CurrentKey[0] == key[0] && CurrentKey[1] == key[1] && CurrentKey[2] == key[2])
					{
						artist = this.Window.LAFContainer.ExceptionsReplacements[key][0];
						album = this.Window.LAFContainer.ExceptionsReplacements[key][1];
						title = this.Window.LAFContainer.ExceptionsReplacements[key][2];
						break;
					}
				}
			}
			else
			{
				foreach (List<string> key in this.Window.LAFContainer.ExceptionsReplacements.Keys)
				{
					if (CurrentKey[0] == key[0] && CurrentKey[1] == key[1] && key[2] == "")
					{
						artist = this.Window.LAFContainer.ExceptionsReplacements[key][0];
						album = this.Window.LAFContainer.ExceptionsReplacements[key][1];
						break;
					}
				}
			}
		}

		private object CheckIfWebpageExists(bool forAlbumYear, string artist, string album, string title, ref string year)
		{
			string url;
			if (forAlbumYear)
			{
				url = "https://www.genius.com/albums/" + this.NamingConventions(artist) + "/" + this.NamingConventions(album);
				if (this.PagesVisited_Year.Keys.Contains(artist + album))
				{
					year = this.PagesVisited_Year[artist + album].ToString();
					return "Skip";
				}
			}
			else
			{
				url = "https://genius.com/" + this.NamingConventions(artist + " " + title) + "-lyrics";
			}
			var htmlWeb = new HtmlWeb();
			var htmlDoc = htmlWeb.Load(url);
			var pageTitle = htmlDoc.DocumentNode.Descendants("title").ToList()[0];
			if (this.PagesVisited_Year.Keys.Contains(artist + album) && forAlbumYear)
			{
				year = this.PagesVisited_Year[artist + album].ToString();
				return "Skip";
			}
			if (pageTitle.InnerText == "Burrr! | Genius" || pageTitle.InnerText == "Application Error")
			{
				return null;
			}
			return htmlDoc;
		}

		private void SetYearInFile(string filename, string year)
		{
			////Console.WriteLine(filename + " SetYearInFile");
			if (year != "Skip")
			{
				using (var mp3 = TagLib.File.Create(filename))
				{
					mp3.Tag.Year = Convert.ToUInt32(year);
					mp3.Save();
				}
			}
		}
		private void GetYear(int threadIndex, string filename, ref string artist, ref string album, ref string title, ref string year, uint trackCount)
		{
			List<string> key = new List<string>(3);
			List<string> value = new List<string>(3);
			key.Add(artist); key.Add(album); key.Add(title);
			while (true)
			{
				//Console.WriteLine("3Thread " + threadIndex);
				var htmlDoc = this.CheckIfWebpageExists(true, artist, album, title, ref year);
				if (htmlDoc != null && htmlDoc.ToString() == "Skip")
				{
					if (this.ErrorOcurred && threadIndex == this.WorkerIndexError)
					{
						this.SemError.Release();
						this.ErrorOcurred = false;
					}
					this.SetYearInFile(filename, year);
					return;
				}
				if (htmlDoc != null)
				{
					////Console.WriteLine(threadIndex + " GetYear");
					string yearTemp = "";
					var soup = (HtmlAgilityPack.HtmlDocument)htmlDoc;
					foreach (var div in soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "metadata_unit").ToList())
					{
						yearTemp += div.InnerText.Trim();
						break;
					}
					year = yearTemp.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries).Last();
					if (!this.PagesVisited_Year.ContainsKey(artist + album))
					{
						this.PagesVisited_Year.Add(artist + album, Int32.Parse(year));
					}
					if (this.ErrorOcurred && threadIndex == this.WorkerIndexError)
					{
						if (key[2] == value[2])
						{
							key[2] = value[2] = "";
						}
						try
						{
							this.Window.LAFContainer.ExceptionsReplacements[key] = value;
						}
						catch (ArgumentException)
						{
							this.Window.LAFContainer.ExceptionsReplacements[key] = value;
						}
						this.ErrorOcurred = false;
						this.WorkerIndexError = -1;
						this.SemError.Release();
					}
					this.SetYearInFile(filename, year);
					return;
				}
				else
				{
					if (trackCount < 5)
					{
						htmlDoc = this.CheckIfWebpageExists(false, artist, album, title, ref year);
						if (htmlDoc != null)
						{
							var soup = (HtmlAgilityPack.HtmlDocument)htmlDoc;
							var auxList = soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "HeaderMetadata__Section-sc-1p42fnf-2 hAhJBU").ToList();
							if (auxList.Count != 0)
							{
								foreach (var div in auxList)
								{
									if (div.InnerText.Contains("Release Date"))
									{
										var aux = div.InnerText.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
										year = aux.Last().Trim();
										if (this.ErrorOcurred && threadIndex == this.WorkerIndexError)
										{
											if (key[2] == value[2])
											{
												key[2] = value[2] = "";
											}
											try
											{
												this.Window.LAFContainer.ExceptionsReplacements[key] = value;
											}
											catch (ArgumentException)
											{
												this.Window.LAFContainer.ExceptionsReplacements[key] = value;
											}
											this.ErrorOcurred = false;
											this.WorkerIndexError = -1;
											this.SemError.Release();
										}
										this.SetYearInFile(filename, year);
										return;
									}
								}
							}
							else
							{
								auxList = soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "metadata_unit metadata_unit--table_row").ToList();
								foreach (var div in auxList)
								{
									if (div.InnerText.Contains("Release Date"))
									{
										var aux = div.InnerText.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
										year = aux.Last().Trim();
										if (this.ErrorOcurred && threadIndex == this.WorkerIndexError)
										{
											if (key[2] == value[2])
											{
												key[2] = value[2] = "";
											}
											try
											{
												this.Window.LAFContainer.ExceptionsReplacements[key] = value;
											}
											catch (ArgumentException)
											{
												this.Window.LAFContainer.ExceptionsReplacements[key] = value;
											}
											this.ErrorOcurred = false;
											this.WorkerIndexError = -1;
											this.SemError.Release();
										}
										this.SetYearInFile(filename, year);
										return;
									}
								}
							}
						}
					}
					this.SemError.WaitOne();
					this.WorkerIndexError = threadIndex;
					this.ErrorOcurred = true;
					string url = "https://genius.com/" + this.NamingConventions(artist + " " + title) + "-lyrics";
					SystemSounds.Exclamation.Play();
					if (trackCount < 5)
					{
						//worker.ReportProgress(6, "https://genius.com/" + this.NamingConventions(artist + " " + title) + "-lyrics");
						Process.Start(string.Format("https://www.google.com.tr/search?q={0}", artist.Replace(" &", "").Replace(" ", "+") + "+" + title.Replace(" &", "").Replace(" ", "+") + "+lyrics+site:Genius.com"));
					}
					else
					{
						url = "https://www.genius.com/albums/" + this.NamingConventions(artist) + "/" + this.NamingConventions(album);
						//worker.ReportProgress(6, "https://www.genius.com/albums/" + this.NamingConventions(artist) + "/" + this.NamingConventions(album));
						Process.Start(string.Format("https://www.google.com.tr/search?q={0}", artist.Replace(" &", "").Replace(" ", "+") + "+" + album.Replace(" &", "").Replace(" ", "+") + "+site:Genius.com"));
					}
					this.EnableComponents(true, artist, album, title, year, url);
					this.SemErrorHandled.WaitOne();
					if (this.SkipYear)
					{
						this.SkipYear = false;
						this.Window.LAFContainer.SongsToSkipYear.Add(key.Take(2).ToList());
						break;
					}
					else
					{
						string aux = "";
						Action update = () => aux = this.textBoxArtist.Text;
						this.textBoxArtist.Invoke(update);
						artist = aux;
						update = () => aux = this.textBoxAlbum.Text;
						this.textBoxAlbum.Invoke(update);
						album = aux;
						update = () => aux = this.textBoxTitle.Text;
						this.textBoxTitle.Invoke(update);
						title = aux;
						value.Add(artist); value.Add(album); value.Add(title);
					}
					this.DisableComponents();
				}

			}
		}

		private void SetLyricsInFile(string filename, string lyrics)
		{
			using (var mp3 = TagLib.File.Create(filename))
			{
				//var mp3 = TagLib.File.Create(Filename);
				mp3.Tag.Lyrics = lyrics;
				mp3.Save();
			}
		}

		private void GetLyrics(int threadIndex, string filename, ref string artist, ref string album, ref string title, ref string lyrics)
		{
			var disposable = "";
			List<string> key = new List<string>(3);
			List<string> value = new List<string>(3);
			key.Add(artist); key.Add(album); key.Add(title);
			while (true)
			{
				var htmlDoc = this.CheckIfWebpageExists(false, artist, album, title, ref disposable);
				if (htmlDoc != null)
				{
					var soup = (HtmlAgilityPack.HtmlDocument)htmlDoc;
					foreach (var div in soup.DocumentNode.Descendants("div").Where(element => element.GetAttributeValue("class", "nothing") == "lyrics").ToList())
					{
						lyrics += WebUtility.HtmlDecode(div.InnerText.Trim());
					}
					if (lyrics != "")
					{
						if (this.ErrorOcurred && threadIndex == this.WorkerIndexError)
						{
							this.Window.LAFContainer.ExceptionsReplacements[key] = value;
							this.ErrorOcurred = false;
							this.WorkerIndexError = -1;
							this.SemError.Release();
						}
						this.SetLyricsInFile(filename, lyrics);
						return;
					}
				}
				else
				{
					this.SemError.WaitOne();
					this.WorkerIndexError = threadIndex;
					this.ErrorOcurred = true;
					SystemSounds.Exclamation.Play();
					Process.Start(string.Format("https://www.google.com.tr/search?q={0}", artist.Replace(" &", "").Replace(" ", "+") + "+" + title.Replace(" &", "").Replace(" ", "+") + "+lyrics+site:Genius.com"));
					this.EnableComponents(false, artist, album, title, "0000", "https://genius.com/" + this.NamingConventions(artist + " " + title) + "-lyrics");
					this.SemErrorHandled.WaitOne();
					if (this.SkipLyrics)
					{
						this.SkipLyrics = false;
						this.Window.LAFContainer.SongsToSkipLyrics.Add(key);
						break;
					}
					else
					{
						string aux = "";
						Action update = () => aux = this.textBoxArtist.Text;
						this.textBoxArtist.Invoke(update);
						artist = aux;
						update = () => aux = this.textBoxAlbum.Text;
						this.textBoxAlbum.Invoke(update);
						album = aux;
						update = () => aux = this.textBoxTitle.Text;
						this.textBoxTitle.Invoke(update);
						title = aux;
						value.Add(artist); value.Add(album); value.Add(title);
					}
					this.DisableComponents();
				}
			}
		}

		public void GetLyricsAndYear(object parameters)
		{
			string currentArtist, currentAlbum, currentTitle, currentYear, currentLyrics;
			string fileArtist, fileAlbum, fileTitle;
			Array argArray = (Array)parameters;
			List<string> list = argArray.GetValue(1) as List<string>;
			int threadIndex = (int)argArray.GetValue(0);
			uint trackCount;
			bool skipSong;
			int filesProcessed = 0;
			foreach (string filename in list)
			{
				currentLyrics = "";
				using (var mp3 = TagLib.File.Create(filename))
				{
					currentArtist = fileArtist = mp3.Tag.AlbumArtists[0];
					currentAlbum = fileAlbum = mp3.Tag.Album;
					currentTitle = fileTitle = this.Window.LAFContainer.RemoveWordsFromWord(new List<string>() { "feat", "Feat", "bonus", "Bonus", "Conclusion", "Hidden Track", "Vocal Mix", "Explicit", "explicit", "Extended" }, mp3.Tag.Title);
					currentYear = mp3.Tag.Year.ToString();
					trackCount = mp3.Tag.TrackCount;
					mp3.Save();
				}
				this.ChangeArtistAlbumTitle(true, ref currentArtist, ref currentAlbum, ref currentTitle, trackCount);
				this.AddToOutput(currentArtist, currentAlbum, currentTitle, threadIndex);
				skipSong = false;
				foreach (var item in this.Window.LAFContainer.SongsToSkipYear)
				{
					if (item[0] == currentArtist && item[1] == currentAlbum)
					{
						skipSong = true;
						break;
					}
				}
				if (!skipSong)
				{
					this.GetYear(threadIndex, filename, ref currentArtist, ref currentAlbum, ref currentTitle, ref currentYear, trackCount);
				}
				this.ChangeTextColor(0, threadIndex, 0, 0);
				currentArtist = fileArtist;
				currentAlbum = fileAlbum;
				currentTitle = fileTitle;
				this.ChangeArtistAlbumTitle(false, ref currentArtist, ref currentAlbum, ref currentTitle, trackCount);
				skipSong = false;
				foreach (var item in this.Window.LAFContainer.SongsToSkipLyrics)
				{
					if (item[0] == currentArtist && item[1] == currentAlbum && item[2] == currentTitle)
					{
						skipSong = true;
						break;
					}
				}
				if (!skipSong)
				{
					this.GetLyrics(threadIndex, filename, ref currentArtist, ref currentAlbum, ref currentTitle, ref currentLyrics);
				}
				lock (Mutex)
				{
					this.ChangeTextColor(1, threadIndex, 0, 0);
					var opStatus = this.Window.LAFContainer.iTunesLibrary.AddFile(filename);
					while (opStatus.InProgress) { }
					var addedTrack = opStatus.Tracks[1];
					if (currentYear != "Skip" && Int32.Parse(currentYear) < 1985)
					{
						addedTrack.VolumeAdjustment = 50;
					}
					this.NumberFilesProcessed++;
					this.Window.LAFContainer.AddMusicFile(filename);
				}
				filesProcessed++;
				this.ChangeTextColor(2, threadIndex, filesProcessed, list.Count);
			}
			lock (Mutex)
			{
				if (this.NumberFilesProcessed == this.NewFiles.Count)
				{
					this.SemAllFiles.Release();
					this.Clock.Stop();
				}
			}
		}

	}

}
