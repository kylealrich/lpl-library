import os
import re
from collections import defaultdict

def analyze_conditions_in_file(file_path):
    """Extract conditions from a single BusinessClass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find Conditions section
        conditions_match = re.search(r'\tConditions\s*\n(.*?)(?=\n\t[A-Z]|\Z)', content, re.DOTALL)
        if not conditions_match:
            return []
        
        conditions_content = conditions_match.group(1)
        
        # Parse individual conditions
        condition_blocks = re.findall(r'\t\t([^\n\t]+)\n((?:\t\t\t[^\n]*\n?)*)', conditions_content)
        conditions = []
        for name, definition in condition_blocks:
            clean_def = re.sub(r'\n\t\t\t', ' ', definition.strip())
            is_restricted = 'restricted' in clean_def
            conditions.append((name.strip(), clean_def, is_restricted))
        
        return conditions
    except:
        return []

def analyze_all_conditions():
    """Analyze conditions across all BusinessClass files"""
    directory = r"C:\Visual Basic Code\LPL Library\References\business class"
    
    stats = {
        'total_files': 0,
        'files_with_conditions': 0,
        'total_conditions': 0,
        'restricted_conditions': 0,
        'condition_names': defaultdict(int),
        'files_by_condition_count': defaultdict(int)
    }
    
    detailed_results = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.businessclass'):
            stats['total_files'] += 1
            file_path = os.path.join(directory, filename)
            conditions = analyze_conditions_in_file(file_path)
            
            if conditions:
                stats['files_with_conditions'] += 1
                stats['total_conditions'] += len(conditions)
                stats['files_by_condition_count'][len(conditions)] += 1
                
                for name, definition, is_restricted in conditions:
                    stats['condition_names'][name] += 1
                    if is_restricted:
                        stats['restricted_conditions'] += 1
                
                detailed_results.append((filename, len(conditions), conditions))
    
    # Generate report
    report = "=== COMPREHENSIVE CONDITIONS ANALYSIS (ALL BUSINESSCLASS FILES) ===\n\n"
    report += f"**Statistics:**\n"
    report += f"- Total BusinessClass files: {stats['total_files']:,}\n"
    report += f"- Files with Conditions: {stats['files_with_conditions']:,} ({stats['files_with_conditions']/stats['total_files']*100:.1f}%)\n"
    report += f"- Files without Conditions: {stats['total_files']-stats['files_with_conditions']:,} ({(stats['total_files']-stats['files_with_conditions'])/stats['total_files']*100:.1f}%)\n"
    report += f"- Total Conditions found: {stats['total_conditions']:,}\n"
    report += f"- Restricted Conditions: {stats['restricted_conditions']:,} ({stats['restricted_conditions']/stats['total_conditions']*100:.1f}%)\n\n"
    
    # Top condition names
    report += "**Top 20 Most Common Condition Names:**\n"
    for i, (name, count) in enumerate(sorted(stats['condition_names'].items(), key=lambda x: x[1], reverse=True)[:20], 1):
        report += f"{i}. {name} ({count} files)\n"
    report += "\n"
    
    # Files by condition count
    report += "**Condition Count Distribution:**\n"
    for count in sorted(stats['files_by_condition_count'].keys()):
        files = stats['files_by_condition_count'][count]
        report += f"- {count} conditions: {files} files\n"
    report += "\n"
    
    # Top complex files
    detailed_results.sort(key=lambda x: x[1], reverse=True)
    report += "**Top 20 Most Complex Classes (Most Conditions):**\n"
    for i, (filename, count, conditions) in enumerate(detailed_results[:20], 1):
        class_name = filename.replace('.businessclass', '')
        report += f"{i}. {class_name} ({count} conditions)\n"
    
    return report

# Run analysis
print("Analyzing Conditions sections in all BusinessClass files...")
analysis = analyze_all_conditions()
print(analysis)

# Save to output file
output_path = r"C:\Visual Basic Code\LPL Library\Outputs\comprehensive_conditions_analysis.txt"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(analysis)

print(f"\nComprehensive analysis saved to: {output_path}")