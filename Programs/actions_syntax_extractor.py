import os
import re
from collections import defaultdict, Counter
from pathlib import Path

class ActionsSyntaxExtractor:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.true_actions = []
        self.action_types = Counter()
        self.action_attributes = Counter()
        self.parameter_patterns = Counter()
        self.rule_sections = Counter()
        self.syntax_examples = defaultdict(list)
        
    def find_businessclass_files(self):
        return list(self.base_dir.rglob("*.businessclass"))
    
    def extract_actions_section(self, content):
        # Find Actions section - more precise matching
        match = re.search(r'\n\s*Actions\s*\n(.*?)(?=\n\s*(?:Ontology|$))', content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1)
        
        # Fallback patterns
        patterns = [
            r'\n\s*Actions\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\s*\n|\Z)',
            r'Actions\s*\n(.*?)(?=\n[A-Z][a-zA-Z\s]*\s*\n|\Z)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def is_true_action(self, action_type):
        """Filter out non-action types like DerivedField, MessageField"""
        action_keywords = [
            'Action', 'Create Action', 'Update Action', 'Delete Action', 
            'Instance Action', 'Set Action', 'Purge Action', 'Import Action'
        ]
        return any(keyword in action_type for keyword in action_keywords)
    
    def parse_action_comprehensive(self, action_text, filename):
        """Parse action with comprehensive section extraction"""
        lines = [line.rstrip() for line in action_text.split('\n') if line.strip()]
        if not lines:
            return None
        
        # Find action header
        header_match = re.match(r'^\s*(\w+)\s+is\s+an?\s+(.+?)(?:\s*$)', lines[0])
        if not header_match:
            return None
        
        action_name = header_match.group(1)
        action_type = header_match.group(2).strip()
        
        # Filter out non-actions
        if not self.is_true_action(action_type):
            return None
        
        action_data = {
            'name': action_name,
            'type': action_type,
            'filename': filename,
            'full_text': action_text,
            'attributes': [],
            'sections': {},
            'parameters': [],
            'has_confirmation': False,
            'has_bod': False,
            'has_invoke': False,
            'has_background': False,
            'complexity_score': 0
        }
        
        # Parse content
        current_section = None
        section_content = []
        
        for line in lines[1:]:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Check for attributes (single words, not indented much)
            if re.match(r'^\s*\w+\s*$', line) and len(line) - len(line.lstrip()) <= 2:
                attr = stripped
                action_data['attributes'].append(attr)
                
                # Track special attributes
                if attr == 'restricted':
                    action_data['complexity_score'] += 1
                elif 'background' in attr.lower():
                    action_data['has_background'] = True
                    action_data['complexity_score'] += 2
                continue
            
            # Check for confirmation required
            if 'confirmation required' in line.lower():
                action_data['has_confirmation'] = True
                action_data['complexity_score'] += 2
            
            # Check for BOD/trigger patterns
            if any(keyword in line.lower() for keyword in ['bod', 'trigger', 'service']):
                action_data['has_bod'] = True
                action_data['complexity_score'] += 3
            
            # Check for invoke patterns
            if 'invoke' in line.lower():
                action_data['has_invoke'] = True
                action_data['complexity_score'] += 2
            
            # Check for section headers
            section_match = re.match(r'^\s*([A-Z][a-zA-Z\s]*)\s*$', line)
            if section_match and len(line) - len(line.lstrip()) <= 2:
                # Save previous section
                if current_section and section_content:
                    action_data['sections'][current_section] = '\n'.join(section_content)
                
                current_section = section_match.group(1).strip()
                section_content = []
                action_data['complexity_score'] += 1
                continue
            
            # Add to current section
            if current_section:
                section_content.append(line)
            else:
                # Content without section header
                if 'sections' not in action_data:
                    action_data['sections']['Main'] = []
                if 'Main' not in action_data['sections']:
                    action_data['sections']['Main'] = []
                if isinstance(action_data['sections']['Main'], list):
                    action_data['sections']['Main'].append(line)
        
        # Save final section
        if current_section and section_content:
            action_data['sections'][current_section] = '\n'.join(section_content)
        
        return action_data
    
    def analyze_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            actions_section = self.extract_actions_section(content)
            if not actions_section:
                return
            
            # Split into action blocks
            action_blocks = []
            current_block = []
            
            for line in actions_section.split('\n'):
                # Check if this starts a new action (not indented, has "is a/an")
                if re.match(r'^\s*\w+\s+is\s+an?\s+', line) and len(line) - len(line.lstrip()) <= 2:
                    if current_block:
                        action_blocks.append('\n'.join(current_block))
                    current_block = [line]
                else:
                    current_block.append(line)
            
            # Add final block
            if current_block:
                action_blocks.append('\n'.join(current_block))
            
            # Parse each action
            for block in action_blocks:
                if not block.strip():
                    continue
                
                action_data = self.parse_action_comprehensive(block, file_path.name)
                if action_data:
                    self.true_actions.append(action_data)
                    self.action_types[action_data['type']] += 1
                    
                    for attr in action_data['attributes']:
                        self.action_attributes[attr] += 1
                    
                    for section_name in action_data['sections']:
                        self.rule_sections[section_name] += 1
                    
                    # Collect examples by complexity and type
                    if action_data['complexity_score'] > 5:
                        self.syntax_examples['complex_actions'].append(action_data)
                    if action_data['has_bod']:
                        self.syntax_examples['bod_actions'].append(action_data)
                    if action_data['has_confirmation']:
                        self.syntax_examples['confirmation_actions'].append(action_data)
                    if len(action_data['sections']) > 2:
                        self.syntax_examples['multi_section'].append(action_data)
                    
                    # Collect best examples per type
                    self.syntax_examples[action_data['type']].append(action_data)
                        
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    def generate_syntax_report(self):
        total_actions = len(self.true_actions)
        files_with_actions = len(set(action['filename'] for action in self.true_actions))
        
        report = f"""=== COMPREHENSIVE ACTIONS SYNTAX PATTERNS ===

**ANALYSIS SUMMARY:**
- Total BusinessClass files analyzed: {len(self.find_businessclass_files())}
- Files with Actions: {files_with_actions} ({files_with_actions/4761*100:.1f}%)
- Total Actions found: {total_actions}
- Most common Action types: Create Action, Instance Action, Update Action, Delete Action, Set Action

**ACTION TYPES WITH USAGE STATISTICS:**
"""
        
        for i, (action_type, count) in enumerate(self.action_types.most_common(10), 1):
            percentage = (count / total_actions * 100) if total_actions > 0 else 0
            report += f"- **{action_type}:** {count} instances ({percentage:.1f}%) - "
            
            # Add description based on type
            if 'Create' in action_type:
                report += "Entity creation with validation\n"
            elif 'Instance' in action_type:
                report += "Single entity operations\n"
            elif 'Update' in action_type:
                report += "Entity modification\n"
            elif 'Delete' in action_type:
                report += "Entity removal\n"
            elif 'Set' in action_type:
                report += "Bulk operations with filtering\n"
            elif 'Purge' in action_type:
                report += "Data cleanup and archival\n"
            elif 'Import' in action_type:
                report += "Data import processing\n"
            else:
                report += "General business operations\n"
        
        report += "\n**ACTION ATTRIBUTES (MOST COMMON):**\n"
        for attr, count in self.action_attributes.most_common(15):
            report += f"- **{attr}:** {count} uses"
            if attr == 'restricted':
                report += " - Internal system use only\n"
            elif 'confirmation' in attr.lower():
                report += " - User confirmation prompts\n"
            elif 'background' in attr.lower():
                report += " - Asynchronous execution\n"
            elif 'error' in attr.lower():
                report += " - Error handling continuation\n"
            else:
                report += "\n"
        
        report += "\n**ACTION SECTIONS FREQUENCY:**\n"
        for section, count in self.rule_sections.most_common(15):
            report += f"- **{section}:** {count} occurrences\n"
        
        # Add comprehensive syntax examples
        report += "\n**COMPLETE ACTION TYPE SYNTAX SAMPLES:**\n\n"
        
        for action_type, count in self.action_types.most_common(8):
            examples = self.syntax_examples.get(action_type, [])
            if examples:
                # Sort by complexity to get best example
                examples.sort(key=lambda x: x['complexity_score'], reverse=True)
                best_example = examples[0]
                
                report += f"**{action_type.upper()}:**\n```lpl\n{best_example['full_text']}\n```\n\n"
        
        # Add pattern examples
        if self.syntax_examples['complex_actions']:
            report += "**COMPLEX ACTIONS WITH MULTIPLE SECTIONS:**\n"
            for action in sorted(self.syntax_examples['complex_actions'], 
                               key=lambda x: x['complexity_score'], reverse=True)[:3]:
                report += f"```lpl\n{action['full_text']}\n```\n\n"
        
        if self.syntax_examples['bod_actions']:
            report += "**BOD INTEGRATION PATTERNS:**\n"
            for action in self.syntax_examples['bod_actions'][:2]:
                report += f"```lpl\n{action['full_text']}\n```\n\n"
        
        if self.syntax_examples['confirmation_actions']:
            report += "**CONFIRMATION REQUIRED PATTERNS:**\n"
            for action in self.syntax_examples['confirmation_actions'][:2]:
                report += f"```lpl\n{action['full_text']}\n```\n\n"
        
        # Add statistics
        report += f"""**ACTION COMPLEXITY STATISTICS:**
- Actions with BOD Integration: {len([a for a in self.true_actions if a['has_bod']])}
- Actions with Confirmation: {len([a for a in self.true_actions if a['has_confirmation']])}
- Actions with Invoke Statements: {len([a for a in self.true_actions if a['has_invoke']])}
- Actions with Background Processing: {len([a for a in self.true_actions if a['has_background']])}
- Complex Actions (5+ complexity): {len([a for a in self.true_actions if a['complexity_score'] > 5])}
- Multi-section Actions: {len([a for a in self.true_actions if len(a['sections']) > 2])}

**ACTIONS SECTION PLACEMENT:**

Actions sections appear after other major sections in BusinessClass files:

```lpl
BusinessClassName is a BusinessClass
\towned by ParentEntity
\tprefix is PREFIX
\t
\tPersistent Fields
\t\t[field definitions]
\t
\tTransient Fields
\t\t[field definitions]
\t
\tLocal Fields
\t\t[field definitions]
\t
\tDerived Fields
\t\t[field definitions]
\t
\tConditions
\t\t[condition definitions]
\t
\tRelations
\t\t[relation definitions]
\t
\tSets
\t\t[set definitions]
\t
\tField Rules
\t\t[field validation rules]
\t
\tRule Blocks
\t\t[reusable rule blocks]
\t
\tActions
\t\t[action definitions]
```
"""
        
        return report
    
    def run_analysis(self):
        print("Finding BusinessClass files...")
        files = self.find_businessclass_files()
        print(f"Found {len(files)} BusinessClass files")
        
        print("Extracting Actions syntax patterns...")
        for i, file_path in enumerate(files, 1):
            if i % 300 == 0:
                print(f"Processed {i}/{len(files)} files...")
            self.analyze_file(file_path)
        
        print("Generating syntax report...")
        return self.generate_syntax_report()

if __name__ == "__main__":
    extractor = ActionsSyntaxExtractor("C:/Visual Basic Code/LPL Library/References/business class")
    report = extractor.run_analysis()
    
    # Save report
    output_path = "C:/Visual Basic Code/LPL Library/Outputs/actions_syntax_patterns.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Analysis complete! Report saved to: {output_path}")
    print(f"\nFound {len(extractor.true_actions)} true Actions across {len(set(a['filename'] for a in extractor.true_actions))} files")
    print(f"Top action types: {', '.join([f'{t}({c})' for t, c in extractor.action_types.most_common(5)])}")