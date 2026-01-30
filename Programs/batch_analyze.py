import os
import re

def analyze_businessclass(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    class_match = re.search(r'(\w+)\s+is\s+a\s+BusinessClass', content)
    class_name = class_match.group(1) if class_match else "Unknown"
    
    persistent_match = re.search(r'Persistent Fields\s*\n(.*?)\n\s*(?:Transient Fields|Local Fields|Derived Fields|Context Fields|Conditions|Relations|$)', content, re.DOTALL)
    
    if not persistent_match:
        return f"{class_name} (0 fields)"
    
    section = persistent_match.group(1)
    field_count = len(re.findall(r'\t\t\w+\s+is\s+', section))
    
    # Get key patterns
    has_states = 'value is' in section
    has_required = 'required' in section
    has_pii = 'holds pii' in section
    
    patterns = []
    if has_states: patterns.append("states")
    if has_required: patterns.append("required")
    if has_pii: patterns.append("pii")
    
    pattern_str = f" [{', '.join(patterns)}]" if patterns else ""
    
    return f"{class_name} ({field_count} fields){pattern_str}"

# Process all files in batches
directory = r'C:\Visual Basic Code\LPL Library\References\business class'
files = [f for f in os.listdir(directory) if f.endswith('.businessclass')]

batch_size = 50
total_files = len(files)
batch_num = 1

for i in range(0, total_files, batch_size):
    batch_files = files[i:i+batch_size]
    
    print(f"BATCH {batch_num} (files {i+1}-{min(i+batch_size, total_files)}):")
    
    for filename in batch_files:
        filepath = os.path.join(directory, filename)
        try:
            result = analyze_businessclass(filepath)
            print(f"  {result}")
        except Exception as e:
            print(f"  {filename}: ERROR")
    
    print()
    batch_num += 1
    
    if batch_num > 10:  # Limit to first 10 batches for now
        break

print(f"Processed {min(10*batch_size, total_files)} of {total_files} files")