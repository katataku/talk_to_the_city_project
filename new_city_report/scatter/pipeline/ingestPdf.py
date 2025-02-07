import requests
import pandas as pd
import re
from typing import List, Dict
import os
from urllib.parse import urlparse
from tqdm import tqdm
import logging
import pdfplumber  

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PDFProcessor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def download_pdf(self, url: str, save_path: str) -> bool:
        try:
            response = requests.get(url, headers=self.headers, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            progress_bar = tqdm(
                total=total_size,
                unit='iB',
                unit_scale=True,
                desc=f'Downloading {os.path.basename(save_path)}'
            )

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
            with pdfplumber.open(pdf_path) as pdf:
                for page in tqdm(pdf.pages, desc="Extracting text from PDF"):
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {str(e)}")
            return ""

    def parse_content(self, content: str) -> List[Dict]:
        try:
            entries = re.split(r'●受付番号\s+\d+', content)[1:]  # 跳过第一个空分割
            receipt_numbers = re.findall(r'●受付番号\s+(\d+)', content)
            
            parsed_data = []
            
            for i, (entry, receipt_num) in enumerate(tqdm(
                zip(entries, receipt_numbers),
                total=len(entries),
                desc="Parsing entries"
            )):
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

def main():
    processor = PDFProcessor()

    pdf_url = "YOUR_PDF_URL_HERE"  # 替换为实际的PDF URL
    pdf_save_path = "downloaded.pdf"
    csv_output = "output.csv"
    
    try:
        if not processor.download_pdf(pdf_url, pdf_save_path):
            logging.error("Failed to download PDF")
            return
            
        content = processor.extract_text_from_pdf(pdf_save_path)
        if not content.strip():
            logging.error("No text extracted from PDF")
            return
            
        parsed_data = processor.parse_content(content)
        if not parsed_data:
            logging.error("No data parsed")
            return
            
        processor.save_to_csv(parsed_data, csv_output)
        
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        
if __name__ == "__main__":
    main()