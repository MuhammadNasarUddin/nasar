import os
from openai import OpenAI
import time
import re
class Didx_admin_bot:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("openai_api_key"))
        self.assistant_id = "asst_ds3aRHZd5G2dP7TaLD9V3DB6"

        # Update the assistant
        self.client.beta.assistants.update(
            self.assistant_id,
            name="DIDx Financial Assistant",     
            instructions="Act as a DIDX Financial assistant to retrieve information from the given files. Do not include the source of the file in the output.",
            model="gpt-4-turbo",
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": ["vs_m2vxi3gZ3tRlVySzbhsRmERy"]
                }
            }
        )

    # Function to chat with the bot
    def user_chat(self, query):
        thread = self.client.beta.threads.create()

        # Send the user message
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role='user',
            content=query
        )

        # Create a run
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
            instructions=""
        )

        # Poll the run until it completes
        while True:
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run.status == 'completed':
                break
            time.sleep(1)

        # Retrieve the messages
        messages = self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
        messages_list = list(messages)
        print(f"Messages: {messages_list}")
        messages_content = messages_list[0].content[0].text
        print(f"Messages Content: {messages_content}")
        cleaned_text = re.sub('【.*?†.*】', '', messages_content.value)
        return cleaned_text
