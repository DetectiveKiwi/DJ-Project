import numpy as np
import pandas as pd
import GUI
import controller
import tracks
import audio
import trace

audio = audio.audio()
controller = controller.controller()
trackLeft = tracks.track()
trackRight = tracks.track()
trackLibrary = tracks.track_library()
traceLeft = trace.trace()
traceRight = trace.trace()
GUI.createWindow(controller, audio, trackLeft, trackRight, trackLibrary, traceLeft, traceRight)