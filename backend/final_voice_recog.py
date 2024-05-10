import speech_recognition as sr
from fastapi import FastAPI
import openai
import asyncio
import time  # Importing the time module to use time.sleep()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from all origins (replace "*" with your frontend domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# app = FastAPI()
 
@app.get("/get_result", tags=["get_result"])
async def recognize_voice_and_get_result():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 4000
 
    # microphone as the audio source
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Speak something...")
        audio = await asyncio.to_thread(recognizer.listen, source, phrase_time_limit=5)
        try:
            # Google Web Speech API for recognition
            text = await asyncio.to_thread(recognizer.recognize_google, audio)
            print("You said:", text)
            try:
                # Set your API key
                api_key = "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"
                openai.api_key = api_key
 
                # Adjusted prompt to simulate a dynamic, interactive job interview
                resume_summary = """
                Narahari Daggupatti
                - Mobile: + (91) 8919797124
                - Email: hariiaa12345@gmail.com
                - Career Objective: Dynamic and results-driven DevOps and AI engineer with 4+ years of experience, delivering transformative solutions across industries.
                - Work Experience:
                - Senior AI DevOps Engineer, Deloitte (2019-Present)
                - AI Platform Engineer, JPMorgan Chase & Co. (2019-2021)
                - Education: B.Tech in Computer Science & Engineering, AIIT Hyderabad, 2017
                - Certifications: Certified Kubernetes Application Developer (CKAD), AWS Certified DevOps Engineer - Professional
                - Technical Skills: Python, Java, Go, Git, Jenkins, Kubernetes, Terraform, Docker, and more.
                """
                prompt = f"""You're Narahari Daggupatti, a DevOps and AI engineer with extensive experience, based on this resume summary:
                {resume_summary}
                
                I'm the recruiter asking questions to assess your skills and expertise. Respond to any technical or non-technical question in a clear, concise, and conversational manner, as if we're speaking face-to-face, showcasing your achievements, skills, and problem-solving abilities.
                
                Here's my first question: {text}"""
                # Generate text using the chat completion endpoint
                response = await asyncio.to_thread(
                    openai.ChatCompletion.create,
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
 
                # Simulate real-time typing of the generated text
                response_content = response['choices'][0]['message']['content'].strip()
                print(response_content)
                return response_content
                # for char in response_content:
                #     print(char, end='', flush=True)
                #     time.sleep(0.01)  # Delay to mimic real-time typing
 
            except Exception as error:
                print("Error with OpenAI API:", error)
 
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API:", e)
