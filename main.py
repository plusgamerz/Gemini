#---------
# Gemini
#---------

# Libraries
from google import genai
from google.genai import types
from tools import file_tools as ft
import os
import subprocess, json

# Variables
chat_name = "new_chat.json"

# System Prompt
sys_inst = f"""# GENERAL

You are an AI assistant.
You are helpful, honest, and concise.
You are required to use the name_chat function on the first message.
You are running on a Windows 8.1 machine.
Always try to answer as short you can and try not to repeat something.

Current working directory:
{os.getcwd()}
"""

# Tools    
def name_chat(name: str) -> str:
    global chat_name

    try:
        os.rename(chat_name, name)
        chat_name = name
        return "Chat renamed successfully."
    except Exception as e:
        return f"Error: {e}"
    
def basic_terminal(command:str,timeout:int) -> str:
    """basic_terminal tool can only do commands that has no input or don't have a timeout, use it carefully and with caution."""
    return "OUTPUT: " + subprocess.run(command,shell=True,timeout=timeout)

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=sys_inst,
        tools=[
            ft.create_file,
            ft.create_folder,
            ft.copy_item,
            ft.move_item,
            ft.delete_item,
            ft.list_items,
            name_chat,
        ],
    ),
)

# Chat Loop
if __name__ == "__main__":
    try:
        while True:
            user = input("> ")

            if not user.strip():
                continue

            response = chat.send_message(user)

            print(response.text)

            def json_converter(obj):
                if isinstance(obj, bytes):
                    return obj.decode("utf-8", errors="replace")
                return str(obj)

            history = [item.model_dump() for item in chat.get_history()]

            with open(chat_name, "w", encoding="utf-8") as f:
                json.dump(
                    history,
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=json_converter
            )

    except KeyboardInterrupt:
        print("\nExiting...")

    except Exception as e:
        print(f"\nError: {e}")