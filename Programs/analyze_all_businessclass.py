import os
import re

def analyze_single_businessclass(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract class name
    class_match = re.search(r'(\w+)\s+is\s+a\s+BusinessClass', content)
    class_name = class_match.group(1) if class_match else "Unknown"
    
    # Extract Persistent Fields
    persistent_match = re.search(r'Persistent Fields\s*\n(.*?)\n\s*(?:Transient Fields|Local Fields|Derived Fields|Context Fields|Conditions|Relations|$)', content, re.DOTALL)
    
    if not persistent_match:
        return f"{class_name}: No Persistent Fields found"
    
    section = persistent_match.group(1)
    fields = []
    
    # Parse fields
    lines = section.split('\n')
    current_field = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Field definition
        if '\t\t' in line and 'is' in line:
            parts = line.split('\t\t')
            field_name = parts[0].strip()
            field_def = parts[1].strip() if len(parts) > 1 else ''
            
            current_field = {'name': field_name, 'definition': field_def, 'states': [], 'attributes': []}
            fields.append(current_field)
        
        # States
        elif 'value is' in line and current_field:
            state_match = re.search(r'(\w+)\s+value is (\d+)', line)
            if state_match:
                current_field['states'].append(f"{state_match.group(1)}={state_match.group(2)}")
        
        # Attributes
        elif line in ['required', 'restricted', 'holds pii', 'delete ignored', 'translatable'] and current_field:
            current_field['attributes'].append(line)
    
    result = f"{class_name} ({len(fields)} fields):\n"
    for field in fields[:3]:  # Show first 3 fields
        result += f"  {field['name']}: {field['definition']}\n"
        if field['states']:
            result += f"    States: {', '.join(field['states'])}\n"
        if field['attributes']:
            result += f"    Attrs: {', '.join(field['attributes'])}\n"
    
    if len(fields) > 3:
        result += f"  ... and {len(fields)-3} more fields\n"
    
    return result

# Process all files
directory = r'C:\Visual Basic Code\LPL Library\References\business class'
files = [f for f in os.listdir(directory) if f.endswith('.businessclass')]

print(f"Analyzing {len(files)} BusinessClass files...\n")

for i, filename in enumerate(files[:5], 1):  # Process first 5 files
    filepath = os.path.join(directory, filename)
    try:
        result = analyze_single_businessclass(filepath)
        print(f"{i}. {result}\n")
    except Exception as e:
        print(f"{i}. {filename}: Error - {str(e)}\n")