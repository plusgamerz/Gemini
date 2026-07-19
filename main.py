from google import genai
from google.genai import types
import os
import shutil, json


# -----------------------------
# Running terminal sessions
# -----------------------------
_sessions = {}

chat_name = "new_chat.json"

# -----------------------------
# System Prompt
# -----------------------------
sys_inst = f"""# GENERAL

You are an AI assistant.
You are helpful, honest, and concise.

You are running on a Windows 8.1 machine.

Current working directory:
{os.getcwd()}

# TOOLS

Terminal:
- start_terminal(command)
  Starts a new cmd terminal.

- input_terminal(session_id, text)
  Sends text to the running terminal.
"""

# -----------------------------
# TOOLS
# -----------------------------
def name_chat(name: str) -> str:
    global chat_name

    try:
        os.rename(chat_name, name)
        chat_name = name
        return "Chat renamed successfully."
    except Exception as e:
        return f"Error: {e}"


def create_file(path: str, content: str) -> str:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Created file:\n{path}"

    except Exception as e:
        return f"Error: {e}"


def delete_item(path: str) -> str:
    try:
        if os.path.isfile(path):
            os.remove(path)
            return f"Deleted file:\n{path}"

        elif os.path.isdir(path):
            shutil.rmtree(path)
            return f"Deleted folder:\n{path}"

        return "Path does not exist."

    except Exception as e:
        return f"Error: {e}"


def list_items(path: str) -> str:
    try:
        if not os.path.exists(path):
            return "Path does not exist."

        items = os.listdir(path)

        if not items:
            return "Folder is empty."

        result = []

        for item in items:
            full = os.path.join(path, item)

            if os.path.isfile(full):
                t = "File"
            else:
                t = "Folder"

            result.append(f"{item} ({t})")

        return "\n".join(result)

    except Exception as e:
        return f"Error: {e}"

# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client(
    api_key="API_KEY_HERE"
)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=sys_inst,
        tools=[
            create_file,
            delete_item,
            list_items,
            name_chat,
        ],
    ),
)

# -----------------------------
# Chat Loop
# -----------------------------
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