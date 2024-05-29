# from fastapi import APIRouter
# import speech_recognition as sr

# router = APIRouter(prefix="/api")
 
# recognizer = sr.Recognizer()
# mic = sr.Microphone()
# stop_listening = None  # This will hold the function to stop listening
 
# @router.on_event("startup")
# async def startup_event():
#     global recognizer, mic
#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source)
 
# @router.get("/start")
# async def start_listening():
#     global stop_listening, recognizer, mic
#     if stop_listening is None:  # Start listening only if not already listening
#         stop_listening = recognizer.listen_in_background(mic, callback)
#         return {"message": "Listening started"}
#     return {"message": "Already listening"}
 
# def callback(recognizer, audio):
#     try:
#         text = recognizer.recognize_google(audio)
#         print(f"You said: {text}")
#     except sr.UnknownValueError:
#         print("Could not understand audio")
#     except sr.RequestError as e:
#         print(f"Could not request results; {e}")
 
# @router.get("/stop")
# async def stop_listening():
#     global stop_listening
#     if stop_listening is not None:
#         stop_listening(wait_for_stop=False)
#         stop_listening = None
#         return {"message": "Listening stopped"}
#     return {"message": "Not currently listening"}
 
# @router.get("/cancel")
# async def cancel_listening():
#     global stop_listening
#     if stop_listening is not None:
#         stop_listening(wait_for_stop=True)
#         stop_listening = None
#         return {"message": "Listening cancelled"}
#     return {"message": "Not currently listening"}



# You're Akhileswar Redy, a FullStack Developer with extensive experience in Python,FastAPi and React, based on this resume summary:



# Akhileswar Reddy
#         - Mobile: 8217220343
#         - Email: akhileswarreddymp9177@gmail.com
#         - Location: Bengaluru, India
#         - Career Objective: Having 3 years of experience in Python backend Development using FastAPI, proficient in Git, FastApi, Python, Redis, Mongodb, ElasticSearch, React js, Html and css.
#         - Work Experience:
#         - Software Engineer | Quicknify SOftware Technologies (feb 2021 - feb 2024, Bengaluru, India)
#         - Project: Retail outlet automation for IOCL, IOML and BPCL
#         - Project Description: Lead end to end backend and front end development using Python, FastAPI and react js where we have completely automated the outlets by building alerting and interlocing mechanism for reducing the frudelent activities in retail outlet with auto price mechanism as well.
#         - Education:
#         - B.Tech (ECE), Sri Krishnadevaraya University COllege of Engineering and Technology
#         - Technical Skills:
#         - Python, FastAPI, Elasticsearch, Mongodb, Redis, Html,css,React Js, ThingsBoard,RabbitMq.
#         - SCM Tools: GIT
#         - Monitoring Tool: Kibana
#         - Scripting: Shell Scripting, Python
#         - Languages:
#         - English