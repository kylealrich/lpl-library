import PyPDF2
import re

def list_pdf_sections(pdf_path):
    """List all sections from PDF file"""
    sections = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                
                # Find section headers (lines that start with numbers or are in caps)
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (re.match(r'^\d+\.', line) or 
                               re.match(r'^[A-Z][A-Z\s]+$', line) or
                               re.match(r'^Chapter \d+', line, re.IGNORECASE)):
                        sections.append(f"Page {page_num}: {line}")
        
        return sections
    
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def save_section_list(sections, output_path):
    """Save section list to output file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("PDF SECTIONS LIST\n")
        f.write("=" * 50 + "\n\n")
        for section in sections:
            f.write(f"{section}\n")

# Main execution
if __name__ == "__main__":
    pdf_file = r"C:\Visual Basic Code\LPL Library\References\inforlandmarkconfigurationconsolelpl.pdf"
    output_file = r"C:\Visual Basic Code\LPL Library\Outputs\pdf_sections_list.txt"
    
    sections = list_pdf_sections(pdf_file)
    
    if sections:
        save_section_list(sections, output_file)
        print(f"Found {len(sections)} sections:")
        for section in sections[:20]:  # Show first 20 sections
            print(section)
        if len(sections) > 20:
            print(f"... and {len(sections) - 20} more sections")
        print(f"\nComplete list saved to: {output_file}")
    else:
        print("Failed to list sections from PDF")