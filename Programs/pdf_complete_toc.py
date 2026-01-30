import PyPDF2

def extract_complete_toc(pdf_path):
    """Extract complete Table of Contents from PDF file"""
    toc_entries = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Search all pages for TOC content
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                if "Contents" in text:
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and len(line) > 5:
                            toc_entries.append(f"Page {page_num + 1}: {line}")
        
        return toc_entries
    
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# Main execution
if __name__ == "__main__":
    pdf_file = r"C:\Visual Basic Code\LPL Library\References\inforlandmarkconfigurationconsolelpl.pdf"
    output_file = r"C:\Visual Basic Code\LPL Library\Outputs\pdf_complete_toc.txt"
    
    toc = extract_complete_toc(pdf_file)
    
    if toc:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("COMPLETE TABLE OF CONTENTS\n")
            f.write("=" * 60 + "\n\n")
            for entry in toc:
                f.write(f"{entry}\n")
        
        print(f"Extracted {len(toc)} TOC entries")
        print(f"Complete TOC saved to: {output_file}")
    else:
        print("Failed to extract complete TOC")