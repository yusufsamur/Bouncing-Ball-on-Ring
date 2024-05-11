import soundfile as sf
import os

def split_mp3_to_custom_length(input_file, output_folder, custom_length):
    # Giriş dosyasını aç
    audio, samplerate = sf.read(input_file)
    
    # Dosyanın uzunluğunu saniye cinsinden al
    length_seconds = len(audio) / samplerate
    
    # Parça sayısını belirle
    num_parts = int(length_seconds / custom_length)
    
    # Dosyayı belirli uzunlukta parçalara böl
    for i in range(num_parts):
        start_sample = i * int(custom_length * samplerate)  # Başlangıç örneği
        end_sample = (i + 1) * int(custom_length * samplerate)  # Bitiş örneği
        output_file = os.path.join(output_folder, f"part_{i+1}.wav")  # Çıktı dosyası adı ve yolu
        sf.write(output_file, audio[start_sample:end_sample], samplerate)  # Parçayı dışa aktar

    # Eğer dosyanın son kısmı kalan süre kadar uzunsa, son parçayı oluştur
    if length_seconds % custom_length != 0:
        start_sample = num_parts * int(custom_length * samplerate)
        output_file = os.path.join(output_folder, f"part_{num_parts+1}.wav")
        sf.write(output_file, audio[start_sample:], samplerate)

# Örnek kullanım:
input_file = "godzilla.mp3"  # Bölünecek MP3 dosyasının yolu
output_folder = "./ses"  # Parçaların kaydedileceği klasör
custom_length = 0.5  # Parçaların istenen uzunluğu (saniye cinsinden)
split_mp3_to_custom_length(input_file, output_folder, custom_length)
