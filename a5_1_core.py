import wave
import random
import struct

class A5_1:
    def __init__(self, key=None):
        self.R1 = [0] * 19
        self.R2 = [0] * 22
        self.R3 = [0] * 23
        
        self.R1_clock = 8
        self.R2_clock = 10
        self.R3_clock = 10
        
        self.R1_taps = [13, 16, 17, 18]
        self.R2_taps = [20, 21]
        self.R3_taps = [7, 20, 21, 22]
        
        if key is None:
            self.key = self.generate_key()
        else:
            self.key = key
            
        self.initialize_registers()
    
    def generate_key(self):
        return [random.randint(0, 1) for _ in range(64)]
    
    def initialize_registers(self):
        self.R1 = [0] * 19
        self.R2 = [0] * 22
        self.R3 = [0] * 23
        
        for i in range(64):
            self.clock_all()
            feedback_R1 = self.calculate_feedback(self.R1, self.R1_taps)
            feedback_R2 = self.calculate_feedback(self.R2, self.R2_taps)
            feedback_R3 = self.calculate_feedback(self.R3, self.R3_taps)
            
            self.R1[0] ^= self.key[i]
            self.R2[0] ^= self.key[i]
            self.R3[0] ^= self.key[i]
    
    def calculate_feedback(self, register, taps):
        feedback = 0
        for tap in taps:
            feedback ^= register[tap]
        return feedback
    
    def majority(self):
        sum_bits = self.R1[self.R1_clock] + self.R2[self.R2_clock] + self.R3[self.R3_clock]
        return 1 if sum_bits >= 2 else 0
    
    def clock_register(self, register, taps):
        feedback = self.calculate_feedback(register, taps)
        register.pop()
        register.insert(0, feedback)
    
    def clock_all(self):
        maj = self.majority()
        
        if self.R1[self.R1_clock] == maj:
            self.clock_register(self.R1, self.R1_taps)
            
        if self.R2[self.R2_clock] == maj:
            self.clock_register(self.R2, self.R2_taps)
            
        if self.R3[self.R3_clock] == maj:
            self.clock_register(self.R3, self.R3_taps)
    
    def generate_keystream_bit(self):
        self.clock_all()
        return self.R1[-1] ^ self.R2[-1] ^ self.R3[-1]
    
    def generate_keystream(self, length):
        return [self.generate_keystream_bit() for _ in range(length)]
    
    def reset(self):
        self.initialize_registers()
    
    def get_key_as_string(self):
        key_str = ""
        for i in range(0, 64, 4):
            nibble = 8*self.key[i] + 4*self.key[i+1] + 2*self.key[i+2] + self.key[i+3]
            key_str += hex(nibble)[2:]
        return key_str
    
    def set_key_from_string(self, key_str):
        if len(key_str) != 16:
            raise ValueError("Key must be 16 hex characters (64 bits)")
        
        self.key = []
        for char in key_str:
            value = int(char, 16)
            self.key.extend([
                (value >> 3) & 1,
                (value >> 2) & 1,
                (value >> 1) & 1,
                value & 1
            ])
        
        self.initialize_registers()


def process_audio_file(input_file, output_file, cipher, mode):
    try:
        with wave.open(input_file, 'rb') as wav_in:
            n_channels = wav_in.getnchannels()
            sample_width = wav_in.getsampwidth()
            framerate = wav_in.getframerate()
            n_frames = wav_in.getnframes()
            
            frames = wav_in.readframes(n_frames)
            
            if sample_width == 1:
                fmt = f"{len(frames)}B"
                samples = list(struct.unpack(fmt, frames))
                max_value = 255
            elif sample_width == 2:
                fmt = f"{len(frames)//sample_width}h"
                samples = list(struct.unpack(fmt, frames))
                max_value = 32767
            else:
                raise ValueError("Unsupported sample width")
            
            chunk_size = 10000
            processed_samples = []
            
            cipher.reset()
            
            for i in range(0, len(samples), chunk_size):
                chunk = samples[i:i+chunk_size]
                
                keystream = cipher.generate_keystream(len(chunk))
                
                for j, sample in enumerate(chunk):
                    key_value = keystream[j] * max_value
                    processed_sample = sample ^ key_value
                    
                    if sample_width == 1:
                        processed_sample = max(0, min(255, processed_sample))
                    elif sample_width == 2:
                        processed_sample = max(-32768, min(32767, processed_sample))
                    
                    processed_samples.append(processed_sample)
            
            if sample_width == 1:
                processed_frames = struct.pack(f"{len(processed_samples)}B", *processed_samples)
            elif sample_width == 2:
                processed_frames = struct.pack(f"{len(processed_samples)}h", *processed_samples)
            
            with wave.open(output_file, 'wb') as wav_out:
                wav_out.setnchannels(n_channels)
                wav_out.setsampwidth(sample_width)
                wav_out.setframerate(framerate)
                wav_out.writeframes(processed_frames)
        
        return True, f"Successfully {'encrypted' if mode == 'encrypt' else 'decrypted'} audio file.\nOutput saved to: {output_file}"
        
    except Exception as e:
        return False, f"Error processing audio file: {e}"
