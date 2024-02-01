import json
import os

import pytest

from app.schemas.answer_response import AnswerResponse
from app.utils.dir import write_result_file_for_task

sample_file_content = 'Sample file content.'


@pytest.fixture
def sample_data(tmpdir):
    # Using tmpdir to create a temporary directory for the test
    temp_dir = tmpdir.mkdir("temp_data")

    task_id = 'sample_task'
    loaded_file_path = str(temp_dir.join("sample_file.txt"))

    # Creating a sample file with content
    with open(loaded_file_path, 'w', encoding='utf-8') as sample_file:
        sample_file.write(sample_file_content)

    results = [AnswerResponse(question="q1", answer="ans1")]

    return {
        'task_id': task_id,
        'loaded_file_path': loaded_file_path,
        'results': results,
        'temp_dir': temp_dir
    }


def test_write_result_file_for_task(sample_data):
    # Arrange
    task_id = sample_data['task_id']
    loaded_file_path = sample_data['loaded_file_path']
    results = sample_data['results']
    temp_dir = sample_data['temp_dir']

    new_file_path = write_result_file_for_task(task_id, loaded_file_path, results)

    # Assert
    assert os.path.exists(new_file_path)

    # Verify the content of the file
    with open(new_file_path, 'r', encoding='utf-8') as output_file:
        data_dict_list = json.load(output_file)
        assert data_dict_list[0].get('question') == results[0].question
        assert data_dict_list[0].get('answer') == results[0].answer

    # Verify the content of the loaded file
    with open(loaded_file_path, 'r', encoding='utf-8') as sample_file:
        assert sample_file.read() == sample_file_content

    # Cleanup (optional)
    os.remove(new_file_path)
    temp_dir.remove()
