import PyPDF2

# def load_pdf(path):
#     text=""
#     reader = PyPDF2.PdfReader(path)
#     for page in reader:
#         text +=page.extact_text()
#     return text    

# def load_pdf(path):
#     try:
#         with open("data/handbook.txt", "r") as f:
#             return f.read()
#     except:
#         return "No data found"

def load_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "No Data found"
