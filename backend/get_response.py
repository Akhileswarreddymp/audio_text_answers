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
        IRFAN
        - Mobile: 9686498545
        - Email: irfanronaldo37@gmail.com
        - Location: Bengaluru, India
        - Career Objective: Having 4 years of experience in IT Infrastructure with DevOps and AWS Management as a DevOps Engineer, proficient in Git, Maven, Jenkins, Docker, Kubernetes, Ansible, Terraform, and AWS, Shell scripting.
        - Work Experience:
        - DevOps Engineer | Deloitte (Jan 2020 - Present, Bengaluru, India)
        - Project: tms (Texas municipal league) (Sep 2022 - June 2023)
        - Project Description: Lead the migration process of servers & data from the on-premises data center to AWS Cloud. Automated CI/CD pipelines using Jenkins, managed Docker containers, and Kubernetes for orchestration.
        - Education:
        - B.Tech (Electrical), Chaitanya Bharathi Institute Of Technology (2015)
        - Technical Skills:
        - SCM Tools: GIT, SVN
        - Build Tools: MAVEN
        - Continuous Integration Tools: Jenkins
        - Configuration Management Tool: Ansible
        - Containerization Tool: Docker
        - Containerization Orchestration Tool: Kubernetes, Helm, Argocd
        - Infrastructure Tool: Terraform
        - Monitoring Tool: Grafana, Kibana, Prometheus
        - Cloud Platform: AWS (EC2, S3, VPC, IAM, Cloud Watch, EBS, Route53, ELB, Auto Scaling)
        - Scripting: Shell Scripting, Python
        - Languages:
        - English
        - Interests: Cloud Computing, Infrastructure Automation, Continuous Integration/Continuous Deployment
        """
        prompt = f"""You're IRFAN, a DevOps Engineer with extensive experience in AWS and infrastructure automation, based on this resume summary:
        {resume_summary}
    
        I'm the recruiter asking questions to assess your skills and expertise. Respond to any technical or non-technical question in a clear, concise, and conversational manner, as if we're speaking face-to-face, showcasing your achievements, skills, and problem-solving abilities.and use butler english like daily conversation,just give me the answer in butler english,i want the answer like clear story telling way,
    
        Here's my first question: {request.prompt_text}"""
    
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
 