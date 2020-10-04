using System.Linq;

namespace Downloader
{
    partial class SchoolScreen
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
            this.SuspendLayout();
            // 
            // labelFilesFound
            // 
            this.labelFilesFound.AutoSize = true;
            this.labelFilesFound.Font = new System.Drawing.Font("Microsoft Sans Serif", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelFilesFound.ForeColor = System.Drawing.Color.White;
            this.labelFilesFound.Location = new System.Drawing.Point(353, 22);
            this.labelFilesFound.Name = "labelFilesFound";
            this.labelFilesFound.Size = new System.Drawing.Size(143, 25);
            this.labelFilesFound.TabIndex = 2;
            this.labelFilesFound.Text = "0 Files Found";
            // 
            // SchoolScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.Controls.Add(this.labelFilesFound);
            this.Name = "SchoolScreen";
            this.Size = new System.Drawing.Size(861, 555);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label labelFilesFound;
    }
}
