This repo contains scripts related to processing, converting, and cleaning up subtitles.

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
- ffmpeg is required to handle some processes
- python3

### How to run:
- python3 batch-vtt-to-srt.py in terminal or commandline
- Input filepath to folder containing VTT files and hit enter
