import os
import re
from collections import defaultdict

def analyze_local_fields(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        local_fields_match = re.search(r'Local Fields\s*\n(.*?)(?=\n\w|\nEnd|\Z)', content, re.DOTALL)
        
        if not local_fields_match:
            return {"field_count": 0, "has_local_fields": False}
        
        local_fields_content = local_fields_match.group(1)
        field_pattern = r'\t([A-Za-z_][A-Za-z0-9_]*)\s+is\s+(.*?)(?=\n\t[A-Za-z_]|\n\w|\Z)'
        
        fields = []
        for match in re.finditer(field_pattern, local_fields_content, re.DOTALL):
            field_name = match.group(1)
            field_definition = match.group(2).strip()
            fields.append({"name": field_name, "definition": field_definition})
        
        return {
            "field_count": len(fields),
            "has_local_fields": True,
            "fields": fields
        }
    except Exception as e:
        return {"field_count": 0, "has_local_fields": False, "error": str(e)}

# Analyze all .businessclass files
base_dir = r"c:\Visual Basic Code\LPL Library\References\business class"
results = {}
field_counts = defaultdict(int)
total_files = 0
files_with_local_fields = 0

for filename in os.listdir(base_dir):
    if filename.endswith('.businessclass'):
        total_files += 1
        file_path = os.path.join(base_dir, filename)
        class_name = filename.replace('.businessclass', '')
        
        result = analyze_local_fields(file_path)
        results[class_name] = result
        
        if result['has_local_fields']:
            files_with_local_fields += 1
            field_counts[result['field_count']] += 1

# Summary statistics
print(f"=== LOCAL FIELDS ANALYSIS SUMMARY ===")
print(f"Total BusinessClass files: {total_files}")
print(f"Files with Local Fields: {files_with_local_fields}")
print(f"Files without Local Fields: {total_files - files_with_local_fields}")

print(f"\n=== FIELD COUNT DISTRIBUTION ===")
for count in sorted(field_counts.keys()):
    print(f"{count} fields: {field_counts[count]} files")

# Top 10 classes with most local fields
top_classes = sorted([(k, v['field_count']) for k, v in results.items() if v['has_local_fields']], 
                    key=lambda x: x[1], reverse=True)[:10]

print(f"\n=== TOP 10 CLASSES BY LOCAL FIELD COUNT ===")
for class_name, count in top_classes:
    print(f"{class_name}: {count} fields")

# Sample field types analysis
field_types = defaultdict(int)
for class_name, result in results.items():
    if result['has_local_fields']:
        for field in result['fields']:
            definition = field['definition'].lower()
            if 'derivedfield' in definition:
                field_types['DerivedField'] += 1
            elif 'set' in definition:
                field_types['Set'] += 1
            elif 'relation' in definition:
                field_types['Relation'] += 1
            elif 'messagefield' in definition:
                field_types['MessageField'] += 1
            else:
                field_types['Reference'] += 1

print(f"\n=== LOCAL FIELD TYPES DISTRIBUTION ===")
for field_type, count in sorted(field_types.items(), key=lambda x: x[1], reverse=True):
    print(f"{field_type}: {count}")