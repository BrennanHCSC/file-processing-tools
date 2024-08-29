import os
from unittest.mock import patch
from datetime import datetime
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError


variable_names = "path, text_length, subject, date, sender"
values = [
    ('tests/resources/test_files/Test Email.msg', 19, 'Test Email', 'Mon, 18 Sep 2023 13:57:16 -0400', '"Burnett, Taylen (HC/SC)" <Taylen.Burnett@hc-sc.gc.ca>'),
    ('tests/resources/test_files/Health Canada Overview from Wikipedia.msg', 13876, 'Health Canada Overview from Wikipedia', 'Tue, 31 Oct 2023 14:54:03 -0400', '"Prazuch, Karolina (HC/SC)" <karolina.prazuch@hc-sc.gc.ca>')
]


@pytest.mark.parametrize(variable_names, values)
def test_msg_metadata(path, text_length, subject, date, sender):
    file_obj = File(path)

    # Compare dates from different timezones
    processed_date = datetime.strptime(
        file_obj.metadata['date'], "%a, %d %b %Y %H:%M:%S %z")
    true_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")

    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['subject'] == subject
    assert processed_date == true_date
    assert file_obj.metadata['sender'] == sender


@pytest.mark.parametrize(variable_names, values)
def test_save_msg_metadata(copy_file, text_length, subject, date, sender):
    test_msg_metadata(copy_file, text_length, subject, date, sender)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_msg_invalid_save_location(path):
    msg_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        msg_file.processor.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()
