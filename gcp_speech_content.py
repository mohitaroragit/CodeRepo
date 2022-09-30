import os,io
from google.cloud import speech
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
speech_client=speech.SpeechClient()
media_file_mp4='D:\Pycharm\LRMonoPhase4.mp3'
with open(media_file_mp4,'rb') as media_file:
    byte_data=media_file.read()

audio_mp3=speech.RecognitionAudio(content=byte_data)
config_wave=speech.RecognitionConfig(
    sample_rate_hertz=44100,
    enable_automatic_punctuation=True,
    language_code='en-US',
    audio_channel_count=2

)
# response=speech_client.recognize(
#     config=config_mp3,
#     audio=audio_mp3
# )
media_uri="gs://speech_to_text_bucket_101/Free_Test_Data_5MB_WAV.wav"
long_uri=speech.RecognitionAudio(uri=media_uri)
config_mp3_enhanced=speech.RecognitionConfig(
    sample_rate_hertz=44100,
    enable_automatic_punctuation=True,
    language_code='en-US',
    use_enhanced=True,
    model='video'
)
operation=speech_client.long_running_recognize(
    config=config_wave,
    audio=long_uri
)
response=operation.result(timeout=90)
print(response)