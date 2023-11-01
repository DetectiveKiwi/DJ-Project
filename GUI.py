from numpy import exp
from numpy import log
import numpy as np
import pandas as pd
import tkinter as tk
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# TODO
# Add Visualization of Song?
    # Get rid of animation error
    # Make sure it stops but ends the thread
    # Add this to right side too
    
# Try and fix that one error that I listed somewhere else
# Clean code a bit
# Add ability to change bpm of new song


def createWindow(controller, audio, trackLeft, trackRight, trackLibrary, traceLeft, traceRight):
    def _loadLeftButton():
        m = trackLeft.load_song(trackLibrary, controller.idxLeft, audio.fs, controller.bpm)
        leftSongName['text'] = str(trackLeft.info)
        message.configure(text=m)
        traceLeft.update_ydata(trackLeft.song, trackLeft.cue_frame)
    def _loadRightButton():
        m = trackRight.load_song(trackLibrary, controller.idxRight, audio.fs, controller.bpm)
        rightSongName['text'] = str(trackRight.info)
        message.configure(text=m)
        traceRight.update_ydata(trackRight.song, trackRight.cue_frame)
    def _playLeftTrack():
        audio.play_track(trackLeft, 0)
        leftSongName['background'] = 'green'
        traceLeft.animateSong(audio, 0)
    def _playRightTrack():
        audio.play_track(trackRight, 1)
        rightSongName['background'] = 'green'
        traceRight.animateSong(audio, 1)
    def _stopLeftTrack():
        audio.stop_track(0)
        leftSongName['background'] = 'gray'
    def _stopRightTrack():
        audio.stop_track(1)
        rightSongName['background'] = 'gray'
    
    window = ttk.Window()
    window.title('DJ')
    window.geometry('1500x800')
    
    style = ttk.Style()
    style.configure('Fixed.TButton', font=('Courier', 16))

    leftNextSongName = ttk.StringVar()
    leftSongList = ttk.OptionMenu(
        window, 
        leftNextSongName, 
        'No Song Selected',
        *trackLibrary.metadata['info'].values,
        command=lambda x:controller.setLeftIdx(
            trackLibrary.metadata[trackLibrary.metadata['info']==x].index.values[0]
        ),
        style='Fixed.TButton'
    )
    leftSongList["menu"].configure(font=('Courier', 16))
    rightNextSongName = ttk.StringVar()
    rightSongList = ttk.OptionMenu(
        window, 
        rightNextSongName, 
        'No Song Selected',
        *trackLibrary.metadata['info'].values,
        command=lambda x:controller.setRightIdx(
            trackLibrary.metadata[trackLibrary.metadata['info']==x].index.values[0]
        ),
        style='Fixed.TButton'
    )
    rightSongList["menu"].configure(font=('Courier', 16))
    
    leftSongName = ttk.Label(
        master=window,
        text=str(trackLeft.title),
        background="gray", 
        foreground='white',
        padding=10,
        style='Fixed.TButton'
    )
    loadLeftButton = ttk.Button(
        master=window, 
        text='Load', 
        style='secondary.TButton', 
        command=_loadLeftButton
    )
    playLeftButton = ttk.Button(
        master=window,
        text='Play',
        command=_playLeftTrack
    )
    stopLeftButton = ttk.Button(
        master=window, 
        text='Stop', 
        style='danger.TButton', 
        command=_stopLeftTrack
    )
    loadLeftButton.place(x=100, y=600, height=100, width=150)
    playLeftButton.place(x=350, y=600, height=100, width=150)
    stopLeftButton.place(x=500, y=600, height=100, width=150)
    leftSongName.place(x=100, y=500, height=50, width=550)
    leftSongList.place(x=100, y=400, height=50, width=550)
    
    rightSongName = ttk.Label(
        master=window, 
        text=str(trackRight.title), 
        background="gray", 
        foreground='white',
        padding=10,
        style='Fixed.TButton'
    )
    loadRightButton = ttk.Button(
        master=window, 
        text='Load', 
        style='secondary.TButton', 
        command=_loadRightButton
    )
    playRightButton = ttk.Button(
        master=window, 
        text='Play',
        command=_playRightTrack
    )
    stopRightButton = ttk.Button(
        master=window, 
        text='Stop', 
        style='danger.TButton', 
        command=_stopRightTrack
    )
    loadRightButton.place(x=850, y=600, height=100, width=150)
    playRightButton.place(x=1100, y=600, height=100, width=150)
    stopRightButton.place(x=1250, y=600, height=100, width=150)
    rightSongName.place(x=850, y=500, height=50, width=550)
    rightSongList.place(x=850, y=400, height=50, width=550)
    
    # Cross Fader
    crossFaderValue = tk.DoubleVar(value=audio.crossfader)
    crossFader = tk.Scale(
        master=window,
        from_=-1,
        to=1,
        orient='horizontal',
        variable=crossFaderValue,
        resolution=0.1,
        command=lambda x:audio.setCrossFaderVal(float(x))
    )
    crossFader.place(x=675, y=680, width=150)
    
    # Master Volume
    masterVolValue = tk.DoubleVar(value=audio.master_vol)
    masterVol = tk.Scale(
        master=window,
        from_=1,
        to=0,
        orient='vertical',
        variable=masterVolValue,
        resolution=0.05,
        command=lambda x:audio.setMasterVol(float(x))
    )
    masterVol.place(x=740, y=200, height=150)
    
    # Left Volume
    leftVolValue = tk.DoubleVar(value=audio.vol[0])
    leftVol = tk.Scale(
        master=window,
        from_=1,
        to=0,
        orient='vertical',
        variable=leftVolValue,
        resolution=0.05,
        command=lambda x:audio.setTrackVol(float(x), 0)
    )
    leftVol.place(x=660, y=200, height=150)
    
    # Right Volume
    rightVolValue = tk.DoubleVar(value=audio.vol[1])
    rightVol = tk.Scale(
        master=window,
        from_=1,
        to=0,
        orient='vertical',
        variable=rightVolValue,
        resolution=0.05,
        command=lambda x:audio.setTrackVol(float(x), 1)
    )
    rightVol.place(x=820, y=200, height=150)
    
    # Left HPF
    leftHPFValue = tk.DoubleVar(value=log(audio.hpf[0]))
    leftHPF = tk.Scale(
        master=window,
        from_=log(15000),
        to=log(150),
        orient='vertical',
        variable=leftHPFValue,
        resolution=0.2,
        command=lambda x:audio.setHPF(exp(1)**float(x), 0)
    )
    leftHPF.place(x=700, y=360, height=150)
    
    # Right HPF
    rightHPFValue = tk.DoubleVar(value=log(audio.hpf[1]))
    rightHPF = tk.Scale(
        master=window,
        from_=log(15000),
        to=log(150),
        orient='vertical',
        variable=rightHPFValue,
        resolution=0.2,
        command=lambda x:audio.setHPF(exp(1)**float(x), 1)
    )
    rightHPF.place(x=780, y=360, height=150)
    
    # Left LPF
    leftLPFValue = tk.DoubleVar(value=log(audio.lpf[0]))
    leftLPF = tk.Scale(
        master=window,
        from_=log(17000),
        to=log(400),
        orient='vertical',
        variable=leftLPFValue,
        resolution=0.2,
        command=lambda x:audio.setLPF(exp(1)**float(x), 0)
    )
    leftLPF.place(x=700, y=520, height=150)
    
    # Right LPF
    rightLPFValue = tk.DoubleVar(value=log(audio.lpf[1]))
    rightLPF = tk.Scale(
        master=window,
        from_=log(17000),
        to=log(400),
        orient='vertical',
        variable=rightLPFValue,
        resolution=0.2,
        command=lambda x:audio.setLPF(exp(1)**float(x), 1)
    )
    rightLPF.place(x=780, y=520, height=150)
    
    # Left EQ Low
    leftEQLowValue = tk.DoubleVar(value=audio.eq_gain[0][0])
    leftEQLow = tk.Scale(
        master=window,
        from_=2,
        to=0.5,
        orient='vertical',
        variable=leftEQLowValue,
        resolution=0.1,
        command=lambda x:audio.setEQ(float(x), 0, 0)
    )
    leftEQLow.place(x=200, y=230, height=150)
    
    # Left EQ Mid
    leftEQMidValue = tk.DoubleVar(value=audio.eq_gain[0][1])
    leftEQMid = tk.Scale(
        master=window,
        from_=2,
        to=0.5,
        orient='vertical',
        variable=leftEQMidValue,
        resolution=0.1,
        command=lambda x:audio.setEQ(float(x), 0, 1)
    )
    leftEQMid.place(x=300, y=230, height=150)
    
    # Left EQ High
    leftEQHighValue = tk.DoubleVar(value=audio.eq_gain[0][2])
    leftEQHigh = tk.Scale(
        master=window,
        from_=2,
        to=0.5,
        orient='vertical',
        variable=leftEQHighValue,
        resolution=0.1,
        command=lambda x:audio.setEQ(float(x), 0, 2)
    )
    leftEQHigh.place(x=400, y=230, height=150)
    
    # Right EQ Low
    rightEQLowValue = tk.DoubleVar(value=audio.eq_gain[1][0])
    rightEQLow = tk.Scale(
        master=window,
        from_=2,
        to=0.5,
        orient='vertical',
        variable=rightEQLowValue,
        resolution=0.1,
        command=lambda x:audio.setEQ(float(x), 1, 0)
    )
    rightEQLow.place(x=1100, y=230, height=150)
    
    # Right EQ Mid
    rightEQMidValue = tk.DoubleVar(value=audio.eq_gain[1][1])
    rightEQMid = tk.Scale(
        master=window,
        from_=2,
        to=0.5,
        orient='vertical',
        variable=rightEQMidValue,
        resolution=0.1,
        command=lambda x:audio.setEQ(float(x), 1, 1)
    )
    rightEQMid.place(x=1200, y=230, height=150)
    
    # Left EQ High
    rightEQHighValue = tk.DoubleVar(value=audio.eq_gain[1][2])
    rightEQHigh = tk.Scale(
        master=window,
        from_=2,
        to=0.5,
        orient='vertical',
        variable=rightEQHighValue,
        resolution=0.1,
        command=lambda x:audio.setEQ(float(x), 1, 2)
    )
    rightEQHigh.place(x=1300, y=230, height=150)
    
    # Error message at the bottom of the screen
    message = ttk.Label(
        master=window, 
        text=''
    )
    message.place(x=100, y=750, height=50, width=1400)
    
    # Left Song Trace
    canvas = FigureCanvasTkAgg(traceLeft.fig, master=window)
    canvas.get_tk_widget().place(x=100, y=0, height=200, width=600)
    
    # Right Song Trace
    canvas = FigureCanvasTkAgg(traceRight.fig, master=window)
    canvas.get_tk_widget().place(x=800, y=0, height=200, width=600)
    

    # Run
    window.mainloop()
    audio.stop_all_tracks()