namespace Handler
{
    partial class RegisterWorkoutScreen
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
            this.labelWD = new System.Windows.Forms.Label();
            this.labelNewWorkout = new System.Windows.Forms.Label();
            this.labelTTC = new System.Windows.Forms.Label();
            this.textBoxNewWorkout = new System.Windows.Forms.TextBox();
            this.textBoxTimeToComplete = new System.Windows.Forms.TextBox();
            this.labelFormat = new System.Windows.Forms.Label();
            this.comboBoxWokouts = new System.Windows.Forms.ComboBox();
            this.buttonBack = new System.Windows.Forms.Button();
            this.buttonConfirm = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // labelWD
            // 
            this.labelWD.AutoSize = true;
            this.labelWD.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelWD.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.labelWD.Location = new System.Drawing.Point(3, 30);
            this.labelWD.Name = "labelWD";
            this.labelWD.Size = new System.Drawing.Size(126, 17);
            this.labelWD.TabIndex = 0;
            this.labelWD.Text = "Workout Database";
            // 
            // labelNewWorkout
            // 
            this.labelNewWorkout.AutoSize = true;
            this.labelNewWorkout.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelNewWorkout.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.labelNewWorkout.Location = new System.Drawing.Point(3, 63);
            this.labelNewWorkout.Name = "labelNewWorkout";
            this.labelNewWorkout.Size = new System.Drawing.Size(92, 17);
            this.labelNewWorkout.TabIndex = 1;
            this.labelNewWorkout.Text = "New Workout";
            // 
            // labelTTC
            // 
            this.labelTTC.AutoSize = true;
            this.labelTTC.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelTTC.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.labelTTC.Location = new System.Drawing.Point(3, 98);
            this.labelTTC.Name = "labelTTC";
            this.labelTTC.Size = new System.Drawing.Size(123, 17);
            this.labelTTC.TabIndex = 2;
            this.labelTTC.Text = "Time To Complete";
            // 
            // textBoxNewWorkout
            // 
            this.textBoxNewWorkout.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(4)))), ((int)(((byte)(64)))));
            this.textBoxNewWorkout.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.textBoxNewWorkout.Enabled = false;
            this.textBoxNewWorkout.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxNewWorkout.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.textBoxNewWorkout.Location = new System.Drawing.Point(135, 60);
            this.textBoxNewWorkout.Name = "textBoxNewWorkout";
            this.textBoxNewWorkout.Size = new System.Drawing.Size(334, 23);
            this.textBoxNewWorkout.TabIndex = 3;
            // 
            // textBoxTimeToComplete
            // 
            this.textBoxTimeToComplete.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(4)))), ((int)(((byte)(64)))));
            this.textBoxTimeToComplete.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.textBoxTimeToComplete.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxTimeToComplete.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.textBoxTimeToComplete.Location = new System.Drawing.Point(135, 95);
            this.textBoxTimeToComplete.Name = "textBoxTimeToComplete";
            this.textBoxTimeToComplete.Size = new System.Drawing.Size(154, 23);
            this.textBoxTimeToComplete.TabIndex = 4;
            // 
            // labelFormat
            // 
            this.labelFormat.AutoSize = true;
            this.labelFormat.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelFormat.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.labelFormat.Location = new System.Drawing.Point(295, 98);
            this.labelFormat.Name = "labelFormat";
            this.labelFormat.Size = new System.Drawing.Size(104, 17);
            this.labelFormat.TabIndex = 5;
            this.labelFormat.Text = "Format: MM:SS";
            // 
            // comboBoxWokouts
            // 
            this.comboBoxWokouts.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(4)))), ((int)(((byte)(64)))));
            this.comboBoxWokouts.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxWokouts.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.comboBoxWokouts.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBoxWokouts.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(151)))), ((int)(((byte)(151)))), ((int)(((byte)(161)))));
            this.comboBoxWokouts.FormattingEnabled = true;
            this.comboBoxWokouts.Location = new System.Drawing.Point(135, 27);
            this.comboBoxWokouts.Name = "comboBoxWokouts";
            this.comboBoxWokouts.Size = new System.Drawing.Size(334, 24);
            this.comboBoxWokouts.TabIndex = 6;
            this.comboBoxWokouts.SelectedIndexChanged += new System.EventHandler(this.comboBoxWokouts_SelectedIndexChanged);
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
            this.buttonBack.Location = new System.Drawing.Point(0, 0);
            this.buttonBack.Name = "buttonBack";
            this.buttonBack.Size = new System.Drawing.Size(49, 27);
            this.buttonBack.TabIndex = 7;
            this.buttonBack.Text = "Back";
            this.buttonBack.UseVisualStyleBackColor = true;
            this.buttonBack.Click += new System.EventHandler(this.buttonBack_Click);
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
            this.buttonConfirm.Location = new System.Drawing.Point(261, 124);
            this.buttonConfirm.Name = "buttonConfirm";
            this.buttonConfirm.Size = new System.Drawing.Size(66, 27);
            this.buttonConfirm.TabIndex = 8;
            this.buttonConfirm.Text = "Confirm";
            this.buttonConfirm.UseVisualStyleBackColor = true;
            this.buttonConfirm.Click += new System.EventHandler(this.buttonConfirm_Click);
            // 
            // RegisterWorkoutScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.buttonConfirm);
            this.Controls.Add(this.buttonBack);
            this.Controls.Add(this.comboBoxWokouts);
            this.Controls.Add(this.labelFormat);
            this.Controls.Add(this.textBoxTimeToComplete);
            this.Controls.Add(this.textBoxNewWorkout);
            this.Controls.Add(this.labelTTC);
            this.Controls.Add(this.labelNewWorkout);
            this.Controls.Add(this.labelWD);
            this.Name = "RegisterWorkoutScreen";
            this.Size = new System.Drawing.Size(472, 154);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label labelWD;
        private System.Windows.Forms.Label labelNewWorkout;
        private System.Windows.Forms.Label labelTTC;
        private System.Windows.Forms.TextBox textBoxNewWorkout;
        private System.Windows.Forms.TextBox textBoxTimeToComplete;
        private System.Windows.Forms.Label labelFormat;
        private System.Windows.Forms.ComboBox comboBoxWokouts;
        private System.Windows.Forms.Button buttonBack;
        private System.Windows.Forms.Button buttonConfirm;
    }
}
