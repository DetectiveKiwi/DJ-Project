import numpy as np
from threading import Thread
import sounddevice as sd
import time as time_module
from scipy.signal import butter
from scipy.signal import filtfilt
from audio_dspy import design_highshelf
from audio_dspy import design_lowshelf
from audio_dspy import design_bell

class audio:
    def __init__(self, fs=44100, num_channels=2):
        self.fs = fs
        self.num_channels = num_channels
        self.crossfader = 0
        self.slots = np.zeros((2), dtype=int)
        self.vol = [0.8,0.8]
        self.master_vol = 0.8
        self.songs = [[],[]]
        self.current_frame = np.zeros((2), dtype=int)
        self.lpf = [20000,20000]
        self.hpf = [35,35]
        self.eq_gain = [[1,1,1], [1,1,1]]
        self._filter_edge_len = 100
        self.first = True
        
    def setCrossFaderVal(self, val):
        self.crossfader = val
        
    def setMasterVol(self, val):
        self.master_vol = val
        
    def setTrackVol(self, val, idx):
        self.vol[idx] = val
        
    def setHPF(self, val, idx):
        self.hpf[idx] = val
        
    def setLPF(self, val, idx):
        self.lpf[idx] = val
        
    def setEQ(self, val, idx, eq_idx):
        self.eq_gain[idx][eq_idx] = val
        
    def play_track(self, track_to_play, slot_idx):
        self.songs[slot_idx] = track_to_play.song.copy()
        self.current_frame[slot_idx] = track_to_play.cue_frame
        
        if not self.first:
            cue_adjustment = track_to_play.cue_frame - track_to_play.grid
            cue_adjustment = cue_adjustment[cue_adjustment <= 0][0]
            next_measure = self.grid - self.grid_frame[1]
            if np.any(next_measure > 0):
                next_measure = next_measure[next_measure > 0][0]
            else:
                next_measure = 0
            
            self.current_frame[slot_idx] = track_to_play.cue_frame - cue_adjustment - next_measure
            #Possible error here, may try and access negative numbers. Make sure this still works here
            
            self.songs[slot_idx][:track_to_play.cue_frame] = 0
            self.grid = track_to_play.grid
            self.grid_frame = np.array([slot_idx, self.current_frame[slot_idx]])
                
        self.slots[slot_idx] = 1
        
        if self.first:
            self.thread = Thread(target=self._play_sound, args=())
            self.thread.start()
            self.grid = track_to_play.grid
            self.grid_frame = np.array([slot_idx, self.current_frame[slot_idx]])
            self.first = False
            
    def stop_track(self, idx):
        self.slots[idx] = 0
        self.songs[idx] = []
        self.current_frame[idx] = 0
        if idx==0:
            self.grid_frame = np.array([1, self.current_frame[1]])
        elif idx==1:
            self.grid_frame = np.array([0, self.current_frame[0]])
        
    def stop_all_tracks(self):
        for idx in range(len(self.slots)):
            self.stop_track(idx)
        self.first = True
    
    def _song_math(self, frames):
        self.playing = np.zeros((frames, self.num_channels))
        for idx in np.argwhere(self.slots==1)[:,0]:
            chunksize = min(len(self.songs[idx]) - (self.current_frame[idx]), frames)
            if self.current_frame[idx] - self._filter_edge_len >=0:
                vol = self._linear_fader(self.crossfader, idx) * self.vol[idx] * self.master_vol
                if (vol > 1):
                    vol = 1
                elif (vol < 0):
                    vol = 0
                y = vol * self.songs[idx][self.current_frame[idx] - \
                                          self._filter_edge_len:self.current_frame[idx] + \
                                          chunksize + \
                                          self._filter_edge_len]
                y = self._low_shelf(y, self.eq_gain[idx][0])
                y = self._bell_filter(y, self.eq_gain[idx][1])
                y = self._high_shelf(y, self.eq_gain[idx][2])
                if(self.lpf[idx]<17000):
                    y_l = self._butter_filter(y, self.lpf[idx], 'low')
                else:
                    y_l = y
                if(self.hpf[idx]>=150):
                    y_h = self._butter_filter(y_l, self.hpf[idx], 'high')
                    self.playing[:chunksize] += y_h[self._filter_edge_len:-self._filter_edge_len]
                else:
                    self.playing[:chunksize] += y_l[self._filter_edge_len:-self._filter_edge_len]
            self.playing[chunksize:] = 0
            self.current_frame[idx] += chunksize
        self.grid_frame[1] = self.current_frame[self.grid_frame[0]]
        
    def _play_sound(self):
        def callback(outdata, frames, time_c, status):
            if status:
                print(status)
            self.time = time_c
            self._song_math(frames)
            self.next_frame = np.array([time_c.outputBufferDacTime - time_c.currentTime, time_module.time()])
            outdata[:] = self.playing

        stream = sd.OutputStream(
            samplerate=self.fs, channels=self.num_channels,
            callback=callback, finished_callback=self.stop_all_tracks, latency=0.3,
            blocksize=1024
        )
        with stream:
            while np.sum(self.slots) > 0:
                time_module.sleep(1)
                continue
    
    def _linear_fader(self, x, idx):
        if(idx>0):
            x = -x
        if x<=0:
            return(1)
        elif x>=1:
            return(0)
        else:
            return(1-x)
        
    def _butter_filter_ba(self, cutoff, btype, order=5):
        nyq = 0.5 * self.fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype=btype, analog=False)
        return b, a
    
    def _butter_filter(self, data, cutoff, btype, order=5):
        b, a = self._butter_filter_ba(cutoff, btype, order=order)
        y = filtfilt(b, a, data, axis=0)
        return y
    
    def _high_shelf(self, data, gain, Q=1, cutoff=2000):
        b, a = design_highshelf(cutoff, Q, gain, self.fs)
        y = filtfilt(b, a, data, axis=0)
        return y
    
    def _low_shelf(self, data, gain, Q=1, cutoff=2000):
        b, a = design_lowshelf(cutoff, Q, gain, self.fs)
        y = filtfilt(b, a, data, axis=0)
        return y
    
    def _bell_filter(self, data, gain, Q=1, cutoff=2000):
        b, a = design_bell(cutoff, Q, gain, self.fs)
        y = filtfilt(b, a, data, axis=0)
        return y