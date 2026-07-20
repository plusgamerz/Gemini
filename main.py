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
history = None

# System Prompt
sys_inst = f"""# GENERAL

You are an Programming AI assistant. You are helpful, honest, and concise.
When user asks to make web, code or app, make the UI as best as you can.
You are required to use the name_chat function on the first message.
You are running on a Windows 8.1 machine.
Always try to answer as short and try not to repeat something.
Try not to leave your cwd.
Don't tell the user the same code that you just wrote in a file.

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
    
def basic_terminal(command:str,user_input:str,timeout:int) -> str:
    """basic_terminal tool can only do commands that has no input, use it carefully and with caution but still use it to run one command code."""
    return "OUTPUT: " + subprocess.run(command,shell=True,timeout=timeout,input=user_input)

def background_terminal(command: str,user_input:str, timeout: int):
    """Same as basic_terminal but runs in bg, use it to run code or downloads."""
    p = subprocess.Popen(
        command,
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    try:
        p.wait(timeout=timeout)
        return f"Exited with code {p.returncode}"
    except subprocess.TimeoutExpired:
        p.kill()
        return "Timed out and was terminated."

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def start_chat(model="gemini-3.1-flash-lite",history=None):
    chat = client.chats.create(
        model=model,
        config=types.GenerateContentConfig(
            system_instruction=sys_inst,
            history=history,
            tools=[
                ft.create_file,
                ft.create_folder,
                ft.copy_item,
                ft.move_item,
                ft.delete_item,
                ft.list_items,
                name_chat,
                basic_terminal,
                background_terminal
            ],
        ),
    )
    return chat

chat = start_chat()

# Initializing Code
models = client.models.list()

# Chat Loop
if __name__ == "__main__":
    try:
        while True:
            user = input("> ")

            if user[0] == "/":
                # Detect Command
                command = user.split()
                op = (command[0])[1:]
                args = command[1:]

                # Commands
                if op.lower() == "model": # Change model
                    if args[0] in models:
                        print(f"SYS: Changing to {args[0]}!")
                        chat = start_chat(args[0],history=history)
                    else:
                        print("SYS: Model not in your API!")
                
                continue

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