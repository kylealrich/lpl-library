#!/usr/bin/env python3
"""
Analyze Actions sections in ALL .businessclass files
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def extract_actions_section(file_content):
    """Extract Actions section from LPL file"""
    actions_start = file_content.find('    Actions')
    if actions_start == -1:
        return None
    
    actions_end = file_content.find('\tAction Exit Rules', actions_start)
    if actions_end == -1:
        actions_end = len(file_content)
    
    return file_content[actions_start:actions_end]

def parse_actions(actions_content):
    """Parse actions from Actions section"""
    actions = []
    lines = actions_content.split('\n')
    current_action = None
    current_body = []
    
    for line in lines:
        if line.startswith('\t\t') and ' is a' in line and 'Action' in line:
            if current_action:
                actions.append({
                    'name': current_action['name'],
                    'type': current_action['type'],
                    'body': '\n'.join(current_body)
                })
            
            parts = line.strip().split(' is a')
            if len(parts) >= 2:
                action_name = parts[0].strip()
                action_type = 'a' + parts[1].strip()
                current_action = {'name': action_name, 'type': action_type}
                current_body = []
        elif current_action and line.strip():
            current_body.append(line)
    
    if current_action:
        actions.append({
            'name': current_action['name'],
            'type': current_action['type'],
            'body': '\n'.join(current_body)
        })
    
    return actions

def analyze_action(action):
    """Analyze single action details"""
    body = action['body']
    
    # Count parameters
    param_match = re.search(r'Parameters\s*\n(.*?)(?=\n\s*(?:Parameter Rules|Action Rules|Local Fields|\w+\s+is))', body, re.DOTALL)
    param_count = 0
    if param_match:
        param_lines = [line.strip() for line in param_match.group(1).split('\n') if line.strip() and 'is' in line and not line.startswith('States')]
        param_count = len(param_lines)
    
    # Count action rules
    rules_match = re.search(r'Action Rules\s*\n(.*?)(?=\n\s*(?:Field Rules|Parameter Rules|Local Fields|\w+\s+is)|\Z)', body, re.DOTALL)
    rules_count = 0
    if rules_match:
        rule_lines = [line for line in rules_match.group(1).split('\n') if line.strip() and not line.strip().startswith('//')]
        rules_count = len(rule_lines)
    
    return {
        'parameters': param_count,
        'rules': rules_count,
        'restricted': 'restricted' in body,
        'confirmation': 'confirmation required' in body,
        'local_fields': 'Local Fields' in body
    }

def main():
    business_class_dir = Path("C:/Visual Basic Code/LPL Library/References/business class")
    
    # Statistics
    total_files = 0
    files_with_actions = 0
    total_actions = 0
    action_types = defaultdict(int)
    restricted_actions = 0
    confirmation_actions = 0
    
    # Complex actions tracking
    complex_actions = []
    files_by_action_count = defaultdict(int)
    
    print("Analyzing ALL .businessclass files for Actions sections...")
    
    # Process all .businessclass files
    for file_path in business_class_dir.glob("*.businessclass"):
        total_files += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        actions_section = extract_actions_section(content)
        if not actions_section:
            continue
        
        files_with_actions += 1
        actions = parse_actions(actions_section)
        
        if actions:
            file_action_count = len(actions)
            total_actions += file_action_count
            files_by_action_count[file_action_count] += 1
            
            for action in actions:
                details = analyze_action(action)
                action_types[action['type']] += 1
                
                if details['restricted']:
                    restricted_actions += 1
                if details['confirmation']:
                    confirmation_actions += 1
                
                # Track complex actions
                if details['rules'] > 50 or details['parameters'] > 10:
                    complex_actions.append({
                        'file': file_path.name,
                        'name': action['name'],
                        'type': action['type'],
                        'rules': details['rules'],
                        'parameters': details['parameters']
                    })
        
        if total_files % 500 == 0:
            print(f"Processed {total_files} files...")
    
    # Generate report
    report = f"""=== COMPREHENSIVE ACTIONS ANALYSIS ({total_files} files) ===

**Statistics:**
- Total BusinessClass files: {total_files:,}
- Files with Actions: {files_with_actions:,} ({files_with_actions/total_files*100:.1f}%)
- Files without Actions: {total_files-files_with_actions:,} ({(total_files-files_with_actions)/total_files*100:.1f}%)
- Total Actions found: {total_actions:,}
- Average actions per file (with actions): {total_actions/files_with_actions:.1f}

**Action Types Distribution:**"""
    
    for action_type, count in sorted(action_types.items(), key=lambda x: x[1], reverse=True):
        percentage = count/total_actions*100
        report += f"\n- {action_type}: {count:,} ({percentage:.1f}%)"
    
    report += f"""

**Action Characteristics:**
- Restricted Actions: {restricted_actions:,} ({restricted_actions/total_actions*100:.1f}%)
- Actions with Confirmation: {confirmation_actions:,} ({confirmation_actions/total_actions*100:.1f}%)

**Files by Action Count:**"""
    
    for count in sorted(files_by_action_count.keys(), reverse=True)[:10]:
        report += f"\n- {count} actions: {files_by_action_count[count]} files"
    
    # Top complex actions
    complex_actions.sort(key=lambda x: x['rules'], reverse=True)
    report += f"""

**Most Complex Actions (by rule count):**"""
    
    for action in complex_actions[:20]:
        report += f"\n- {action['file']}.{action['name']}: {action['rules']} rules, {action['parameters']} params"
    
    print(report)
    
    # Save to file
    with open("C:/Visual Basic Code/LPL Library/Outputs/all_actions_analysis.txt", 'w') as f:
        f.write(report)
    
    print(f"\nAnalysis complete. Results saved to Outputs/all_actions_analysis.txt")

if __name__ == "__main__":
    main()