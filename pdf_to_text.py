from tika import parser # pip install tika
from os import listdir
from os.path import isfile, join


def parse_pdf(pdf_folder):
    pdf_texts = []
    pdf_docs = [f for f in listdir(pdf_folder) if isfile(join(pdf_folder, f))]
    for pdf in pdf_docs:
        parsed = parser.from_file(pdf)
        pdf_texts.append(parsed['content'])
    return pdf_texts
