import pdfplumber
import re
from collections import Counter
resume_path = "AISHVARYA_Testing_Resume.pdf"
job_path = "job.pdf"
stopwords = set([
    "a", "an", "the", "and", "or", "but", "if", "in", "on", "with",
    "for", "to", "from", "by", "of", "at", "as", "is", "are", "this",
    "that", "these", "those", "you", "your", "it", "its", "be", "was",
    "were", "will", "can", "has", "have", "not", "we", "they", "i",
    "my", "our", "so", "such", "like"
])

def read_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text
print("Reading files...")
resume_text = read_pdf(resume_path).lower()
job_text = read_pdf(job_path).lower()
resume_words_list = [word for word in re.findall(r"[a-zA-Z]+", resume_text) if word not in stopwords]
job_words_list = [word for word in re.findall(r"[a-zA-Z]+", job_text) if word not in stopwords]
resume_counter = Counter(resume_words_list)
job_counter = Counter(job_words_list)
matched_keywords = []
missing_keywords = []
for word in set(job_counter.keys()):
    if word in resume_counter:
        matched_keywords.append(word)
    else:
        missing_keywords.append(word)

matched_count = sum(resume_counter[word] for word in matched_keywords)
total_job_count = sum(job_counter.values())
ats_score = (matched_count / total_job_count) * 100
print("\n ATS Summary ")
print(f"Total important keywords in job description : {len(job_counter)}")
print(f"Keywords matched in resume                 : {len(matched_keywords)}")
print(f"Keywords missing in resume                 : {len(missing_keywords)}")
print(f"Weighted ATS score                         : {ats_score:.2f}%")

print("\n Include the following keywords to improve your resume:")
print(", ".join(sorted(missing_keywords)))

