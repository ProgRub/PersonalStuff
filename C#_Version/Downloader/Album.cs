using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Downloader
{
    public class Album
    {
        public string Title { get; set; }
        public string Artist { get; set; }
        public int NumberOfTracks { get; set; }
        public int NumberOfDiscs { get; set; }
        public string Genre { get; set; }
        public int Year { get; set; }

        public List<List<MusicFile>> TracksByDiscs;

        public int Length { get; set; }

        public float AveragePlayCount { get; set; }

        public Album(string title, string artist, int numberOfTracks, int numberOfDiscs, string genre, int year)
        {
            this.Title = title;
            this.Artist = artist;
            this.NumberOfTracks = numberOfTracks;
            this.NumberOfDiscs = numberOfDiscs;
            this.Genre = genre;
            this.Year = year;
            this.Length = 0;
            this.AveragePlayCount = 0;
            this.TracksByDiscs = new List<List<MusicFile>>();
            for (int disc = 0; disc < this.NumberOfDiscs; disc++)
            {
                this.TracksByDiscs.Add(new List<MusicFile>());
            }
        }

        public void AddTrack(MusicFile track)
        {
            this.TracksByDiscs[track.DiscNumber - 1].Add(track);
            for (int index = this.TracksByDiscs[track.DiscNumber - 1].Count - 1; index >= 0; index--)
            {
                if (this.TracksByDiscs[track.DiscNumber - 1][index].TrackNumber < this.TracksByDiscs[track.DiscNumber - 1][index - 1].TrackNumber)
                {
                    MusicFile aux = this.TracksByDiscs[track.DiscNumber - 1][index - 1];
                    this.TracksByDiscs[track.DiscNumber - 1][index - 1] = this.TracksByDiscs[track.DiscNumber - 1][index];
                    this.TracksByDiscs[track.DiscNumber - 1][index] = aux;
                }
                else
                {
                    break;
                }
            }
            this.Length += track.Length;
            this.AveragePlayCount += track.PlayCount;
        }
    }
}
