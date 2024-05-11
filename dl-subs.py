import re
import os
import subprocess

def download_and_convert_vtt_to_srt(vtt_link, srt_file_path):
    command = f'ffmpeg -i "{vtt_link}" -c:s subrip "{srt_file_path}"'
    subprocess.call(command, shell=True)

def download_tver_and_convert_vtt_to_srt(tver_link):
    # Download VTT using yt-dlp
    yt_dlp_command = f'yt-dlp "{tver_link}" --write-sub --convert-sub=srt --skip-download -k'
    subprocess.call(yt_dlp_command, shell=True)

def download_convert_nhk_caps(nhk_link):
    # Path to the convert.py script - Replace with absolute path to convert-ttml
    convert_script_path = "/path/to/convert-ttml.py"

    # Prompt for TTML file name
    ttml_file_name = input("Enter the name of the TTML file (without extension): ")
    ttml_file_path = f"{ttml_file_name}.ttml"

    # Download TTML file using curl
    command = f'curl -o "{ttml_file_path}" "{nhk_link}"'
    subprocess.call(command, shell=True)   

    # Run the conversion script on the downloaded TTML file
    convert_command = f'python3 "{convert_script_path}" "{ttml_file_path}"'
    subprocess.call(convert_command, shell=True)

    print("TTML to SRT conversion completed.") 

def process_vtt_files_in_folder(folder_path):
    # Get all .vtt files in the specified folder
    vtt_files = [file for file in os.listdir(folder_path) if file.endswith(".vtt")]

    if not vtt_files:
        print("No .vtt files found in the specified folder.")
        return

    # Create a list to store all FFmpeg commands
    commands = []    

    for vtt_file in vtt_files:
        srt_file = os.path.join(folder_path, os.path.splitext(vtt_file)[0] + ".srt")
        vtt_file_path = os.path.join(folder_path, vtt_file)
        print(f"Converting {vtt_file_path} to {srt_file}")

        # Append the FFmpeg command to the list
        commands.append(f'ffmpeg -i "{vtt_file_path}" -c:s subrip "{srt_file}"')

    # Join all commands into a single string and execute them in one subprocess.run call
    bulk_command = " && ".join(commands)
    subprocess.run(bulk_command, shell=True)    

    print(f"Bulk conversion of .vtt files in {folder_path} to .srt completed.")



#def download_tver_and_check_vtt(tver_link):
    # Download VTT using yt-dlp
#    downloaded_vtt_path = f"{tver_link.split('/')[-1]}.vtt"
#    yt_dlp_command = f'yt-dlp "{tver_link}" --write-sub --skip-download -k -o "{downloaded_vtt_path}"'
#    subprocess.call(yt_dlp_command, shell=True)

    # Check if "align:start" and "position:" are present in the downloaded .vtt file
#    if os.path.exists(downloaded_vtt_path) and \
#            any("align:start" in line or "position:" in line for line in open(downloaded_vtt_path, 'r')):
#        print("Flag: Downloaded .vtt has 'align:start' or 'position:' information.")

        # Convert VTT to SRT using FFmpeg
#        converted_srt_path = f"{downloaded_vtt_path[:-4]}_overlaps.srt"
#        download_and_convert_vtt_to_srt(downloaded_vtt_path, converted_srt_path)

        # Auto-convert using the specified command
#        convert_command = f'./subtitle-overlap-fixer {converted_srt_path}'
#        subprocess.call(convert_command, shell=True)

#        print("Overlap Fixer process completed.")
#    else:
#        print("Flag: Downloaded .vtt does not have 'align:start' or 'position:' information.")

        # Download VTT using yt-dlp
#        yt_dlp_command = f'yt-dlp "{tver_link}" --write-sub --convert-sub=srt --skip-download -k'
#        subprocess.call(yt_dlp_command, shell=True)

#        print("VTT converted to SRT.")

def clean_srt_file(srt_file_path):
    # Path to the cleaned SRT file
    new_file_path = os.path.splitext(srt_file_path)[0] + ".ja-JP.srt"
    with open(srt_file_path, "r") as file:
        content = file.read()

    # Remove "/h", "📱", "🔊", "📺" from the content
    content = re.sub(r'[\\📱🔊📺h]', '', content)

    # Remove WEBVTT and positioning information if present
    content = re.sub(r"WEBVTT\n", "", content)
    content = re.sub(r"X-TIMESTAMP-MAP=.+\n", "", content)

    # Write the cleaned SRT file
    with open(new_file_path, "w") as file:
        file.write(content)

    return new_file_path

# Prompt for input type
input_type = input("Enter '1' for VTT link or '2' for local SRT file or '3' for TVer link or '4' for ttml link: ")

if input_type == '1':
    # Prompt for VTT link
    vtt_link = input("Enter the VTT link: ")
    
    # Prompt for SRT file name
    srt_file_name = input("Enter the name of the SRT file (without extension): ")
    srt_file_path = f"{srt_file_name}.srt"
    
    # Download and convert VTT to SRT using FFmpeg
    download_and_convert_vtt_to_srt(vtt_link, srt_file_path)

    # Clean up the SRT file
    fixed_srt_file_path = clean_srt_file(srt_file_path)
    print(f"The cleaned SRT file has been saved as: {fixed_srt_file_path}")
    
elif input_type == '2':
    # Prompt for local SRT file path
    local_srt_path = input("Enter the path of the local SRT file: ").strip()  # Remove leading/trailing spaces
    
    # Use the local SRT file directly
    srt_file_path = local_srt_path
    
    # Clean up the SRT file
    fixed_srt_file_path = clean_srt_file(srt_file_path)
    print(f"The cleaned SRT file has been saved as: {fixed_srt_file_path}")

elif input_type == '3':
    # Prompt for TVer link
    tver_link = input("Enter TVer link: ")

    # Download from TVer and convert VTT to SRT
    download_tver_and_convert_vtt_to_srt(tver_link)
    print(f"VTT converted to SRT.")

elif input_type == '4':
    # Prompt for TTML link
    nhk_link = input("Enter the NHK-TTML link: ")
    
    # Download and convert TTML to SRT using FFmpeg
    download_convert_nhk_caps(nhk_link)  

elif input_type == '5':
    # Prompt for folder path
    folder_path = input("Enter the path of the folder containing .vtt files: ")

    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        process_vtt_files_in_folder(folder_path)
    else:
        print("Invalid folder path. Please provide a valid folder path.")    


    # Download from TVer and convert VTT to SRT
    #download_tver_and_convert_vtt_to_srt(tver_link)

    # Check if "align:start" and "position:" are present in the converted .srt file
    #converted_srt_path = f"{tver_link.split('/')[-1]}.srt"
    #if os.path.exists(converted_srt_path) and \
    #        any("align:start" in line or "position:" in line for line in open(converted_srt_path, 'r')):
    #    print("Flag: Converted .srt has 'align:start' or 'position:' information.")
    #    
        # Auto-convert using the specified command
    #    convert_command = f'./subtitle-overlap-fixer {converted_srt_path}'
    #    subprocess.call(convert_command, shell=True)
        
    #    print("Overlap Fixer process completed.")
    #else:
    #    print("Option 3 completed. The SRT file will not be cleaned up.")
    
else:
    print("Invalid input type.")
