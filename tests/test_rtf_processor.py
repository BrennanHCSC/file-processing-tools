import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError

variable_names = "path, text_length"
values = [
    ('tests/resources/test_files/Test_for_RTF.rtf', 5306)
]


@pytest.mark.parametrize(variable_names, values)
def test_rtf_metadata(path, text_length):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length


@pytest.mark.parametrize(variable_names, values)
def test_save_rtf_metadata(copy_file, text_length):
    test_rtf_metadata(copy_file, text_length)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_rtf_invalid_save_location(path):
    rtf_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        rtf_file.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()
