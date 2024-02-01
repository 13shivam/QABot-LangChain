import json
import os
from pypdf import PdfReader
from app.utils.dir import get_project_root_resources_dir


# TODO
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def load_pdf(file_path: str):
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    file_name = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
    path = get_project_root_resources_dir()
    final_file_path = path + file_name
    with open(final_file_path, "w") as f:
        for i in range(number_of_pages):
            page = reader.pages[i]
            text = page.extract_text().strip()
            f.write(text.replace("\n", " "))

        f.close()

    return final_file_path
