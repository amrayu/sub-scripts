import os
import sys
import shlex
from pysrt import SubRipFile, SubRipItem

def merge_duplicate_subtitles(input_srt):
    # Expand tilde (~) and escape sequences in file paths
    input_srt = os.path.expanduser(input_srt)
    input_srt = os.path.abspath(input_srt)

    if not os.path.exists(input_srt):
        print(f"❌ Error: File '{input_srt}' not found.")
        return
    
    subs = SubRipFile.open(input_srt)
    merged_subs = []
    
    i = 0
    while i < len(subs):
        start_time = subs[i].start
        end_time = subs[i].end
        text = subs[i].text.strip()
        
        j = i + 1
        while j < len(subs) and subs[j].text.strip() == text:
            end_time = subs[j].end  # Extend end time to last occurrence
            j += 1
        
        merged_subs.append(SubRipItem(index=len(merged_subs) + 1, start=start_time, end=end_time, text=text))
        i = j  # Move to the next non-duplicate entry
    
    # Define output filename
    output_srt = os.path.splitext(input_srt)[0] + "_merged.srt"
    
    # Save the modified SRT file
    merged_srt = SubRipFile()
    merged_srt.extend(merged_subs)
    merged_srt.save(output_srt, encoding='utf-8')
    
    print(f"✅ Process complete! Merged subtitles saved to: {output_srt}")

if __name__ == "__main__":
    print("📂 Drag and drop your .srt file here and press Enter:")
    input_srt = input().strip()
    
    # Properly handle escape sequences in file paths
    input_srt = shlex.split(input_srt)[0] if "\\" in input_srt or " " in input_srt else input_srt
    
    merge_duplicate_subtitles(input_srt)
