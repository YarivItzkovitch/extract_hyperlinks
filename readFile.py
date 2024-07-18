import fitz  # PyMuPDF
import re
import requests

def extract_hyperlinks_from_pdf(pdf_file):
    links = []
    try:
        doc = fitz.open(pdf_file)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            links_on_page = page.get_links()
            for link in links_on_page:
                if 'uri' in link:
                    # Link to an external URL
                    uri = link['uri']
                    text = page.get_textbox(link['from'])
                    links.append((text, uri))

        doc.close()
    except Exception as e:
        print(f"Error extracting hyperlinks from PDF: {str(e)}")

    return links

def download_pdf_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open('downloaded_pdf.pdf', 'wb') as f:
                f.write(response.content)
            return 'downloaded_pdf.pdf'
        else:
            print(f"Failed to download PDF from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to download PDF from {url}: {str(e)}")
        return None

if __name__ == "__main__":
    file_path_or_url = input("Enter the file path or URL: ")

    if file_path_or_url.startswith('http://') or file_path_or_url.startswith('https://'):
        pdf_file = download_pdf_from_url(file_path_or_url)
        if not pdf_file:
            print(f"Failed to download PDF from {file_path_or_url}")
            exit()
    else:
        pdf_file = file_path_or_url

    links = extract_hyperlinks_from_pdf(pdf_file)

    if links:
        print(f"Found {len(links)} external hyperlinks:")
        for text, link in links:
            print(f"Text: {text}, Link: {link}")
    else:
        print("No external hyperlinks found in the PDF.")
