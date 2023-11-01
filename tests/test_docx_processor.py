import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File
from docx import Document


variable_names = "path, text_length, last_modified_by, author"
values = [
   ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia.docx', 1631, 'Test last_modified_by One', 'Test Author One'),
   ('tests/resources/test_files/SampleReport.docx', 3220, 'last_modified_by Test Author', 'Second Test Author')
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
def test_docx_invalid_save_location(invalid_save_location):
    invalid_save_location


corrupted_files = [
    'tests/resources/test_files/HealthCanadaOverviewFromWikipedia_corrupted.pptx'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_docx_corrupted_file_processing(corrupted_file_processing_lock):
    corrupted_file_processing_lock

locked_files = [
     ('tests/resources/test_files/SampleReport_Locked.docx'), 
     ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia_Locked.docx')
]

@pytest.mark.parametrize("path", locked_files)
def test_docx_locked(path):
    assert File(path).metadata["has_password"] == True