from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import speech_recognition as sr
import threading
import asyncio
 
router = APIRouter(prefix="/api")
 
recognizer = sr.Recognizer()
mic = sr.Microphone()
is_listening = False
lock = threading.Lock()
 
async def recognize_speech(websocket: WebSocket):
    global is_listening
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Press 'Stop Listening' to stop.")
        while is_listening:
            try:
                audio = await asyncio.to_thread(recognizer.listen, source, timeout=15, phrase_time_limit=10)
                speech_to_text = await asyncio.to_thread(recognizer.recognize_google, audio)
                print("You said:", speech_to_text)
                await websocket.send_text(speech_to_text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                is_listening = False
                print(f"An error occurred: {e}")
    return {"msg" : "Caputred Successfully"}
 
 
async def start_recognition(websocket: WebSocket):
    global is_listening
    is_listening = True
    await recognize_speech(websocket)
 
def stop_recognition():
    global is_listening
    is_listening = False
 
@router.websocket("/ws/start-recognition")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await start_recognition(websocket)
    except WebSocketDisconnect:
        stop_recognition()
        print("WebSocket disconnected")
    except HTTPException as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        stop_recognition()
 
@router.get("/stop-recognition", tags=["Voice"])
async def stop_listening_command():
    stop_recognition()
    print("Listening stopped.")
    return {"status": "Listening stopped."}