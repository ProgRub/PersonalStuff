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
            this.listBoxPossibleAlbums = new System.Windows.Forms.ListBox();
            this.listBoxPossibleHalfAlbums = new System.Windows.Forms.ListBox();
            this.SuspendLayout();
            // 
            // labelPossibleAlbums
            // 
            this.labelPossibleAlbums.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelPossibleAlbums.ForeColor = System.Drawing.Color.White;
            this.labelPossibleAlbums.Location = new System.Drawing.Point(44, 13);
            this.labelPossibleAlbums.Name = "labelPossibleAlbums";
            this.labelPossibleAlbums.Size = new System.Drawing.Size(1026, 23);
            this.labelPossibleAlbums.TabIndex = 0;
            this.labelPossibleAlbums.Text = "labelPossibleAlbums";
            this.labelPossibleAlbums.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelPossibleHalfAlbums
            // 
            this.labelPossibleHalfAlbums.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelPossibleHalfAlbums.ForeColor = System.Drawing.Color.White;
            this.labelPossibleHalfAlbums.Location = new System.Drawing.Point(45, 478);
            this.labelPossibleHalfAlbums.Name = "labelPossibleHalfAlbums";
            this.labelPossibleHalfAlbums.Size = new System.Drawing.Size(1025, 23);
            this.labelPossibleHalfAlbums.TabIndex = 1;
            this.labelPossibleHalfAlbums.Text = "labelPossibleHalfAlbums";
            this.labelPossibleHalfAlbums.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // listBoxPossibleAlbums
            // 
            this.listBoxPossibleAlbums.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.listBoxPossibleAlbums.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listBoxPossibleAlbums.ForeColor = System.Drawing.Color.White;
            this.listBoxPossibleAlbums.FormattingEnabled = true;
            this.listBoxPossibleAlbums.ItemHeight = 16;
            this.listBoxPossibleAlbums.Location = new System.Drawing.Point(44, 39);
            this.listBoxPossibleAlbums.Name = "listBoxPossibleAlbums";
            this.listBoxPossibleAlbums.Size = new System.Drawing.Size(1026, 436);
            this.listBoxPossibleAlbums.TabIndex = 2;
            this.listBoxPossibleAlbums.DrawItem += new System.Windows.Forms.DrawItemEventHandler(this.listBoxPossibleAlbums_DrawItem);
            // 
            // listBoxPossibleHalfAlbums
            // 
            this.listBoxPossibleHalfAlbums.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.listBoxPossibleHalfAlbums.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listBoxPossibleHalfAlbums.ForeColor = System.Drawing.Color.White;
            this.listBoxPossibleHalfAlbums.FormattingEnabled = true;
            this.listBoxPossibleHalfAlbums.ItemHeight = 16;
            this.listBoxPossibleHalfAlbums.Location = new System.Drawing.Point(44, 504);
            this.listBoxPossibleHalfAlbums.Name = "listBoxPossibleHalfAlbums";
            this.listBoxPossibleHalfAlbums.Size = new System.Drawing.Size(1026, 436);
            this.listBoxPossibleHalfAlbums.TabIndex = 3;
            this.listBoxPossibleHalfAlbums.DrawItem += new System.Windows.Forms.DrawItemEventHandler(this.listBoxPossibleHalfAlbums_DrawItem);
            // 
            // ChooseAlbumScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.listBoxPossibleHalfAlbums);
            this.Controls.Add(this.listBoxPossibleAlbums);
            this.Controls.Add(this.labelPossibleHalfAlbums);
            this.Controls.Add(this.labelPossibleAlbums);
            this.Name = "ChooseAlbumScreen";
            this.Size = new System.Drawing.Size(1318, 998);
            this.Load += new System.EventHandler(this.ChooseAlbumScreen_Load);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label labelPossibleAlbums;
        private System.Windows.Forms.Label labelPossibleHalfAlbums;
        private System.Windows.Forms.ListBox listBoxPossibleAlbums;
        private System.Windows.Forms.ListBox listBoxPossibleHalfAlbums;
    }
}
