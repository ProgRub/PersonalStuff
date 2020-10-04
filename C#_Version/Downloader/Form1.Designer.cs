namespace Downloader
{
    partial class DownloaderForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            Microsoft.WindowsAPICodePack.Dialogs.CommonOpenFileDialog commonOpenFileDialog1 = new Microsoft.WindowsAPICodePack.Dialogs.CommonOpenFileDialog();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(DownloaderForm));
            this.homeScreen1 = new Downloader.HomeScreen();
            this.SuspendLayout();
            // 
            // homeScreen1
            // 
            this.homeScreen1.AutoSize = true;
            this.homeScreen1.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.homeScreen1.Dock = System.Windows.Forms.DockStyle.Fill;
            commonOpenFileDialog1.AddToMostRecentlyUsedList = true;
            commonOpenFileDialog1.AllowNonFileSystemItems = false;
            commonOpenFileDialog1.AllowPropertyEditing = false;
            commonOpenFileDialog1.CookieIdentifier = new System.Guid("00000000-0000-0000-0000-000000000000");
            commonOpenFileDialog1.DefaultDirectory = null;
            commonOpenFileDialog1.DefaultDirectoryShellContainer = null;
            commonOpenFileDialog1.DefaultExtension = null;
            commonOpenFileDialog1.DefaultFileName = null;
            commonOpenFileDialog1.EnsureFileExists = false;
            commonOpenFileDialog1.EnsurePathExists = false;
            commonOpenFileDialog1.EnsureReadOnly = true;
            commonOpenFileDialog1.EnsureValidNames = false;
            commonOpenFileDialog1.InitialDirectory = null;
            commonOpenFileDialog1.InitialDirectoryShellContainer = null;
            commonOpenFileDialog1.IsFolderPicker = true;
            commonOpenFileDialog1.Multiselect = false;
            commonOpenFileDialog1.NavigateToShortcut = true;
            commonOpenFileDialog1.RestoreDirectory = false;
            commonOpenFileDialog1.ShowHiddenItems = false;
            commonOpenFileDialog1.ShowPlacesList = true;
            commonOpenFileDialog1.Title = null;
            this.homeScreen1.folderDialog = commonOpenFileDialog1;
            this.homeScreen1.Location = new System.Drawing.Point(0, 0);
            this.homeScreen1.Name = "homeScreen1";
            this.homeScreen1.Size = new System.Drawing.Size(975, 391);
            this.homeScreen1.TabIndex = 0;
            this.homeScreen1.Window = null;
            // 
            // DownloaderForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.ClientSize = new System.Drawing.Size(975, 391);
            this.Controls.Add(this.homeScreen1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "DownloaderForm";
            this.Text = "Downloader";
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.Downloader_FormClosed);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private HomeScreen homeScreen1;
    }
}

