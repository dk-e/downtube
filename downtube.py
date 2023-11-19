from pytube import YouTube
import os
from colorama import Fore, Back, Style

# Function to download mp3
def download_mp3(url, destination_folder):
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
        print(Style.BRIGHT + Fore.WHITE + "[🎬]Video Title: ", yt.title)
        print(Style.BRIGHT + Fore.WHITE + "[🎬]Video Views: ", yt.views)

        if file_number > 1:
            print(Fore.YELLOW + f"The filename '{os.path.basename(base)}.mp3' was already taken, so now it will be called '{os.path.basename(new_file)}'.")
        
        print(Style.BRIGHT + Fore.GREEN + yt.title + f" has been successfully downloaded as '{os.path.basename(new_file)}'.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

# Function to download mp4
def download_mp4(url, destination_folder):
    try:
        yt = YouTube(url)

        # Print title and views
        print(Style.BRIGHT + Fore.WHITE + "[🎬]Video Title: ", yt.title)
        print(Style.BRIGHT + Fore.WHITE + "[🎬]Video Views: ", yt.views)

        # downloads the highest resolution video
        yd = yt.streams.get_highest_resolution()
        out_file = yd.download(destination_folder)

        # Check if the file already exists
        file_number = 1
        while os.path.exists(out_file):
            base, ext = os.path.splitext(out_file)
            new_file = f"{base}_{file_number}.mp4"
            file_number += 1

        os.rename(out_file, new_file)

        if file_number > 1:
            print(Fore.YELLOW + f"The filename '{os.path.basename(base)}.mp4' was already taken, so now it will be called '{os.path.basename(new_file)}'.")
        
        print(Style.BRIGHT + Fore.GREEN + yt.title + f" has been successfully downloaded as '{os.path.basename(new_file)}'.")
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

    # Ask for the downloads folder name
    folder_name = str(input(Fore.CYAN + "What do you want the downloads folder to be called > ")) or 'downloads'

    # Check if the downloads folder already exists
    downloads_folder = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    else:
        print(Fore.YELLOW + f"The folder '{folder_name}' already exists. Using existing folder.")

    # Ask for the YouTube URL
    url = str(input(Fore.CYAN + "Enter youtube link > "))

    if choice == 'mp3':
        download_mp3(url, downloads_folder)
    elif choice == 'mp4':
        download_mp4(url, downloads_folder)
    else:
        print(Fore.RED + "Invalid choice. Please choose 'mp3' or 'mp4'.")
