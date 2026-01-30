import re

def extract_relations_section(file_path):
    """Extract and analyze the Relations section from Account.businessclass"""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find Relations section
    relations_match = re.search(r'\tRelations\n(.*?)(?=\n\t[A-Z]|\n[A-Z]|$)', content, re.DOTALL)
    
    if not relations_match:
        print("No Relations section found")
        return
    
    relations_content = relations_match.group(1)
    
    # Parse individual relations
    relations = []
    current_relation = None
    
    for line in relations_content.split('\n'):
        line = line.rstrip()
        if not line:
            continue
            
        # New relation starts
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
        
        # Relation type and target
        elif line.strip().startswith('one-to-'):
            parts = line.strip().split(' relation to ')
            current_relation['type'] = parts[0]
            current_relation['target'] = parts[1] if len(parts) > 1 else ''
        
        # Field mapping
        elif 'Field Mapping' in line:
            mapping_type = line.split('uses ')[-1] if 'uses ' in line else 'default'
            current_relation['mapping_type'] = mapping_type
        
        elif line.strip().startswith('related.'):
            current_relation['field_mapping'].append(line.strip())
        
        # Instance selection
        elif line.strip().startswith('where ('):
            current_relation['instance_selection'].append(line.strip())
    
    # Add last relation
    if current_relation:
        relations.append(current_relation)
    
    return relations

def analyze_relations(relations):
    """Analyze the relations data"""
    
    print("=== ACCOUNT RELATIONS ANALYSIS ===\n")
    print(f"Total Relations: {len(relations)}\n")
    
    # Categorize by type
    relation_types = {}
    targets = {}
    
    for rel in relations:
        rel_type = rel.get('type') or 'unknown'
        target = rel.get('target') or 'unknown'
        
        relation_types[rel_type] = relation_types.get(rel_type, 0) + 1
        targets[target] = targets.get(target, 0) + 1
    
    print("RELATION TYPES:")
    for rtype, count in sorted(relation_types.items(), key=lambda x: x[0] or ''):
        print(f"  {rtype}: {count}")
    
    print("\nTARGET ENTITIES:")
    for target, count in sorted(targets.items(), key=lambda x: x[0] or ''):
        print(f"  {target}: {count}")
    
    print("\nDETAILED RELATIONS:")
    for i, rel in enumerate(relations, 1):
        print(f"\n{i}. {rel['name']}")
        print(f"   Type: {rel.get('type', 'N/A')}")
        print(f"   Target: {rel.get('target', 'N/A')}")
        
        if rel.get('mapping_type'):
            print(f"   Mapping: {rel['mapping_type']}")
        
        if rel['field_mapping']:
            print("   Field Mappings:")
            for mapping in rel['field_mapping']:
                print(f"     {mapping}")
        
        if rel['instance_selection']:
            print("   Instance Selection:")
            for selection in rel['instance_selection']:
                print(f"     {selection}")

# Main execution
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\Account.businessclass"
relations = extract_relations_section(file_path)

if relations:
    analyze_relations(relations)
else:
    print("No relations found to analyze")