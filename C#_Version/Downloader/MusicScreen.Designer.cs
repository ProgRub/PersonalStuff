using System.Linq;

namespace Downloader
{
    partial class MusicScreen
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
            this.labelFilesFound = new System.Windows.Forms.Label();
            this.buttonEndCycleAdvance = new System.Windows.Forms.Button();
            this.TextBoxFilesFound = new System.Windows.Forms.TextBox();
            this.TextBoxFilesMoved = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // labelFilesFound
            // 
            this.labelFilesFound.AutoSize = true;
            this.labelFilesFound.Font = new System.Drawing.Font("Microsoft Sans Serif", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelFilesFound.ForeColor = System.Drawing.Color.White;
            this.labelFilesFound.Location = new System.Drawing.Point(482, 6);
            this.labelFilesFound.Name = "labelFilesFound";
            this.labelFilesFound.Size = new System.Drawing.Size(143, 25);
            this.labelFilesFound.TabIndex = 5;
            this.labelFilesFound.Text = "0 Files Found";
            // 
            // buttonEndCycleAdvance
            // 
            this.buttonEndCycleAdvance.AutoSize = true;
            this.buttonEndCycleAdvance.Location = new System.Drawing.Point(453, 494);
            this.buttonEndCycleAdvance.Name = "buttonEndCycleAdvance";
            this.buttonEndCycleAdvance.Size = new System.Drawing.Size(194, 23);
            this.buttonEndCycleAdvance.TabIndex = 6;
            this.buttonEndCycleAdvance.Text = "Move Files";
            this.buttonEndCycleAdvance.UseVisualStyleBackColor = true;
            this.buttonEndCycleAdvance.Click += new System.EventHandler(this.buttonEndCycleAdvance_Click);
            // 
            // TextBoxFilesFound
            // 
            this.TextBoxFilesFound.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.TextBoxFilesFound.Cursor = System.Windows.Forms.Cursors.Default;
            this.TextBoxFilesFound.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.TextBoxFilesFound.ForeColor = System.Drawing.Color.White;
            this.TextBoxFilesFound.Location = new System.Drawing.Point(6, 34);
            this.TextBoxFilesFound.Multiline = true;
            this.TextBoxFilesFound.Name = "TextBoxFilesFound";
            this.TextBoxFilesFound.ReadOnly = true;
            this.TextBoxFilesFound.Size = new System.Drawing.Size(539, 454);
            this.TextBoxFilesFound.TabIndex = 7;
            // 
            // TextBoxFilesMoved
            // 
            this.TextBoxFilesMoved.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.TextBoxFilesMoved.Cursor = System.Windows.Forms.Cursors.Default;
            this.TextBoxFilesMoved.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.TextBoxFilesMoved.ForeColor = System.Drawing.Color.White;
            this.TextBoxFilesMoved.Location = new System.Drawing.Point(551, 34);
            this.TextBoxFilesMoved.Multiline = true;
            this.TextBoxFilesMoved.Name = "TextBoxFilesMoved";
            this.TextBoxFilesMoved.ReadOnly = true;
            this.TextBoxFilesMoved.Size = new System.Drawing.Size(539, 454);
            this.TextBoxFilesMoved.TabIndex = 8;
            // 
            // MusicScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.TextBoxFilesMoved);
            this.Controls.Add(this.TextBoxFilesFound);
            this.Controls.Add(this.buttonEndCycleAdvance);
            this.Controls.Add(this.labelFilesFound);
            this.Name = "MusicScreen";
            this.Size = new System.Drawing.Size(1103, 525);
            this.Load += new System.EventHandler(this.MusicScreen_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label labelFilesFound;
        private System.Windows.Forms.Button buttonEndCycleAdvance;
        private System.Windows.Forms.TextBox TextBoxFilesFound;
        private System.Windows.Forms.TextBox TextBoxFilesMoved;
    }
}
