import re

def extract_context_fields(file_path):
    """Extract Context Fields section from Requisition.businessclass"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find Context Fields section - look for the exact pattern
        context_match = re.search(r'Context Fields\s*\n(.*?)(?=\n[A-Z][a-zA-Z\s]*Fields|\nend|\Z)', content, re.DOTALL)
        
        if not context_match:
            return "No Context Fields section found"
        
        context_section = context_match.group(1).strip()
        
        # Split into lines and filter for actual field definitions
        lines = context_section.split('\n')
        fields = []
        
        for line in lines:
            line = line.strip()
            # Look for field definitions (not indented code or comments)
            if line and not line.startswith('\t') and not line.startswith('//') and 'is' in line:
                # Simple field pattern: FieldName is Type
                if re.match(r'^[A-Za-z][A-Za-z0-9_]*\s+is\s+', line):
                    parts = line.split('is', 1)
                    if len(parts) == 2:
                        field_name = parts[0].strip()
                        field_type = parts[1].strip()
                        fields.append({'name': field_name, 'type': field_type})
        
        return {
            'total_fields': len(fields),
            'fields': fields,
            'raw_section': context_section[:1000] + "..." if len(context_section) > 1000 else context_section
        }
        
    except Exception as e:
        return f"Error: {str(e)}"

# Analyze the file
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\Requisition.businessclass"
result = extract_context_fields(file_path)

if isinstance(result, dict):
    print("CONTEXT FIELDS ANALYSIS - Requisition.businessclass")
    print(f"Total Context Fields Found: {result['total_fields']}")
    print("\nField Definitions:")
    for field in result['fields']:
        print(f"  {field['name']} is {field['type']}")
    
    print(f"\nRaw Section Preview:")
    print(result['raw_section'])
else:
    print(result)