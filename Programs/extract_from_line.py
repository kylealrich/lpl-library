def extract_set_action_from_line(file_path, start_line):
    """Extract Set Action content starting from a specific line number"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return "File not found"
    
    # Start from the specified line (convert to 0-based index)
    start_idx = start_line - 1
    
    if start_idx >= len(lines):
        return "Line number out of range"
    
    # Extract content starting from the Set Action line
    content_lines = []
    in_set_action = False
    indent_level = None
    
    for i in range(start_idx, len(lines)):
        line = lines[i]
        
        # Check if we're starting the Set Action
        if 'JournalizeTransactions is a Set Action' in line:
            in_set_action = True
            content_lines.append(line)
            # Determine the base indentation level
            indent_level = len(line) - len(line.lstrip())
            continue
        
        if in_set_action:
            # Check if we've reached the end of the Set Action
            # This happens when we encounter a line with same or less indentation that starts a new section
            current_indent = len(line) - len(line.lstrip())
            
            # If line is not empty and has same or less indentation, check if it's a new section
            if line.strip() and current_indent <= indent_level:
                # Check if this line starts a new major section
                if any(keyword in line for keyword in ['Create Rules', 'Create Exit Rules', 'Action Exit Rules', 'Field Groups']):
                    break
            
            content_lines.append(line)
            
            # Safety check - stop after reasonable number of lines
            if len(content_lines) > 2000:
                break
    
    return ''.join(content_lines)

def analyze_set_action_structure(content):
    """Analyze the structure of the Set Action content"""
    
    sections = {}
    current_section = None
    section_content = []
    
    lines = content.split('\n')
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            if current_section:
                section_content.append(line)
            continue
        
        # Check for major section headers
        section_keywords = [
            'Parameters', 'Queue Mapping Fields', 'Parameter Rules', 
            'Local Fields', 'Instance Selection', 'Sort Order', 
            'Accumulators', 'Action Rules', 'Set Rules'
        ]
        
        is_section_header = False
        for keyword in section_keywords:
            if stripped.startswith(keyword):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(section_content)
                
                # Start new section
                current_section = keyword
                section_content = [line]
                is_section_header = True
                break
        
        if not is_section_header and current_section:
            section_content.append(line)
    
    # Save the last section
    if current_section:
        sections[current_section] = '\n'.join(section_content)
    
    return sections

# Main execution
if __name__ == "__main__":
    file_path = r"c:\lpl-library\References\business class\GLTransactionDetail.busclass"
    start_line = 2837  # Line where JournalizeTransactions is found
    
    print(f"Extracting Set Action content starting from line {start_line}...")
    
    content = extract_set_action_from_line(file_path, start_line)
    
    if isinstance(content, str) and content.startswith("File not found"):
        print(f"Error: {content}")
    else:
        print(f"Extracted {len(content.split())} lines of content")
        
        # Analyze structure
        sections = analyze_set_action_structure(content)
        
        # Save to file
        with open(r"c:\lpl-library\Outputs\journalize_transactions_complete.txt", 'w', encoding='utf-8') as f:
            f.write("COMPLETE JOURNALIZE TRANSACTIONS SET ACTION\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("RAW CONTENT:\n")
            f.write("-" * 40 + "\n")
            f.write(content)
            f.write("\n\n")
            
            f.write("STRUCTURED ANALYSIS:\n")
            f.write("-" * 40 + "\n")
            
            for section_name, section_content in sections.items():
                f.write(f"\n{section_name.upper()}:\n")
                f.write("=" * len(section_name) + "\n")
                f.write(section_content)
                f.write("\n")
        
        print("Complete analysis saved to: c:\\lpl-library\\Outputs\\journalize_transactions_complete.txt")
        
        print(f"\nSections found: {list(sections.keys())}")
        
        # Show first few lines of content
        content_lines = content.split('\n')
        print(f"\nFirst 10 lines of extracted content:")
        for i, line in enumerate(content_lines[:10]):
            print(f"{start_line + i}: {line}")