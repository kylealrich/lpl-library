import os
import re
from collections import defaultdict

def extract_context_fields(file_path):
    """Extract Context Fields from a single businessclass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find Context Fields section
        context_match = re.search(r'Context Fields\s*\n(.*?)(?=\n[A-Z][a-zA-Z\s]*Fields|\nend|\Z)', content, re.DOTALL)
        
        if not context_match:
            return []
        
        context_section = context_match.group(1).strip()
        lines = context_section.split('\n')
        fields = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('\t') and not line.startswith('//') and 'is' in line:
                if re.match(r'^[A-Za-z][A-Za-z0-9_]*\s+is\s+', line):
                    parts = line.split('is', 1)
                    if len(parts) == 2:
                        field_name = parts[0].strip()
                        field_type = parts[1].strip()
                        fields.append({'name': field_name, 'type': field_type})
        
        return fields
        
    except Exception:
        return []

def analyze_all_context_fields():
    """Analyze Context Fields across all businessclass files"""
    base_path = r"C:\Visual Basic Code\LPL Library\References\business class"
    
    results = []
    field_type_counts = defaultdict(int)
    total_files = 0
    files_with_context = 0
    total_context_fields = 0
    
    # Process all .businessclass files
    for filename in os.listdir(base_path):
        if filename.endswith('.businessclass'):
            total_files += 1
            file_path = os.path.join(base_path, filename)
            fields = extract_context_fields(file_path)
            
            if fields:
                files_with_context += 1
                total_context_fields += len(fields)
                results.append({
                    'filename': filename,
                    'field_count': len(fields),
                    'fields': fields
                })
                
                # Count field types
                for field in fields:
                    base_type = field['type'].split()[0]
                    field_type_counts[base_type] += 1
    
    # Sort results by field count (descending)
    results.sort(key=lambda x: x['field_count'], reverse=True)
    
    return {
        'total_files': total_files,
        'files_with_context': files_with_context,
        'total_context_fields': total_context_fields,
        'results': results,
        'field_type_counts': dict(field_type_counts)
    }

# Run analysis
print("Analyzing Context Fields across all BusinessClass files...")
analysis = analyze_all_context_fields()

# Display summary
print(f"\nCONTEXT FIELDS ANALYSIS - ALL BUSINESSCLASS FILES")
print(f"Total BusinessClass files: {analysis['total_files']}")
print(f"Files with Context Fields: {analysis['files_with_context']} ({analysis['files_with_context']/analysis['total_files']*100:.1f}%)")
print(f"Total Context Fields: {analysis['total_context_fields']}")

print(f"\nTop 20 Classes by Context Field Count:")
for i, result in enumerate(analysis['results'][:20]):
    print(f"{i+1:2d}. {result['filename']:<40} ({result['field_count']} fields)")

print(f"\nField Type Distribution:")
sorted_types = sorted(analysis['field_type_counts'].items(), key=lambda x: x[1], reverse=True)
for field_type, count in sorted_types[:15]:
    print(f"  {field_type:<20}: {count}")

# Save detailed results
output_file = r"C:\Visual Basic Code\LPL Library\Outputs\All_Context_Fields_Analysis.txt"
with open(output_file, 'w') as f:
    f.write("COMPREHENSIVE CONTEXT FIELDS ANALYSIS\n")
    f.write("====================================\n\n")
    f.write(f"Total BusinessClass files: {analysis['total_files']}\n")
    f.write(f"Files with Context Fields: {analysis['files_with_context']} ({analysis['files_with_context']/analysis['total_files']*100:.1f}%)\n")
    f.write(f"Total Context Fields: {analysis['total_context_fields']}\n\n")
    
    f.write("COMPLETE RESULTS BY FILE:\n")
    for result in analysis['results']:
        f.write(f"\n{result['filename']} ({result['field_count']} fields):\n")
        for field in result['fields']:
            f.write(f"  {field['name']} is {field['type']}\n")

print(f"\nDetailed analysis saved to: {output_file}")