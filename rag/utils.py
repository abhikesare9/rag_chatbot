import requests
from pypdf import PdfReader
import re

class Utils:
    def __init__(self):
        pass
    @staticmethod
    def download_pdf(url,save_path):
        response = requests.get(url)
        with open(save_path, 'wb') as f:
            f.write(response.content)

        
    @staticmethod
    def split_text(text):
        return [i for i in re.split('\n\n', text) if i.strip()]

    @staticmethod
    def load_pdf(file_path):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text



