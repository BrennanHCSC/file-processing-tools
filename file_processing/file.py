from pathlib import Path
from txt_processor import TextFileProcessor
from pdf_processor import PdfFileProcessor
from docx_processor import DocxFileProcessor
from ocr_decorator import OCRDecorator
from msg_processor import MsgFileProcessor
from png_processor import PngFileProcessor
from xlsx_processor import xlsxFileProcessor
from pptx_processor import PptxFileProcessor
from rtf_processor import RtfFileProcessor
from html_processor import HtmlFileProcessor
from xml_processor import XmlFileProcessor
from jpeg_processor import JpegFileProcessor
from csv_processor import CsvFileProcessor
from json_processor import JsonFileProcessor
from zip_processor import ZipFileProcessor
from py_processor import PyFileProcessor
from mp3_processor import Mp3FileProcessor
from errors import UnsupportedFileTypeError, NotOCRApplciableError

class File:
    OCR_APPLICABLE_EXTENSIONS = {".pdf", ".jpeg", ".png"}

    PROCESSORS = {
        ".csv": CsvFileProcessor,
        ".txt": TextFileProcessor,
        ".pdf": PdfFileProcessor,
        ".docx": DocxFileProcessor,
        ".msg": MsgFileProcessor,
        ".pptx": PptxFileProcessor,
        ".rtf": RtfFileProcessor,
        ".html": HtmlFileProcessor,
        ".xml": XmlFileProcessor,
        ".png": PngFileProcessor,
        ".xlsx": xlsxFileProcessor,
        ".jpeg": JpegFileProcessor,
        ".jpg": JpegFileProcessor,
        ".json": JsonFileProcessor,
        ".zip": ZipFileProcessor,
        ".py": PyFileProcessor,
        ".mp3": Mp3FileProcessor
    }

    def __init__(self, path: str, use_ocr: bool = False) -> None:
        self.path = Path(path)
        self.processor = self._get_processor(use_ocr)
        self.process()

    def _get_processor(self, use_ocr: bool) -> 'FileProcessorStrategy':
        extension = self.path.suffix

        processor_class = File.PROCESSORS.get(extension)
        if not processor_class:
            raise UnsupportedFileTypeError(f"No processor for file type {extension}")

        processor = processor_class(str(self.path))

        if use_ocr:
            if extension not in File.OCR_APPLICABLE_EXTENSIONS:
                raise NotOCRApplciableError(f"OCR is not applicable for file type {extension}.")
            return OCRDecorator(processor)

        return processor


    def save(self, output_path: str = None) -> None:
        self.processor.save(output_path)


    def process(self) -> None:
        return self.processor.process()

    
    @property
    def file_path(self) -> str:
        return self.processor.file_path


    @property
    def file_name(self) -> str:
        return self.processor.file_name


    @property
    def extension(self) -> str:
        return self.processor.extension

    @property
    def size(self) -> str:
        return self.processor.size

    @property
    def modification_time(self) -> str:
        return self.processor.modification_time

    @property
    def access_time(self) -> str:
        return self.processor.access_time

    @property
    def metadata(self) -> dict:
        return self.processor.metadata
