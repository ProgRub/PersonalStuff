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
    public partial class AlbumPropertiesScreen : UserControl
    {
        private HandlerForm Window;
        private List<CheckBox> GenresCheckBoxes;
        public AlbumPropertiesScreen(HandlerForm window)
        {
            InitializeComponent();
            this.Window = window;
            this.Window.AcceptButton = this.buttonConfirm;
            this.GenresCheckBoxes = new List<CheckBox>();
            this.radioButtonBoth.Checked = true;
            int index = 1;
            BackgroundWorker worker = new BackgroundWorker();
            worker.DoWork += new DoWorkEventHandler(this.Window.LAFContainer.GenerateAlbums);
            foreach (string genre in this.Window.LAFContainer.GenresColors.Keys)
            {
                CheckBox checkBox = new CheckBox();
                checkBox.AutoSize = true;
                checkBox.Font = new Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
                checkBox.ForeColor = this.Window.LAFContainer.GenresColors[genre];
                checkBox.Location = new Point(83, 232 + index * 25);
                checkBox.Name = "checkBox" + genre;
                checkBox.Size = new Size(93, 21);
                checkBox.TabIndex = 4 + index;
                checkBox.Text = genre;
                checkBox.UseMnemonic = false;
                checkBox.UseVisualStyleBackColor = true;
                checkBox.MouseClick += new MouseEventHandler(this.checkBox_MouseClick);
                index++;
                this.Controls.Add(checkBox);
                this.GenresCheckBoxes.Add(checkBox);
            }
            worker.RunWorkerAsync();
            this.dropdownWorkouts.Items.AddRange(this.Window.LAFContainer.WorkoutDatabase.Keys.ToArray());
            //this.Window.Controls.OfType<HomeScreen>().ToList()[0].Dispose();
        }

        #region Event Handlers

        private void checkBoxAllGenres_MouseClick(object sender, MouseEventArgs e)
        {
            Console.WriteLine(this.checkBoxAllGenres.Checked);
            for (int index = 0; index < this.GenresCheckBoxes.Count; index++)
            {
                this.GenresCheckBoxes[index].Checked = this.checkBoxAllGenres.Checked;
            }
        }

        private void checkBox_MouseClick(object sender, MouseEventArgs e)
        {
            this.checkBoxAllGenres.Checked = this.GenresCheckBoxes.All(checkBox => checkBox.Checked);
        }

        private void buttonAllAlbums_Click(object sender, EventArgs e)
        {
            this.textBoxTimeAlbum.Text = "240";
            this.textBoxLeewayAlbum.Text = "240";
            this.checkBoxAllGenres.Checked = true;
            this.GenresCheckBoxes.ForEach(checkBox => checkBox.Checked = true);
        }

        private void buttonAlbumForCar_Click(object sender, EventArgs e)
        {
            this.textBoxTimeAlbum.Text = "35";
            this.textBoxLeewayAlbum.Text = "10";
        }

        private void buttonAlbumForWorkout_Click(object sender, EventArgs e)
        {
            this.buttonAlbumForCar.Visible = false;
            this.buttonAlbumForWorkout.Visible = false;
            this.dropdownWorkouts.Visible = true;
            this.buttonConfirmWorkout.Visible = true;
            this.Window.AcceptButton = this.buttonConfirmWorkout;
        }

        private void buttonConfirmWorkout_Click(object sender, EventArgs e)
        {
            string workoutName = this.dropdownWorkouts.SelectedItem.ToString();
            var times = this.Window.LAFContainer.WorkoutDatabase[workoutName];
            int average = (times.Sum() / times.Count) / 60;
            if (times.Count == 1)
            {
                this.textBoxLeewayAlbum.Text = "5";
            }
            else
            {
                int leewayMinimum = Math.Abs(average - (times[0] / 60));
                int leewayMaximum = Math.Abs(average - (times.Last() / 60));
                this.textBoxLeewayAlbum.Text = Math.Max(leewayMinimum, leewayMaximum).ToString();
            }
            this.textBoxTimeAlbum.Text = average.ToString();
            this.buttonAlbumForCar.Visible = true;
            this.buttonAlbumForWorkout.Visible = true;
            this.dropdownWorkouts.Visible = false;
            this.buttonConfirmWorkout.Visible = false;
            this.Window.AcceptButton = this.buttonConfirm;
        }

        private void buttonConfirm_Click(object sender, EventArgs e)
        {
            int albumTime = 0;
            int albumLeeway = 0;
            int leewayMode = 0;
            if (radioButtonOver.Checked)
            {
                leewayMode = 1;
            }
            else if (radioButtonUnder.Checked)
            {
                leewayMode = 2;
            }
            bool advance = true;
            try
            {
                albumTime = Int32.Parse(this.textBoxTimeAlbum.Text);
            }
            catch (FormatException)
            {
                this.textBoxTimeAlbum.ForeColor = Color.Red;
                this.textBoxTimeAlbum.Text = "Missing the Time!";
                advance = false;
            }
            try
            {
                albumLeeway = Int32.Parse(this.textBoxLeewayAlbum.Text);
            }
            catch (FormatException)
            {
                this.textBoxLeewayAlbum.ForeColor = Color.Red;
                this.textBoxLeewayAlbum.Text = "Missing the Leeway!";
                advance = false;
            }
            if (advance)
            {
                this.Hide();
                List<string> genresPicked = new List<string>();
                foreach (var checkBox in this.GenresCheckBoxes)
                {
                    if (checkBox.Checked)
                    {
                        genresPicked.Add(checkBox.Text);
                    }
                }
                ChooseAlbumScreen aux = new ChooseAlbumScreen(this.Window, albumTime * 60, albumLeeway * 60, genresPicked, leewayMode);
                aux.Dock = DockStyle.Fill;
                this.Window.Controls.Add(aux);
                this.Window.ActiveControl = aux;
            }
        }

        private void textBoxTimeAlbum_Click(object sender, EventArgs e)
        {
            if (this.textBoxTimeAlbum.Text == "Missing the Time!")
            {
                this.textBoxTimeAlbum.ForeColor = Color.Black;
                this.textBoxTimeAlbum.Text = "";
            }
            if (this.textBoxLeewayAlbum.Text == "Missing the Leeway!")
            {
                this.textBoxLeewayAlbum.ForeColor = Color.Black;
                this.textBoxLeewayAlbum.Text = "";
            }
        }

        private void textBoxLeewayAlbum_Click(object sender, EventArgs e)
        {
            if (this.textBoxTimeAlbum.Text == "Missing the Time!")
            {
                this.textBoxTimeAlbum.ForeColor = Color.Black;
                this.textBoxTimeAlbum.Text = "";
            }
            if (this.textBoxLeewayAlbum.Text == "Missing the Leeway!")
            {
                this.textBoxLeewayAlbum.ForeColor = Color.Black;
                this.textBoxLeewayAlbum.Text = "";
            }
        }
        #endregion
    }
}
