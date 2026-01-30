import PyPDF2
import re

def extract_table_of_contents(pdf_path):
    """Extract Table of Contents from PDF file"""
    toc_entries = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Look for TOC in first few pages
            for page_num in range(min(10, len(pdf_reader.pages))):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                if "Contents" in text or "Table of Contents" in text:
                    lines = text.split('\n')
                    in_toc = False
                    
                    for line in lines:
                        line = line.strip()
                        
                        if "Contents" in line:
                            in_toc = True
                            continue
                            
                        if in_toc and line:
                            # Look for lines with page numbers
                            if re.search(r'\d+$', line) or '...' in line:
                                toc_entries.append(line)
                            elif len(line) > 3 and not line.isdigit():
                                toc_entries.append(line)
        
        return toc_entries
    
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# Main execution
if __name__ == "__main__":
    pdf_file = r"C:\Visual Basic Code\LPL Library\References\inforlandmarkconfigurationconsolelpl.pdf"
    output_file = r"C:\Visual Basic Code\LPL Library\Outputs\pdf_table_of_contents.txt"
    
    toc = extract_table_of_contents(pdf_file)
    
    if toc:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("TABLE OF CONTENTS\n")
            f.write("=" * 50 + "\n\n")
            for entry in toc:
                f.write(f"{entry}\n")
        
        print("Table of Contents:")
        for entry in toc:
            print(entry)
        print(f"\nSaved to: {output_file}")
    else:
        print("Failed to extract Table of Contents")