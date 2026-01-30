import PyPDF2

def list_all_content_sections(pdf_path):
    """List all content sections from PDF file"""
    sections = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                lines = text.split('\n')
                
                for line_num, line in enumerate(lines):
                    line = line.strip()
                    if len(line) > 5 and len(line) < 100:  # Reasonable section title length
                        sections.append(f"Page {page_num}, Line {line_num + 1}: {line}")
        
        return sections
    
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# Main execution
if __name__ == "__main__":
    pdf_file = r"C:\Visual Basic Code\LPL Library\References\inforlandmarkconfigurationconsolelpl.pdf"
    output_file = r"C:\Visual Basic Code\LPL Library\Outputs\pdf_all_sections.txt"
    
    sections = list_all_content_sections(pdf_file)
    
    if sections:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("ALL PDF CONTENT SECTIONS\n")
            f.write("=" * 50 + "\n\n")
            for section in sections:
                f.write(f"{section}\n")
        
        print(f"Found {len(sections)} content sections")
        print(f"Complete list saved to: {output_file}")
        
        # Show first 50 sections
        for section in sections[:50]:
            print(section)
        if len(sections) > 50:
            print(f"... and {len(sections) - 50} more sections")
    else:
        print("Failed to list sections from PDF")