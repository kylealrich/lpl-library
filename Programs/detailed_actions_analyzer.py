import os
import re
from collections import defaultdict, Counter
from pathlib import Path

class DetailedActionsAnalyzer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.all_actions = []
        self.action_types = Counter()
        self.action_attributes = Counter()
        self.parameter_patterns = Counter()
        self.rule_patterns = Counter()
        self.complex_examples = defaultdict(list)
        
    def find_businessclass_files(self):
        return list(self.base_dir.rglob("*.businessclass"))
    
    def extract_actions_section(self, content):
        # More robust Actions section extraction
        patterns = [
            r'\nActions\s*\n(.*?)(?=\n[A-Z][a-zA-Z\s]*\n|\Z)',
            r'\n\s*Actions\s*\n(.*?)(?=\n\s*[A-Z][a-zA-Z\s]*\n|\Z)',
            r'Actions\s*\n(.*?)(?=\n[A-Z][a-zA-Z\s]*\n|\Z)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def parse_action_block(self, action_text, filename):
        """Parse complete action block with all sections"""
        lines = [line.rstrip() for line in action_text.split('\n')]
        if not lines or not lines[0].strip():
            return None
        
        # Find action header
        header_line = None
        for i, line in enumerate(lines):
            if re.match(r'^\s*\w+\s+is\s+an?\s+', line):
                header_line = line
                break
        
        if not header_line:
            return None
        
        # Parse header
        header_match = re.match(r'^\s*(\w+)\s+is\s+an?\s+(.+?)(?:\s*$)', header_line)
        if not header_match:
            return None
        
        action_name = header_match.group(1)
        action_type = header_match.group(2).strip()
        
        action_data = {
            'name': action_name,
            'type': action_type,
            'filename': filename,
            'full_text': action_text,
            'attributes': [],
            'parameters': [],
            'sections': {},
            'has_confirmation': 'confirmation required' in action_text.lower(),
            'has_bod': 'BOD' in action_text or 'trigger' in action_text.lower(),
            'has_invoke': 'invoke' in action_text.lower(),
            'has_parameters': 'Parameters' in action_text,
            'line_count': len([l for l in lines if l.strip()])
        }
        
        # Parse sections and attributes
        current_section = None
        section_lines = []
        indent_level = 0
        
        for line in lines[1:]:  # Skip header
            if not line.strip():
                continue
            
            line_indent = len(line) - len(line.lstrip())
            
            # Check for single-word attributes (restricted, etc.)
            if re.match(r'^\s*\w+\s*$', line) and line_indent <= 1:
                action_data['attributes'].append(line.strip())
                continue
            
            # Check for section headers
            if re.match(r'^\s*[A-Z][a-zA-Z\s]*\s*$', line) and line_indent <= 1:
                # Save previous section
                if current_section and section_lines:
                    action_data['sections'][current_section] = '\n'.join(section_lines)
                
                current_section = line.strip()
                section_lines = []
                continue
            
            # Add to current section
            if current_section:
                section_lines.append(line)
        
        # Save final section
        if current_section and section_lines:
            action_data['sections'][current_section] = '\n'.join(section_lines)
        
        return action_data
    
    def analyze_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            actions_section = self.extract_actions_section(content)
            if not actions_section:
                return
            
            # Split into action blocks more carefully
            action_blocks = []
            current_block = []
            
            for line in actions_section.split('\n'):
                # Check if this starts a new action
                if re.match(r'^\s*\w+\s+is\s+an?\s+', line) and current_block:
                    action_blocks.append('\n'.join(current_block))
                    current_block = [line]
                else:
                    current_block.append(line)
            
            # Add final block
            if current_block:
                action_blocks.append('\n'.join(current_block))
            
            # Parse each action block
            for block in action_blocks:
                if not block.strip():
                    continue
                
                action_data = self.parse_action_block(block, file_path.name)
                if action_data:
                    self.all_actions.append(action_data)
                    self.action_types[action_data['type']] += 1
                    
                    for attr in action_data['attributes']:
                        self.action_attributes[attr] += 1
                    
                    # Collect patterns
                    for section_name, section_content in action_data['sections'].items():
                        self.rule_patterns[section_name] += 1
                        
                        # Extract parameter patterns
                        if section_name == 'Parameters':
                            for line in section_content.split('\n'):
                                param_match = re.search(r'is\s+(.*?)(?:\s|$)', line)
                                if param_match:
                                    self.parameter_patterns[param_match.group(1).strip()] += 1
                    
                    # Collect complex examples
                    if action_data['line_count'] > 10:
                        self.complex_examples['large_actions'].append(action_data)
                    if action_data['has_bod']:
                        self.complex_examples['bod_actions'].append(action_data)
                    if action_data['has_confirmation']:
                        self.complex_examples['confirmation_actions'].append(action_data)
                    if len(action_data['sections']) > 3:
                        self.complex_examples['multi_section_actions'].append(action_data)
                        
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    def generate_comprehensive_report(self):
        total_actions = len(self.all_actions)
        files_with_actions = len(set(action['filename'] for action in self.all_actions))
        
        report = f"""=== COMPREHENSIVE ACTIONS SYNTAX ANALYSIS ===

**ANALYSIS SUMMARY:**
- Total BusinessClass files analyzed: {len(self.find_businessclass_files())}
- Files with Actions: {files_with_actions} ({files_with_actions/4761*100:.1f}%)
- Total Actions found: {total_actions}
- Most common Action types: {', '.join([f"{t} ({c})" for t, c in self.action_types.most_common(5)])}

**TOP ACTION TYPES BY FREQUENCY:**
"""
        
        for i, (action_type, count) in enumerate(self.action_types.most_common(10), 1):
            percentage = (count / total_actions * 100) if total_actions > 0 else 0
            report += f"{i}. {action_type}: {count} ({percentage:.1f}%)\n"
        
        report += "\n**MOST COMMON ACTION ATTRIBUTES:**\n"
        for attr, count in self.action_attributes.most_common(15):
            percentage = (count / total_actions * 100) if total_actions > 0 else 0
            report += f"- {attr}: {count} ({percentage:.1f}%)\n"
        
        report += "\n**PARAMETER TYPES ANALYSIS:**\n"
        for param_type, count in self.parameter_patterns.most_common(15):
            report += f"- {param_type}: {count}\n"
        
        report += "\n**ACTION SECTIONS FREQUENCY:**\n"
        for section, count in self.rule_patterns.most_common(15):
            report += f"- {section}: {count}\n"
        
        # Add detailed syntax examples for each action type
        report += "\n**COMPLETE ACTION TYPE SYNTAX SAMPLES:**\n\n"
        
        for action_type, count in self.action_types.most_common(8):
            # Find best example for this type
            examples = [a for a in self.all_actions if a['type'] == action_type]
            if examples:
                # Sort by complexity (more sections = better example)
                examples.sort(key=lambda x: len(x['sections']), reverse=True)
                best_example = examples[0]
                
                report += f"**{action_type.upper()}:**\n```lpl\n{best_example['full_text'][:1000]}\n```\n\n"
        
        # Add complex pattern examples
        if self.complex_examples['bod_actions']:
            report += "**BOD INTEGRATION PATTERNS:**\n"
            for action in self.complex_examples['bod_actions'][:3]:
                report += f"```lpl\n{action['full_text'][:800]}\n```\n\n"
        
        if self.complex_examples['confirmation_actions']:
            report += "**CONFIRMATION REQUIRED PATTERNS:**\n"
            for action in self.complex_examples['confirmation_actions'][:2]:
                report += f"```lpl\n{action['full_text'][:600]}\n```\n\n"
        
        if self.complex_examples['multi_section_actions']:
            report += "**MULTI-SECTION COMPLEX ACTIONS:**\n"
            for action in self.complex_examples['multi_section_actions'][:3]:
                report += f"```lpl\n{action['full_text'][:800]}\n```\n\n"
        
        # Add statistics
        report += f"""**ACTION COMPLEXITY STATISTICS:**
- Actions with Parameters: {len([a for a in self.all_actions if a['has_parameters']])}
- Actions with BOD Integration: {len([a for a in self.all_actions if a['has_bod']])}
- Actions with Confirmation: {len([a for a in self.all_actions if a['has_confirmation']])}
- Actions with Invoke Statements: {len([a for a in self.all_actions if a['has_invoke']])}
- Large Actions (10+ lines): {len([a for a in self.all_actions if a['line_count'] > 10])}
"""
        
        return report
    
    def run_analysis(self):
        print("Finding BusinessClass files...")
        files = self.find_businessclass_files()
        print(f"Found {len(files)} BusinessClass files")
        
        print("Analyzing Actions sections...")
        for i, file_path in enumerate(files, 1):
            if i % 200 == 0:
                print(f"Processed {i}/{len(files)} files...")
            self.analyze_file(file_path)
        
        print("Generating comprehensive report...")
        return self.generate_comprehensive_report()

if __name__ == "__main__":
    analyzer = DetailedActionsAnalyzer("C:/Visual Basic Code/LPL Library/References/business class")
    report = analyzer.run_analysis()
    
    # Save report
    output_path = "C:/Visual Basic Code/LPL Library/Outputs/detailed_actions_analysis.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Analysis complete! Report saved to: {output_path}")
    print("\nKey findings:")
    print(report[:1500] + "..." if len(report) > 1500 else report)