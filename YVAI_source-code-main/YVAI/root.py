import tkinter
from tkinter import ttk, messagebox
import os
import webbrowser
from pytube import YouTube
from PIL import Image
import requests
from io import BytesIO
from moviepy.video.io.VideoFileClip import VideoFileClip
from pathlib import Path


# ---------APP Configeration----------

app = tkinter.Tk()
app.geometry('800x500+250+100')
app.resizable(False, False)
app.title("YVAI")
# CONFIGGGGGGGGGGGGG
app.iconbitmap((f'{os.getcwd()}\icons\YVAI.ico'))

# ---------BACKGROUND IMAGE-------------

bgImage = tkinter.PhotoImage(
    file=((f'{os.getcwd()}\icons\BG.png')))
bgPANEL = tkinter.Label(app, image=bgImage)
bgPANEL.pack()

# --------------LOGO-------------------

logo = tkinter.PhotoImage(
    file=((f'{os.getcwd()}\icons\icon.in.app.png')))
logo_resize = logo.subsample(2)
logoPANEL = tkinter.Label(app, image=logo_resize, background='#CFCFCF')
logoPANEL.place(x=320, y=60)

# --------------DESCRIPTION OF APP--------------

labelDescription = tkinter.Label(
    app, text="Download Video, Audio or See Information About Youtube Videos", font=('Segoe UI', 12, 'bold'), fg="black", bg='#CFCFCF')
labelDescription.place(x=140, y=40)

# ----------------ENTER LINK LABEL----------------

labelEntry = tkinter.Label(
    app, text="Enter The Video Link Below", font=('Segoe UI', 11,), fg="black", bg='#CFCFCF')
labelEntry.place(x=290, y=170)
# --------------ENTRY FIELD OF LINK--------------

entry_field = tkinter.Entry(app, font='5', width=70,
                            justify='center')
entry_field.place(x=70, y=200)


def getlink():
    Youtube_link = entry_field.get()
    return Youtube_link


# -----------------QUALITY BUTTONS----------

QualityBox = ttk.Combobox(app,
                          values=('Lowest Quality', '240p', '360p', '480p', 'Highest Quality'), state='readonly')


QualityLabel = tkinter.Label(app, text='Choose Video Quality To Download :',  font=(
    'Segoe UI', 9, 'bold'), fg="black", bg='#CFCFCF')

ClickToRefreshLabel = tkinter.Label(
    app, text='Restart App Before Making Another Choice', fg='black', bg='#CFCFCF', font=('Tahoma', 8))

# -----------------SHOW BUTTON FUNCTIONS--------------


def ShowQualityButtons():
    QualityBox.place(x=220, y=310)
    QualityLabel.place(x=10, y=307)


def ShowRefreshLabel():
    ClickToRefreshLabel.place(x=275, y=5)

# -----------------MAIN FUNCTIONS-------------------


def DownloadedAudio():
    messagebox.showinfo(
        'Success!', 'The Audio downloaded succesfully in\n \App Directory\Downloads')


def Downloaded():
    messagebox.showinfo(
        'Success!', 'The Video downloaded succesfully in\n \App Directory\Downloads')


def callback():
    global buttonClicked
    buttonClicked = not buttonClicked
    if chooiceBox.get() == 'Download Video' and getlink() != '':
        ShowQualityButtons()
        ShowRefreshLabel()

        def callbackDone():
            global buttonDoneClicked
            buttonDoneClicked = not buttonDoneClicked
            try:
                if QualityBox.get() == 'Lowest Quality':
                    Youtube_VideoLowest = YouTube(
                        getlink()).streams.get_lowest_resolution()
                    Youtube_VideoLowest.download(output_path=(
                        (rf'{os.getcwd()}\Downloads')))
                    Downloaded()
                elif QualityBox.get() == '240p':
                    Youtube_Video240 = YouTube(
                        getlink()).streams.get_by_resolution("240p")
                    Youtube_Video240.download(output_path=(
                        (rf'{os.getcwd()}\Downloads')))
                    Downloaded()
                elif QualityBox.get() == '360p':
                    Youtube_Video360 = YouTube(
                        getlink()).streams.get_by_resolution("360p")
                    Youtube_Video360.download(output_path=(
                        (rf'{os.getcwd()}\Downloads')))
                    Downloaded()
                elif QualityBox.get() == '480p':
                    Youtube_Video480 = YouTube(
                        getlink()).streams.get_by_resolution("480p")
                    Youtube_Video480.download(output_path=(
                        (rf'{os.getcwd()}\Downloads')))
                    Downloaded()
                elif QualityBox.get() == 'Highest Quality':
                    Youtube_VideoHighest = YouTube(
                        getlink()).streams.get_highest_resolution()
                    Youtube_VideoHighest.download(output_path=(
                        (rf'{os.getcwd()}\Downloads')))
                    Downloaded()
                elif QualityBox.get() == '':
                    def nonQuality():
                        messagebox.showerror('ERROR', 'Choose Quality')
                    nonQuality()

            except:
                def nonLink():
                    messagebox.showerror(
                        'ERROR', 'Undefined Link or Quality Not Available')
                nonLink()
        DownloadButton = tkinter.Button(app, command=callbackDone, text="Download", font=(
            'Segoe UI', 11), fg="black", bg="white", activebackground='black', activeforeground='white')
        DownloadButton.place(x=420, y=310)
    elif chooiceBox.get() == 'Download Audio' and getlink() != '':
        ShowRefreshLabel()

        def callbackAudio():
            try:
                global buttonAudioClicked
                buttonAudioClicked = not buttonAudioClicked
                Youtube_Audio = YouTube(
                    getlink()).streams.get_lowest_resolution()
                Video = Youtube_Audio.download(
                    output_path=(rf'{os.getcwd()}\Downloads'))
                VideoMP4 = VideoFileClip(os.path.abspath(Video))
                VideoMP4.audio.write_audiofile(
                    rf'{os.getcwd()}\Downloads\{(Path(os.path.abspath(Video))).stem}.mp3')
                VideoMP4.close()
                os.remove(os.path.abspath(Video))
                Downloaded()

            except:
                def nonLink():
                    messagebox.showerror(
                        'ERROR', 'Undefined Link or Quality Not Available')
                nonLink()
        AudioButton = tkinter.Button(app,  text="Download Audio", command=callbackAudio, font=(
            'Segoe UI', 11), fg="black", bg="white", activebackground='black', activeforeground='white')
        AudioButton.place(x=325, y=320)
    elif chooiceBox.get() == 'Info' and getlink() != '':
        ShowRefreshLabel()

        try:
            def display_Info():
                def display_Title():
                    Youtube_Title = YouTube(getlink()).title
                    labelTitle = tkinter.Label(app, text=(f"Video Title : \"{Youtube_Title}\"."), font=(
                        'Segoe UI', 11), fg="black", bg='#CFCFCF')
                    labelTitle.place(x=70, y=275)

                def display_Channel():
                    YoutubeVideo_Channel = YouTube(getlink()).author
                    labelChannel = tkinter.Label(app, text=(f"Video Published by {YoutubeVideo_Channel}."), font=(
                        'Segoe UI', 11), fg="black", bg='#CFCFCF')
                    labelChannel.place(x=70, y=300)

                def display_Thumbnail():
                    YoutubeVideo_thumbnail = YouTube(
                        f"{getlink()}").thumbnail_url
                    response = requests.get(YoutubeVideo_thumbnail)
                    imageOPEN = Image.open(BytesIO(response.content))
                    imageOPEN.show()

                def display_View():
                    YouTubeVideo_Views = YouTube(f'{getlink()}').views
                    labelViews = tkinter.Label(app, text=(f"{YouTubeVideo_Views :,d} Views."), font=(
                        'Segoe UI', 11), fg="black", bg='#CFCFCF')
                    labelViews.place(x=70, y=325)

                def display_Length():
                    YouTubeVideo_SecsLength = (YouTube(f'{getlink()}').length)
                    YouTubeVideo_MinsLength = (YouTubeVideo_SecsLength // 60)
                    YouTubeVideo_Secs = (YouTubeVideo_SecsLength % 60)
                    labelLength = tkinter.Label(app, text=(f"Video Length {YouTubeVideo_MinsLength}:{YouTubeVideo_Secs:d}"), font=(
                        'Segoe UI', 11), fg="black", bg='#CFCFCF')
                    labelLength.place(x=70, y=350)

                def PublishDate():
                    YoutubeVideo_Date = (YouTube(getlink()).publish_date)
                    return YoutubeVideo_Date

                YoutubeVideo_PublishDate = PublishDate().strftime(r"%Y/%B/%d")

                def display_PublishDate():
                    labelPublishDate = tkinter.Label(app, text=(
                        f"Video Published In {YoutubeVideo_PublishDate}"), font=('Segoe UI', 11), fg="black", bg='#CFCFCF')
                    labelPublishDate.place(x=70, y=375)

                display_Title()
                display_Channel()
                display_Length()
                display_View()
                display_PublishDate()
                display_Thumbnail()
            display_Info()

        except:
            def nonLink():
                messagebox.showerror('ERROR', 'Undefined Link')
            nonLink()
    else:
        def nonChoose():
            messagebox.showerror(
                'ERROR', 'You might be didn\'t choose from the box, or didn\'t write link.')
        nonChoose()


# ----------------ENTER BUTTON---------------------
buttonAudioClicked = False
buttonDoneClicked = False
buttonClicked = False

Enter_BUTTON = tkinter.Button(app, command=callback,  text="Enter Link", font=(
    'Segoe UI', 11), fg="black", bg="white", activebackground='black', activeforeground='white')
Enter_BUTTON.place(x=420, y=230)


# ------------CHOOICE BOX OF OPTIONS--------------

chooiceBox = ttk.Combobox(app,
                          values=('Download Video', 'Download Audio', 'Info'), state='readonly')
chooiceBox.place(x=220, y=230)

# ----------------MENU BAR OF ABOUT FUNCTIONS-------


def aboutapp():
    messagebox.showinfo(
        'About YVAI', 'YVAI is a program with a specific mission,\nit downloads videos and audios from Youtube, collect info from Videos and make it easily available to user.')


def howus():
    messagebox.showinfo('How US', "I'm a beginner programmer , still learing, this App it's my first experience in the programming journey, there's a button to communicate via Instagram if you like it, I hope you like the App, Thank You.")

# ----------------MENU BAR OF ABOUT-----------------


menubar = tkinter.Menu(app)
f = tkinter.Menu(menubar, tearoff=False)
f.add_command(label='About App', command=aboutapp)
f.add_command(label='How Us?', command=howus)
f.add_separator()
f.add_command(label='Exit', command=app.quit)
menubar.add_cascade(label='About', menu=f)

# ----------------SCROLL BAR-------------------

scroll_bar = tkinter.Scrollbar(app, orient='vertical')
scroll_bar.pack(side='right', fill='y')
app.config(menu=menubar)

# ----------------SOCIAL BUTTONS FUNCTIONS-------------------


def openINSTAGRAM():
    URL = webbrowser.open_new_tab(
        'https://www.instagram.com/a4rafff/')
    return URL


def openFacebook():
    URL = webbrowser.open_new_tab(
        'https://www.facebook.com/m.ashraff6')
    return URL


# ----------------INSTAGRAM BUTTONS---------------------
InstaImage = tkinter.PhotoImage(
    file=((f'{os.getcwd()}\icons\instagram.logo.png')))
resizeInsta = InstaImage.subsample(8)
Instagram_BUTTON = tkinter.Button(
    app, image=resizeInsta, command=openINSTAGRAM)
Instagram_BUTTON.place(x=10, y=450)

# ----------------FACEBOOK BUTTONS---------------------
FaceImage = tkinter.PhotoImage(
    file=((rf'{os.getcwd()}\icons\facebook.logo.png')))
resizeFace = FaceImage.subsample(11)
Facebook_BUTTON = tkinter.Button(
    app, image=resizeFace, command=openFacebook)
Facebook_BUTTON.place(x=40, y=450)


# ---------------MAIN LOOP OF APP------------------

app.mainloop()
