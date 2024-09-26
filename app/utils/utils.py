import os


def find_or_create_temp_dir():
    current_path = os.path.dirname(os.path.abspath(__file__))

    app_dir = os.path.dirname(current_path)
    project_root = os.path.dirname(app_dir)

    # Define the temp directory path relative to the project root
    temp_dir = os.path.join(project_root, "temp")

    # Check if the temp directory exists, if not, create it
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)

    return temp_dir


if __name__ == "__main__":
    temp_directory = find_or_create_temp_dir()
    print(f"Using temp directory: {temp_directory}")
