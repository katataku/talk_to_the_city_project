import requests
import pandas as pd
import re
from typing import List, Dict
import os
from urllib.parse import urlparse
from tqdm import tqdm
import logging
import pypdf

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PDFProcessor:
    def __init__(self):
        self.headers = {}

    def download_pdf(self, url: str, save_path: str) -> bool:
        try:
            response = requests.get(url, headers=self.headers, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=f'Downloading {os.path.basename(save_path)}')

            with open(save_path, 'wb') as file:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    progress_bar.update(size)
            
            progress_bar.close()
            logging.info(f"Successfully downloaded PDF to {save_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error downloading PDF: {str(e)}")
            return False

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            text = ""
            reader = pypdf.PdfReader(pdf_path)
            for page in tqdm(reader.pages, desc="Extracting text from PDF"):
                text += page.extract_text() or ""
            return text
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {str(e)}")
            return ""

    def parse_content(self, content: str) -> List[Dict]:
        try:
            entries = re.split(r'●受付番号\s+\d+', content)[1:]
            receipt_numbers = re.findall(r'●受付番号\s+(\d+)', content)
            
            parsed_data = []
            for i, (entry, receipt_num) in enumerate(tqdm(zip(entries, receipt_numbers), total=len(entries), desc="Parsing entries")):
                parsed_data.append({
                    '受付番号': receipt_num,
                    '内容': entry.strip()
                })
                
            logging.info(f"Successfully parsed {len(parsed_data)} entries")
            return parsed_data
            
        except Exception as e:
            logging.error(f"Error parsing content: {str(e)}")
            return []

    def save_to_csv(self, data: List[Dict], output_file: str):
        try:
            df = pd.DataFrame(data)
            df.to_csv(output_file, index=False, encoding='utf-8')
            logging.info(f"Successfully saved data to {output_file}")
        except Exception as e:
            logging.error(f"Error saving to CSV: {str(e)}")

    def process_urls(self, urls: List[str], output_dir: str = "output"):
        os.makedirs(output_dir, exist_ok=True)
        all_data = []

        for i, url in enumerate(urls, 1):
            pdf_name = f"doc_{i}.pdf"
            pdf_path = os.path.join(output_dir, pdf_name)
            
            if self.download_pdf(url, pdf_path):
                content = self.extract_text_from_pdf(pdf_path)
                if content.strip():
                    parsed_data = self.parse_content(content)
                    all_data.extend(parsed_data)
                    
                    # Optional: Remove PDF after processing
                    os.remove(pdf_path)
                    
        if all_data:
            output_csv = os.path.join(output_dir, "combined_output.csv")
            self.save_to_csv(all_data, output_csv)

def main():
    processor = PDFProcessor()
    
    with open('pdf_path.txt', 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    try:
        processor.process_urls(urls)
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        
if __name__ == "__main__":
    main()