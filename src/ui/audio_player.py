from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices
from PySide6.QtCore import QUrl, QObject

class AudioStreamer(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- PLAYER FOR DISCORD (VB-Cable) ---
        self.cable_player = QMediaPlayer(self)
        self.cable_audio_output = QAudioOutput(self)
        
        # 1. Search existing audio devices for the virtual cable
        devices = QMediaDevices.audioOutputs()
        virtual_cable = next((
            d for d in devices 
            if "CABLE" in d.description().upper() 
            or "CABLE" in bytes(d.id()).decode().upper()
        ), None)
        
        # 2. Assign the specific VB-Cable device if we found it
        if virtual_cable:
            print(f"Attached VB-Cable Device: {virtual_cable.description()}")
            self.cable_audio_output.setDevice(virtual_cable)
        else:
            print("Virtual Cable not found! Falling back to default device for secondary output.")
            
        self.cable_player.setAudioOutput(self.cable_audio_output)
        
        # --- PLAYER FOR YOU (Headphones) ---
        # We create a second player that defaults to your system speakers/headphones
        self.local_player = QMediaPlayer(self)
        self.local_audio_output = QAudioOutput(self) 
        self.local_player.setAudioOutput(self.local_audio_output)

    def play_sound(self, file_path):
        url = QUrl.fromLocalFile(file_path)
        
        # Stop if currently playing
        self.cable_player.stop()
        self.local_player.stop()
        
        # Load the sound into both players
        self.cable_player.setSource(url)
        self.local_player.setSource(url)
        
        # Play them simultaneously
        self.cable_player.play()
        self.local_player.play()
