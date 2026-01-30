import re

def analyze_sets_section(file_path):
    """Extract and analyze Sets section from PurchaseOrder.businessclass"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Search for Sets section with better pattern matching
        # Look for "Sets" at start of line followed by content until next major section
        sets_pattern = r'^\s*Sets\s*\n(.*?)(?=^\s*\w+\s*Fields|^\s*Conditions|^\s*Relations|^\s*Dimensions|^\s*Measures|^\s*Rule\s+Blocks|^\s*Derived\s+Fields|\Z)'
        sets_match = re.search(sets_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not sets_match:
            # Try alternative pattern - look for any mention of Sets
            alt_pattern = r'Sets.*?\n'
            alt_matches = re.findall(alt_pattern, content, re.IGNORECASE)
            if alt_matches:
                return f"Sets section pattern found but couldn't parse: {alt_matches[:3]}..."
            else:
                return "No Sets section found in PurchaseOrder.businessclass"
        
        sets_content = sets_match.group(1).strip()
        
        if not sets_content:
            return "Sets section exists but is empty"
        
        # Parse individual sets
        sets = []
        lines = sets_content.split('\n')
        current_set = None
        
        for line in lines:
            line = line.rstrip()
            if not line:
                continue
                
            # Set definition (starts at column 1, no leading tabs)
            if not line.startswith('\t') and line.strip():
                if current_set:
                    sets.append(current_set)
                current_set = {'name': line.strip(), 'properties': []}
            
            # Set properties (indented with tabs)
            elif line.startswith('\t') and current_set:
                current_set['properties'].append(line.strip())
        
        if current_set:
            sets.append(current_set)
        
        # Generate analysis
        analysis = f"=== PURCHASEORDER SETS ANALYSIS ===\n\n"
        analysis += f"Total Sets Found: {len(sets)}\n\n"
        
        if sets:
            for i, set_def in enumerate(sets, 1):
                analysis += f"{i}. {set_def['name']}\n"
                for prop in set_def['properties']:
                    analysis += f"   {prop}\n"
                analysis += "\n"
        else:
            analysis += "Raw Sets content:\n"
            analysis += sets_content[:500] + "..." if len(sets_content) > 500 else sets_content
        
        return analysis
        
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"

# Main execution
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\PurchaseOrder.businessclass"
result = analyze_sets_section(file_path)
print(result)

# Save analysis to output file
output_path = r"C:\Visual Basic Code\LPL Library\Outputs\PurchaseOrder_Sets_Analysis.txt"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"\nAnalysis saved to: {output_path}")