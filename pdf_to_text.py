from tika import parser # pip install tika
from os import listdir
from os.path import isfile, join
from io import StringIO
from bs4 import BeautifulSoup


def parse_pdf(pdf_folder):
    pdf_texts = []
    texts_folder = 'texts/'
    pdf_docs = [f for f in listdir(pdf_folder) if isfile(join(pdf_folder, f))]
    i = 0
    for pdf in pdf_docs:
        _buffer = StringIO()
        data = parser.from_file(pdf_folder+'/'+pdf, xmlContent=True)
        xhtml_data = BeautifulSoup(data['content'], features="html.parser")
        for page, content in enumerate(xhtml_data.find_all('div', attrs={'class': 'page'})):
            print('Parsing page {} of pdf file...{}'.format(page + 1, pdf))
            _buffer.write(str(content))
            parsed_content = parser.from_buffer(_buffer.getvalue())
            _buffer.truncate()
            content = parsed_content['content'].encode('utf-8', errors='ignore')
            content = str(content).replace("\n", "").replace("\\", "")
            pdf_texts.append(content)
            print(content, file=open(texts_folder + str(i) + '.txt', 'w'))
            i += 1
    return pdf_texts
