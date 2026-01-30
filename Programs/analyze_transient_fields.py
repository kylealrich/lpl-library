import re

def analyze_transient_fields(file_path):
    """Extract and analyze Transient Fields section from LPL BusinessClass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find Transient Fields section
        pattern = r'Transient Fields\s*\n(.*?)(?=\n\t[A-Z]|\nLocal Fields|\nContext Fields|\nRule Blocks|\nDerived Fields|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if not match:
            return "No Transient Fields section found"
        
        transient_section = match.group(1).strip()
        
        # Parse fields - look for field definitions
        field_lines = transient_section.split('\n')
        fields = []
        current_field = None
        
        for line in field_lines:
            if line.strip():
                # Field definition line (starts with tab and contains 'is')
                if line.startswith('\t\t') and 'is' in line and not line.strip().startswith('derive'):
                    parts = line.strip().split()
                    if len(parts) >= 3 and parts[1] == 'is':
                        field_name = parts[0]
                        field_type = ' '.join(parts[2:])
                        fields.append({'name': field_name, 'type': field_type})
                        current_field = field_name
        
        # Analysis
        print(f"=== TRANSIENT FIELDS ANALYSIS: Requisition ===")
        print(f"Total fields: {len(fields)}")
        print(f"\nFields found:")
        for i, field in enumerate(fields, 1):
            print(f"{i:2d}. {field['name']:<35} -> {field['type']}")
        
        return transient_section
        
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"

# Execute analysis
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\Requisition.businessclass"
result = analyze_transient_fields(file_path)
print(f"\n=== RAW TRANSIENT FIELDS SECTION ===")
print(result)