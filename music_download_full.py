import youtube_dl
import shutil
import os
from pytube import YouTube

path_given = False
path_destination = ''


def vav_single_file(url):
    yt = YouTube(str(url))
    video = yt.streams.filter(only_audio=True).first()
    destination = os.getcwd()
    out_file = video.download(output_path=destination)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.wav'
    os.rename(out_file, new_file)


def download_channel_vav(path_name):
    pass


def mp4_download(url):
    yt = YouTube(str(url))
    video = yt.streams.filter().first()
    destination = os.getcwd()
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp4'
    os.rename(out_file, new_file)


while True:

    print('''
    Usage:
    If you want to specify a directory the files should be downloaded to use [0] command 
    *note the path is saved till the end of the session
    *note all files with the .wav and .mp4 extension shall be moved to the new directory
    If you want to download a single file with the .wav extension use [1] command
    If you want to download the full content of the channel with the .wav extension use the [2] command
    If you want  to download a file with the .mp4 extension use [3] command
    if you want to exit the program use [4] command''')
    a = input('I want to []: ')
    list_var = ['1', '2', '3', '4', '0']

    if a not in list_var:
        print('the input is not correct, you may only choose 0, 1, 2, 3 or 4')

    else:
        if a == '1':
            url = input('please give the url of the file you want to download from youtube: ')
            vav_single_file(url)

        elif a == '2':
            print('Firstly you must copy the output of the program after giving it the "youtube.com/@channel/videos"'
                  'url and then specify the the text file you pasted the output into')
            url = input('please give the url of the channel you want to download from youtube: ')
            youtube_dl_options = {
                'skip_download': True,
                'ignoreerrors': True
            }
            with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:

                ydl.extract_info(url)
            text_file = input('please input the file directory: ')
            download_channel_vav(text_file)

        elif a == '3':
            url = input('please give the url of the file you want to download from youtube: ')
            mp4_download(url)

        elif a == '4':
            break
        else:
            path_temp = input('input the file directory you want to download to: ')
            if os.path.exists(path_temp):
                path_given = True
                path_destination = path_temp
            else:
                print('the specified path does not exist, please try again')
        if path_given:
            cwd = os.listdir(os.getcwd())
            list_elements = ['.git', '.gitignore', '.idea', 'cv_projects', 'LICENSE', 'music_download_full.py',
                             'README.md', 'requirments.txt', 'word_parser.py']
            for file in cwd:
                if file not in list_elements:
                    full_path_current = str(os.getcwd())+'\\'+file
                    try:
                        shutil.move(full_path_current, path_destination)
                    except Exception as e:
                        print(f'Failed to move the file due to {e}')
