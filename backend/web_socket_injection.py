from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import speech_recognition as sr
import threading
import asyncio
 
router = APIRouter(prefix="/api")
 
class SpeechRecognitionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.is_listening = False
        self.complete_voice = ""
        self.lock = threading.Lock()
   
    async def recognize_speech(self, websocket: WebSocket):
        with self.lock:
            self.complete_voice = ""
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening... Press 'Stop Listening' to stop.")
            while self.is_listening:
                try:
                    audio = await asyncio.to_thread(self.recognizer.listen, source, timeout=5, phrase_time_limit=5)
                    speech_to_text = await asyncio.to_thread(self.recognizer.recognize_google, audio)
                    with self.lock:
                        self.complete_voice += " " + speech_to_text
                    print("You said:", speech_to_text)
                    await websocket.send_text(speech_to_text)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.WaitTimeoutError:
                    print("Listening timed out while waiting for phrase to start")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
        print("Final captured text:", self.complete_voice)
        return self.complete_voice
   
    async def start_recognition(self, websocket: WebSocket):
        if self.is_listening:
            raise HTTPException(status_code=400, detail="Recognition already in progress")
        self.is_listening = True
        await self.recognize_speech(websocket)
   
    def stop_recognition(self):
        self.is_listening = False
 
speech_service = SpeechRecognitionService()
 
@router.websocket("/ws/start-recognition")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await speech_service.start_recognition(websocket)
    except WebSocketDisconnect:
        speech_service.stop_recognition()
        print("WebSocket disconnected")
    except HTTPException as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        speech_service.stop_recognition()
 
@router.get("/stop-recognition", tags=["Voice"])
async def stop_listening_command():
    speech_service.stop_recognition()
    print("Listening stopped.")
    return {"status": "Listening stopped."}
 
@router.get("/get-captured-text", tags=["Voice"])
async def get_captured_text():
    with speech_service.lock:
        return {"captured_text": speech_service.complete_voice}