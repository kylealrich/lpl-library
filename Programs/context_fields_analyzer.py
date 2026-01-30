import os
import re

def analyze_context_fields(file_path):
    """Extract and analyze Context Fields section from a businessclass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract business class name
        class_match = re.search(r'^(\w+)\s+is\s+a\s+BusinessClass', content, re.MULTILINE)
        class_name = class_match.group(1) if class_match else "UNKNOWN"
        
        # Find Context Fields section
        context_match = re.search(r'\n\s*Context Fields\s*\n(.*?)(?=\n\s*(?:Local Fields|Derived Fields|Transient Fields|Persistent Fields|Rule Blocks|Relations|Sets|Field Rules|Conditions|Actions|$))', content, re.DOTALL)
        
        if not context_match:
            return f"=== CONTEXT FIELDS ANALYSIS - {class_name.upper()}.BUSINESSCLASS ===\n\n**No Context Fields section found**"
        
        context_content = context_match.group(1).strip()
        if not context_content:
            return f"=== CONTEXT FIELDS ANALYSIS - {class_name.upper()}.BUSINESSCLASS ===\n\n**Context Fields Section (0 fields):**\n- No context fields defined"
        
        # Parse fields
        field_lines = [line.strip() for line in context_content.split('\n') if line.strip() and not line.strip().startswith('\t\t')]
        fields = []
        
        for line in field_lines:
            if '\t' in line:
                field_name = line.split('\t')[0].strip()
                if field_name and not field_name.startswith('is '):
                    fields.append(line.strip())
        
        field_count = len(fields)
        
        # Generate analysis
        analysis = f"=== CONTEXT FIELDS ANALYSIS - {class_name.upper()}.BUSINESSCLASS ===\n\n"
        analysis += f"**Context Fields Section ({field_count} fields):**\n"
        
        if field_count == 0:
            analysis += "- No context fields defined"
        else:
            analysis += "- Internal processing and temporary data storage\n\n"
            analysis += "**Field Categories:**\n"
            
            # Categorize fields
            categories = {}
            for field in fields:
                if any(keyword in field.lower() for keyword in ['date', 'range']):
                    categories.setdefault('Date/Range Fields', []).append(field)
                elif any(keyword in field.lower() for keyword in ['accounting', 'finance', 'dimension', 'project', 'account']):
                    categories.setdefault('Financial Fields', []).append(field)
                elif any(keyword in field.lower() for keyword in ['bod', 'tracker', 'integration']):
                    categories.setdefault('BOD Integration', []).append(field)
                elif any(keyword in field.lower() for keyword in ['audit']):
                    categories.setdefault('Audit Fields', []).append(field)
                else:
                    categories.setdefault('Other', []).append(field)
            
            for i, (category, field_list) in enumerate(categories.items(), 1):
                field_names = [f.split('\t')[0].strip() for f in field_list[:3]]
                remaining = len(field_list) - 3
                if remaining > 0:
                    field_names.append(f"and {remaining} more")
                analysis += f"{i}. **{category}** - {', '.join(field_names)}\n"
        
        return analysis
        
    except Exception as e:
        return f"=== CONTEXT FIELDS ANALYSIS - ERROR ===\n\n**Error analyzing {file_path}:** {str(e)}"

def main():
    """Process all businessclass files and update knowledge base"""
    base_path = r"c:\Visual Basic Code\LPL Library\References\business class"
    knowledge_file = r"c:\Visual Basic Code\LPL Library\Knowledge.txt"
    
    # Get all businessclass files
    files = [f for f in os.listdir(base_path) if f.endswith('.businessclass')]
    files.sort()
    
    # Skip already analyzed files
    skip_files = {'Requisition.businessclass', 'Requester.businessclass'}
    files = [f for f in files if f not in skip_files]
    
    print(f"Found {len(files)} businessclass files to analyze")
    
    # Process each file
    for i, filename in enumerate(files, 1):
        file_path = os.path.join(base_path, filename)
        print(f"Processing {i}/{len(files)}: {filename}")
        
        analysis = analyze_context_fields(file_path)
        
        # Append to knowledge file
        with open(knowledge_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{analysis}\n")
    
    print(f"Analysis complete. Updated {knowledge_file}")

if __name__ == "__main__":
    main()