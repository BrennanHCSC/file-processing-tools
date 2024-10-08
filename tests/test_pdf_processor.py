import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, ocr_text_length"
values = [
    (test_files_path / 'SampleReportScreenShot.pdf', 3225),
    (test_files_path / 'HealthCanadaOverviewFromWikipedia.pdf', 1673)
]


@pytest.mark.parametrize(variable_names, values)
def test_pdf_metadata(path, ocr_text_length):
    file_obj = File(path, use_ocr=True)
    # Must check approximate match as pytesseract transcribes differently based on OS
    assert ocr_text_length == pytest.approx(
        len(file_obj.metadata['ocr_text']), 1)


locked_files = [
    (test_files_path / 'SampleReport_Locked.pdf'),
    (test_files_path / 'ArtificialNeuralNetworksForBeginners_Locked.pdf')
]


@pytest.mark.parametrize("path", locked_files)
def test_pdf_locked(path):
    assert File(path).metadata["has_password"] is True


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_pdf_invalid_save_location(path):
    pdf_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        pdf_file.processor.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()
