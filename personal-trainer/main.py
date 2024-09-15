import openai
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")  # Add this line to verify the API key is loaded

client = openai.OpenAI(api_key=api_key)

model = "gpt-3.5-turbo"

# personal_assistant = client.beta.assistants.create(name="Personal Assistant", instructions="You are a personal assistant. Your name is Personal Assistant. You are helpful, respectful, honest, and an excellent problem solver.", 
# model=model)

# print(personal_assistant.id)

# thread = client.beta.threads.create(messages=[{"role": "user", "content": "I need help with my personal trainer"}])

# print(thread.id)

assistant_id = "asst_Gz5zbJtWBTQLj5L0AJpYjr1d"
thread_id = "thread_IUwnmbR3fbtz8xTlAMp7Mp55"

message = "What can you do for me?"

message = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=message)

run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, instructions="Please address the user as Jane Doe. The user has a premium account.")






