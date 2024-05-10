import openai

# Set your API key
api_key = "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"
openai.api_key = api_key

# Example prompt
prompt = "I am the interviewer and you are the interviewee now answer my questions. Tell me about dictionaries in Python"

# Generate text using the chat completion endpoint
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt}
  ]
)

# Print the generated text
print(response['choices'][0]['message']['content'].strip())
