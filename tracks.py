import soundfile as sf
import pandas as pd
import numpy as np
from librosa import resample
from pyrubberband import time_stretch

class track_library:
    def __init__(self):
        self.metadata = pd.read_csv('metadata.csv')
        self.metadata['info'] = self.metadata['title'].str[:42].str.pad(42,'right') + \
            self.metadata['key'].str.pad(5,'both') + self.metadata['bpm'].round(0).astype(int).astype(str)
        

class track:
    def __init__(self):
        self.loc = None
        self.song = None
        self.fs = None
        
        self.title = None
        self.info = None
        self.loc = None
        self.bpm = None
        self.time_signature = None
        self.key = None
        self.cue = None
        self.start_frame = None
        self.end_frame = None
        self.cue_frame = None
        
        self.grid = None

    def load_song(self, track_library, idx, fs, bpm):
        if np.any(track_library.metadata.index.values==idx):
            info = track_library.metadata[track_library.metadata.index.values==idx]
            self.loc = info['loc'].values[0]
            self.song, self.fs = sf.read(self.loc, always_2d=True)
            
            self.title = info['title'].values[0]
            self.info = info['info'].values[0]
            self.bpm = info['bpm'].values[0]
            self.time_signature = info['time_signature'].values[0]
            self.key = info['key'].values[0]
            self.cue = info['cue'].values[0]
            self.start_frame = info['start_frame'].values[0]
            self.end_frame = info['end_frame'].values[0]
            self.cue_frame = info['cue_frame'].values[0]
            
            self.compute_grid()
            if self.fs != fs:
                self.change_fs(fs)
            self.change_bpm(bpm)
        else:
            return "Song Not Found"
        return self.title + ' Loaded Successfully'
        
    def compute_grid(self):
        start_line = int(0-self.start_frame / (60 * (self.fs / self.bpm))) - 1
        end_line = int((len(self.song)-self.start_frame) / (60 * (self.fs / self.bpm))) + 1
        self.grid = self.start_frame + np.arange(start_line - start_line%self.time_signature, \
                                                 end_line, self.time_signature)*60*(self.fs / self.bpm)
        
        
    def change_fs(self, fs_new):
        self.song = resample(self.song.T, self.fs, fs_new, res_type='kaiser_fast').T
        self.start_frame = int(self.start_frame * fs_new / self.fs)
        self.end_frame = int(self.end_frame * fs_new / self.fs)
        self.cue_frame = int(self.cue_frame * fs_new / self.fs)
        self.fs = fs_new
        self.compute_grid()
        
    def change_bpm(self, bpm_new):
        self.song = time_stretch(self.song, self.fs, bpm_new / self.bpm)
        self.grid = np.array([int(b) for b in self.grid * self.bpm / bpm_new])
        self.start_frame = int(self.start_frame * self.bpm / bpm_new)
        self.end_frame = int(self.end_frame * self.bpm / bpm_new)
        self.cue_frame = int(self.cue_frame * self.bpm / bpm_new)
        self.bpm = bpm_new
        