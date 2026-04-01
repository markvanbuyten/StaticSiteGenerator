import os
import shutil

def clean_directory(directory_path):
    if not os.path.exists(directory_path):
        print(f"Pad doesn't exist: {directory_path}")
        return
    
    for item_name in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item_name)

        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Error while deleting {item_path}: {e}")
    print(f"Content of {directory_path} was deleted.")

def copy_files_recusive(source_node_path, destination_node_path):
    if not os.path.exists(destination_node_path):
        os.mkdir(destination_node_path)

    for item in os.listdir(source_node_path):
        from_path = os.path.join(source_node_path, item)
        to_path = os.path.join(destination_node_path, item)

        print(f" * {from_path} -> {to_path}")

        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_files_recusive(from_path, to_path)