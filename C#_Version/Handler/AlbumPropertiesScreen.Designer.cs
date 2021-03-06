﻿namespace Handler
{
    partial class AlbumPropertiesScreen
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
            this.textBoxTimeAlbum = new System.Windows.Forms.TextBox();
            this.textBoxLeewayAlbum = new System.Windows.Forms.TextBox();
            this.labelTime = new System.Windows.Forms.Label();
            this.labelLeeway = new System.Windows.Forms.Label();
            this.checkBoxAllGenres = new System.Windows.Forms.CheckBox();
            this.buttonAllAlbums = new System.Windows.Forms.Button();
            this.buttonAlbumForWorkout = new System.Windows.Forms.Button();
            this.buttonAlbumForCar = new System.Windows.Forms.Button();
            this.dropdownWorkouts = new System.Windows.Forms.ComboBox();
            this.buttonConfirmWorkout = new System.Windows.Forms.Button();
            this.buttonConfirm = new System.Windows.Forms.Button();
            this.radioButtonBoth = new System.Windows.Forms.RadioButton();
            this.radioButtonOver = new System.Windows.Forms.RadioButton();
            this.radioButtonUnder = new System.Windows.Forms.RadioButton();
            this.labelLeewayType = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // textBoxTimeAlbum
            // 
            this.textBoxTimeAlbum.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(4)))), ((int)(((byte)(64)))));
            this.textBoxTimeAlbum.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.textBoxTimeAlbum.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxTimeAlbum.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.textBoxTimeAlbum.Location = new System.Drawing.Point(235, 31);
            this.textBoxTimeAlbum.Name = "textBoxTimeAlbum";
            this.textBoxTimeAlbum.Size = new System.Drawing.Size(162, 23);
            this.textBoxTimeAlbum.TabIndex = 0;
            this.textBoxTimeAlbum.Click += new System.EventHandler(this.textBoxTimeAlbum_Click);
            // 
            // textBoxLeewayAlbum
            // 
            this.textBoxLeewayAlbum.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(4)))), ((int)(((byte)(64)))));
            this.textBoxLeewayAlbum.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.textBoxLeewayAlbum.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxLeewayAlbum.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.textBoxLeewayAlbum.Location = new System.Drawing.Point(235, 63);
            this.textBoxLeewayAlbum.Name = "textBoxLeewayAlbum";
            this.textBoxLeewayAlbum.Size = new System.Drawing.Size(162, 23);
            this.textBoxLeewayAlbum.TabIndex = 1;
            this.textBoxLeewayAlbum.Click += new System.EventHandler(this.textBoxLeewayAlbum_Click);
            // 
            // labelTime
            // 
            this.labelTime.AutoSize = true;
            this.labelTime.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelTime.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.labelTime.Location = new System.Drawing.Point(190, 37);
            this.labelTime.Name = "labelTime";
            this.labelTime.Size = new System.Drawing.Size(39, 17);
            this.labelTime.TabIndex = 2;
            this.labelTime.Text = "Time";
            // 
            // labelLeeway
            // 
            this.labelLeeway.AutoSize = true;
            this.labelLeeway.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelLeeway.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.labelLeeway.Location = new System.Drawing.Point(173, 69);
            this.labelLeeway.Name = "labelLeeway";
            this.labelLeeway.Size = new System.Drawing.Size(56, 17);
            this.labelLeeway.TabIndex = 3;
            this.labelLeeway.Text = "Leeway";
            // 
            // checkBoxAllGenres
            // 
            this.checkBoxAllGenres.AutoSize = true;
            this.checkBoxAllGenres.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxAllGenres.ForeColor = System.Drawing.Color.White;
            this.checkBoxAllGenres.Location = new System.Drawing.Point(83, 232);
            this.checkBoxAllGenres.Name = "checkBoxAllGenres";
            this.checkBoxAllGenres.Size = new System.Drawing.Size(93, 21);
            this.checkBoxAllGenres.TabIndex = 4;
            this.checkBoxAllGenres.Text = "All Genres";
            this.checkBoxAllGenres.UseVisualStyleBackColor = true;
            this.checkBoxAllGenres.MouseClick += new System.Windows.Forms.MouseEventHandler(this.checkBoxAllGenres_MouseClick);
            // 
            // buttonAllAlbums
            // 
            this.buttonAllAlbums.AutoSize = true;
            this.buttonAllAlbums.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.buttonAllAlbums.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(3)))), ((int)(((byte)(3)))), ((int)(((byte)(31)))));
            this.buttonAllAlbums.FlatAppearance.BorderSize = 0;
            this.buttonAllAlbums.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.buttonAllAlbums.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.buttonAllAlbums.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonAllAlbums.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonAllAlbums.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(124)))), ((int)(((byte)(219)))));
            this.buttonAllAlbums.Location = new System.Drawing.Point(83, 203);
            this.buttonAllAlbums.Name = "buttonAllAlbums";
            this.buttonAllAlbums.Size = new System.Drawing.Size(83, 27);
            this.buttonAllAlbums.TabIndex = 5;
            this.buttonAllAlbums.Text = "All Albums";
            this.buttonAllAlbums.UseVisualStyleBackColor = true;
            this.buttonAllAlbums.Click += new System.EventHandler(this.buttonAllAlbums_Click);
            // 
            // buttonAlbumForWorkout
            // 
            this.buttonAlbumForWorkout.AutoSize = true;
            this.buttonAlbumForWorkout.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.buttonAlbumForWorkout.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(3)))), ((int)(((byte)(3)))), ((int)(((byte)(31)))));
            this.buttonAlbumForWorkout.FlatAppearance.BorderSize = 0;
            this.buttonAlbumForWorkout.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.buttonAlbumForWorkout.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.buttonAlbumForWorkout.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonAlbumForWorkout.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonAlbumForWorkout.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(124)))), ((int)(((byte)(219)))));
            this.buttonAlbumForWorkout.Location = new System.Drawing.Point(437, 31);
            this.buttonAlbumForWorkout.Name = "buttonAlbumForWorkout";
            this.buttonAlbumForWorkout.Size = new System.Drawing.Size(96, 27);
            this.buttonAlbumForWorkout.TabIndex = 6;
            this.buttonAlbumForWorkout.Text = "For Workout";
            this.buttonAlbumForWorkout.UseVisualStyleBackColor = true;
            this.buttonAlbumForWorkout.Click += new System.EventHandler(this.buttonAlbumForWorkout_Click);
            // 
            // buttonAlbumForCar
            // 
            this.buttonAlbumForCar.AutoSize = true;
            this.buttonAlbumForCar.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.buttonAlbumForCar.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(3)))), ((int)(((byte)(3)))), ((int)(((byte)(31)))));
            this.buttonAlbumForCar.FlatAppearance.BorderSize = 0;
            this.buttonAlbumForCar.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.buttonAlbumForCar.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.buttonAlbumForCar.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonAlbumForCar.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonAlbumForCar.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(124)))), ((int)(((byte)(219)))));
            this.buttonAlbumForCar.Location = new System.Drawing.Point(437, 63);
            this.buttonAlbumForCar.Name = "buttonAlbumForCar";
            this.buttonAlbumForCar.Size = new System.Drawing.Size(65, 27);
            this.buttonAlbumForCar.TabIndex = 7;
            this.buttonAlbumForCar.Text = "For Car";
            this.buttonAlbumForCar.UseVisualStyleBackColor = true;
            this.buttonAlbumForCar.Click += new System.EventHandler(this.buttonAlbumForCar_Click);
            // 
            // dropdownWorkouts
            // 
            this.dropdownWorkouts.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(4)))), ((int)(((byte)(64)))));
            this.dropdownWorkouts.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.dropdownWorkouts.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.dropdownWorkouts.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.dropdownWorkouts.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.dropdownWorkouts.FormattingEnabled = true;
            this.dropdownWorkouts.Location = new System.Drawing.Point(437, 30);
            this.dropdownWorkouts.Name = "dropdownWorkouts";
            this.dropdownWorkouts.Size = new System.Drawing.Size(208, 24);
            this.dropdownWorkouts.TabIndex = 8;
            this.dropdownWorkouts.Visible = false;
            // 
            // buttonConfirmWorkout
            // 
            this.buttonConfirmWorkout.AutoSize = true;
            this.buttonConfirmWorkout.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.buttonConfirmWorkout.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(3)))), ((int)(((byte)(3)))), ((int)(((byte)(31)))));
            this.buttonConfirmWorkout.FlatAppearance.BorderSize = 0;
            this.buttonConfirmWorkout.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.buttonConfirmWorkout.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.buttonConfirmWorkout.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonConfirmWorkout.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonConfirmWorkout.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(124)))), ((int)(((byte)(219)))));
            this.buttonConfirmWorkout.Location = new System.Drawing.Point(478, 64);
            this.buttonConfirmWorkout.Name = "buttonConfirmWorkout";
            this.buttonConfirmWorkout.Size = new System.Drawing.Size(123, 27);
            this.buttonConfirmWorkout.TabIndex = 9;
            this.buttonConfirmWorkout.Text = "Confirm Workout";
            this.buttonConfirmWorkout.UseVisualStyleBackColor = true;
            this.buttonConfirmWorkout.Visible = false;
            this.buttonConfirmWorkout.Click += new System.EventHandler(this.buttonConfirmWorkout_Click);
            // 
            // buttonConfirm
            // 
            this.buttonConfirm.AutoSize = true;
            this.buttonConfirm.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.buttonConfirm.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(3)))), ((int)(((byte)(3)))), ((int)(((byte)(31)))));
            this.buttonConfirm.FlatAppearance.BorderSize = 0;
            this.buttonConfirm.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.buttonConfirm.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.buttonConfirm.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonConfirm.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonConfirm.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(124)))), ((int)(((byte)(219)))));
            this.buttonConfirm.Location = new System.Drawing.Point(286, 103);
            this.buttonConfirm.Name = "buttonConfirm";
            this.buttonConfirm.Size = new System.Drawing.Size(66, 27);
            this.buttonConfirm.TabIndex = 10;
            this.buttonConfirm.Text = "Confirm";
            this.buttonConfirm.UseVisualStyleBackColor = true;
            this.buttonConfirm.Click += new System.EventHandler(this.buttonConfirm_Click);
            // 
            // radioButtonBoth
            // 
            this.radioButtonBoth.AutoSize = true;
            this.radioButtonBoth.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBoth.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.radioButtonBoth.Location = new System.Drawing.Point(83, 123);
            this.radioButtonBoth.Name = "radioButtonBoth";
            this.radioButtonBoth.Size = new System.Drawing.Size(55, 21);
            this.radioButtonBoth.TabIndex = 11;
            this.radioButtonBoth.TabStop = true;
            this.radioButtonBoth.Text = "Both";
            this.radioButtonBoth.UseVisualStyleBackColor = true;
            // 
            // radioButtonOver
            // 
            this.radioButtonOver.AutoSize = true;
            this.radioButtonOver.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonOver.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.radioButtonOver.Location = new System.Drawing.Point(83, 146);
            this.radioButtonOver.Name = "radioButtonOver";
            this.radioButtonOver.Size = new System.Drawing.Size(57, 21);
            this.radioButtonOver.TabIndex = 12;
            this.radioButtonOver.TabStop = true;
            this.radioButtonOver.Text = "Over";
            this.radioButtonOver.UseVisualStyleBackColor = true;
            // 
            // radioButtonUnder
            // 
            this.radioButtonUnder.AutoSize = true;
            this.radioButtonUnder.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonUnder.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.radioButtonUnder.Location = new System.Drawing.Point(83, 169);
            this.radioButtonUnder.Name = "radioButtonUnder";
            this.radioButtonUnder.Size = new System.Drawing.Size(65, 21);
            this.radioButtonUnder.TabIndex = 13;
            this.radioButtonUnder.TabStop = true;
            this.radioButtonUnder.Text = "Under";
            this.radioButtonUnder.UseVisualStyleBackColor = true;
            // 
            // labelLeewayType
            // 
            this.labelLeewayType.AutoSize = true;
            this.labelLeewayType.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelLeewayType.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.labelLeewayType.Location = new System.Drawing.Point(80, 103);
            this.labelLeewayType.Name = "labelLeewayType";
            this.labelLeewayType.Size = new System.Drawing.Size(92, 17);
            this.labelLeewayType.TabIndex = 14;
            this.labelLeewayType.Text = "Leeway Type";
            // 
            // AlbumPropertiesScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.labelLeewayType);
            this.Controls.Add(this.radioButtonUnder);
            this.Controls.Add(this.radioButtonOver);
            this.Controls.Add(this.radioButtonBoth);
            this.Controls.Add(this.buttonConfirm);
            this.Controls.Add(this.buttonConfirmWorkout);
            this.Controls.Add(this.dropdownWorkouts);
            this.Controls.Add(this.buttonAlbumForCar);
            this.Controls.Add(this.buttonAlbumForWorkout);
            this.Controls.Add(this.buttonAllAlbums);
            this.Controls.Add(this.checkBoxAllGenres);
            this.Controls.Add(this.labelLeeway);
            this.Controls.Add(this.labelTime);
            this.Controls.Add(this.textBoxLeewayAlbum);
            this.Controls.Add(this.textBoxTimeAlbum);
            this.Name = "AlbumPropertiesScreen";
            this.Size = new System.Drawing.Size(704, 660);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBoxTimeAlbum;
        private System.Windows.Forms.TextBox textBoxLeewayAlbum;
        private System.Windows.Forms.Label labelTime;
        private System.Windows.Forms.Label labelLeeway;
        private System.Windows.Forms.CheckBox checkBoxAllGenres;
        private System.Windows.Forms.Button buttonAllAlbums;
        private System.Windows.Forms.Button buttonAlbumForWorkout;
        private System.Windows.Forms.Button buttonAlbumForCar;
        private System.Windows.Forms.ComboBox dropdownWorkouts;
        private System.Windows.Forms.Button buttonConfirmWorkout;
        private System.Windows.Forms.Button buttonConfirm;
        private System.Windows.Forms.RadioButton radioButtonBoth;
        private System.Windows.Forms.RadioButton radioButtonOver;
        private System.Windows.Forms.RadioButton radioButtonUnder;
        private System.Windows.Forms.Label labelLeewayType;
    }
}
