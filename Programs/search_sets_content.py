import re

def search_sets_content(file_path):
    """Search for any Sets-related content in PurchaseOrder.businessclass"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Search for various patterns related to Sets
        patterns = [
            r'(?i)sets?\s*\n',
            r'(?i)sets?\s*$',
            r'(?i)^.*sets?.*$',
            r'set\s+exists',
            r'set\s*$',
            r'is\s+a\s+\w+\s+set'
        ]
        
        results = []
        
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                results.append(f"Pattern {i+1} '{pattern}': {len(matches)} matches")
                results.extend([f"  - {match}" for match in matches[:5]])  # Show first 5 matches
        
        # Look for section headers to understand file structure
        section_pattern = r'^(\w+(?:\s+\w+)*)\s*$'
        sections = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines[:200]):  # Check first 200 lines
            line = line.strip()
            if line and not line.startswith('\t') and not line.startswith(' '):
                if re.match(r'^[A-Z][a-zA-Z\s]*$', line):
                    sections.append(f"Line {line_num+1}: {line}")
        
        analysis = "=== SETS CONTENT SEARCH RESULTS ===\n\n"
        
        if results:
            analysis += "Sets-related matches found:\n"
            analysis += "\n".join(results) + "\n\n"
        else:
            analysis += "No Sets-related content found\n\n"
        
        analysis += "Major sections found in file:\n"
        analysis += "\n".join(sections[:20]) + "\n\n"  # Show first 20 sections
        
        # Search for specific LPL sections
        lpl_sections = ['Persistent Fields', 'Transient Fields', 'Local Fields', 'Context Fields', 
                       'Derived Fields', 'Relations', 'Conditions', 'Sets', 'Dimensions', 'Measures']
        
        found_sections = []
        for section in lpl_sections:
            if section in content:
                found_sections.append(section)
        
        analysis += f"LPL sections found: {', '.join(found_sections)}\n"
        
        return analysis
        
    except Exception as e:
        return f"Error: {str(e)}"

# Main execution
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\PurchaseOrder.businessclass"
result = search_sets_content(file_path)
print(result)

# Save analysis to output file
output_path = r"C:\Visual Basic Code\LPL Library\Outputs\PurchaseOrder_Sets_Search.txt"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"\nSearch results saved to: {output_path}")