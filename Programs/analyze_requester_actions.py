#!/usr/bin/env python3
"""
Analyze the Actions section of Requester.businessclass file
"""

import re
from pathlib import Path

def extract_actions_section(file_content):
    """Extract the Actions section from the LPL file content"""
    # Find the Actions section - look for "Actions" followed by action definitions
    actions_start = file_content.find('    Actions')
    if actions_start == -1:
        return None
    
    # Find the end of Actions section (Action Exit Rules or end of file)
    actions_end = file_content.find('\tAction Exit Rules', actions_start)
    if actions_end == -1:
        actions_end = len(file_content)
    
    return file_content[actions_start:actions_end]

def parse_actions(actions_content):
    """Parse individual actions from the Actions section"""
    actions = []
    
    # Look for action definitions with proper indentation
    lines = actions_content.split('\n')
    current_action = None
    current_body = []
    
    for line in lines:
        # Check if this is an action definition (starts with tab and contains "is a/an ... Action")
        if line.startswith('\t\t') and ' is a' in line and 'Action' in line:
            # Save previous action if exists
            if current_action:
                actions.append({
                    'name': current_action['name'],
                    'type': current_action['type'],
                    'body': '\n'.join(current_body)
                })
            
            # Parse new action
            parts = line.strip().split(' is a')
            if len(parts) >= 2:
                action_name = parts[0].strip()
                action_type = 'a' + parts[1].strip()
                current_action = {'name': action_name, 'type': action_type}
                current_body = []
        elif current_action and line.strip():
            current_body.append(line)
    
    # Add the last action
    if current_action:
        actions.append({
            'name': current_action['name'],
            'type': current_action['type'],
            'body': '\n'.join(current_body)
        })
    
    return actions

def analyze_action_details(action):
    """Analyze details of a single action"""
    body = action['body']
    
    # Extract parameters
    parameters = []
    param_match = re.search(r'Parameters\s*\n(.*?)(?=\n\s*(?:Parameter Rules|Action Rules|Local Fields|\w+\s+is))', 
                           body, re.DOTALL)
    if param_match:
        param_content = param_match.group(1)
        param_lines = [line.strip() for line in param_content.split('\n') if line.strip()]
        for line in param_lines:
            if 'is' in line and not line.startswith('States'):
                parameters.append(line)
    
    # Extract action rules count
    action_rules_match = re.search(r'Action Rules\s*\n(.*?)(?=\n\s*(?:Field Rules|Parameter Rules|Local Fields|\w+\s+is)|\Z)', 
                                  body, re.DOTALL)
    action_rules_count = 0
    if action_rules_match:
        rules_content = action_rules_match.group(1)
        # Count significant rule lines (not just whitespace or comments)
        rule_lines = [line for line in rules_content.split('\n') 
                     if line.strip() and not line.strip().startswith('//')]
        action_rules_count = len(rule_lines)
    
    # Check for restrictions
    is_restricted = 'restricted' in body
    
    # Check for confirmations
    has_confirmation = 'confirmation required' in body
    
    # Check for local fields
    has_local_fields = 'Local Fields' in body
    
    return {
        'parameters_count': len(parameters),
        'parameters': parameters,
        'action_rules_count': action_rules_count,
        'is_restricted': is_restricted,
        'has_confirmation': has_confirmation,
        'has_local_fields': has_local_fields
    }

def main():
    # Read the Requester.businessclass file
    file_path = Path("C:/Visual Basic Code/LPL Library/References/business class/Requester.businessclass")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Extract Actions section
    actions_section = extract_actions_section(content)
    
    if actions_section:
        print(f"Actions section found, length: {len(actions_section)} characters")
        # Show first few lines for debugging
        preview_lines = actions_section.split('\n')[:10]
        print("Preview of Actions section:")
        for line in preview_lines:
            print(f"  {repr(line)}")
        print()
    
    if not actions_section:
        print("No Actions section found in the file")
        return
    
    # Parse actions
    actions = parse_actions(actions_section)
    
    print("=== REQUESTER.BUSINESSCLASS ACTIONS ANALYSIS ===\n")
    print(f"Total Actions Found: {len(actions)}\n")
    
    # Analyze each action
    action_types = {}
    restricted_count = 0
    confirmation_count = 0
    
    for action in actions:
        details = analyze_action_details(action)
        
        # Count action types
        action_type = action['type']
        action_types[action_type] = action_types.get(action_type, 0) + 1
        
        if details['is_restricted']:
            restricted_count += 1
        if details['has_confirmation']:
            confirmation_count += 1
        
        print(f"Action: {action['name']}")
        print(f"  Type: {action_type}")
        print(f"  Parameters: {details['parameters_count']}")
        print(f"  Action Rules: {details['action_rules_count']}")
        print(f"  Restricted: {details['is_restricted']}")
        print(f"  Confirmation Required: {details['has_confirmation']}")
        print(f"  Has Local Fields: {details['has_local_fields']}")
        
        if details['parameters']:
            print("  Parameter Details:")
            for param in details['parameters'][:3]:  # Show first 3 parameters
                print(f"    {param}")
            if len(details['parameters']) > 3:
                print(f"    ... and {len(details['parameters']) - 3} more")
        print()
    
    # Summary statistics
    print("=== SUMMARY STATISTICS ===")
    print(f"Total Actions: {len(actions)}")
    print(f"Restricted Actions: {restricted_count}")
    print(f"Actions with Confirmation: {confirmation_count}")
    print()
    
    print("Action Types Distribution:")
    for action_type, count in sorted(action_types.items()):
        print(f"  {action_type}: {count}")
    print()
    
    # Find most complex actions (by parameter count)
    complex_actions = sorted(actions, 
                           key=lambda x: analyze_action_details(x)['parameters_count'], 
                           reverse=True)[:5]
    
    print("Most Complex Actions (by parameter count):")
    for action in complex_actions:
        details = analyze_action_details(action)
        print(f"  {action['name']}: {details['parameters_count']} parameters")

if __name__ == "__main__":
    main()