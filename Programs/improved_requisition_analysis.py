import re

def analyze_derived_fields(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find Derived Fields section
    match = re.search(r'Derived Fields\s*\n(.*?)(?=\n\w|\nend|\Z)', content, re.DOTALL)
    if not match:
        return "No Derived Fields section found"
    
    derived_section = match.group(1)
    
    # Extract field definitions with improved pattern
    fields = []
    field_pattern = r'^\t\t(\w+)\s+is\s+a\s+(\w+)'
    
    for line in derived_section.split('\n'):
        field_match = re.match(field_pattern, line)
        if field_match:
            field_name = field_match.group(1)
            field_type = field_match.group(2)
            fields.append({'name': field_name, 'type': field_type})
    
    # Count field types
    type_counts = {}
    for field in fields:
        field_type = field['type']
        type_counts[field_type] = type_counts.get(field_type, 0) + 1
    
    # Analysis
    print(f"=== DERIVED FIELDS ANALYSIS - Requisition.businessclass ===\n")
    print(f"Total Derived Fields: {len(fields)}\n")
    
    if fields:
        print("Field Type Distribution:")
        for field_type, count in sorted(type_counts.items()):
            print(f"  {field_type}: {count} fields")
        
        print(f"\nAll Fields Found:")
        for i, field in enumerate(fields, 1):
            print(f"  {i:2d}. {field['name']} (type: {field['type']})")
    
    return fields

# Run analysis
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\Requisition.businessclass"
result = analyze_derived_fields(file_path)