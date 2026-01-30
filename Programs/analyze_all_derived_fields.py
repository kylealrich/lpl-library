import os
import re
from collections import defaultdict

def analyze_derived_fields(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        match = re.search(r'Derived Fields\s*\n(.*?)(?=\n\w|\nend|\Z)', content, re.DOTALL)
        if not match:
            return []
        
        derived_section = match.group(1)
        fields = []
        field_pattern = r'^\t\t(\w+)\s+is\s+a\s+(\w+)'
        
        for line in derived_section.split('\n'):
            field_match = re.match(field_pattern, line)
            if field_match:
                fields.append({'name': field_match.group(1), 'type': field_match.group(2)})
        
        return fields
    except:
        return []

# Analyze all .businessclass files
root_dir = r"C:\Visual Basic Code\LPL Library\References\business class"
results = {}
type_counts = defaultdict(int)
total_files = 0
files_with_derived = 0
total_derived_fields = 0

for filename in os.listdir(root_dir):
    if filename.endswith('.businessclass'):
        total_files += 1
        file_path = os.path.join(root_dir, filename)
        fields = analyze_derived_fields(file_path)
        
        if fields:
            files_with_derived += 1
            results[filename] = fields
            total_derived_fields += len(fields)
            
            for field in fields:
                type_counts[field['type']] += 1

# Sort by field count
sorted_results = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)

# Output analysis
print(f"=== COMPREHENSIVE DERIVED FIELDS ANALYSIS ({total_files} files) ===\n")
print(f"Statistics:")
print(f"- Total BusinessClass files: {total_files}")
print(f"- Files with Derived Fields: {files_with_derived} ({files_with_derived/total_files*100:.1f}%)")
print(f"- Files without Derived Fields: {total_files-files_with_derived} ({(total_files-files_with_derived)/total_files*100:.1f}%)")
print(f"- Total Derived Fields found: {total_derived_fields}")

print(f"\nField Type Distribution:")
for field_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"- {field_type}: {count} fields ({count/total_derived_fields*100:.1f}%)")

print(f"\nTop 20 Complex Classes (Most Derived Fields):")
for i, (filename, fields) in enumerate(sorted_results[:20], 1):
    class_name = filename.replace('.businessclass', '')
    print(f"{i:2d}. {class_name} ({len(fields)} fields)")

# Save detailed results
with open(r"C:\Visual Basic Code\LPL Library\Outputs\All_Derived_Fields_Analysis.txt", 'w') as f:
    f.write(f"=== COMPREHENSIVE DERIVED FIELDS ANALYSIS ({total_files} files) ===\n\n")
    f.write(f"Statistics:\n")
    f.write(f"- Total BusinessClass files: {total_files}\n")
    f.write(f"- Files with Derived Fields: {files_with_derived} ({files_with_derived/total_files*100:.1f}%)\n")
    f.write(f"- Files without Derived Fields: {total_files-files_with_derived} ({(total_files-files_with_derived)/total_files*100:.1f}%)\n")
    f.write(f"- Total Derived Fields found: {total_derived_fields}\n\n")
    
    f.write(f"Field Type Distribution:\n")
    for field_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        f.write(f"- {field_type}: {count} fields ({count/total_derived_fields*100:.1f}%)\n")
    
    f.write(f"\nAll Classes with Derived Fields (sorted by field count):\n")
    for filename, fields in sorted_results:
        class_name = filename.replace('.businessclass', '')
        f.write(f"{class_name}: {len(fields)} fields\n")

print(f"\nDetailed analysis saved to Outputs directory.")