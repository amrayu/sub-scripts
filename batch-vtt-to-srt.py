import os
import re
import ffmpeg
import shutil

def preprocess_vtt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        vtt_content = f.read()
    
    # Remove "WEBVTT" line at the top of the file
    vtt_content = re.sub(r"^WEBVTT\s*\n", "", vtt_content)

    # Replace periods with commas in timestamp lines
    vtt_content = re.sub(r"(\d{2}:\d{2}:\d{2})[.,](\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2})[.,](\d{3})", r"\1,\2 --> \3,\4", vtt_content)
    
    # Remove metadata and unnecessary tags
    vtt_content = re.sub(r"^NOTE.*?$", "", vtt_content, flags=re.MULTILINE)  # Remove NOTE lines
    vtt_content = vtt_content.replace("&lrm;", "")  # Remove &lrm; content

    # Remove empty lines and leading spaces at the beginning of the file
    vtt_content = vtt_content.strip()
    
    # Replace <i></i> tags with {\i1} and {\i0}
    vtt_content = re.sub(r"<(?!/i)(\w+)>", r"{\\i1}", vtt_content)  # Replace opening tags
    vtt_content = re.sub(r"</(\w+)>", r"{\\i0}", vtt_content)  # Replace closing tags

    # Remove <c.bg_transparent> tags
    # vtt_content = vtt_content.replace("<c.bg_transparent>", "").replace("</c.bg_transparent>", "")

    # Remove all HTML tags
    vtt_content = re.sub(r"<[^>]+>", "", vtt_content)
    
    # Remove positioning metadata
    vtt_content = re.sub(r"position:.*$", "", vtt_content, flags=re.MULTILINE)
    
    # Write preprocessed content to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(vtt_content)

def convert_vtt_to_srt(input_file):
    output_file = os.path.splitext(input_file)[0] + ".srt"
    print(f"Converting {input_file} to {output_file}...")
    try:
        preprocess_vtt(input_file, output_file)
        stream = ffmpeg.input(output_file)
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream, overwrite_output=True, quiet=True, capture_stderr=True)  # Capture stderr output
    except ffmpeg._run.Error as e:
        print(f"Error converting {input_file}: {e.stderr.decode()}")  # Print stderr output

def batch_convert_vtt_to_srt():
    input_folder = input("Enter the path to the folder containing VTT files: ")
    if not os.path.exists(input_folder):
        print(f"Error: Directory '{input_folder}' not found.")
        return
    
    for file in os.listdir(input_folder):
        if file.endswith(".vtt"):
            input_file = os.path.join(input_folder, file)
            convert_vtt_to_srt(input_file)

if __name__ == "__main__":
    batch_convert_vtt_to_srt()
