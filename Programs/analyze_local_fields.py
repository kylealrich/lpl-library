import os
import re

def analyze_local_fields(file_path):
    """Analyze Local Fields section of a BusinessClass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract BusinessClass name
        class_match = re.search(r'(\w+)\s+is\s+a\s+BusinessClass', content)
        class_name = class_match.group(1) if class_match else "Unknown"
        
        # Find Local Fields section
        local_fields_match = re.search(r'\tLocal Fields\n(.*?)(?=\n\t[A-Z]|\n[A-Z]|\Z)', content, re.DOTALL)
        
        if not local_fields_match:
            return f"=== LOCAL FIELDS ANALYSIS - {class_name.upper()}.BUSINESSCLASS ===\n\n**No Local Fields section found**\n"
        
        local_fields_content = local_fields_match.group(1)
        
        # Count fields (lines starting with tabs followed by field names)
        field_lines = re.findall(r'\n\t\t([A-Za-z][A-Za-z0-9_]*)', local_fields_content)
        field_count = len(field_lines)
        
        # Categorize fields by type patterns
        categories = {
            'BOD Integration': [],
            'Error Handling': [],
            'Processing Control': [],
            'Configuration': [],
            'Reference Fields': [],
            'Text Processing': [],
            'Financial': [],
            'Other': []
        }
        
        # Analyze each field
        for field in field_lines:
            field_lower = field.lower()
            if 'bod' in field_lower or 'tracker' in field_lower:
                categories['BOD Integration'].append(field)
            elif 'error' in field_lower:
                categories['Error Handling'].append(field)
            elif 'local' in field_lower and ('execute' in field_lower or 'action' in field_lower or 'trigger' in field_lower):
                categories['Processing Control'].append(field)
            elif 'config' in field_lower or 'parameter' in field_lower:
                categories['Configuration'].append(field)
            elif 'local' in field_lower and ('view' in field_lower or field_lower.startswith('local') and any(x in field_lower for x in ['rel', 'reference'])):
                categories['Reference Fields'].append(field)
            elif 'text' in field_lower or 'title' in field_lower or 'message' in field_lower:
                categories['Text Processing'].append(field)
            elif 'amount' in field_lower or 'total' in field_lower or 'currency' in field_lower:
                categories['Financial'].append(field)
            else:
                categories['Other'].append(field)
        
        # Build analysis
        analysis = f"=== LOCAL FIELDS ANALYSIS - {class_name.upper()}.BUSINESSCLASS ===\n\n"
        analysis += f"**Local Fields Section ({field_count} fields):**\n"
        
        if field_count == 0:
            analysis += "- No local fields defined\n"
        else:
            analysis += "- Internal processing and temporary data storage\n"
            
            # Add categories with fields
            active_categories = {k: v for k, v in categories.items() if v}
            if active_categories:
                analysis += "\n**Field Categories:**\n"
                for i, (cat, fields) in enumerate(active_categories.items(), 1):
                    analysis += f"{i}. **{cat}** - {', '.join(fields[:3])}"
                    if len(fields) > 3:
                        analysis += f" (and {len(fields)-3} more)"
                    analysis += "\n"
            
            # Extract notable patterns
            notable_fields = []
            for field in field_lines[:5]:  # Top 5 fields
                if any(x in field.lower() for x in ['view', 'tracker', 'template', 'config']):
                    notable_fields.append(field)
            
            if notable_fields:
                analysis += "\n**Notable Fields:**\n"
                for field in notable_fields:
                    analysis += f"- {field}\n"
        
        return analysis + "\n"
        
    except Exception as e:
        return f"=== ERROR ANALYZING {file_path} ===\n{str(e)}\n\n"

def main():
    """Process all .businessclass files and update knowledge base"""
    references_dir = r"c:\Visual Basic Code\LPL Library\References\business class"
    knowledge_file = r"c:\Visual Basic Code\LPL Library\Knowledge.txt"
    
    # Get all .businessclass files
    businessclass_files = []
    for file in os.listdir(references_dir):
        if file.endswith('.businessclass'):
            businessclass_files.append(os.path.join(references_dir, file))
    
    print(f"Found {len(businessclass_files)} .businessclass files")
    
    # Read current knowledge base
    with open(knowledge_file, 'r', encoding='utf-8') as f:
        knowledge_content = f.read()
    
    # Process each file
    all_analyses = []
    processed_files = []
    
    for i, file_path in enumerate(businessclass_files, 1):
        filename = os.path.basename(file_path)
        print(f"Processing {i}/{len(businessclass_files)}: {filename}")
        
        # Skip already analyzed files
        if filename.replace('.businessclass', '').upper() in knowledge_content:
            print(f"  Skipping {filename} - already analyzed")
            continue
            
        analysis = analyze_local_fields(file_path)
        all_analyses.append(analysis)
        processed_files.append(filename)
        
        # Update knowledge base every 10 files
        if len(all_analyses) >= 10:
            insert_point = knowledge_content.find("=== CURRENT SESSION ===")
            if insert_point != -1:
                new_content = (knowledge_content[:insert_point] + 
                             "".join(all_analyses) + 
                             knowledge_content[insert_point:])
                
                with open(knowledge_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                knowledge_content = new_content
                all_analyses = []
                print(f"  Updated knowledge base with {len(processed_files)} files")
    
    # Final update
    if all_analyses:
        insert_point = knowledge_content.find("=== CURRENT SESSION ===")
        if insert_point != -1:
            new_content = (knowledge_content[:insert_point] + 
                         "".join(all_analyses) + 
                         knowledge_content[insert_point:])
            
            with open(knowledge_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
    
    print(f"Completed analysis of {len(processed_files)} new files")

if __name__ == "__main__":
    main()