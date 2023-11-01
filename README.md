# DJ-Project

This project is to create my own DJ software with Python. While one can easily buy software, I was interested in building my own software. This allows for extremely fine tuning in DJ tricks that can be performed live. It currently is in a stage where one could DJ live with it. Specifically, it works very well with House music, or music with a fairly consistent BPM. It is relatively difficult to transition between large BPM differences, although one could in principle do so by de-syncing the decks. Also, I'm working on an easy way to set cue points with a GUI, instead of the current method of doing so in a notebook.

For anyone interested in building your own DJ software, here is a list of skills that I found extremely useful:

- Threading: One needs to be able to start processes and still perform independent actions
- tkinter: This library has been useful in building a GUI in Python
- Digital Sound Processing (DSP): There are a ton of digital filters that one needs to be familiar with. E.g. high/low pass filters, shelf filters, bell filters, etc.
- pyrubberband: This library has some nice functions for stretching sounds (necessary for BPM conversions). While one could change the playback rate, this modifies the pitch (not wanted). pyrubberband fixes this.

Stay tuned for the stand-alone application!

## Demo

Stay tuned for a video demo!

## Current Features

- Graphical User Interface (GUI) for easy mixing
- Visualizes where in the track one is
- Converts BPM of any song upon loading
- Ability to high/low pass filter decks while mixing
- Ability to modify volume and crossfade between decks while mixing
- Ability to modify EQ while mixing
- Synchronizes tracks

## Features to be Included

- Integration with MIDI controllers
- GUI for development mode, where one can easily set cue points for new songs
- BPM conversion while playing, which allows one to move to new genres
- Minor bug fixes and GUI modifications
- Stand alone application