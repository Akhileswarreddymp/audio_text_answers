# import speech_recognition as sr
# from fastapi import FastAPI


# app = FastAPI()

# @app.get("/get_result",tags=["get_result"])
# async def recognaize_voice_and_get_result():

#     recognizer = sr.Recognizer()

#     # microphone as the audio source
#     with sr.Microphone() as source:
#         print("Speak something...")
#         audio = recognizer.listen(source)

#         try:
#             # Google Web Speech API for recognition
#             audio_to_text = recognizer.recognize_google(audio)
#             print("You said:", audio_to_text)
#             try:
#                 import openai

#                 # Set your API key
#                 api_key = "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"
#                 openai.api_key = api_key

#                 # Example prompt
#                 prompt = "I am going to intervew you so, answer my questions on real time basic just like face-to-face intervier"+ " " + audio_to_text

#                 # Generate text using the chat completion endpoint
#                 response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt}
#                 ]
#                 )

#                 # Print the generated text
#                 print(response['choices'][0]['message']['content'].strip())
#                 return response['choice'][0]["msessage"]
#             except Exception as error:
#                 print(error)


#         except sr.UnknownValueError:
#             print("Sorry, could not understand audio")
#         except sr.RequestError as e:
#             print("Could not request results from Google Web Speech API",e)

        