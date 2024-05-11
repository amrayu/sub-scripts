This repo contains scripts that tie together various frameworks related to processing, converting, and cleaning up subtitles.

## batch-vtt-to-srt.py
Mainly created to clean-up NetFlix .vtt files and convert to .srt

### What does the script do?
- Removes WEBVTT header information
- Converts periods with commas in timestamps since .srt convention uses commas
- Removes metadata and unnecessary tags
- Removes empty lines and leading spaces at the beginning of the file
- Replaces HTML <i></i> tags with .srt convention tags {\i1}{\i0}
- Removes all HTML tags
- Removes positioning metadata

### Script requirements:
- [ffmpeg](https://ffmpeg.org/download.html) is required to handle some processes
- python3

### How to run:
- python3 batch-vtt-to-srt.py in terminal or commandline
- Input filepath to folder containing VTT files and hit enter

## dl-subs.py
Easy way to download, clean-up, and convert subtitles to .srt

## What does this script do?
- Download a .vtt file from Hulu JP and cleans, converts to .srt
- - Removes emojis from Hulu JP files
  - Removes WEBVTT metadata 
- Download a .vtt file from TVer and converts to .srt

### Script requirements:
- python3
- [ffmpeg](https://ffmpeg.org/download.html)
- subrip - I think this comes bundled with ffmpeg
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

### How to run:
- python3 dl-subs.py in terminal or commandline
- Input number based on prompt
- Either add direct link to Hulu JP .vtt or add TVer link
