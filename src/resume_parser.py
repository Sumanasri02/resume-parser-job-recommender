# take a resume pdf -> convert it into usable text -> extract contact details
import pdfplumber #read text from PDF
import re #Regex library (used for email & phone detection)

def extract_text_from_pdf(pdf_path: str) -> str:
    #text- plan text - becomes all future NLP task
    text = "" #an empty str to store resume content
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
          for page in pdf.pages:
            # Resumes can be multi-page , no data loss
            page_text = page.extract_text() #extract readable-page from each page, rtn none if page no text
            if page_text:
                text += page_text + "\n" #append only valid text
    except Exception as e:
        raise RuntimeError(f"Error reading PDF file: {e}")
            
    text = re.sub(r'\s+' , ' ', text)
    return text.strip()  #remove spaces/ line break, Converts text into clean NLP-ready format

#3. extract email
def extract_email(text: str):
    #Find the first valid email address from resume text.
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, text) # Scans entire resume text, returns a list of all emails found
    return emails[0] if emails else None
# 4. extract phome
def extract_phone(text: str):
    #Extract candidate phone number from messy resume text.
    phone_pattern = r'(\+?\d{1,3}[\s-]?)?\d{10}'
    phones = re.findall(phone_pattern, text) #Checks if phone-like patterns exist
    match = re.search(phone_pattern, text)
    return match.group() if match else None # returns actual matched number, ignores partial or invalid matches


def main():
    pdf_path = "resumes\Sumanasri_k_Resume.pdf"
    print("Loading Resume..\n")
    
    resume_text = extract_text_from_pdf(pdf_path)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    
    print("Resume parsed successfully\n")
    print(f"Extracted Email: {email}")
    print(f"Extracted Phone: {phone}")

if __name__ == "__main__":
    main()