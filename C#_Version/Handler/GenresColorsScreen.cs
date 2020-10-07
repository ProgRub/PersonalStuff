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
        private Dictionary<string, List<Control>> GenreControls;
        public GenresColorsScreen()
        {
            InitializeComponent();
            this.GenreControls = new Dictionary<string, List<Control>>();
        }

        private void GenresColorsScreen_Load(object sender, EventArgs e)
        {
            this.Window = this.Parent as HandlerForm;
            int index = 0;
            foreach (string genre in this.Window.LAFContainer.GenresColors.Keys)
            {
                Button button = new Button();
                button.AutoSize = true;
                button.Font = new Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
                button.ForeColor = this.Window.LAFContainer.GenresColors[genre];
                button.Location = new Point(10, 10 + index * 30);
                button.Name = "checkBox" + genre;
                button.Size = new Size(93, 21);
                button.TabIndex = 5 + index;
                button.Text = genre;
                button.UseVisualStyleBackColor = true;
                button.Click += new System.EventHandler(this.ChangeGenreColor);
                Label label = new Label();
                label.AutoSize = true;
                label.Font = new Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
                label.ForeColor = this.Window.LAFContainer.GenresColors[genre];
                label.Location = new Point(150, 15 + index * 30);
                label.Name = "label" + genre;
                label.Size = new Size(93, 21);
                label.TabIndex = 5 + index;
                label.Text = genre;
                label.TextAlign = ContentAlignment.MiddleCenter;
                index++;
                this.Controls.Add(button);
                this.Controls.Add(label);
                this.GenreControls[genre] = new List<Control>() { button, label };
                //this.GenresCheckBoxes.Add(checkBox);
            }
        }

        private void ChangeGenreColor(object sender, EventArgs e)
        {
            DialogResult dialogResult = this.colorDialog1.ShowDialog();
            if (dialogResult == DialogResult.OK)
            {
                this.Window.LAFContainer.GenresColors[((Button)sender).Text] = this.colorDialog1.Color;
                this.GenreControls[((Button)sender).Text][0].ForeColor = this.colorDialog1.Color;
                this.GenreControls[((Button)sender).Text][1].ForeColor = this.colorDialog1.Color;
                //Color color = Color.FromArgb(this.colorDialog1.Color.ToArgb());
                //Console.WriteLine(color);
            }
            //Console.WriteLine(dialogResult);
            //Console.WriteLine(((Button)sender).Text);
        }
    }
}
