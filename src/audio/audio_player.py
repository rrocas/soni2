from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices
from PySide6.QtCore import QUrl, QObject

import threading
import sounddevice as sd
import numpy as np

class MicLoopback:
    def __init__(self):
        self.running = False
        self.stream = None
        self.hostapi = self._find_wasapi()
        self.input_index = self._find_mic()
        self.output_index = self._find_device("CABLE")

    def _find_wasapi(self):
        apis = sd.query_hostapis()
        for i, api in enumerate(apis):
            if "WASAPI" in api['name'].upper():
                return i
        return sd.default.hostapi

    def _find_mic(self):
        devices = sd.query_devices()
        
        # 1. Look for a hardware mic on WASAPI (low latency, avoids MME mappers)
        for i, d in enumerate(devices):
            if d['hostapi'] == self.hostapi and d['max_input_channels'] > 0:
                name = d['name'].upper()
                # Ignore cables, mappers, and stereo mix to guarantee we get a real mic
                if "CABLE" not in name and "MIX" not in name and "MAPPER" not in name:
                    return i
                    
        # 2. Fallback to default if no specific match
        return sd.default.device[0]

    def _find_device(self, name):
        devices = sd.query_devices()
        
        # 1. Try to find the device on our preferred API
        for i, d in enumerate(devices):
            if d['hostapi'] == self.hostapi and d['max_output_channels'] > 0:
                if name.upper() in d['name'].upper():
                    return i
                    
        # 2. Fallback to any API
        for i, d in enumerate(devices):
            if name.upper() in d['name'].upper() and d['max_output_channels'] > 0:
                return i
                
        print("MicLoopback: CABLE output not found!")
        return None

    def start(self):
        if self.running or self.output_index is None:
            return
        self.running = True

        def callback(indata, outdata, frames, time, status):
            if status:
                pass  # Ignore status prints to avoid console spam on minor drops
            outdata[:, 0] = indata[:, 0]
            if outdata.shape[1] > 1:
                outdata[:, 1] = indata[:, 0]

        try:
            in_info = sd.query_devices(self.input_index)
            out_info = sd.query_devices(self.output_index)
            in_name = in_info['name']
            out_name = out_info['name']
            
            # Default rate of the mic is the safest choice, fallback to standard rates
            rates_to_try = [int(in_info['default_samplerate']), 48000, 44100]
            
            success = False
            for rate in rates_to_try:
                try:
                    self.stream = sd.Stream(
                        channels=(1, 2),
                        samplerate=rate,
                        callback=callback,
                        device=(self.input_index, self.output_index)
                    )
                    self.stream.start()
                    print(f"Looping Hardware Mic: {in_name} -> {out_name} @ {rate}Hz")
                    success = True
                    break
                except Exception as e:
                    if "sample rate" in str(e).lower():
                        continue # Try the next sample rate
                    else:
                        raise e
            
            if not success:
                raise Exception("None of the sample rates (native, 48000, 44100) were accepted by your hardware.")

        except Exception as e:
            print(f"Mic loopback failed: {e}")
            self.running = False
            self.stream = None

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.running = False


class AudioStreamer(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- PLAYER FOR DISCORD (VB-Cable) ---
        self.cable_player = QMediaPlayer(self)
        self.cable_audio_output = QAudioOutput(self)

        devices = QMediaDevices.audioOutputs()
        virtual_cable = next((
            d for d in devices
            if "CABLE" in d.description().upper()
            or "CABLE" in bytes(d.id()).decode().upper()
        ), None)

        if virtual_cable:
            print(f"Attached VB-Cable Device: {virtual_cable.description()}")
            self.cable_audio_output.setDevice(virtual_cable)
        else:
            print("Virtual Cable not found! Falling back to default device.")

        self.cable_player.setAudioOutput(self.cable_audio_output)

        # --- PLAYER FOR YOU (Headphones) ---
        self.local_player = QMediaPlayer(self)
        self.local_audio_output = QAudioOutput(self)
        self.local_player.setAudioOutput(self.local_audio_output)

        # --- MIC LOOPBACK ---
        self.mic_loopback = MicLoopback()
        self.start_loopback()

    def play_sound(self, file_path):
        url = QUrl.fromLocalFile(file_path)
        self.cable_player.stop()
        self.local_player.stop()
        self.cable_player.setSource(url)
        self.local_player.setSource(url)
        self.cable_player.play()
        self.local_player.play()

    def start_loopback(self):
        self.mic_loopback.start()

    def stop_loopback(self):
        self.mic_loopback.stop()