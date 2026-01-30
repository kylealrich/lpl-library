import re

def analyze_context_fields(file_path):
    """Analyze Context Fields section from LPL BusinessClass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find Context Fields section
        context_match = re.search(r'Context Fields\s*\n(.*?)(?=\n\w|\nend|\Z)', content, re.DOTALL)
        
        if not context_match:
            return "No Context Fields section found"
        
        context_section = context_match.group(1)
        
        # Parse fields
        field_lines = [line.strip() for line in context_section.split('\n') if line.strip()]
        fields = []
        
        for line in field_lines:
            if not line.startswith('\t') and 'is' in line:
                # Extract field name and type
                parts = line.split('is')
                if len(parts) >= 2:
                    field_name = parts[0].strip()
                    field_type = parts[1].strip()
                    fields.append({'name': field_name, 'type': field_type})
        
        # Generate analysis
        analysis = {
            'total_fields': len(fields),
            'fields': fields,
            'field_types': {}
        }
        
        # Count field types
        for field in fields:
            field_type = field['type'].split()[0]  # Get base type
            analysis['field_types'][field_type] = analysis['field_types'].get(field_type, 0) + 1
        
        return analysis
        
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"

# Analyze Requisition.businessclass
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\Requisition.businessclass"
result = analyze_context_fields(file_path)

if isinstance(result, dict):
    print(f"CONTEXT FIELDS ANALYSIS - Requisition.businessclass")
    print(f"Total Context Fields: {result['total_fields']}")
    print("\nFields Found:")
    for field in result['fields']:
        print(f"  {field['name']} -> {field['type']}")
    
    print(f"\nField Type Distribution:")
    for field_type, count in result['field_types'].items():
        print(f"  {field_type}: {count}")
else:
    print(result)