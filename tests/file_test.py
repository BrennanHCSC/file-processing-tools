import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))

def test_txt_text():
    from file_processing.file import File
    txt_1 = File('tests/resources/test_files/government_of_canada_wikipedia.txt')
    txt_2 = File('tests/resources/test_files/usa_government_wikipedia.txt')
    assert len(txt_1.metadata['text']) == 38983
    assert len(txt_2.metadata['text']) == 47819

def test_txt_num_lines():
    # indirectly tests lines attribute
    from file_processing.file import File
    txt_1 = File('tests/resources/test_files/government_of_canada_wikipedia.txt')
    txt_2 = File('tests/resources/test_files/usa_government_wikipedia.txt')
    assert txt_1.metadata['num_lines'] == 306
    assert txt_2.metadata['num_lines'] == 383

def test_txt_num_words():
    # indirectly tests words attribute
    from file_processing.file import File
    txt_1 = File('tests/resources/test_files/government_of_canada_wikipedia.txt')
    txt_2 = File('tests/resources/test_files/usa_government_wikipedia.txt')
    assert txt_1.metadata['num_words'] == 5691
    assert txt_2.metadata['num_words'] == 7160


def test_docx_text():
    from file_processing.file import File
    docx_1 = File('tests/resources/test_files/HealthCanadaOverviewFromWikipedia.docx')
    docx_2 = File('tests/resources/test_files/SampleReport.docx')
    assert len(docx_1.metadata['text']) == 1631
    assert len(docx_2.metadata['text']) == 3220


def test_docx_author():
    from file_processing.file import File
    from docx import Document

    # Paths of test files
    test_docx_1_path = 'tests/resources/test_files/HealthCanadaOverviewFromWikipedia.docx'
    test_docx_2_path = 'tests/resources/test_files/SampleReport.docx'

    # Arbitrary test author names
    test_author_1 = 'Test Author One'
    test_author_2 = 'Second Test Author'

    # Update test docx files to have test names
    for x in [(test_docx_1_path,test_author_1), (test_docx_2_path, test_author_2)]:
        doc = Document(x[0])
        doc.core_properties.author = x[1]
        doc.save(x[0])

    # Test author names match
    docx_1 = File(test_docx_1_path)
    docx_2 = File(test_docx_2_path)
    assert docx_1.metadata['author'] == test_author_1
    assert docx_2.metadata['author'] == test_author_2


def test_docx_last_modified_by():
    from file_processing.file import File
    from docx import Document

    # Paths of test files
    test_docx_1_path = 'tests/resources/test_files/HealthCanadaOverviewFromWikipedia.docx'
    test_docx_2_path = 'tests/resources/test_files/SampleReport.docx'

    # Arbitrary test last_modified_by names
    test_last_modified_by_1 = 'Test last_modified_by One'
    test_last_modified_by_2 = 'last_modified_by Test Author'

    # Update test docx files to have test names
    for x in [(test_docx_1_path,test_last_modified_by_1), (test_docx_2_path, test_last_modified_by_2)]:
        doc = Document(x[0])
        doc.core_properties.last_modified_by = x[1]
        doc.save(x[0])

    # Test last_modified_by names match
    docx_1 = File(test_docx_1_path)
    docx_2 = File(test_docx_2_path)
    assert docx_1.metadata['last_modified_by'] == test_last_modified_by_1
    assert docx_2.metadata['last_modified_by'] == test_last_modified_by_2


def test_pdf_ocr_text_found():
    from file_processing.file import File
    pdf_1 = File('tests/resources/test_files/SampleReportScreenShot.pdf', use_ocr=True)
    ocr_text = pdf_1.metadata['ocr_text']
    assert len(ocr_text) > 0

def test_msg_text():
    from file_processing.file import File
    msg = File('tests/resources/test_files/Test Email.msg')
    msg_text = msg.metadata['text']
    assert msg_text == 'Body text.\r\n\r\n \r\n\r\n'

def test_msg_subject():
    from file_processing.file import File
    msg = File('tests/resources/test_files/Test Email.msg')
    msg_subject = msg.metadata['subject']
    assert msg_subject == 'Test Email'

def test_msg_date():
    from file_processing.file import File
    msg = File('tests/resources/test_files/Test Email.msg')
    msg_date = msg.metadata['date']
    assert msg_date == 'Mon, 18 Sep 2023 13:57:16 -0400'

def test_msg_sender():
    from file_processing.file import File
    msg = File('tests/resources/test_files/Test Email.msg')
    msg_sender = msg.metadata['sender']
    assert msg_sender == '"Burnett, Taylen (HC/SC)" <Taylen.Burnett@hc-sc.gc.ca>'

def test_pptx_text():
    from file_processing.file import File
    pptx_1 = File('tests/resources/test_files/HealthCanadaOverviewFromWikipedia.pptx')
    pptx_2 = File('tests/resources/test_files/SampleReport.pptx')
    assert len(pptx_1.metadata['text']) == 1655
    assert len(pptx_2.metadata['text']) == 2037


def test_pptx_author():
    from file_processing.file import File
    from pptx import Presentation

    # Paths of test files
    test_pptx_1_path = 'tests/resources/test_files/HealthCanadaOverviewFromWikipedia.pptx'
    test_pptx_2_path = 'tests/resources/test_files/SampleReport.pptx'

    # Arbitrary test author names
    test_author_1 = 'Test Author One'
    test_author_2 = 'Second Test Author'

    # Update test pptx files to have test names
    for x in [(test_pptx_1_path,test_author_1), (test_pptx_2_path, test_author_2)]:
        ppt = Presentation(x[0])
        ppt.core_properties.author = x[1]
        ppt.save(x[0])

    # Test author names match
    pptx_1 = File(test_pptx_1_path)
    pptx_2 = File(test_pptx_2_path)
    assert pptx_1.metadata['author'] == test_author_1
    assert pptx_2.metadata['author'] == test_author_2


def test_pptx_last_modified_by():
    from file_processing.file import File
    from pptx import Presentation

    # Paths of test files
    test_pptx_1_path = 'tests/resources/test_files/HealthCanadaOverviewFromWikipedia.pptx'
    test_pptx_2_path = 'tests/resources/test_files/SampleReport.pptx'

    # Arbitrary test last_modified_by names
    test_last_modified_by_1 = 'Test last_modified_by One'
    test_last_modified_by_2 = 'last_modified_by Test Author'

    # Update test pptx files to have test names
    for x in [(test_pptx_1_path,test_last_modified_by_1), (test_pptx_2_path, test_last_modified_by_2)]:
        ppt = Presentation(x[0])
        ppt.core_properties.last_modified_by = x[1]
        ppt.save(x[0])

    # Test last_modified_by names match
    pptx_1 = File(test_pptx_1_path)
    pptx_2 = File(test_pptx_2_path)
    assert pptx_1.metadata['last_modified_by'] == test_last_modified_by_1
    assert pptx_2.metadata['last_modified_by'] == test_last_modified_by_2

def test_pptx_num_slides():
    from file_processing.file import File
    pptx_1 = File('tests/resources/test_files/HealthCanadaOverviewFromWikipedia.pptx')
    pptx_2 = File('tests/resources/test_files/SampleReport.pptx')
    assert pptx_1.metadata['num_slides'] == 4
    assert pptx_2.metadata['num_slides'] == 5