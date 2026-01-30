import re

def analyze_sets_section(file_path):
    """Extract and analyze the Sets section from Account.businessclass"""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find Sets section
    sets_match = re.search(r'\n\tSets\n(.*?)(?=\n\t[A-Z]|\n[A-Z]|\Z)', content, re.DOTALL)
    
    if not sets_match:
        print("No Sets section found in Account.businessclass")
        return
    
    sets_content = sets_match.group(1)
    print("=== SETS SECTION ANALYSIS ===")
    print(f"Raw Sets Content:\n{sets_content}")
    
    # Parse set definitions
    set_definitions = []
    lines = sets_content.split('\n')
    
    current_set = None
    for line in lines:
        line = line.rstrip()
        if not line or line.isspace():
            continue
            
        # Set name (starts with tab + name)
        if re.match(r'\t\t[A-Za-z]', line):
            set_name = line.strip()
            current_set = {'name': set_name, 'properties': []}
            set_definitions.append(current_set)
        # Set properties (more indented)
        elif current_set and line.startswith('\t\t\t'):
            current_set['properties'].append(line.strip())
    
    # Display analysis
    print(f"\n=== ANALYSIS RESULTS ===")
    print(f"Number of Sets defined: {len(set_definitions)}")
    
    for i, set_def in enumerate(set_definitions, 1):
        print(f"\nSet {i}: {set_def['name']}")
        print(f"  Properties: {len(set_def['properties'])}")
        for prop in set_def['properties']:
            print(f"    - {prop}")
    
    return set_definitions

# Run analysis
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\Account.businessclass"
sets_data = analyze_sets_section(file_path)