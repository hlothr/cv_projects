import youtube_dl


def vav_single_file(url):
    try:
        video_info = youtube_dl.YoutubeDL().extract_info(
            url=url,
            download=False
        )
        file_name = f'{video_info["title"]}.wav'
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': file_name,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        print(f'download complete... {file_name}')
    except Exception:
        print(f'download failed')


def download_channel_vav(path_name):
    with open(path_name, 'r') as f:
        lines = f.readlines()
    lista = []
    for line in lines:
        if str(line).startswith('[youtube]'):
            done = str(line).replace('[youtube] ', '')
            done = done.replace(': Downloading webpage\n', '')
            lista.append(done)
    for el in lista:
        result = 'https://www.youtube.com/watch?v='+str(el)
        vav_single_file(result)


def mp4_download(url):
    try:
        video_info = youtube_dl.YoutubeDL().extract_info(
            url=url, download=True
        )
        filename = f"{video_info['title']}.mp4"
        options = {
            'format': 'bestaudio/best',
            'keepvideo': True,
            'outtmpl': filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        print("Download complete... {}".format(filename))
    except Exception:
        print('download failed')


while True:

    print('''
    Usage:
    If you want to download a single file with the .vav extension use [1] command
    If you want to download the full content of the channel with the .vav extension use the [2] command
    If you want  to download a file with the .mp4 extension use [3] command
    if you want to exit the program use [4] command''')
    a = input('I want to []: ')
    list_var = ['1', '2', '3', '4']

    if a not in list_var:
        print('the input is not correct, you may only choose 1, 2, 3 or 4')

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

        else:
            break
