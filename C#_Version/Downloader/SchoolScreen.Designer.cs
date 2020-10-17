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
            this.TextBoxFilesMoved = new System.Windows.Forms.TextBox();
            this.TextBoxFilesFound = new System.Windows.Forms.TextBox();
            this.buttonMoveFile = new System.Windows.Forms.Button();
            this.labelFilesFound = new System.Windows.Forms.Label();
            this.dropdownDirectories = new System.Windows.Forms.ComboBox();
            this.textBoxFilename = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // TextBoxFilesMoved
            // 
            this.TextBoxFilesMoved.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.TextBoxFilesMoved.Cursor = System.Windows.Forms.Cursors.Default;
            this.TextBoxFilesMoved.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.TextBoxFilesMoved.ForeColor = System.Drawing.Color.White;
            this.TextBoxFilesMoved.Location = new System.Drawing.Point(555, 37);
            this.TextBoxFilesMoved.Multiline = true;
            this.TextBoxFilesMoved.Name = "TextBoxFilesMoved";
            this.TextBoxFilesMoved.ReadOnly = true;
            this.TextBoxFilesMoved.Size = new System.Drawing.Size(539, 454);
            this.TextBoxFilesMoved.TabIndex = 12;
            // 
            // TextBoxFilesFound
            // 
            this.TextBoxFilesFound.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(64)))));
            this.TextBoxFilesFound.Cursor = System.Windows.Forms.Cursors.Default;
            this.TextBoxFilesFound.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.TextBoxFilesFound.ForeColor = System.Drawing.Color.White;
            this.TextBoxFilesFound.Location = new System.Drawing.Point(10, 37);
            this.TextBoxFilesFound.Multiline = true;
            this.TextBoxFilesFound.Name = "TextBoxFilesFound";
            this.TextBoxFilesFound.ReadOnly = true;
            this.TextBoxFilesFound.Size = new System.Drawing.Size(539, 454);
            this.TextBoxFilesFound.TabIndex = 11;
            // 
            // buttonMoveFile
            // 
            this.buttonMoveFile.AutoSize = true;
            this.buttonMoveFile.Location = new System.Drawing.Point(482, 550);
            this.buttonMoveFile.Name = "buttonMoveFile";
            this.buttonMoveFile.Size = new System.Drawing.Size(138, 23);
            this.buttonMoveFile.TabIndex = 10;
            this.buttonMoveFile.Text = "Move File";
            this.buttonMoveFile.UseVisualStyleBackColor = true;
            this.buttonMoveFile.Click += new System.EventHandler(this.buttonMoveFile_Click);
            // 
            // labelFilesFound
            // 
            this.labelFilesFound.AutoSize = true;
            this.labelFilesFound.Font = new System.Drawing.Font("Microsoft Sans Serif", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelFilesFound.ForeColor = System.Drawing.Color.White;
            this.labelFilesFound.Location = new System.Drawing.Point(477, 9);
            this.labelFilesFound.Name = "labelFilesFound";
            this.labelFilesFound.Size = new System.Drawing.Size(143, 25);
            this.labelFilesFound.TabIndex = 9;
            this.labelFilesFound.Text = "0 Files Found";
            // 
            // dropdownDirectories
            // 
            this.dropdownDirectories.FormattingEnabled = true;
            this.dropdownDirectories.Location = new System.Drawing.Point(367, 523);
            this.dropdownDirectories.Name = "dropdownDirectories";
            this.dropdownDirectories.Size = new System.Drawing.Size(380, 21);
            this.dropdownDirectories.TabIndex = 13;
            // 
            // textBoxFilename
            // 
            this.textBoxFilename.Location = new System.Drawing.Point(367, 497);
            this.textBoxFilename.Name = "textBoxFilename";
            this.textBoxFilename.Size = new System.Drawing.Size(380, 20);
            this.textBoxFilename.TabIndex = 14;
            // 
            // SchoolScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.textBoxFilename);
            this.Controls.Add(this.dropdownDirectories);
            this.Controls.Add(this.TextBoxFilesMoved);
            this.Controls.Add(this.TextBoxFilesFound);
            this.Controls.Add(this.buttonMoveFile);
            this.Controls.Add(this.labelFilesFound);
            this.Name = "SchoolScreen";
            this.Size = new System.Drawing.Size(1106, 586);
            this.Load += new System.EventHandler(this.SchoolScreen_Load);
            this.Enter += new System.EventHandler(this.SchoolScreen_Enter);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox TextBoxFilesMoved;
        private System.Windows.Forms.TextBox TextBoxFilesFound;
        private System.Windows.Forms.Button buttonMoveFile;
        private System.Windows.Forms.Label labelFilesFound;
        private System.Windows.Forms.ComboBox dropdownDirectories;
        private System.Windows.Forms.TextBox textBoxFilename;
    }
}
