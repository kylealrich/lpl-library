import os
import re

def analyze_context_fields(file_path):
    """Analyze Context Fields section in a businessclass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract class name
        class_match = re.search(r'(\w+)\s+is\s+a\s+BusinessClass', content)
        class_name = class_match.group(1) if class_match else "Unknown"
        
        # Find Context Fields section
        context_match = re.search(r'\n\s*Context Fields\s*\n(.*?)(?=\n\s*(?:Local Fields|Rule Blocks|Derived Fields|Transient Fields|Persistent Fields|Relations|Sets|Field Rules|Conditions|Actions|$))', content, re.DOTALL)
        
        if not context_match:
            return f"**{class_name}:** No Context Fields section found"
        
        context_content = context_match.group(1).strip()
        if not context_content:
            return f"**{class_name}:** Context Fields section exists but is empty"
        
        # Count fields and extract field names
        field_lines = [line.strip() for line in context_content.split('\n') if line.strip() and not line.strip().startswith('#')]
        field_names = []
        
        for line in field_lines:
            # Extract field name (first word before 'is' or standalone)
            field_match = re.match(r'\s*(\w+)', line)
            if field_match:
                field_names.append(field_match.group(1))
        
        field_count = len(field_names)
        fields_list = ", ".join(field_names) if field_names else "None"
        
        return f"**{class_name}:** {field_count} fields - {fields_list}"
        
    except Exception as e:
        return f"**Error analyzing {os.path.basename(file_path)}:** {str(e)}"

def main():
    """Analyze all .businessclass files in the References directory"""
    base_dir = r"C:\Visual Basic Code\LPL Library\References"
    results = []
    
    # Find all .businessclass files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.businessclass'):
                file_path = os.path.join(root, file)
                result = analyze_context_fields(file_path)
                results.append(result)
    
    # Sort results and write to output
    results.sort()
    
    output_path = r"C:\Visual Basic Code\LPL Library\Outputs\context_fields_analysis.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=== CONTEXT FIELDS ANALYSIS - ALL BUSINESSCLASS FILES ===\n\n")
        for result in results:
            f.write(result + "\n")
        f.write(f"\n=== SUMMARY ===\n")
        f.write(f"Total files analyzed: {len(results)}\n")
    
    print(f"Analysis complete. Results written to: {output_path}")
    print(f"Total files analyzed: {len(results)}")

if __name__ == "__main__":
    main()