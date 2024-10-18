import openai
import PyPDF2
import requests
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key ='sk-proj-gjnNCzC9won47DEA66RiT3BlbkFJSYmfEEs3dIVUZikUBVhS'


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": """use your own knowledge. You are a master in Verification of Answer given by a llm agent against the question"""},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()


def verify_from_document(question, answer, document_text):
    # Truncate document text if too long
    document_text_truncated = document_text[:500] + "..." if len(document_text) > 500 else document_text

    prompt = f"""
    Question: {question}
    Answer: {answer}
    Based on the following document, is the answer correct? Provide a detailed explanation.
    Document: {document_text_truncated}
    """
    return ask_openai(prompt)


def search_web(question):
    search_url = f"https://www.google.com/search?q={question.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract relevant information from the web search results
        web_text = soup.get_text()  # This needs to be improved
        return web_text
    except requests.RequestException as e:
        print(f"Error during web search: {e}")
        return ""


def verify_from_web(question, answer, web_text):
    prompt = f"""
    Question: {question}
    Answer: {answer}
    Based on the following web search results, is the answer correct? Provide a detailed explanation.Keep the search related to the pdf given.Do not include unnecessary results that is not related to the pdf given.
    Web Search Results: {web_text}... (truncated for brevity)
    """
    return ask_openai(prompt)

def ask_openai_for_final_verdict(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": """You are an advanced AI language model tasked with verifying the accuracy of a given answer with respect to the given question. Provide the final verdict based on your examination of the document, web search, and your own knowledge.

If the answer is correct, state "Final Verdict: Correct".
If the answer is incorrect, state "Final Verdict: Incorrect"""},
            {"role": "user", "content": prompt}
        ],
        max_tokens=5000
    )
    return response.choices[0].message['content'].strip()

def question_answer_critic(file_path, question, answer):
    document_text = extract_text_from_pdf(file_path)

    # Verify from document
    doc_verification = verify_from_document(question, answer, document_text)

    # Verify from web
    web_text = search_web(question)
    web_verification = verify_from_web(question, answer, web_text)

    # AI Knowledge Verification
    ai_verification = ask_openai(f"Question: {question}\nAnswer: {answer}\nBased on the given question and answer, is the answer correct?")

    # Determine final verdict based on document, web, and AI verifications
    # Final Verdict
    final_verdict = ask_openai_for_final_verdict(f"Document Verification: {doc_verification}\nWeb Verification: {web_verification}\nAI Knowledge Verification: {ai_verification}\nBased on the verification process, is the answer correct or incorrect? Reply in one word")


    print(final_verdict)

    # Ask the user if they want verification details and explanation
    if input("Do you want to see the verification details and explanation? (yes/no): ").lower() == "yes":
        print("Verification Details:")
        print("\nDocument Verification:")
        print(doc_verification.split("Explanation:")[0].strip())
        print("\nWeb Verification:")
        print(web_verification.split("Web Feedback:")[0].strip())
        print("\nAI Knowledge Verification:")
        print(ai_verification)




# Example usage
# file_path = "path/to/your/document.pdf"
# question = "What is the capital of France?"
# answer = "Paris"
# result = question_answer_critic(file_path, question, answer)
# print(result)