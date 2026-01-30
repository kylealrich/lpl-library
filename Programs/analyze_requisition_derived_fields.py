import re

def analyze_derived_fields(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find Derived Fields section
    match = re.search(r'Derived Fields\s*\n(.*?)(?=\n\w|\nend|\Z)', content, re.DOTALL)
    if not match:
        return "No Derived Fields section found"
    
    derived_section = match.group(1)
    
    # Extract field definitions
    fields = []
    field_pattern = r'^\t(\w+)\s+is\s+a\s+(\w+)'
    
    for line in derived_section.split('\n'):
        field_match = re.match(field_pattern, line)
        if field_match:
            field_name = field_match.group(1)
            field_type = field_match.group(2)
            fields.append({'name': field_name, 'type': field_type})
    
    # Analysis
    print(f"=== DERIVED FIELDS ANALYSIS - Requisition.businessclass ===\n")
    print(f"Total Derived Fields: {len(fields)}\n")
    
    if fields:
        print("Fields Found:")
        for field in fields:
            print(f"  - {field['name']} (type: {field['type']})")
    
    print(f"\nRaw Section Content:\n{derived_section}")
    
    return fields

# Run analysis
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\Requisition.businessclass"
result = analyze_derived_fields(file_path)