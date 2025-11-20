"""
Audio manager for Snake AI Game
Handles sound effects and background music with procedural generation
"""
import pygame
import numpy as np
import io
import struct


class AudioManager:
    """Manages all game audio"""
    
    def __init__(self, enabled=True, volume=70):
        """
        Initialize audio manager
        
        Args:
            enabled: Whether audio is enabled
            volume: Volume level 0-100
        """
        self.enabled = enabled
        self.volume = volume / 100.0
        self.sounds = {}
        
        if self.enabled:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                self._generate_sounds()
            except pygame.error as e:
                print(f"Warning: Could not initialize audio: {e}")
                self.enabled = False
    
    def _generate_sounds(self):
        """Generate procedural sound effects"""
        # Eat sound: short chirp
        self.sounds['eat'] = self._generate_chirp(duration=0.1, start_freq=800, end_freq=1200)
        
        # Click sound: short blip
        self.sounds['click'] = self._generate_click(duration=0.05, freq=600)
        
        # Game over sound: descending tone
        self.sounds['gameover'] = self._generate_chirp(duration=0.5, start_freq=400, end_freq=200)
        
        # Menu transition: swoosh
        self.sounds['transition'] = self._generate_swoosh(duration=0.3)
    
    def _generate_chirp(self, duration, start_freq, end_freq, sample_rate=22050):
        """Generate a frequency sweep (chirp) sound"""
        num_samples = int(duration * sample_rate)
        samples = np.zeros(num_samples, dtype=np.int16)
        
        for i in range(num_samples):
            t = i / sample_rate
            # Linear frequency sweep
            freq = start_freq + (end_freq - start_freq) * (i / num_samples)
            # Envelope to avoid clicks
            envelope = np.sin(np.pi * i / num_samples)
            samples[i] = int(32767 * 0.3 * envelope * np.sin(2 * np.pi * freq * t))
        
        return self._numpy_to_sound(samples)
    
    def _generate_click(self, duration, freq, sample_rate=22050):
        """Generate a short click sound"""
        num_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, num_samples)
        
        # Short sine burst with envelope
        envelope = np.exp(-t * 50)  # Fast decay
        samples = (32767 * 0.4 * envelope * np.sin(2 * np.pi * freq * t)).astype(np.int16)
        
        return self._numpy_to_sound(samples)
    
    def _generate_swoosh(self, duration, sample_rate=22050):
        """Generate a swoosh sound (white noise with envelope)"""
        num_samples = int(duration * sample_rate)
        
        # White noise
        noise = np.random.uniform(-1, 1, num_samples)
        
        # Apply envelope
        t = np.linspace(0, 1, num_samples)
        envelope = np.sin(np.pi * t)  # Bell curve
        
        samples = (32767 * 0.2 * envelope * noise).astype(np.int16)
        
        return self._numpy_to_sound(samples)
    
    def _numpy_to_sound(self, samples):
        """Convert numpy array to pygame Sound object"""
        # Convert to stereo
        stereo_samples = np.column_stack((samples, samples))
        
        # Create pygame Sound from array
        sound = pygame.sndarray.make_sound(stereo_samples)
        return sound
    
    def play(self, sound_name):
        """
        Play a sound effect
        
        Args:
            sound_name: Name of the sound to play
        """
        if not self.enabled or sound_name not in self.sounds:
            return
        
        try:
            sound = self.sounds[sound_name]
            sound.set_volume(self.volume)
            sound.play()
        except Exception as e:
            print(f"Warning: Could not play sound {sound_name}: {e}")
    
    def set_volume(self, volume):
        """
        Set volume level
        
        Args:
            volume: Volume level 0-100
        """
        self.volume = max(0, min(100, volume)) / 100.0
    
    def toggle_enabled(self):
        """Toggle audio on/off"""
        self.enabled = not self.enabled
        return self.enabled
    
    def stop_all(self):
        """Stop all playing sounds"""
        if self.enabled:
            pygame.mixer.stop()