import os
import re
from collections import defaultdict

def extract_relations_section(content):
    """Extract Relations section from businessclass content"""
    relations_match = re.search(r'\tRelations\n(.*?)(?=\n\t[A-Z]|\n[A-Z]|$)', content, re.DOTALL)
    if not relations_match:
        return []
    
    relations_content = relations_match.group(1)
    relations = []
    current_relation = None
    
    for line in relations_content.split('\n'):
        line = line.rstrip()
        if not line:
            continue
            
        if line.startswith('\t\t') and not line.startswith('\t\t\t'):
            if current_relation:
                relations.append(current_relation)
            
            relation_name = line.strip()
            current_relation = {
                'name': relation_name,
                'type': None,
                'target': None,
                'field_mapping': [],
                'instance_selection': []
            }
        
        elif line.strip().startswith('one-to-'):
            parts = line.strip().split(' relation to ')
            current_relation['type'] = parts[0]
            current_relation['target'] = parts[1] if len(parts) > 1 else ''
        
        elif 'Field Mapping' in line:
            mapping_type = line.split('uses ')[-1] if 'uses ' in line else 'default'
            current_relation['mapping_type'] = mapping_type
        
        elif line.strip().startswith('related.'):
            current_relation['field_mapping'].append(line.strip())
        
        elif line.strip().startswith('where ('):
            current_relation['instance_selection'].append(line.strip())
    
    if current_relation:
        relations.append(current_relation)
    
    return relations

def analyze_all_relations():
    """Analyze Relations sections in all .businessclass files"""
    
    directory = r"C:\Visual Basic Code\LPL Library\References\business class"
    
    # Statistics
    total_files = 0
    files_with_relations = 0
    total_relations = 0
    
    # Aggregated data
    relation_types = defaultdict(int)
    target_entities = defaultdict(int)
    mapping_types = defaultdict(int)
    
    # Complex classes
    complex_classes = []
    
    print("Analyzing Relations sections in all .businessclass files...")
    
    for filename in os.listdir(directory):
        if not filename.endswith('.businessclass'):
            continue
            
        total_files += 1
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            relations = extract_relations_section(content)
            
            if relations:
                files_with_relations += 1
                relation_count = len(relations)
                total_relations += relation_count
                
                if relation_count >= 10:
                    complex_classes.append((filename, relation_count))
                
                for rel in relations:
                    rel_type = rel.get('type') or 'set/unknown'
                    target = rel.get('target') or 'set/unknown'
                    mapping = rel.get('mapping_type') or 'none'
                    
                    relation_types[rel_type] += 1
                    target_entities[target] += 1
                    mapping_types[mapping] += 1
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Results
    print(f"\n=== COMPREHENSIVE RELATIONS ANALYSIS ({total_files} files) ===\n")
    print(f"Total BusinessClass files: {total_files}")
    print(f"Files with Relations: {files_with_relations} ({files_with_relations/total_files*100:.1f}%)")
    print(f"Files without Relations: {total_files - files_with_relations} ({(total_files-files_with_relations)/total_files*100:.1f}%)")
    print(f"Total Relations found: {total_relations}")
    
    print(f"\n**Top 20 Relation Types:**")
    for rtype, count in sorted(relation_types.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {rtype}: {count}")
    
    print(f"\n**Top 20 Target Entities:**")
    for target, count in sorted(target_entities.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {target}: {count}")
    
    print(f"\n**Top 10 Mapping Types:**")
    for mapping, count in sorted(mapping_types.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {mapping}: {count}")
    
    print(f"\n**Top 20 Complex Classes (10+ Relations):**")
    for filename, count in sorted(complex_classes, key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {filename}: {count} relations")
    
    # Save detailed results
    output_file = r"C:\Visual Basic Code\LPL Library\Outputs\comprehensive_relations_analysis.txt"
    with open(output_file, 'w') as f:
        f.write(f"=== COMPREHENSIVE RELATIONS ANALYSIS ({total_files} files) ===\n\n")
        f.write(f"Statistics:\n")
        f.write(f"- Total BusinessClass files: {total_files}\n")
        f.write(f"- Files with Relations: {files_with_relations} ({files_with_relations/total_files*100:.1f}%)\n")
        f.write(f"- Files without Relations: {total_files - files_with_relations} ({(total_files-files_with_relations)/total_files*100:.1f}%)\n")
        f.write(f"- Total Relations found: {total_relations}\n\n")
        
        f.write("Relation Type Distribution:\n")
        for rtype, count in sorted(relation_types.items(), key=lambda x: x[1], reverse=True):
            f.write(f"  {rtype}: {count}\n")
        
        f.write("\nTarget Entity Distribution:\n")
        for target, count in sorted(target_entities.items(), key=lambda x: x[1], reverse=True):
            f.write(f"  {target}: {count}\n")
        
        f.write("\nMapping Type Distribution:\n")
        for mapping, count in sorted(mapping_types.items(), key=lambda x: x[1], reverse=True):
            f.write(f"  {mapping}: {count}\n")
        
        f.write(f"\nComplex Classes ({len(complex_classes)} classes with 10+ relations):\n")
        for filename, count in sorted(complex_classes, key=lambda x: x[1], reverse=True):
            f.write(f"  {filename}: {count} relations\n")
    
    print(f"\nDetailed analysis saved to: {output_file}")

if __name__ == "__main__":
    analyze_all_relations()