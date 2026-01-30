import os
import re
from collections import defaultdict

def analyze_field_rules_all():
    """Analyze Field Rules sections from all .businessclass files"""
    directory = r"C:\Visual Basic Code\LPL Library\References\business class"
    
    results = {
        'total_files': 0,
        'files_with_rules': 0,
        'total_rules': 0,
        'constraint_types': defaultdict(int),
        'error_patterns': defaultdict(int),
        'files_by_rule_count': defaultdict(int),
        'top_files': []
    }
    
    for filename in os.listdir(directory):
        if not filename.endswith('.businessclass'):
            continue
            
        results['total_files'] += 1
        file_path = os.path.join(directory, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Find Field Rules section
            field_rules_match = re.search(r'Field Rules\s*\n(.*?)(?=\n[A-Z][a-zA-Z\s]*\n|\nend\s|\Z)', content, re.DOTALL)
            
            if not field_rules_match:
                continue
                
            results['files_with_rules'] += 1
            field_rules_content = field_rules_match.group(1)
            
            # Count rules and analyze patterns
            rule_count = 0
            for line in field_rules_content.split('\n'):
                line = line.strip()
                if not line or line.startswith('\t'):
                    continue
                rule_count += 1
                
                # Analyze constraint types
                if 'constraint' in line.lower():
                    if 'matches' in line:
                        results['constraint_types']['matches'] += 1
                    elif 'exists' in line:
                        results['constraint_types']['exists'] += 1
                    elif '=' in line:
                        results['constraint_types']['equality'] += 1
                    else:
                        results['constraint_types']['other'] += 1
                
                if 'required' in line.lower():
                    results['constraint_types']['required'] += 1
                if 'default to' in line.lower():
                    results['constraint_types']['default'] += 1
            
            # Analyze error message patterns
            error_messages = re.findall(r'"([^"]*)"', field_rules_content)
            for msg in error_messages:
                if '<' in msg and '>' in msg:
                    results['error_patterns']['dynamic'] += 1
                else:
                    results['error_patterns']['static'] += 1
            
            results['total_rules'] += rule_count
            results['files_by_rule_count'][rule_count] += 1
            
            if rule_count > 0:
                results['top_files'].append((filename, rule_count))
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Sort top files by rule count
    results['top_files'].sort(key=lambda x: x[1], reverse=True)
    results['top_files'] = results['top_files'][:20]  # Top 20
    
    return results

def display_results(results):
    """Display comprehensive Field Rules analysis results"""
    print("COMPREHENSIVE FIELD RULES ANALYSIS")
    print("=" * 50)
    print(f"Total BusinessClass files: {results['total_files']:,}")
    print(f"Files with Field Rules: {results['files_with_rules']:,} ({results['files_with_rules']/results['total_files']*100:.1f}%)")
    print(f"Files without Field Rules: {results['total_files']-results['files_with_rules']:,} ({(results['total_files']-results['files_with_rules'])/results['total_files']*100:.1f}%)")
    print(f"Total Field Rules found: {results['total_rules']:,}")
    print()
    
    print("TOP FILES BY FIELD RULE COUNT:")
    for i, (filename, count) in enumerate(results['top_files'], 1):
        print(f"{i:2d}. {filename:<40} ({count:3d} rules)")
    print()
    
    print("CONSTRAINT TYPE DISTRIBUTION:")
    total_constraints = sum(results['constraint_types'].values())
    for constraint_type, count in sorted(results['constraint_types'].items(), key=lambda x: x[1], reverse=True):
        pct = count/total_constraints*100 if total_constraints > 0 else 0
        print(f"  {constraint_type:<12}: {count:4d} ({pct:4.1f}%)")
    print()
    
    print("ERROR MESSAGE PATTERNS:")
    total_errors = sum(results['error_patterns'].values())
    for pattern, count in results['error_patterns'].items():
        pct = count/total_errors*100 if total_errors > 0 else 0
        print(f"  {pattern:<12}: {count:4d} ({pct:4.1f}%)")
    print()
    
    print("FIELD RULES COUNT DISTRIBUTION:")
    for rule_count in sorted(results['files_by_rule_count'].keys()):
        file_count = results['files_by_rule_count'][rule_count]
        print(f"  {rule_count:3d} rules: {file_count:3d} files")

if __name__ == "__main__":
    results = analyze_field_rules_all()
    display_results(results)
    
    # Save detailed results
    output_file = r"C:\Visual Basic Code\LPL Library\Outputs\All_Field_Rules_Analysis.txt"
    with open(output_file, 'w') as f:
        f.write("COMPREHENSIVE FIELD RULES ANALYSIS - ALL BUSINESSCLASS FILES\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Analysis Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("SUMMARY STATISTICS:\n")
        f.write(f"- Total BusinessClass files: {results['total_files']:,}\n")
        f.write(f"- Files with Field Rules: {results['files_with_rules']:,} ({results['files_with_rules']/results['total_files']*100:.1f}%)\n")
        f.write(f"- Total Field Rules: {results['total_rules']:,}\n")
        f.write(f"- Average rules per file (with rules): {results['total_rules']/results['files_with_rules']:.1f}\n\n")
        
        f.write("TOP 20 FILES BY FIELD RULE COUNT:\n")
        for i, (filename, count) in enumerate(results['top_files'], 1):
            f.write(f"{i:2d}. {filename:<50} {count:3d} rules\n")
        
        f.write(f"\nCONSTRAINT TYPES: {dict(results['constraint_types'])}\n")
        f.write(f"ERROR PATTERNS: {dict(results['error_patterns'])}\n")
    
    print(f"\nDetailed results saved to: {output_file}")