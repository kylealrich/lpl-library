import re

def extract_journalize_transactions_action(file_path):
    """Extract the complete JournalizeTransactions Set Action from GLTransactionDetail.busclass"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return "File not found"
    
    # Find the JournalizeTransactions Set Action
    # Look for the pattern starting with "JournalizeTransactions is a Set Action"
    pattern = r'JournalizeTransactions\s+is\s+a\s+Set\s+Action(.*?)(?=\n\s*\w+\s+is\s+a\s+|\n\s*[A-Z][a-zA-Z\s]*\s*Rules|\n\s*$)'
    
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return "JournalizeTransactions Set Action not found"
    
    action_content = match.group(1)
    
    # Parse the different sections
    sections = {
        'parameters': extract_section(action_content, 'Parameters'),
        'queue_mapping_fields': extract_section(action_content, 'Queue Mapping Fields'),
        'parameter_rules': extract_section(action_content, 'Parameter Rules'),
        'local_fields': extract_section(action_content, 'Local Fields'),
        'instance_selection': extract_instance_selection(action_content),
        'sort_order': extract_section(action_content, 'Sort Order'),
        'accumulators': extract_section(action_content, 'Accumulators'),
        'action_rules': extract_section(action_content, 'Action Rules'),
        'set_rules': extract_set_rules(action_content)
    }
    
    return sections

def extract_section(content, section_name):
    """Extract a specific section from the Set Action content"""
    
    pattern = rf'{section_name}\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*(?:Rules|Fields|Selection|Order|Accumulators)|\n\s*$)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if match:
        section_content = match.group(1).strip()
        return section_content
    
    return None

def extract_instance_selection(content):
    """Extract Instance Selection with where clause"""
    
    pattern = r'Instance\s+Selection\s*\n\s*where\s*\((.*?)\)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    return None

def extract_set_rules(content):
    """Extract Set Rules section which contains nested rules"""
    
    # Look for various Set Rules patterns
    patterns = [
        r'Set\s+Rules\s*\n(.*?)(?=\n\s*Action\s+Rules|\n\s*$)',
        r'(\w+)\s+Set\s+Rules\s*\n(.*?)(?=\n\s*\w+\s+Set\s+Rules|\n\s*Action\s+Rules|\n\s*$)'
    ]
    
    set_rules = {}
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                rule_name, rule_content = match
                set_rules[rule_name] = rule_content.strip()
            else:
                set_rules['General'] = match.strip()
    
    return set_rules if set_rules else None

def analyze_parameters(params_content):
    """Analyze parameters section to extract individual parameters"""
    
    if not params_content:
        return []
    
    parameters = []
    
    # Split by parameter definitions
    param_lines = params_content.split('\n')
    current_param = None
    
    for line in param_lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a parameter definition
        param_match = re.match(r'(\w+)\s+is\s+(.+)', line)
        if param_match:
            if current_param:
                parameters.append(current_param)
            
            current_param = {
                'name': param_match.group(1),
                'type': param_match.group(2).strip(),
                'attributes': []
            }
        elif current_param and 'default label' in line.lower():
            current_param['attributes'].append(line)
    
    if current_param:
        parameters.append(current_param)
    
    return parameters

# Main execution
if __name__ == "__main__":
    file_path = r"c:\lpl-library\References\business class\GLTransactionDetail.busclass"
    
    print("Extracting JournalizeTransactions Set Action...")
    
    sections = extract_journalize_transactions_action(file_path)
    
    if isinstance(sections, str):
        print(f"Error: {sections}")
    else:
        # Save detailed analysis
        with open(r"c:\lpl-library\Outputs\journalize_transactions_analysis.txt", 'w', encoding='utf-8') as f:
            f.write("JOURNALIZE TRANSACTIONS SET ACTION ANALYSIS\n")
            f.write("=" * 60 + "\n\n")
            
            for section_name, section_content in sections.items():
                if section_content:
                    f.write(f"{section_name.upper().replace('_', ' ')}:\n")
                    f.write("-" * 40 + "\n")
                    
                    if section_name == 'parameters' and section_content:
                        # Analyze parameters in detail
                        params = analyze_parameters(section_content)
                        if params:
                            for param in params:
                                f.write(f"Parameter: {param['name']}\n")
                                f.write(f"  Type: {param['type']}\n")
                                if param['attributes']:
                                    f.write(f"  Attributes: {param['attributes']}\n")
                                f.write("\n")
                        else:
                            f.write(section_content)
                    elif isinstance(section_content, dict):
                        for key, value in section_content.items():
                            f.write(f"{key}:\n{value}\n\n")
                    else:
                        f.write(section_content)
                    
                    f.write("\n\n")
        
        print("Analysis saved to: c:\\lpl-library\\Outputs\\journalize_transactions_analysis.txt")
        
        # Print summary
        print("\nSections found:")
        for section_name, section_content in sections.items():
            if section_content:
                print(f"- {section_name.replace('_', ' ').title()}")