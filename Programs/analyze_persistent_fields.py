import os
import re

def analyze_persistent_fields(file_path):
    """Extract and analyze Persistent Fields section from a businessclass file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract class name
        class_match = re.search(r'(\w+)\s+is\s+a\s+BusinessClass', content)
        class_name = class_match.group(1) if class_match else "Unknown"
        
        # Find Persistent Fields section
        persistent_match = re.search(r'Persistent Fields\s*\n(.*?)(?=\n\s*(?:Transient Fields|Local Fields|Derived Fields|Conditions|Relations|Sets|Field Rules|Actions|$))', content, re.DOTALL)
        
        if not persistent_match:
            return class_name, 0, []
        
        persistent_section = persistent_match.group(1)
        
        # Count fields and extract patterns
        field_lines = [line for line in persistent_section.split('\n') if line.strip() and not line.strip().startswith('States') and not line.strip().startswith('value is') and '\t\t' in line and 'is ' in line]
        
        field_count = len(field_lines)
        patterns = []
        
        for line in field_lines:
            line = line.strip()
            if 'delete ignored' in line:
                patterns.append('delete ignored')
            if 'default label' in line:
                patterns.append('default label')
            if 'is like' in line:
                patterns.append('is like')
            if 'group' in line:
                patterns.append('group')
            if 'States' in persistent_section and line in persistent_section:
                patterns.append('states')
        
        return class_name, field_count, list(set(patterns))
        
    except Exception as e:
        return os.path.basename(file_path), 0, [f"Error: {str(e)}"]

def main():
    directory = r"c:\Visual Basic Code\LPL Library\References\business class"
    results = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.businessclass'):
            file_path = os.path.join(directory, filename)
            class_name, field_count, patterns = analyze_persistent_fields(file_path)
            results.append((class_name, field_count, patterns))
    
    # Sort by field count descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Write analysis to output file
    output_path = r"c:\Visual Basic Code\LPL Library\Others\persistent_fields_analysis.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=== PERSISTENT FIELDS ANALYSIS ===\n\n")
        f.write(f"Total BusinessClass files analyzed: {len(results)}\n\n")
        
        # Summary statistics
        field_counts = [r[1] for r in results]
        f.write(f"Field count range: {min(field_counts)} - {max(field_counts)}\n")
        f.write(f"Average fields per class: {sum(field_counts) / len(field_counts):.1f}\n\n")
        
        # Top classes by field count
        f.write("=== TOP CLASSES BY FIELD COUNT ===\n")
        for class_name, field_count, patterns in results[:10]:
            f.write(f"{class_name}: {field_count} fields\n")
            if patterns:
                f.write(f"  Patterns: {', '.join(patterns)}\n")
        
        f.write("\n=== ALL CLASSES ===\n")
        for class_name, field_count, patterns in results:
            f.write(f"{class_name}: {field_count} fields")
            if patterns:
                f.write(f" - {', '.join(patterns)}")
            f.write("\n")
    
    print(f"Analysis complete. Results written to {output_path}")
    print(f"Analyzed {len(results)} BusinessClass files")

if __name__ == "__main__":
    main()