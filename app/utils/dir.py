import json
import os


def get_project_root_output_dir():
    script_path = os.path.abspath(__file__)
    # Get the directory of the script
    script_directory = os.path.dirname(script_path)
    # Get the project root directory by going up one level
    project_root = os.path.abspath(os.path.join(script_directory, ".."))
    # Append "/output" to the project root directory
    output_directory = os.path.join(project_root, "output/")
    return output_directory


def write_result_file_for_task(task_id: str, loaded_file_path: str, results: dict):
    output_file_path = f"{task_id}.json"
    directory, filename = os.path.split(loaded_file_path)
    new_file_path = os.path.join(directory, output_file_path)

    with open(new_file_path, 'w', encoding='utf-8') as output_file:
        data_dict_list = [entry.dict() for entry in results]
        json.dump(data_dict_list, output_file, indent=2)

    print(f"Results saved to {new_file_path}")

    return new_file_path
