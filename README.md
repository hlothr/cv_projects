# cv_projects
I have created two projects listed below
## Word Parser
A tkinter project, after giving a path to a text file and pressing a button the program will display this file word by word with a speed of 0,15 seconds per word using the following python libraries: [tkinter](https://docs.python.org/3/library/tk.html) and [os](https://docs.python.org/3/library/os.html)
## Usage
In the yellow rectangle specify the the text file and push the "Start" button. After that the words will appear in the pink rectangle
## Music Downloader
In that project I used [youtube_dl](https://github.com/ytdl-org/youtube-dl/blob/master/README.md) in order to download .wav and .mp4 files. The downloads can be done in singular manner or in batch by choosing different option specified in the program. Furthermore, I used the
following libraries to make the program more versatile: [os](https://docs.python.org/3/library/os.html) and [shutil](https://docs.python.org/3/library/shutil.html)
# pip download
to clone the repository and launch the programs all you need to do is to write:


## ssh client
a more robust project than the other two, it uses a variety of python libraries such as subprocess, paramiko, os, ipaddress, sys and pyperclip
While writing this script I had the help of AI from chatgpt.com [site](https://chatgpt.com/)
## Usage
When the program is run, it creates a terminal and a tkinter windows, tkiter windows provides a variety of opetions, to first identify local ip adresses and then connect via ssh
Do mind the ssh protocle has a list of extensive parameters that the program does not help with
To connect the ssh client side to the ssh server, first you must create public and a private key that are kept in the server ssh folder and client ssh folder respectively
#IN CMD (WINDOWS ONLY)
```
git clone https://github.com/hlothr/cv_projects.git
cd cv_projects
pip install -r requirments.txt
python music_download_full.py
python word_parser.py
python ssh client.py
```
