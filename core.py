from pydub import AudioSegment

# Hàm mã hóa/giải mã âm thanh sử dụng thuật toán A5/1 (mô phỏng XOR đơn giản)
def a5_1_encrypt_decrypt(input_file, key, encrypt=True):
    audio = AudioSegment.from_file(input_file)
    audio_data = audio.raw_data

    # Đảm bảo key có đủ độ dài
    key = key.encode('utf-8')  # Chuyển key thành bytes
    key_length = len(key)
    
    # Mã hóa hoặc giải mã (XOR giữa dữ liệu và key)
    result_data = bytearray()
    for i, byte in enumerate(audio_data):
        key_byte = key[i % key_length]
        result_data.append(byte ^ key_byte)

    output_audio = audio._spawn(result_data)
    return output_audio
