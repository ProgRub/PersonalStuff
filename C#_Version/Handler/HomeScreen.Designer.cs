namespace Handler
{
    partial class HomeScreen
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

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label3 = new System.Windows.Forms.Label();
            this.buttonChooseMusicDestinyFolder = new System.Windows.Forms.Button();
            this.textBoxMusicDestinyDir = new System.Windows.Forms.TextBox();
            this.helpLabelFileDialog3 = new System.Windows.Forms.Label();
            this.buttonChooseAlbum = new System.Windows.Forms.Button();
            this.buttonSearchLibrary = new System.Windows.Forms.Button();
            this.buttonGenresColors = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.ForeColor = System.Drawing.Color.White;
            this.label3.Location = new System.Drawing.Point(5, 29);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(87, 13);
            this.label3.TabIndex = 17;
            this.label3.Text = "Music (Stored In)";
            // 
            // buttonChooseMusicDestinyFolder
            // 
            this.buttonChooseMusicDestinyFolder.Location = new System.Drawing.Point(532, 26);
            this.buttonChooseMusicDestinyFolder.Name = "buttonChooseMusicDestinyFolder";
            this.buttonChooseMusicDestinyFolder.Size = new System.Drawing.Size(75, 23);
            this.buttonChooseMusicDestinyFolder.TabIndex = 16;
            this.buttonChooseMusicDestinyFolder.Text = "Open";
            this.buttonChooseMusicDestinyFolder.UseVisualStyleBackColor = true;
            this.buttonChooseMusicDestinyFolder.Click += new System.EventHandler(this.buttonChooseMusicDestinyFolder_Click);
            // 
            // textBoxMusicDestinyDir
            // 
            this.textBoxMusicDestinyDir.Enabled = false;
            this.textBoxMusicDestinyDir.Location = new System.Drawing.Point(100, 26);
            this.textBoxMusicDestinyDir.Name = "textBoxMusicDestinyDir";
            this.textBoxMusicDestinyDir.ReadOnly = true;
            this.textBoxMusicDestinyDir.Size = new System.Drawing.Size(426, 20);
            this.textBoxMusicDestinyDir.TabIndex = 15;
            // 
            // helpLabelFileDialog3
            // 
            this.helpLabelFileDialog3.AutoSize = true;
            this.helpLabelFileDialog3.ForeColor = System.Drawing.Color.White;
            this.helpLabelFileDialog3.Location = new System.Drawing.Point(97, 10);
            this.helpLabelFileDialog3.Name = "helpLabelFileDialog3";
            this.helpLabelFileDialog3.Size = new System.Drawing.Size(48, 13);
            this.helpLabelFileDialog3.TabIndex = 14;
            this.helpLabelFileDialog3.Text = "Location";
            // 
            // buttonChooseAlbum
            // 
            this.buttonChooseAlbum.Location = new System.Drawing.Point(211, 66);
            this.buttonChooseAlbum.Name = "buttonChooseAlbum";
            this.buttonChooseAlbum.Size = new System.Drawing.Size(205, 23);
            this.buttonChooseAlbum.TabIndex = 18;
            this.buttonChooseAlbum.Text = "Choose Album";
            this.buttonChooseAlbum.UseVisualStyleBackColor = true;
            this.buttonChooseAlbum.Click += new System.EventHandler(this.buttonChooseAlbum_Click);
            // 
            // buttonSearchLibrary
            // 
            this.buttonSearchLibrary.Location = new System.Drawing.Point(211, 106);
            this.buttonSearchLibrary.Name = "buttonSearchLibrary";
            this.buttonSearchLibrary.Size = new System.Drawing.Size(205, 23);
            this.buttonSearchLibrary.TabIndex = 19;
            this.buttonSearchLibrary.Text = "Search Library";
            this.buttonSearchLibrary.UseVisualStyleBackColor = true;
            this.buttonSearchLibrary.Click += new System.EventHandler(this.buttonSearchLibrary_Click);
            // 
            // buttonGenresColors
            // 
            this.buttonGenresColors.Location = new System.Drawing.Point(211, 146);
            this.buttonGenresColors.Name = "buttonGenresColors";
            this.buttonGenresColors.Size = new System.Drawing.Size(205, 23);
            this.buttonGenresColors.TabIndex = 20;
            this.buttonGenresColors.Text = "Choose Genres Colors";
            this.buttonGenresColors.UseVisualStyleBackColor = true;
            this.buttonGenresColors.Click += new System.EventHandler(this.buttonGenresColors_Click);
            // 
            // HomeScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.buttonGenresColors);
            this.Controls.Add(this.buttonSearchLibrary);
            this.Controls.Add(this.buttonChooseAlbum);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.buttonChooseMusicDestinyFolder);
            this.Controls.Add(this.textBoxMusicDestinyDir);
            this.Controls.Add(this.helpLabelFileDialog3);
            this.Name = "HomeScreen";
            this.Size = new System.Drawing.Size(615, 185);
            this.Enter += new System.EventHandler(this.HomeScreen_Enter);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button buttonChooseMusicDestinyFolder;
        private System.Windows.Forms.TextBox textBoxMusicDestinyDir;
        private System.Windows.Forms.Label helpLabelFileDialog3;
        private System.Windows.Forms.Button buttonChooseAlbum;
        private System.Windows.Forms.Button buttonSearchLibrary;
        private System.Windows.Forms.Button buttonGenresColors;
    }
}
