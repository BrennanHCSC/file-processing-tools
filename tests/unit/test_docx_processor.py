import os
from unittest.mock import patch
from docx import Document
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, text_length, last_modified_by, author"
values = [
    (test_files_path / 'HealthCanadaOverviewFromWikipedia.docx', 1631, 'Test last_modified_by One', 'Test Author One'),
    (test_files_path / 'SampleReport.docx', 3220, 'last_modified_by Test Author', 'Second Test Author')
]


@pytest.mark.parametrize(variable_names, values)
def test_docx_metadata(path, text_length, last_modified_by, author):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['last_modified_by'] == last_modified_by
    assert file_obj.metadata['author'] == author


@pytest.mark.parametrize("path, text_length", map(lambda x: x[:2], values))
def test_save_docx_metadata(copy_file, text_length):

    # Load and change metadata via File object
    docx_file = File(copy_file)
    docx_file.metadata['last_modified_by'] = 'Modified New'
    docx_file.metadata['author'] = 'New Author'

    # Save the updated file
    docx_file.save()
    test_docx_metadata(copy_file, text_length, 'Modified New', 'New Author')


@pytest.mark.parametrize("path, text_length", map(lambda x: x[:2], values))
def test_change_docx_author_last_modified_by(copy_file, text_length):

    # Change metadata via Document object
    docx_file = Document(copy_file)
    docx_file.core_properties.last_modified_by = "Modified New"
    docx_file.core_properties.author = "New Author"

    # Save the file
    docx_file.save(copy_file)
    test_docx_metadata(copy_file, text_length, 'Modified New', 'New Author')


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_docx_invalid_save_location(path):
    docx_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        docx_file.processor.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()


locked_files = [
    (test_files_path / 'SampleReport_Locked.docx'),
    (test_files_path / 'HealthCanadaOverviewFromWikipedia_Locked.docx')
]


@pytest.mark.parametrize("path", locked_files)
def test_docx_locked(path):
    assert File(path).metadata["has_password"] is True
