import json
import os

def create_assistant(client):
    assistant_file_path = 'assistant.json'
    knowledge_doc_path = 'C:\\Users\\ASUS\\OneDrive\\Desktop\\Diversion\\Compliance\\knowledge.docx'

    try:
        if os.path.exists(assistant_file_path):
            with open(assistant_file_path, 'r') as file:
                assistant_data = json.load(file)
                assistant_id = assistant_data['assistant_id']
                print("Loaded existing assistant ID.")
        else:
            with open(knowledge_doc_path, 'rb') as knowledge_file:
                file = client.files.create(file=knowledge_file, purpose='assistants')

            assistant = client.beta.assistants.create(
                instructions="""
                    You are an expert at drafting various permits for Film production.
                    You will use the outline provided in the document and ask 3 questions to the user one at a time.
                    Finally, you will generate a draft of a permit using all the information you gathered.
                """,
                model="gpt-4-1106-preview",
                tools=[{"type": "retrieval"}],
                file_ids=[file.id]
            )

            with open(assistant_file_path, 'w') as file:
                json.dump({'assistant_id': assistant.id}, file)
                print("Created a new assistant and saved the ID.")

            assistant_id = assistant.id

        return assistant_id

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Handle errors appropriately in your application
