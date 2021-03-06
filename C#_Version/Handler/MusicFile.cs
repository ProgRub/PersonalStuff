﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms.VisualStyles;

namespace Handler
{
    public class MusicFile
    {
        public string Filename { get; set; }
        public string Title { get; set; }
        public string ContributingArtists { get; set; }
        public string AlbumArtist { get; set; }
        public string Album { get; set; }
        public int TrackNumber { get; set; }
        public int NumberOfTracks { get; set; }
        public int DiscNumber { get; set; }
        public int NumberOfDiscs { get; set; }
        public string Genre { get; set; }
        public int Year { get; set; }
        public int Length { get; set; }
        public int PlayCount { get; set; }

        public MusicFile(string filename, string title, string contributingArtists, string albumArtist, string album, int trackNumber, int numberOfTracks, int discNumber, int numberOfDiscs, string genre, int year, int length,int playCount)
        {
            this.Filename = filename;
            this.Title = title;
            this.ContributingArtists = contributingArtists;
            this.AlbumArtist = albumArtist;
            this.Album = album;
            this.TrackNumber = trackNumber;
            this.NumberOfTracks = numberOfTracks;
            this.DiscNumber = discNumber;
            this.NumberOfDiscs = numberOfDiscs;
            this.Genre = genre;
            this.Year = year;
            this.Length = length;
            this.PlayCount = playCount;
        }
    }
}
