import os
import re
from collections import defaultdict

def analyze_all_sets():
    """Analyze Sets sections in all .businessclass files"""
    
    directory = r"C:\Visual Basic Code\LPL Library\References\business class"
    
    # Statistics
    total_files = 0
    files_with_sets = 0
    total_sets = 0
    set_names = defaultdict(int)
    set_properties = defaultdict(int)
    
    # Results storage
    results = []
    
    # Process all .businessclass files
    for filename in os.listdir(directory):
        if not filename.endswith('.businessclass'):
            continue
            
        total_files += 1
        file_path = os.path.join(directory, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except:
            continue
        
        # Find Sets section
        sets_match = re.search(r'\n\tSets\n(.*?)(?=\n\t[A-Z]|\n[A-Z]|\Z)', content, re.DOTALL)
        
        if not sets_match:
            continue
            
        files_with_sets += 1
        sets_content = sets_match.group(1)
        
        # Parse sets
        file_sets = []
        lines = sets_content.split('\n')
        current_set = None
        
        for line in lines:
            line = line.rstrip()
            if not line or line.isspace():
                continue
                
            # Set name
            if re.match(r'\t\t[A-Za-z]', line):
                set_name = line.strip()
                current_set = {'name': set_name, 'properties': []}
                file_sets.append(current_set)
                set_names[set_name] += 1
                total_sets += 1
            # Properties
            elif current_set and line.startswith('\t\t\t'):
                prop = line.strip()
                current_set['properties'].append(prop)
                set_properties[prop] += 1
        
        if file_sets:
            results.append({'file': filename, 'sets': file_sets})
    
    # Output results
    print(f"=== COMPREHENSIVE SETS ANALYSIS ({total_files} files) ===\n")
    print(f"Files with Sets: {files_with_sets} ({files_with_sets/total_files*100:.1f}%)")
    print(f"Total Sets found: {total_sets}")
    
    print(f"\n=== TOP SET NAMES ===")
    for name, count in sorted(set_names.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"{name}: {count} files")
    
    print(f"\n=== TOP SET PROPERTIES ===")
    for prop, count in sorted(set_properties.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"{prop}: {count} occurrences")
    
    print(f"\n=== FILES WITH MOST SETS ===")
    results.sort(key=lambda x: len(x['sets']), reverse=True)
    for result in results[:10]:
        print(f"{result['file']}: {len(result['sets'])} sets")
    
    # Save detailed results
    output_file = r"C:\Visual Basic Code\LPL Library\Outputs\sets_analysis_complete.txt"
    with open(output_file, 'w') as f:
        f.write(f"COMPREHENSIVE SETS ANALYSIS - {total_files} BusinessClass Files\n")
        f.write("="*60 + "\n\n")
        f.write(f"Statistics:\n")
        f.write(f"- Total files: {total_files}\n")
        f.write(f"- Files with Sets: {files_with_sets} ({files_with_sets/total_files*100:.1f}%)\n")
        f.write(f"- Total Sets: {total_sets}\n\n")
        
        f.write("All Files with Sets:\n")
        f.write("-" * 40 + "\n")
        for result in results:
            f.write(f"\n{result['file']} ({len(result['sets'])} sets):\n")
            for s in result['sets']:
                f.write(f"  {s['name']}: {len(s['properties'])} properties\n")
                for prop in s['properties']:
                    f.write(f"    - {prop}\n")
    
    print(f"\nDetailed results saved to: {output_file}")

analyze_all_sets()