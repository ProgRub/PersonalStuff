namespace Handler
{
    partial class SearchLibraryScreen
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
            this.labelAlbumArtist = new System.Windows.Forms.Label();
            this.textBoxAlbumArtist = new System.Windows.Forms.TextBox();
            this.textBoxContributingArtist = new System.Windows.Forms.TextBox();
            this.labelContributingArtists = new System.Windows.Forms.Label();
            this.textBoxAlbum = new System.Windows.Forms.TextBox();
            this.labelAlbum = new System.Windows.Forms.Label();
            this.textBoxTitle = new System.Windows.Forms.TextBox();
            this.labelTitle = new System.Windows.Forms.Label();
            this.textBoxYear = new System.Windows.Forms.TextBox();
            this.labelYear = new System.Windows.Forms.Label();
            this.textBoxGenre = new System.Windows.Forms.TextBox();
            this.labelGenre = new System.Windows.Forms.Label();
            this.listBoxResults = new System.Windows.Forms.ListBox();
            this.buttonBack = new System.Windows.Forms.Button();
            this.buttonTrackDetails = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // labelAlbumArtist
            // 
            this.labelAlbumArtist.AutoSize = true;
            this.labelAlbumArtist.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelAlbumArtist.ForeColor = System.Drawing.Color.White;
            this.labelAlbumArtist.Location = new System.Drawing.Point(46, 33);
            this.labelAlbumArtist.Name = "labelAlbumArtist";
            this.labelAlbumArtist.Size = new System.Drawing.Size(83, 17);
            this.labelAlbumArtist.TabIndex = 0;
            this.labelAlbumArtist.Text = "Album Artist";
            // 
            // textBoxAlbumArtist
            // 
            this.textBoxAlbumArtist.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxAlbumArtist.Location = new System.Drawing.Point(135, 30);
            this.textBoxAlbumArtist.Name = "textBoxAlbumArtist";
            this.textBoxAlbumArtist.Size = new System.Drawing.Size(373, 23);
            this.textBoxAlbumArtist.TabIndex = 1;
            this.textBoxAlbumArtist.TextChanged += new System.EventHandler(this.textBoxAlbumArtist_TextChanged);
            // 
            // textBoxContributingArtist
            // 
            this.textBoxContributingArtist.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxContributingArtist.Location = new System.Drawing.Point(135, 59);
            this.textBoxContributingArtist.Name = "textBoxContributingArtist";
            this.textBoxContributingArtist.Size = new System.Drawing.Size(373, 23);
            this.textBoxContributingArtist.TabIndex = 3;
            this.textBoxContributingArtist.TextChanged += new System.EventHandler(this.textBoxContributingArtist_TextChanged);
            // 
            // labelContributingArtists
            // 
            this.labelContributingArtists.AutoSize = true;
            this.labelContributingArtists.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelContributingArtists.ForeColor = System.Drawing.Color.White;
            this.labelContributingArtists.Location = new System.Drawing.Point(3, 62);
            this.labelContributingArtists.Name = "labelContributingArtists";
            this.labelContributingArtists.Size = new System.Drawing.Size(127, 17);
            this.labelContributingArtists.TabIndex = 2;
            this.labelContributingArtists.Text = "Contributing Artists";
            // 
            // textBoxAlbum
            // 
            this.textBoxAlbum.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxAlbum.Location = new System.Drawing.Point(135, 88);
            this.textBoxAlbum.Name = "textBoxAlbum";
            this.textBoxAlbum.Size = new System.Drawing.Size(373, 23);
            this.textBoxAlbum.TabIndex = 5;
            this.textBoxAlbum.TextChanged += new System.EventHandler(this.textBoxAlbum_TextChanged);
            // 
            // labelAlbum
            // 
            this.labelAlbum.AutoSize = true;
            this.labelAlbum.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelAlbum.ForeColor = System.Drawing.Color.White;
            this.labelAlbum.Location = new System.Drawing.Point(82, 91);
            this.labelAlbum.Name = "labelAlbum";
            this.labelAlbum.Size = new System.Drawing.Size(47, 17);
            this.labelAlbum.TabIndex = 4;
            this.labelAlbum.Text = "Album";
            // 
            // textBoxTitle
            // 
            this.textBoxTitle.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxTitle.Location = new System.Drawing.Point(135, 117);
            this.textBoxTitle.Name = "textBoxTitle";
            this.textBoxTitle.Size = new System.Drawing.Size(373, 23);
            this.textBoxTitle.TabIndex = 7;
            this.textBoxTitle.TextChanged += new System.EventHandler(this.textBoxTitle_TextChanged);
            // 
            // labelTitle
            // 
            this.labelTitle.AutoSize = true;
            this.labelTitle.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelTitle.ForeColor = System.Drawing.Color.White;
            this.labelTitle.Location = new System.Drawing.Point(95, 120);
            this.labelTitle.Name = "labelTitle";
            this.labelTitle.Size = new System.Drawing.Size(35, 17);
            this.labelTitle.TabIndex = 6;
            this.labelTitle.Text = "Title";
            // 
            // textBoxYear
            // 
            this.textBoxYear.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxYear.Location = new System.Drawing.Point(135, 146);
            this.textBoxYear.Name = "textBoxYear";
            this.textBoxYear.Size = new System.Drawing.Size(373, 23);
            this.textBoxYear.TabIndex = 9;
            this.textBoxYear.TextChanged += new System.EventHandler(this.textBoxYear_TextChanged);
            // 
            // labelYear
            // 
            this.labelYear.AutoSize = true;
            this.labelYear.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelYear.ForeColor = System.Drawing.Color.White;
            this.labelYear.Location = new System.Drawing.Point(92, 149);
            this.labelYear.Name = "labelYear";
            this.labelYear.Size = new System.Drawing.Size(38, 17);
            this.labelYear.TabIndex = 8;
            this.labelYear.Text = "Year";
            // 
            // textBoxGenre
            // 
            this.textBoxGenre.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxGenre.Location = new System.Drawing.Point(135, 175);
            this.textBoxGenre.Name = "textBoxGenre";
            this.textBoxGenre.Size = new System.Drawing.Size(373, 23);
            this.textBoxGenre.TabIndex = 11;
            this.textBoxGenre.TextChanged += new System.EventHandler(this.textBoxGenre_TextChanged);
            // 
            // labelGenre
            // 
            this.labelGenre.AutoSize = true;
            this.labelGenre.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelGenre.ForeColor = System.Drawing.Color.White;
            this.labelGenre.Location = new System.Drawing.Point(82, 178);
            this.labelGenre.Name = "labelGenre";
            this.labelGenre.Size = new System.Drawing.Size(48, 17);
            this.labelGenre.TabIndex = 10;
            this.labelGenre.Text = "Genre";
            // 
            // listBoxResults
            // 
            this.listBoxResults.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.listBoxResults.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listBoxResults.ForeColor = System.Drawing.Color.White;
            this.listBoxResults.FormattingEnabled = true;
            this.listBoxResults.ItemHeight = 15;
            this.listBoxResults.Location = new System.Drawing.Point(514, 30);
            this.listBoxResults.Name = "listBoxResults";
            this.listBoxResults.SelectionMode = System.Windows.Forms.SelectionMode.MultiExtended;
            this.listBoxResults.Size = new System.Drawing.Size(734, 379);
            this.listBoxResults.Sorted = true;
            this.listBoxResults.TabIndex = 12;
            this.listBoxResults.KeyDown += new System.Windows.Forms.KeyEventHandler(this.listBoxResults_KeyDown);
            // 
            // buttonBack
            // 
            this.buttonBack.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonBack.Location = new System.Drawing.Point(6, 229);
            this.buttonBack.Name = "buttonBack";
            this.buttonBack.Size = new System.Drawing.Size(75, 23);
            this.buttonBack.TabIndex = 13;
            this.buttonBack.Text = "Back";
            this.buttonBack.UseVisualStyleBackColor = true;
            this.buttonBack.Click += new System.EventHandler(this.buttonBack_Click);
            // 
            // buttonTrackDetails
            // 
            this.buttonTrackDetails.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonTrackDetails.Location = new System.Drawing.Point(799, 415);
            this.buttonTrackDetails.Name = "buttonTrackDetails";
            this.buttonTrackDetails.Size = new System.Drawing.Size(184, 23);
            this.buttonTrackDetails.TabIndex = 14;
            this.buttonTrackDetails.Text = "Track Details";
            this.buttonTrackDetails.UseVisualStyleBackColor = true;
            // 
            // SearchLibraryScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.buttonTrackDetails);
            this.Controls.Add(this.buttonBack);
            this.Controls.Add(this.listBoxResults);
            this.Controls.Add(this.textBoxGenre);
            this.Controls.Add(this.labelGenre);
            this.Controls.Add(this.textBoxYear);
            this.Controls.Add(this.labelYear);
            this.Controls.Add(this.textBoxTitle);
            this.Controls.Add(this.labelTitle);
            this.Controls.Add(this.textBoxAlbum);
            this.Controls.Add(this.labelAlbum);
            this.Controls.Add(this.textBoxContributingArtist);
            this.Controls.Add(this.labelContributingArtists);
            this.Controls.Add(this.textBoxAlbumArtist);
            this.Controls.Add(this.labelAlbumArtist);
            this.Name = "SearchLibraryScreen";
            this.Size = new System.Drawing.Size(1251, 447);
            this.Enter += new System.EventHandler(this.SearchLibraryScreen_Enter);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label labelAlbumArtist;
        private System.Windows.Forms.TextBox textBoxAlbumArtist;
        private System.Windows.Forms.TextBox textBoxContributingArtist;
        private System.Windows.Forms.Label labelContributingArtists;
        private System.Windows.Forms.TextBox textBoxAlbum;
        private System.Windows.Forms.Label labelAlbum;
        private System.Windows.Forms.TextBox textBoxTitle;
        private System.Windows.Forms.Label labelTitle;
        private System.Windows.Forms.TextBox textBoxYear;
        private System.Windows.Forms.Label labelYear;
        private System.Windows.Forms.TextBox textBoxGenre;
        private System.Windows.Forms.Label labelGenre;
        private System.Windows.Forms.ListBox listBoxResults;
        private System.Windows.Forms.Button buttonBack;
        private System.Windows.Forms.Button buttonTrackDetails;
    }
}
