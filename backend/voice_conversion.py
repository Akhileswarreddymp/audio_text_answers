from fastapi import APIRouter
import speech_recognition as sr
import asyncio
 
router = APIRouter(prefix="/api")
recognizer = sr.Recognizer()
mic = sr.Microphone()
is_listening = True
 
async def recognize_speech_from_mic():
    global is_listening
    global complete_voice
    complete_voice = ""
   
    # Adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Press 'Stop Listening' to stop.")
        while is_listening:
            try:
                audio = await asyncio.to_thread(recognizer.listen, source, phrase_time_limit=60)
                speech_to_text = await asyncio.to_thread(recognizer.recognize_google, audio)
                complete_voice += " " + speech_to_text
                print("You said:", speech_to_text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            continue
        print("Final captured text:", complete_voice)
        return complete_voice
            # if not is_listening:
            #     print("Final captured text:", complete_voice)
            #     return complete_voice
 
@router.get("/stop-recognition", tags=["Voice"])
async def stop_listening_command():
    global is_listening
    is_listening = False
    print("Listening stopped.")
 
@router.get("/start-recognition", tags=["Voice"])
async def start_listening_command():
    global is_listening
    is_listening = True
    out = await recognize_speech_from_mic()
    print("Complete captured text:", out)
    return out
 
# if __name__ == "__main__":
#     asyncio.run(start_listening_command())