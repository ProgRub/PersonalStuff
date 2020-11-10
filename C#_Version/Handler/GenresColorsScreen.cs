using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Handler
{
    public partial class GenresColorsScreen : UserControl
    {
        private HandlerForm Window;
        private Dictionary<string, Control> GenreControls;
        public GenresColorsScreen(HandlerForm window)
        {
            InitializeComponent();
            this.Window = window;
            this.Window.CancelButton = this.buttonBack;
            this.GenreControls = new Dictionary<string, Control>();
            int index = 1;
            foreach (string genre in this.Window.LAFContainer.GenresColors.Keys)
            {
                Button button = new Button();
                button.AutoSize = true;
                button.AutoSizeMode = AutoSizeMode.GrowAndShrink;
                button.BackColor = Color.Transparent;
                button.FlatStyle = FlatStyle.Flat;
                button.FlatAppearance.BorderColor = this.Window.BackColor;
                button.FlatAppearance.BorderSize=0;
                button.FlatAppearance.MouseDownBackColor = Color.Transparent;
                button.FlatAppearance.MouseOverBackColor = Color.Transparent;
                button.Font = new Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
                button.ForeColor = this.Window.LAFContainer.GenresColors[genre];
                button.Location = new Point(10, 50 + index * 30);
                button.Name = "checkBox" + genre;
                button.TabIndex = 5 + index;
                button.Text = genre;
                button.UseVisualStyleBackColor = true;
                button.Click += new System.EventHandler(this.ChangeGenreColor);
                index++;
                this.Controls.Add(button);
                this.GenreControls[genre] = button;
                //this.GenresCheckBoxes.Add(checkBox);
            }
        }

        #region Event Handlers

        private void ChangeGenreColor(object sender, EventArgs e)
        {
            DialogResult dialogResult = this.colorDialog1.ShowDialog();
            if (dialogResult == DialogResult.OK)
            {
                this.Window.LAFContainer.GenresColors[((Button)sender).Text] = this.colorDialog1.Color;
                this.GenreControls[((Button)sender).Text].ForeColor = this.colorDialog1.Color;
            }
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            this.Window.LAFContainer.SaveGenreColors();
            this.Dispose();
            this.Window.ActiveControl = this.Window.Controls.OfType<HomeScreen>().ToList()[0];
            this.Window.Controls.OfType<HomeScreen>().ToList()[0].Visible = true;
        }
        #endregion
    }
}
