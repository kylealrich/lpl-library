import re

def analyze_set_actions(file_path):
    """Analyze Set Actions in GLTransactionDetail.busclass file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return "File not found"
    
    # Find Actions section more broadly
    actions_pattern = r'Actions\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*Rules|\n\s*$)'
    actions_match = re.search(actions_pattern, content, re.DOTALL)
    
    if not actions_match:
        return "No Actions section found"
    
    actions_content = actions_match.group(1)
    
    # Look for Set Action pattern more flexibly
    set_action_pattern = r'(\w+)\s+is\s+a\s+Set\s+Action(.*?)(?=\n\s*\w+\s+is\s+a\s+|\n\s*[A-Z][a-zA-Z\s]*\s*Rules|\n\s*$)'
    set_actions = re.findall(set_action_pattern, actions_content, re.DOTALL | re.IGNORECASE)
    
    if not set_actions:
        # Try alternative pattern - look for "Set Action" anywhere in Actions
        alt_pattern = r'(.*?Set\s+Action.*?)(?=\n\s*\w+\s+is\s+|\n\s*[A-Z][a-zA-Z\s]*\s*Rules|\n\s*$)'
        alt_matches = re.findall(alt_pattern, actions_content, re.DOTALL | re.IGNORECASE)
        
        analysis = {
            'total_set_actions': len(alt_matches),
            'raw_content': actions_content[:1000] + "..." if len(actions_content) > 1000 else actions_content,
            'set_actions': []
        }
        
        for match in alt_matches:
            analysis['set_actions'].append({
                'name': 'Unknown',
                'content': match[:500] + "..." if len(match) > 500 else match
            })
        
        return analysis
    
    analysis = {
        'total_set_actions': len(set_actions),
        'set_actions': []
    }
    
    for action_name, action_content in set_actions:
        action_analysis = analyze_single_set_action(action_name, action_content)
        analysis['set_actions'].append(action_analysis)
    
    return analysis

def analyze_single_set_action(name, content):
    """Analyze a single Set Action"""
    
    analysis = {
        'name': name,
        'restricted': 'restricted' in content.lower(),
        'parameters': [],
        'local_fields': [],
        'instance_selection': None,
        'sort_order': [],
        'accumulators': [],
        'set_rules': [],
        'action_rules': [],
        'raw_content': content[:1000] + "..." if len(content) > 1000 else content
    }
    
    # Extract Parameters
    params_pattern = r'Parameters\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    params_match = re.search(params_pattern, content, re.DOTALL | re.IGNORECASE)
    if params_match:
        params_content = params_match.group(1)
        param_pattern = r'(\w+)\s+is\s+([^\n]+)'
        params = re.findall(param_pattern, params_content)
        analysis['parameters'] = [{'name': p[0], 'type': p[1].strip()} for p in params]
    
    # Extract Local Fields
    local_pattern = r'Local\s+Fields\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    local_match = re.search(local_pattern, content, re.DOTALL | re.IGNORECASE)
    if local_match:
        local_content = local_match.group(1)
        field_pattern = r'(\w+)\s+is\s+([^\n]+)'
        fields = re.findall(field_pattern, local_content)
        analysis['local_fields'] = [{'name': f[0], 'type': f[1].strip()} for f in fields]
    
    # Extract Instance Selection
    instance_pattern = r'Instance\s+Selection\s*\n\s*where\s*\((.*?)\)'
    instance_match = re.search(instance_pattern, content, re.DOTALL | re.IGNORECASE)
    if instance_match:
        analysis['instance_selection'] = instance_match.group(1).strip()
    
    # Extract Sort Order
    sort_pattern = r'Sort\s+Order\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    sort_match = re.search(sort_pattern, content, re.DOTALL | re.IGNORECASE)
    if sort_match:
        sort_content = sort_match.group(1)
        sort_fields = [line.strip() for line in sort_content.split('\n') if line.strip()]
        analysis['sort_order'] = sort_fields
    
    # Extract Accumulators
    acc_pattern = r'Accumulators\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    acc_match = re.search(acc_pattern, content, re.DOTALL | re.IGNORECASE)
    if acc_match:
        acc_content = acc_match.group(1)
        accumulators = [line.strip() for line in acc_content.split('\n') if line.strip()]
        analysis['accumulators'] = accumulators
    
    # Check for Set Rules and Action Rules
    if 'set rules' in content.lower():
        analysis['set_rules'] = ['Set Rules found']
    
    if 'action rules' in content.lower():
        analysis['action_rules'] = ['Action Rules found']
    
    return analysis

def extract_key_patterns(content):
    """Extract key LPL patterns from the content"""
    
    patterns = []
    
    # Look for Set Is pattern
    set_is_pattern = r'Set\s+Is\s*\n\s*(\w+)'
    set_is_matches = re.findall(set_is_pattern, content, re.IGNORECASE)
    if set_is_matches:
        patterns.append(f"Set Is patterns found: {set_is_matches}")
    
    # Look for Queue Mapping Fields
    queue_pattern = r'Queue\s+Mapping\s+Fields\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    queue_match = re.search(queue_pattern, content, re.DOTALL | re.IGNORECASE)
    if queue_match:
        patterns.append("Queue Mapping Fields found")
    
    # Look for Parameter Rules
    param_rules_pattern = r'Parameter\s+Rules\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    param_rules_match = re.search(param_rules_pattern, content, re.DOTALL | re.IGNORECASE)
    if param_rules_match:
        patterns.append("Parameter Rules found")
    
    return patterns

# Main execution
if __name__ == "__main__":
    file_path = r"c:\lpl-library\References\business class\GLTransactionDetail.busclass"
    
    print("Analyzing Set Actions in GLTransactionDetail.busclass...")
    analysis = analyze_set_actions(file_path)
    
    if isinstance(analysis, str):
        print(f"Error: {analysis}")
    else:
        print(f"\nFound {analysis['total_set_actions']} Set Action(s)")
        
        # Read file to extract additional patterns
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        key_patterns = extract_key_patterns(content)
        
        # Save detailed analysis
        with open(r"c:\lpl-library\Outputs\set_actions_analysis.txt", 'w', encoding='utf-8') as f:
            f.write("SET ACTIONS ANALYSIS - GLTransactionDetail.busclass\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Total Set Actions Found: {analysis['total_set_actions']}\n\n")
            
            if 'raw_content' in analysis:
                f.write("RAW ACTIONS CONTENT (first 1000 chars):\n")
                f.write("-" * 40 + "\n")
                f.write(analysis['raw_content'])
                f.write("\n\n")
            
            for action in analysis['set_actions']:
                f.write(f"SET ACTION: {action['name']}\n")
                f.write("-" * 40 + "\n")
                
                if 'raw_content' in action:
                    f.write("RAW CONTENT:\n")
                    f.write(action['raw_content'])
                    f.write("\n\n")
                else:
                    f.write(f"Restricted: {action['restricted']}\n")
                    f.write(f"Parameters Count: {len(action['parameters'])}\n")
                    f.write(f"Local Fields Count: {len(action['local_fields'])}\n")
                    f.write(f"Sort Order Fields: {len(action['sort_order'])}\n")
                    f.write(f"Accumulators Count: {len(action['accumulators'])}\n")
                    f.write(f"Has Set Rules: {len(action['set_rules']) > 0}\n")
                    f.write(f"Has Action Rules: {len(action['action_rules']) > 0}\n\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
            
            if key_patterns:
                f.write("KEY PATTERNS FOUND:\n")
                f.write("-" * 40 + "\n")
                for pattern in key_patterns:
                    f.write(f"- {pattern}\n")
                f.write("\n")
        
        print(f"\nAnalysis saved to: c:\\lpl-library\\Outputs\\set_actions_analysis.txt")
        
        if key_patterns:
            print("\nKey patterns found:")
            for pattern in key_patterns:
                print(f"- {pattern}")