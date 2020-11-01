namespace Handler
{
    partial class TracklistScreen
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
            this.textBoxTrackList = new System.Windows.Forms.TextBox();
            this.labelAlbum = new System.Windows.Forms.Label();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.labelLength = new System.Windows.Forms.Label();
            this.buttonBack = new System.Windows.Forms.Button();
            this.buttonShowOnItunes = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // textBoxTrackList
            // 
            this.textBoxTrackList.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(4)))), ((int)(((byte)(64)))));
            this.textBoxTrackList.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.textBoxTrackList.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxTrackList.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.textBoxTrackList.Location = new System.Drawing.Point(49, 50);
            this.textBoxTrackList.Multiline = true;
            this.textBoxTrackList.Name = "textBoxTrackList";
            this.textBoxTrackList.ReadOnly = true;
            this.textBoxTrackList.Size = new System.Drawing.Size(582, 273);
            this.textBoxTrackList.TabIndex = 0;
            // 
            // labelAlbum
            // 
            this.labelAlbum.Font = new System.Drawing.Font("Microsoft Sans Serif", 14F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelAlbum.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.labelAlbum.Location = new System.Drawing.Point(49, 24);
            this.labelAlbum.Name = "labelAlbum";
            this.labelAlbum.Size = new System.Drawing.Size(582, 23);
            this.labelAlbum.TabIndex = 1;
            this.labelAlbum.Text = "This is the Tracklist of ";
            this.labelAlbum.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.labelAlbum.UseMnemonic = false;
            // 
            // pictureBox1
            // 
            this.pictureBox1.Location = new System.Drawing.Point(655, 50);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(300, 300);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 2;
            this.pictureBox1.TabStop = false;
            // 
            // labelLength
            // 
            this.labelLength.Font = new System.Drawing.Font("Microsoft Sans Serif", 14F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelLength.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.labelLength.Location = new System.Drawing.Point(49, 327);
            this.labelLength.Name = "labelLength";
            this.labelLength.Size = new System.Drawing.Size(582, 23);
            this.labelLength.TabIndex = 3;
            this.labelLength.Text = "Length: ";
            this.labelLength.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // buttonBack
            // 
            this.buttonBack.AutoSize = true;
            this.buttonBack.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.buttonBack.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(3)))), ((int)(((byte)(3)))), ((int)(((byte)(31)))));
            this.buttonBack.FlatAppearance.BorderSize = 0;
            this.buttonBack.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.buttonBack.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.buttonBack.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonBack.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonBack.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(124)))), ((int)(((byte)(219)))));
            this.buttonBack.Location = new System.Drawing.Point(0, 20);
            this.buttonBack.Name = "buttonBack";
            this.buttonBack.Size = new System.Drawing.Size(49, 27);
            this.buttonBack.TabIndex = 4;
            this.buttonBack.Text = "Back";
            this.buttonBack.UseVisualStyleBackColor = true;
            this.buttonBack.Click += new System.EventHandler(this.buttonBack_Click);
            // 
            // buttonShowOnItunes
            // 
            this.buttonShowOnItunes.AutoSize = true;
            this.buttonShowOnItunes.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.buttonShowOnItunes.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(3)))), ((int)(((byte)(3)))), ((int)(((byte)(31)))));
            this.buttonShowOnItunes.FlatAppearance.BorderSize = 0;
            this.buttonShowOnItunes.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.buttonShowOnItunes.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.buttonShowOnItunes.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonShowOnItunes.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonShowOnItunes.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(124)))), ((int)(((byte)(219)))));
            this.buttonShowOnItunes.Location = new System.Drawing.Point(750, 356);
            this.buttonShowOnItunes.Name = "buttonShowOnItunes";
            this.buttonShowOnItunes.Size = new System.Drawing.Size(122, 27);
            this.buttonShowOnItunes.TabIndex = 5;
            this.buttonShowOnItunes.Text = "Show On iTunes";
            this.buttonShowOnItunes.UseVisualStyleBackColor = true;
            this.buttonShowOnItunes.Click += new System.EventHandler(this.buttonShowOnItunes_Click);
            // 
            // TracklistScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.buttonShowOnItunes);
            this.Controls.Add(this.buttonBack);
            this.Controls.Add(this.labelLength);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.labelAlbum);
            this.Controls.Add(this.textBoxTrackList);
            this.Name = "TracklistScreen";
            this.Size = new System.Drawing.Size(958, 386);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBoxTrackList;
        private System.Windows.Forms.Label labelAlbum;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Label labelLength;
        private System.Windows.Forms.Button buttonBack;
        private System.Windows.Forms.Button buttonShowOnItunes;
    }
}
