import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import pyttsx3
from ollama import chat
from ollama import ChatResponse
import threading

def main():
    is_running = True
    while is_running:
        result = vtt()
        if result:  # Check if there was a valid transcription
            ai_output = ollama(result)
            if ai_output:
                tts(ai_output)

def vtt():
    # Load model
    model_path = r"C:\\Users\\orang\\OneDrive\\Documents\\GitHub\\T3LLY-\\src\\vosk-model-small-en-us-0.15"
    model = Model(model_path)


    recognizer = KaldiRecognizer(model, 16000)
    q = queue.Queue()
    result = None

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(bytes(indata))

    # Stream audio and transcribe
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎤 Start talking...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print("💬", result.get("text", ""))
                return result.get("text", "")  # Return the transcribed text

def ollama(user_input):
    response: ChatResponse = chat(model='tinyllama', messages=[
        {'role': 'user', 'content': user_input},
    ])
    
    ai_output = response['message']['content']
    return ai_output  # Return the AI output

def tts(ai_output):
    engine = pyttsx3.init()
    engine.say(ai_output)
    engine.runAndWait()  # Blocks here, consider threading if needed for concurrency

if __name__ == "__main__":
    main()
