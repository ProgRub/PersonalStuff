namespace Handler
{
    partial class ChooseAlbumScreen
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
            this.labelPossibleAlbums = new System.Windows.Forms.Label();
            this.labelPossibleHalfAlbums = new System.Windows.Forms.Label();
            this.listViewPossibleHalfAlbums = new System.Windows.Forms.ListView();
            this.columnArtist = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnAlbum = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnTime = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnPlayCount = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.listViewPossibleAlbums = new System.Windows.Forms.ListView();
            this.columnHeader1 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeader2 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeader3 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeader4 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.button1 = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // labelPossibleAlbums
            // 
            this.labelPossibleAlbums.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelPossibleAlbums.ForeColor = System.Drawing.Color.White;
            this.labelPossibleAlbums.Location = new System.Drawing.Point(9, 8);
            this.labelPossibleAlbums.Name = "labelPossibleAlbums";
            this.labelPossibleAlbums.Size = new System.Drawing.Size(774, 23);
            this.labelPossibleAlbums.TabIndex = 0;
            this.labelPossibleAlbums.Text = "labelPossibleAlbums";
            this.labelPossibleAlbums.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelPossibleHalfAlbums
            // 
            this.labelPossibleHalfAlbums.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelPossibleHalfAlbums.ForeColor = System.Drawing.Color.White;
            this.labelPossibleHalfAlbums.Location = new System.Drawing.Point(9, 411);
            this.labelPossibleHalfAlbums.Name = "labelPossibleHalfAlbums";
            this.labelPossibleHalfAlbums.Size = new System.Drawing.Size(774, 23);
            this.labelPossibleHalfAlbums.TabIndex = 1;
            this.labelPossibleHalfAlbums.Text = "labelPossibleHalfAlbums";
            this.labelPossibleHalfAlbums.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // listViewPossibleHalfAlbums
            // 
            this.listViewPossibleHalfAlbums.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.listViewPossibleHalfAlbums.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.columnArtist,
            this.columnAlbum,
            this.columnTime,
            this.columnPlayCount});
            this.listViewPossibleHalfAlbums.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listViewPossibleHalfAlbums.FullRowSelect = true;
            this.listViewPossibleHalfAlbums.HideSelection = false;
            this.listViewPossibleHalfAlbums.Location = new System.Drawing.Point(12, 437);
            this.listViewPossibleHalfAlbums.Name = "listViewPossibleHalfAlbums";
            this.listViewPossibleHalfAlbums.Size = new System.Drawing.Size(771, 374);
            this.listViewPossibleHalfAlbums.TabIndex = 3;
            this.listViewPossibleHalfAlbums.UseCompatibleStateImageBehavior = false;
            this.listViewPossibleHalfAlbums.View = System.Windows.Forms.View.Details;
            this.listViewPossibleHalfAlbums.ColumnClick += new System.Windows.Forms.ColumnClickEventHandler(this.listViewPossibleHalfAlbums_ColumnClick);
            this.listViewPossibleHalfAlbums.DoubleClick += new System.EventHandler(this.listViewPossibleHalfAlbums_DoubleClick);
            // 
            // columnArtist
            // 
            this.columnArtist.Text = "Artist";
            this.columnArtist.Width = 235;
            // 
            // columnAlbum
            // 
            this.columnAlbum.Text = "Album";
            this.columnAlbum.Width = 319;
            // 
            // columnTime
            // 
            this.columnTime.Text = "Time";
            this.columnTime.Width = 65;
            // 
            // columnPlayCount
            // 
            this.columnPlayCount.Text = "Average Play Count";
            this.columnPlayCount.Width = 125;
            // 
            // listViewPossibleAlbums
            // 
            this.listViewPossibleAlbums.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.listViewPossibleAlbums.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.columnHeader1,
            this.columnHeader2,
            this.columnHeader3,
            this.columnHeader4});
            this.listViewPossibleAlbums.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listViewPossibleAlbums.FullRowSelect = true;
            this.listViewPossibleAlbums.HideSelection = false;
            this.listViewPossibleAlbums.Location = new System.Drawing.Point(13, 34);
            this.listViewPossibleAlbums.Name = "listViewPossibleAlbums";
            this.listViewPossibleAlbums.Size = new System.Drawing.Size(770, 374);
            this.listViewPossibleAlbums.TabIndex = 4;
            this.listViewPossibleAlbums.UseCompatibleStateImageBehavior = false;
            this.listViewPossibleAlbums.View = System.Windows.Forms.View.Details;
            this.listViewPossibleAlbums.ColumnClick += new System.Windows.Forms.ColumnClickEventHandler(this.listViewPossibleAlbums_ColumnClick);
            this.listViewPossibleAlbums.DoubleClick += new System.EventHandler(this.listViewPossibleAlbums_DoubleClick);
            // 
            // columnHeader1
            // 
            this.columnHeader1.Text = "Artist";
            this.columnHeader1.Width = 235;
            // 
            // columnHeader2
            // 
            this.columnHeader2.Text = "Album";
            this.columnHeader2.Width = 319;
            // 
            // columnHeader3
            // 
            this.columnHeader3.Text = "Time";
            this.columnHeader3.Width = 65;
            // 
            // columnHeader4
            // 
            this.columnHeader4.Text = "Average Play Count";
            this.columnHeader4.Width = 125;
            // 
            // button1
            // 
            this.button1.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button1.Location = new System.Drawing.Point(851, 413);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(75, 23);
            this.button1.TabIndex = 5;
            this.button1.Text = "Back";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.buttonBack_Click);
            // 
            // ChooseAlbumScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.button1);
            this.Controls.Add(this.listViewPossibleAlbums);
            this.Controls.Add(this.listViewPossibleHalfAlbums);
            this.Controls.Add(this.labelPossibleHalfAlbums);
            this.Controls.Add(this.labelPossibleAlbums);
            this.Name = "ChooseAlbumScreen";
            this.Size = new System.Drawing.Size(1318, 998);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label labelPossibleAlbums;
        private System.Windows.Forms.Label labelPossibleHalfAlbums;
        private System.Windows.Forms.ListView listViewPossibleHalfAlbums;
        private System.Windows.Forms.ColumnHeader columnArtist;
        private System.Windows.Forms.ColumnHeader columnAlbum;
        private System.Windows.Forms.ColumnHeader columnTime;
        private System.Windows.Forms.ColumnHeader columnPlayCount;
        private System.Windows.Forms.ListView listViewPossibleAlbums;
        private System.Windows.Forms.ColumnHeader columnHeader1;
        private System.Windows.Forms.ColumnHeader columnHeader2;
        private System.Windows.Forms.ColumnHeader columnHeader3;
        private System.Windows.Forms.ColumnHeader columnHeader4;
        private System.Windows.Forms.Button button1;
    }
}
