import re

def analyze_local_fields(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find Local Fields section
    local_fields_match = re.search(r'Local Fields\s*\n(.*?)(?=\n\w|\nEnd|\Z)', content, re.DOTALL)
    
    if not local_fields_match:
        return {"error": "Local Fields section not found"}
    
    local_fields_content = local_fields_match.group(1)
    
    # Parse fields
    fields = []
    field_pattern = r'\t([A-Za-z_][A-Za-z0-9_]*)\s+is\s+(.*?)(?=\n\t[A-Za-z_]|\n\w|\Z)'
    
    for match in re.finditer(field_pattern, local_fields_content, re.DOTALL):
        field_name = match.group(1)
        field_definition = match.group(2).strip()
        fields.append({"name": field_name, "definition": field_definition})
    
    return {
        "total_fields": len(fields),
        "fields": fields,
        "raw_content": local_fields_content.strip()
    }

# Analyze Account.businessclass
file_path = r"c:\Visual Basic Code\LPL Library\References\business class\Account.businessclass"
result = analyze_local_fields(file_path)

print("=== ACCOUNT LOCAL FIELDS ANALYSIS ===")
print(f"Total Local Fields: {result.get('total_fields', 0)}")

if 'fields' in result:
    for field in result['fields']:
        print(f"- {field['name']}: {field['definition']}")
else:
    print(f"Error: {result.get('error', 'Unknown error')}")