import soundfile as sf
import os

def split_mp3_to_custom_length(input_file, output_folder, custom_length):
    audio, samplerate = sf.read(input_file)
    length_seconds = len(audio) / samplerate
    num_parts = int(length_seconds / custom_length)

    for i in range(num_parts):
        start_sample = i * int(custom_length * samplerate) 
        end_sample = (i + 1) * int(custom_length * samplerate) 
        output_file = os.path.join(output_folder, f"part_{i+1}.wav")  # output path and name
        sf.write(output_file, audio[start_sample:end_sample], samplerate) 

    if length_seconds % custom_length != 0:
        start_sample = num_parts * int(custom_length * samplerate)
        output_file = os.path.join(output_folder, f"part_{num_parts+1}.wav")
        sf.write(output_file, audio[start_sample:], samplerate)

input_file = "your_music.mp3"  # input music file path and name
output_folder = "./ses"  # save directory
custom_length = 0.5  # the lenght of each files of short music parts as seconds
split_mp3_to_custom_length(input_file, output_folder, custom_length)
