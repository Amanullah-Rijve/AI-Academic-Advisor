import PyPDF2

def load_pdf(path):
    text=""
    reader = PyPDF2.PdfReader(path)
    for page in reader:
        text +=page.extact_text()
    return text    

