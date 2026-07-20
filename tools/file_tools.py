# Libraries
import os, shutil

# Tools
def create_file(path: str, content: str) -> str:
    print("SYS: Creating a file...")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Created file:\n{path}"

    except Exception as e:
        return f"Error: {e}"
    
def create_folder(path:str) -> str:
    print("SYS: Creating a folder...")
    try:
        os.mkdir(path)
        return "Created a folder succesfully."
    except Exception as e:
        return f"Error: {e}"
    
def read_file(path:str, size:int=500000) -> str:
    """The size variable limits how big file this tool can open."""
    print("SYS: Reading a file...")
    if os.path.isfile(path):
        file_size = os.path.getsize(path)
    else:
        return "Given path not a file!"
    
    if file_size < size:
        with open(path,"r") as f:
            data = "Content of the file: " + f.read()
        return data
    else:
        return "File size exceded the given limit!"

def copy_item(src:str, dst:str, overwrite:bool=False) -> str:
    """This function can both copy a folder or file. Overwrite the same file or folder in the dst."""
    print("SYS: Copying...")
    if not os.path.exists(src):
        raise FileNotFoundError(src)

    if os.path.exists(dst):
        if not overwrite:
            raise FileExistsError(dst)

        if os.path.isdir(dst):
            shutil.rmtree(dst)
        else:
            os.remove(dst)

    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        shutil.copy2(src, dst)

    return dst

def move_item(src:str,dst:str,overite:bool=False) -> str:
    print("SYS: Moving...")
    if src == dst:
        return "src cant't be same as dst because it now acts like delete_items."
    try:
        copy_item(src,dst,overwrite=overite)
        delete_item(src)
    except Exception as e:
        return f"Error: {e}"
    
def delete_item(path: str) -> str:
    print("SYS: Deleting...")
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
    
def list_items(path: str, filter_file:bool=False, filter_folder:bool=False) -> str:
    print("SYS: Listing...")
    try:
        if not os.path.exists(path):
            return "Path does not exist."

        items = os.listdir(path)

        if not items:
            return "Folder is empty."

        result = []

        for item in items:
            full = os.path.join(path, item)

            if os.path.isfile(full) and filter_file == False:
                t = "File"
            elif os.path.isdir(full) and filter_folder == False:
                t = "Folder"

            result.append(f"{item} ({t})")

        return "\n".join(result)

    except Exception as e:
        return f"Error: {e}"