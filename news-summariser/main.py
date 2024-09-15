#type: ignore

import openai
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import requests
import json

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")
client = openai.OpenAI()
model = "gpt-3.5-turbo"

def get_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=5"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            news = json.dumps(response.json(), indent=4)
            news_json = json.loads(news)

            data = news_json

            status = data["status"]
            totalResults = data["totalResults"]
            articles = data["articles"]
            final_news = []

            print(f"Status: {status}")
            print(f"Total Results: {totalResults}")
            print(f"Articles: {articles}")

            for article in articles:
                title = article["title"]
                description = article["description"]
                url = article["url"]
                publishedAt = article["publishedAt"]
                content = article["content"]
                print(f"Title: {title}")
                print(f"Description: {description}")
                print(f"URL: {url}")
                print(f"Published At: {publishedAt}")
                print(f"Content: {content}")
                print("\n")
                final_news.append(f"Title: {title}\nDescription: {description}\nURL: {url}\nPublished At: {publishedAt}\nContent: {content}\n\n")

            return final_news
        else:
            print(f"Error fetching news: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def main():
    get_news("bitcoin")

class AssistantManager:
    thread_id = None
    assistant_id = None

    def __init__(self, model:str = model):
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None

        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id=AssistantManager.assistant_id)

        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(thread_id=AssistantManager.thread_id)

    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=self.model
            )
            self.assistant = assistant_obj
            AssistantManager.assistant_id = assistant_obj.id
            print(f"Assistant created with id: {self.assistant_id}")

    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print(f"Thread created with id: {self.thread_id}")

    def add_message(self, thread_id, role, content): 
        if self.thread:
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role=role,
            content=content
        )

    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id
            )
            print(f"Run created with id: {self.run_id}")

    def process_messages(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread_id
            )
            summary = []

            last_message = messages.data[0]
            role = last_message.role
            response = last_message.content[0].text.value

            summary.append(f"{role}: {response}")

            self.summary = "\n".join(summary)
            print(f"Messages retrieved with id: {self.thread_id}")

            # for msg in messages:
            #     role = msg.role
            #     content = msg.content[0].text.value
            #     print(f"{role}: {content}")

    def call_required_functions(self, required_actions):
        if not self.run:
            return
        tools_outputs = []

        for action in required_actions["tool_calls"]:
            func_name = action.function.name
            arguments = json.loads(action.function.arguments)

            if func_name == "get_news":
                news = get_news(topic = arguments["topic"])
                print("STUFFF")


    

    def wait_for_completion(self):
        if self.run and self.thread:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=self.run_id)
                print(f"Run status: {run_status.model_dump_json(indent=4)}")

                if run_status.status == "completed":
                    self.process_messages()
                    break
                elif run_status.status == "requires_action":
                    print("FUNCTION CALLING NOW...")
                    self.call_required_functions(self, required_actions)

    def create_run(self, thread_id, assistant_id):
        if not self.run:
            run_obj = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            self.run = run_obj
            print(f"Run created with id: {self.run_id}")

if __name__ == "__main__":
    main()

