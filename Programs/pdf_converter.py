import PyPDF2
import os

def convert_pdf_to_text(pdf_path, output_path):
    """Extract text from PDF and save to text file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = []
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                text_content.append(f"=== PAGE {page_num} ===\n{text}\n")
            
            # Save to text file
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write('\n'.join(text_content))
            
            print(f"Successfully converted PDF to text: {output_path}")
            print(f"Total pages processed: {len(pdf_reader.pages)}")
            
    except Exception as e:
        print(f"Error converting PDF: {e}")

if __name__ == "__main__":
    pdf_file = r"C:\Visual Basic Code\LPL Library\References\inforlandmarkconfigurationconsolelpl.pdf"
    output_file = r"C:\Visual Basic Code\LPL Library\Outputs\inforlandmarkconfigurationconsolelpl.txt"
    
    convert_pdf_to_text(pdf_file, output_file)