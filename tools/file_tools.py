# Libraries
import os, shutil

# Tools
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