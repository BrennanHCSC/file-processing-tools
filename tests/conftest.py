from pathlib import Path
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError

# copy_file fixture to be used in test_..._processor.py files
@pytest.fixture()
def copy_file(path, tmp_path_factory):
    copy_path = str(tmp_path_factory.mktemp("copy") / Path(path).name)
    file_obj = File(path)
    file_obj.save(copy_path)
    yield copy_path

# invalid_save_location fixture to be used in test_..._processor.py files
@pytest.fixture()
def invalid_save_location(path):
    save_path = '/non_existent_folder/' + path
    file_obj = File(path)
    with pytest.raises(FileProcessingFailedError):
        file_obj.processor.save(save_path)
