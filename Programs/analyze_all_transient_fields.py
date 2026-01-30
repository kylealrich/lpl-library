import os
import re
from collections import defaultdict

def analyze_transient_fields(file_path):
    """Extract Transient Fields from a single LPL BusinessClass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        pattern = r'Transient Fields\s*\n(.*?)(?=\n\t[A-Z]|\\nLocal Fields|\\nContext Fields|\\nRule Blocks|\\nDerived Fields|\\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if not match:
            return []
        
        transient_section = match.group(1).strip()
        field_lines = transient_section.split('\n')
        fields = []
        
        for line in field_lines:
            if line.strip() and line.startswith('\t\t') and 'is' in line and not line.strip().startswith('derive'):
                parts = line.strip().split()
                if len(parts) >= 3 and parts[1] == 'is':
                    field_name = parts[0]
                    field_type = ' '.join(parts[2:])
                    fields.append({'name': field_name, 'type': field_type})
        
        return fields
    except:
        return []

def analyze_all_files():
    """Analyze all .businessclass files"""
    base_path = r"C:\Visual Basic Code\LPL Library\References\business class"
    results = {}
    total_files = 0
    files_with_transient = 0
    total_fields = 0
    
    for filename in os.listdir(base_path):
        if filename.endswith('.businessclass'):
            total_files += 1
            file_path = os.path.join(base_path, filename)
            class_name = filename.replace('.businessclass', '')
            fields = analyze_transient_fields(file_path)
            
            if fields:
                files_with_transient += 1
                total_fields += len(fields)
                results[class_name] = fields
    
    # Summary statistics
    print(f"=== TRANSIENT FIELDS ANALYSIS - ALL BUSINESSCLASS FILES ===")
    print(f"Total files analyzed: {total_files}")
    print(f"Files with Transient Fields: {files_with_transient}")
    print(f"Files without Transient Fields: {total_files - files_with_transient}")
    print(f"Total Transient Fields found: {total_fields}")
    
    # Field count distribution
    field_counts = defaultdict(int)
    for class_name, fields in results.items():
        field_counts[len(fields)] += 1
    
    print(f"\nField Count Distribution:")
    for count in sorted(field_counts.keys()):
        print(f"  {count} fields: {field_counts[count]} classes")
    
    # Top classes by field count
    print(f"\nTop 20 Classes by Transient Field Count:")
    sorted_classes = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)
    for i, (class_name, fields) in enumerate(sorted_classes[:20], 1):
        print(f"{i:2d}. {class_name:<40} ({len(fields)} fields)")
    
    # Save detailed results
    output_path = r"C:\Visual Basic Code\LPL Library\Outputs\all_transient_fields_analysis.txt"
    with open(output_path, 'w') as f:
        f.write("=== COMPLETE TRANSIENT FIELDS ANALYSIS ===\\n\\n")
        f.write(f"Statistics:\\n")
        f.write(f"- Total BusinessClass files: {total_files}\\n")
        f.write(f"- Files with Transient Fields: {files_with_transient} ({files_with_transient/total_files*100:.1f}%)\\n")
        f.write(f"- Total Transient Fields: {total_fields}\\n\\n")
        
        f.write("DETAILED BREAKDOWN:\\n\\n")
        for class_name, fields in sorted_classes:
            f.write(f"{class_name} ({len(fields)} fields):\\n")
            for field in fields:
                f.write(f"  - {field['name']}: {field['type']}\\n")
            f.write("\\n")
    
    print(f"\nDetailed analysis saved to: {output_path}")
    return results

# Execute analysis
analyze_all_files()