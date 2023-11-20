import os
from pytube import YouTube
from colorama import Fore, Style
import requests
import pyperclip

def upload_to_transfersh(file_path):
    try:
        max_file_size = 15 * 1024 * 1024  # 25 MB (adjust as needed)

        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            print(Fore.RED + f"File size exceeds the limit. Maximum allowed size is {max_file_size / (1024 * 1024)} MB.")
            return None

        with open(file_path, 'rb') as file:
            response = requests.post('https://transfer.sh/', files={'file': file})
            if response.status_code == 200:
                link = response.text.strip()
                # Copy the link to the clipboard
                pyperclip.copy(link)
                return link
            else:
                print(Fore.RED + f"Failed to upload to Transfer.sh. Status code: {response.status_code}, Response: {response.text}")
                return None
    except FileNotFoundError:
        print(Fore.RED + "File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        print(Fore.RED + f"An error occurred while uploading to Transfer.sh: {e}")
        return None

# Function to download mp3
def download_mp3(url, destination_folder, upload_to_cloud=False):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()

        # download the file
        out_file = video.download(output_path=destination_folder)

        # save the file as mp3
        base, _ = os.path.splitext(out_file)
        new_file = base + '.mp3'

        # Check if the file already exists
        file_number = 1
        while os.path.exists(new_file):
            base, ext = os.path.splitext(out_file)
            new_file = f"{base}_{file_number}.mp3"
            file_number += 1

        os.rename(out_file, new_file)

        # Print title and views
        print("\n" + Style.BRIGHT + Fore.WHITE + "[🎬] Video Title:", yt.title)
        print(Style.BRIGHT + Fore.WHITE + "[🎬] Video Views:", yt.views)

        if file_number > 1:
            print(Fore.YELLOW + f"The filename '{os.path.basename(base)}.mp3' was already taken, so now it will be called '{os.path.basename(new_file)}'.")

        if upload_to_cloud:
            transfersh_link = upload_to_transfersh(new_file)
            if transfersh_link:
                print(Style.BRIGHT + Fore.GREEN + "File uploaded to Transfer.sh. Here is the link:", transfersh_link)
                print(Fore.GREEN + "Link copied to clipboard. (Ctrl+V to paste)")
            else:
                print(Fore.RED + "Failed to upload to Transfer.sh.")
        else:
            print(Style.BRIGHT + Fore.GREEN + f"The video has been successfully downloaded as '{os.path.basename(new_file)}'.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

# Function to download mp4
def download_mp4(url, destination_folder, upload_to_cloud=False):
    try:
        yt = YouTube(url)

        # Print title and views
        print("\n" + Style.BRIGHT + Fore.WHITE + "[🎬] Video Title:", yt.title)
        print(Style.BRIGHT + Fore.WHITE + "[🎬] Video Views:", yt.views)

        # Get the stream with the highest resolution
        highest_resolution_stream = yt.streams.get_highest_resolution()

        # downloads the highest resolution video
        out_file = highest_resolution_stream.download(destination_folder)

        # Check if the file already exists
        file_number = 1
        while os.path.exists(out_file):
            base, ext = os.path.splitext(out_file)
            new_file = f"{base}_{file_number}.mp4"
            file_number += 1

        os.rename(out_file, new_file)

        if file_number > 1:
            print(Fore.YELLOW + f"The filename '{os.path.basename(base)}.mp4' was already taken, so now it will be called '{os.path.basename(new_file)}'.")

        if upload_to_cloud:
            transfersh_link = upload_to_transfersh(new_file)
            if transfersh_link:
                print(Style.BRIGHT + Fore.GREEN + "File uploaded to Transfer.sh. Here is the link:", transfersh_link)
                print(Fore.GREEN + "Link copied to clipboard. (Ctrl+V to paste)")
            else:
                print(Fore.RED + "Failed to upload to Transfer.sh.")
        else:
            print(Style.BRIGHT + Fore.GREEN + f"The video has been successfully downloaded as '{os.path.basename(new_file)}'.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

# Main script
if __name__ == "__main__":
    print(f"""{Fore.CYAN}
      _                     _         _          
     | |                   | |       | |         
   __| | _____      ___ __ | |_ _   _| |__   ___ 
  / _` |/ _ \ \ /\ / / '_ \| __| | | | '_ \ / _ \.
 | (_| | (_) \ V  V /| | | | |_| |_| | |_) |  __/
  \__,_|\___/ \_/\_/ |_| |_|\__|\__,_|_.__/ \___|                                                                                              
                                      -by zurly
     """)

    # Ask the user if they want to download as mp3 or mp4
    choice = str(input(Fore.CYAN + "Do you want to download as mp3 or mp4 > ")).lower()

    # Ask the user if they want to upload to Transfer.sh
    upload_to_cloud = input(Fore.CYAN + "Do you want to upload to Transfer.sh [to get a raw file link - NOTE: if mp4 it will be very slow]? (yes/no) > ").lower() == 'yes'

    # Check if the user wants to upload to Transfer.sh and skip folder creation
    if upload_to_cloud:
        folder_name = 'temp-transfer-sh'
    else:
        # Ask for the downloads folder name
        folder_name = str(input(Fore.CYAN + "What do you want the downloads folder to be called > ")) or 'downloads'

        # Check if the downloads folder already exists
        downloads_folder = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)
        else:
            print(Fore.YELLOW + f"The folder '{folder_name}' already exists. Using the existing folder.")

    # Ask for the YouTube URL
    url = str(input(Fore.CYAN + "Enter youtube link > "))

    if choice == 'mp3':
        download_mp3(url, folder_name, upload_to_cloud)
    elif choice == 'mp4':
        download_mp4(url, folder_name, upload_to_cloud)
    else:
        print(Fore.RED + "Invalid choice. Please choose 'mp3' or 'mp4'.")
