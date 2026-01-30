import re
import os

def analyze_persistent_fields_syntax(directory):
    patterns = {
        'field_definition': [],
        'data_types': set(),
        'attributes': set(),
        'states': [],
        'field_modifiers': set()
    }
    
    for filename in os.listdir(directory):
        if filename.endswith('.businessclass'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract Persistent Fields section
                persistent_match = re.search(r'Persistent Fields\s*\n(.*?)\n\s*(?:Transient Fields|Local Fields|Derived Fields|Context Fields|Conditions)', content, re.DOTALL)
                if persistent_match:
                    section = persistent_match.group(1)
                    
                    # Field definitions
                    field_lines = re.findall(r'\t\t(\w+)\s+is\s+(.+)', section)
                    for name, definition in field_lines:
                        patterns['field_definition'].append((name, definition.strip()))
                    
                    # Data types
                    types = re.findall(r'is\s+(a\s+)?(\w+)(?:\s+size\s+\d+)?', section)
                    for article, dtype in types:
                        patterns['data_types'].add(dtype)
                    
                    # Attributes
                    attrs = re.findall(r'\t\t\t(required|restricted|holds pii|delete ignored|translatable|disable \w+)', section)
                    patterns['attributes'].update(attrs)
                    
                    # States
                    state_blocks = re.findall(r'States\s*\n(.*?)(?=\n\t\t[A-Z]|\n\t[A-Z]|\Z)', section, re.DOTALL)
                    for block in state_blocks:
                        states = re.findall(r'(\w+)\s+value is (\d+)', block)
                        patterns['states'].extend(states)
                    
                    # Field modifiers
                    modifiers = re.findall(r'is\s+(Alpha|Numeric|Boolean|Date|Text|Description|Decimal)(?:\s+(size\s+\d+|up to \d+|\d+))?', section)
                    for mod_type, size in modifiers:
                        patterns['field_modifiers'].add(f"{mod_type} {size}".strip())
                        
            except Exception as e:
                continue
    
    return patterns

# Analyze syntax patterns
patterns = analyze_persistent_fields_syntax(r'C:\Visual Basic Code\LPL Library\References\business class')

print("PERSISTENT FIELDS SYNTAX ANALYSIS")
print("=" * 40)

print("\nDATA TYPES:")
for dtype in sorted(patterns['data_types']):
    print(f"  {dtype}")

print("\nFIELD ATTRIBUTES:")
for attr in sorted(patterns['attributes']):
    print(f"  {attr}")

print("\nFIELD MODIFIERS:")
for mod in sorted(patterns['field_modifiers']):
    print(f"  {mod}")

print(f"\nSTATE EXAMPLES (first 10):")
for state, value in patterns['states'][:10]:
    print(f"  {state} = {value}")

print(f"\nFIELD DEFINITION EXAMPLES (first 5):")
for name, definition in patterns['field_definition'][:5]:
    print(f"  {name}: {definition}")