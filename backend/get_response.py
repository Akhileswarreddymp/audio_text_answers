from fastapi import APIRouter
import openai
import asyncio
from models import *

router = APIRouter(prefix="/api")

# Set your API key
api_key = "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"
openai.api_key = api_key
 
# Initialize conversation history
conversation_history = []
@router.post("/get_answer",tags=["Voice"])
async def generate_humanlike_response(request : prompt_text):
    print("prompt=====>",request.prompt_text)
    try:
        api_key = "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"
        openai.api_key = api_key
        
        # Initialize conversation history
        conversation_history = []
 
   
        # Record the user's prompt in the conversation history
        conversation_history.append({"role": "user", "content": request.prompt_text})
    
        # Limit the conversation history to the last 3 interactions to manage costs
        limited_history = conversation_history[-3:]
    
        # Adjusted prompt to simulate a dynamic, interactive job interview
        resume_summary = """
        Akhileswar Reddy
        - Mobile: 8217220343
        - Email: akhileswarreddymp9177@gmail.com
        - Location: Bengaluru, India
        - Career Objective: Having 3 years of experience in Python backend Development using FastAPI, proficient in Git, FastApi, Python, Redis, Mongodb, ElasticSearch, React js, Html and css.
        - Work Experience:
        - Software Engineer | Quicknify SOftware Technologies (feb 2021 - feb 2024, Bengaluru, India)
        - Project: Retail outlet automation for IOCL, IOML and BPCL
        - Project Description: Lead end to end backend and front end development using Python, FastAPI and react js where we have completely automated the outlets by building alerting and interlocing mechanism for reducing the frudelent activities in retail outlet with auto price mechanism as well.
        - Education:
        - B.Tech (ECE), Sri Krishnadevaraya University COllege of Engineering and Technology
        - Technical Skills:
        - Python, FastAPI, Elasticsearch, Mongodb, Redis, Html,css,React Js, ThingsBoard,RabbitMq.
        - SCM Tools: GIT
        - Monitoring Tool: Kibana
        - Scripting: Shell Scripting, Python
        - Languages:
        - English
        """
        prompt = f"""You're Akhileswar Redy, a FullStack Developer with extensive experience in Python,FastAPi and React, based on this resume summary:
        {resume_summary}
    
        I'm the recruiter asking questions to assess your skills and expertise. Respond to any technical or non-technical question in normal indian slang English in a concise manner, and conversational manner, as if we're speaking face-to-face, showcasing your achievements, skills, and problem-solving abilities based on question.respond with out using any large vocabulary, complicated words and complicated technologies in the speech,and give the answer short and concise.
   
        answer my questions as you are a human: {request.prompt_text}"""
    
        # Use OpenAI to generate a response considering the limited conversation history                  
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
    
        # Retrieve the generated response and clean it up
        response_content = response['choices'][0]['message']['content'].strip()
    
        # Log the assistant's response to maintain conversation context
        conversation_history.append({"role": "assistant", "content": response_content})
    
        # Display and return the assistant's response in a human-like manner
        print("As a candidate, my response would be:", response_content)
        return response_content
    

    except Exception as error:
        print("Error with OpenAI API:", error)
 