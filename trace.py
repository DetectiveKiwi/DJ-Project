from matplotlib.pyplot import Figure
import numpy as np
from threading import Thread
from matplotlib.animation import FuncAnimation

class trace:
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-30,1000)
        self.ax.axvline(0, color='black')
        self.ydata = None
        self.ani = None
        self.trace, = self.ax.plot(np.arange(1000), np.zeros(1000))
        self.meanNum = 100
        
    def reset_ax(self):
        self.ax.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_ylim(min(self.ydata), max(self.ydata))
        self.ax.set_xlim(-30,1000)
        self.ax.axvline(0, color='black')
        
    def update_ydata(self, song, cueFrame):
        temp = np.mean(song[:len(song)-len(song)%self.meanNum,:], axis=-1)
        ydata = np.mean(
            temp.reshape(-1,self.meanNum), 
            axis=1
        )
        self.ydata = ydata
        
        temp = int(cueFrame//self.meanNum)
        self.reset_ax()
        self.trace, = self.ax.plot(np.arange(1000), self.ydata[temp:temp+1000])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
    def animateSong(self, audio, slotIdx):
        plotThread = Thread(target=self._animateTrace, args=(audio, slotIdx))
        plotThread.start()
        
    def _animateTrace(self, audio, slotIdx):
        def update(frame):
            temp = int(audio.current_frame[slotIdx]//self.meanNum)
            self.trace.set_ydata(self.ydata[temp:temp+1000])
            return self.trace,
        
        def gen():
            i = 0
            while audio.slots[slotIdx] == 1:
                yield i
                i += 1
        
        self.reset_ax()
        if self.ani:
            self.ani.frame_seq = self.ani.new_frame_seq()
        self.ani = FuncAnimation(
            self.fig, 
            update,
            frames=gen, 
            blit=True, 
            interval=10, 
            repeat=False, 
            cache_frame_data=False
        )
    
    
    