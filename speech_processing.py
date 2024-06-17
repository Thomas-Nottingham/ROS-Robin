import azure.cognitiveservices.speech as speechsdk
import os
import time
from datetime import datetime 
from sounds import play_sound
import simpleaudio as sa
import sys
print(sys.executable)


settings = {
    'speechKey': "d14d3ca71c944fb1a045b3dd1d52595b",
    'region': "westeurope",
    'language': "English",
    'openAIKey': "c2e59398051e4e14b2003dd188e548a5"
}

def start_recording():
    # Creates an instance of a speech config with specified subscription key and service region
    speech_config = speechsdk.SpeechConfig(
        subscription = settings['speechKey'], region=settings['region'])
    
    speech_config.request_word_level_timestamps()
    speech_config.set_property(
        property_id=speechsdk.PropertyId.SpeechServiceResponse_OutputFormatOption, value="detailed")

    # Creates a speech recognizer using the default microphone (built in)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)
    

    #--------------------------------------------------------------------------------#
    #                                 Event Handlers                                 #
    #--------------------------------------------------------------------------------#
    results = []
    done = False

    def speech_detected():
        nonlocal last_spoken
        last_spoken = int(datetime.now().timestamp() * 1000)
     


    def handle_results(evt):
        nonlocal results
        #print(evt)
        res = {'text': evt.result.text, 'timestamp': evt.result.offset,
               'duration': evt.result.duration, 'raw': evt.result}
        
        speech_detected()
        text = res["text"]
        print(f"text: {text}")

        if (evt.result.text != ""):
            results.append(res)



    def speech_canceled(evt):
        nonlocal done
        done = True

    speech_recognizer.session_started.connect(lambda evt: print(f"Session Started {evt}"))

    speech_recognizer.session_stopped.connect(speech_canceled)

    speech_recognizer.recognizing.connect(lambda evt: speech_detected())
    
    speech_recognizer.canceled.connect(speech_canceled)
    
    speech_recognizer.recognized.connect(handle_results)
    
    
    result_future = speech_recognizer.start_continuous_recognition_async()
    result_future.get()

    last_spoken = int(datetime.now().timestamp()*1000)

   
    while (not done):
        time.sleep(1)
        now = int(datetime.now().timestamp() * 1000)
        inactivity = now-last_spoken
        # if (inactivity > 1000):
        #     play_sound()

        if (inactivity > 3000):
            print('Stoping async recognition.')
            speech_recognizer.stop_continuous_recognition_async()
            while not done:
                time.sleep(1)


    output = ""
    for item in results:
        output+=(item["text"])

    for item in results:
        print(item["text"])

    return output   

def speak(text,output_folder):

        speech_config = speechsdk.SpeechConfig(subscription = settings['speechKey'], region=settings['region'])

        file_name = f'{output_folder}/{datetime.now().strftime("%Y%m%d_%H%M%S")}wav'

        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True, filename=file_name)

        speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        speech_synthesis_result = speech_synthesizer.speak_text(text)

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            play_obj = sa.WaveObject.from_wave_file(file_name).play()
            play_obj.wait_done()
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(
                cancellation_details.reason))
   #commit
