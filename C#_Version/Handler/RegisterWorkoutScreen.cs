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
    public partial class RegisterWorkoutScreen : UserControl
    {
        private HandlerForm Window;
        public RegisterWorkoutScreen(HandlerForm window)
        {
            InitializeComponent();
            this.Window = window;
            this.Window.AcceptButton = this.buttonConfirm;
            this.Window.CancelButton = this.buttonBack;
            this.comboBoxWokouts.Items.AddRange(this.Window.LAFContainer.WorkoutDatabase.Keys.ToArray());
            this.comboBoxWokouts.Items.Add("New Workout");
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            this.Window.LAFContainer.SaveWorkoutDatabase();
            this.Dispose();
            this.Window.Controls.OfType<HomeScreen>().ToList()[0].Visible = true;
            this.Window.ActiveControl = this.Window.Controls.OfType<HomeScreen>().ToList()[0];
        }

        private int ConvertTimeToSeconds()
        {
            var auxList = this.textBoxTimeToComplete.Text.Split(':');
            if (auxList.Any(x => x.Length != 2))
            {
                return -1;
            }
            auxList = auxList.Reverse().ToArray();
            int seconds = 0;
            for (int index = 0; index < auxList.Length; index++)
            {
                seconds += Int32.Parse(auxList[index]) * Convert.ToInt32(Math.Pow(60,index));
            }
            return seconds;
        }

        private void buttonConfirm_Click(object sender, EventArgs e)
        {
            string workout;
            if(this.comboBoxWokouts.SelectedItem.ToString()=="New Workout")
            {
                workout = this.textBoxNewWorkout.Text.Trim();
                this.Window.LAFContainer.WorkoutDatabase.Add(workout, new List<int>());
                this.textBoxNewWorkout.Text = "";
            }
            else
            {
                workout = this.comboBoxWokouts.SelectedItem.ToString();
            }
            this.Window.LAFContainer.WorkoutDatabase[workout].Add(this.ConvertTimeToSeconds());
            this.textBoxTimeToComplete.Text = "";
            //Console.WriteLine(this.ConvertTimeToSeconds());

        }

        private void comboBoxWokouts_SelectedIndexChanged(object sender, EventArgs e)
        {
            if(this.comboBoxWokouts.SelectedItem.ToString()=="New Workout")
            {
                this.textBoxNewWorkout.Enabled = true;
            }
            else
            {
                this.textBoxNewWorkout.Enabled = false;
            }
        }
    }
}
