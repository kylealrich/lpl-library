import re

def analyze_set_actions(file_path):
    """Analyze Set Actions in GLTransactionDetail.busclass file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return "File not found"
    
    # Find Set Actions section
    set_actions_pattern = r'Actions\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*Rules|\n\s*$)'
    set_actions_match = re.search(set_actions_pattern, content, re.DOTALL)
    
    if not set_actions_match:
        return "No Set Actions found"
    
    set_actions_content = set_actions_match.group(1)
    
    # Extract individual Set Actions
    action_pattern = r'(\w+)\s+is\s+a\s+Set\s+Action(.*?)(?=\n\s*\w+\s+is\s+a\s+Set\s+Action|\n\s*[A-Z][a-zA-Z\s]*\s*Rules|\n\s*$)'
    actions = re.findall(action_pattern, set_actions_content, re.DOTALL)
    
    analysis = {
        'total_set_actions': len(actions),
        'set_actions': []
    }
    
    for action_name, action_content in actions:
        action_analysis = analyze_single_set_action(action_name, action_content)
        analysis['set_actions'].append(action_analysis)
    
    return analysis

def analyze_single_set_action(name, content):
    """Analyze a single Set Action"""
    
    analysis = {
        'name': name,
        'restricted': 'restricted' in content,
        'parameters': [],
        'local_fields': [],
        'instance_selection': None,
        'sort_order': [],
        'accumulators': [],
        'set_rules': [],
        'action_rules': []
    }
    
    # Extract Parameters
    params_pattern = r'Parameters\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    params_match = re.search(params_pattern, content, re.DOTALL)
    if params_match:
        params_content = params_match.group(1)
        param_pattern = r'(\w+)\s+is\s+([^\n]+)'
        params = re.findall(param_pattern, params_content)
        analysis['parameters'] = [{'name': p[0], 'type': p[1].strip()} for p in params]
    
    # Extract Local Fields
    local_pattern = r'Local\s+Fields\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    local_match = re.search(local_pattern, content, re.DOTALL)
    if local_match:
        local_content = local_match.group(1)
        field_pattern = r'(\w+)\s+is\s+([^\n]+)'
        fields = re.findall(field_pattern, local_content)
        analysis['local_fields'] = [{'name': f[0], 'type': f[1].strip()} for f in fields]
    
    # Extract Instance Selection
    instance_pattern = r'Instance\s+Selection\s*\n\s*where\s*\((.*?)\)'
    instance_match = re.search(instance_pattern, content, re.DOTALL)
    if instance_match:
        analysis['instance_selection'] = instance_match.group(1).strip()
    
    # Extract Sort Order
    sort_pattern = r'Sort\s+Order\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    sort_match = re.search(sort_pattern, content, re.DOTALL)
    if sort_match:
        sort_content = sort_match.group(1)
        sort_fields = [line.strip() for line in sort_content.split('\n') if line.strip()]
        analysis['sort_order'] = sort_fields
    
    # Extract Accumulators
    acc_pattern = r'Accumulators\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*|\n\s*$)'
    acc_match = re.search(acc_pattern, content, re.DOTALL)
    if acc_match:
        acc_content = acc_match.group(1)
        accumulators = [line.strip() for line in acc_content.split('\n') if line.strip()]
        analysis['accumulators'] = accumulators
    
    # Extract Set Rules
    set_rules_pattern = r'Set\s+Rules\s*\n(.*?)(?=\n\s*Action\s+Rules|\n\s*$)'
    set_rules_match = re.search(set_rules_pattern, content, re.DOTALL)
    if set_rules_match:
        analysis['set_rules'] = ['Set Rules found - complex nested structure']
    
    # Extract Action Rules
    action_rules_pattern = r'Action\s+Rules\s*\n(.*?)$'
    action_rules_match = re.search(action_rules_pattern, content, re.DOTALL)
    if action_rules_match:
        analysis['action_rules'] = ['Action Rules found - complex nested structure']
    
    return analysis

def generate_syntax_patterns(analysis):
    """Generate LPL Set Action syntax patterns from analysis"""
    
    patterns = []
    
    # Basic Set Action syntax
    patterns.append("""
=== SET ACTION BASIC SYNTAX ===
ActionName is a Set Action
    [restricted]
    Parameters
        ParameterName is DataType
            [default label is "Label"]
    Local Fields
        LocalFieldName is DataType
    Instance Selection
        where (conditions)
    Sort Order
        FieldName1
        FieldName2 [descending]
    Accumulators
        AccumulatorName
    Action Rules
        [Complex processing logic]
""")
    
    # Parameter patterns
    if analysis['set_actions']:
        first_action = analysis['set_actions'][0]
        if first_action['parameters']:
            patterns.append("""
=== PARAMETER PATTERNS ===
Common parameter types found:
""")
            for param in first_action['parameters'][:5]:  # Show first 5 parameters
                patterns.append(f"    {param['name']} is {param['type']}")
    
    # Local Fields patterns
    if analysis['set_actions']:
        first_action = analysis['set_actions'][0]
        if first_action['local_fields']:
            patterns.append("""
=== LOCAL FIELDS PATTERNS ===
Common local field types:
""")
            for field in first_action['local_fields'][:5]:  # Show first 5 fields
                patterns.append(f"    {field['name']} is {field['type']}")
    
    # Accumulator patterns
    if analysis['set_actions']:
        first_action = analysis['set_actions'][0]
        if first_action['accumulators']:
            patterns.append("""
=== ACCUMULATOR PATTERNS ===
Common accumulators:
""")
            for acc in first_action['accumulators'][:5]:  # Show first 5 accumulators
                patterns.append(f"    {acc}")
    
    return '\n'.join(patterns)

# Main execution
if __name__ == "__main__":
    file_path = r"c:\lpl-library\References\business class\GLTransactionDetail.busclass"
    
    print("Analyzing Set Actions in GLTransactionDetail.busclass...")
    analysis = analyze_set_actions(file_path)
    
    if isinstance(analysis, str):
        print(f"Error: {analysis}")
    else:
        print(f"\nFound {analysis['total_set_actions']} Set Action(s)")
        
        for action in analysis['set_actions']:
            print(f"\n--- {action['name']} ---")
            print(f"Restricted: {action['restricted']}")
            print(f"Parameters: {len(action['parameters'])}")
            print(f"Local Fields: {len(action['local_fields'])}")
            print(f"Sort Order Fields: {len(action['sort_order'])}")
            print(f"Accumulators: {len(action['accumulators'])}")
            print(f"Has Set Rules: {len(action['set_rules']) > 0}")
            print(f"Has Action Rules: {len(action['action_rules']) > 0}")
            
            if action['instance_selection']:
                print(f"Instance Selection: {action['instance_selection'][:100]}...")
        
        # Generate syntax patterns
        syntax_patterns = generate_syntax_patterns(analysis)
        
        # Save analysis to file
        with open(r"c:\lpl-library\Outputs\set_actions_analysis.txt", 'w', encoding='utf-8') as f:
            f.write("SET ACTIONS ANALYSIS - GLTransactionDetail.busclass\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Total Set Actions Found: {analysis['total_set_actions']}\n\n")
            
            for action in analysis['set_actions']:
                f.write(f"SET ACTION: {action['name']}\n")
                f.write("-" * 40 + "\n")
                f.write(f"Restricted: {action['restricted']}\n")
                f.write(f"Parameters Count: {len(action['parameters'])}\n")
                f.write(f"Local Fields Count: {len(action['local_fields'])}\n")
                f.write(f"Sort Order Fields: {len(action['sort_order'])}\n")
                f.write(f"Accumulators Count: {len(action['accumulators'])}\n")
                f.write(f"Has Set Rules: {len(action['set_rules']) > 0}\n")
                f.write(f"Has Action Rules: {len(action['action_rules']) > 0}\n\n")
                
                if action['parameters']:
                    f.write("PARAMETERS:\n")
                    for param in action['parameters']:
                        f.write(f"  {param['name']} is {param['type']}\n")
                    f.write("\n")
                
                if action['local_fields']:
                    f.write("LOCAL FIELDS:\n")
                    for field in action['local_fields']:
                        f.write(f"  {field['name']} is {field['type']}\n")
                    f.write("\n")
                
                if action['sort_order']:
                    f.write("SORT ORDER:\n")
                    for field in action['sort_order']:
                        f.write(f"  {field}\n")
                    f.write("\n")
                
                if action['accumulators']:
                    f.write("ACCUMULATORS:\n")
                    for acc in action['accumulators']:
                        f.write(f"  {acc}\n")
                    f.write("\n")
                
                if action['instance_selection']:
                    f.write("INSTANCE SELECTION:\n")
                    f.write(f"  where ({action['instance_selection']})\n\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
            
            f.write("SYNTAX PATTERNS:\n")
            f.write(syntax_patterns)
        
        print(f"\nAnalysis saved to: c:\\lpl-library\\Outputs\\set_actions_analysis.txt")
        print("\nSyntax patterns generated and ready for knowledge base update.")