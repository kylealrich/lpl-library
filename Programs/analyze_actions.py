import os
import re
from collections import defaultdict, Counter
from pathlib import Path

class ActionsAnalyzer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.actions_data = defaultdict(list)
        self.action_types = Counter()
        self.action_attributes = Counter()
        self.parameter_types = Counter()
        self.action_patterns = defaultdict(list)
        
    def find_businessclass_files(self):
        """Find all .businessclass files recursively"""
        return list(self.base_dir.rglob("*.businessclass"))
    
    def extract_actions_section(self, content):
        """Extract Actions section from BusinessClass content"""
        # Find Actions section
        actions_match = re.search(r'\n\s*Actions\s*\n(.*?)(?=\n\s*(?:[A-Z][a-zA-Z\s]*\n|\Z))', content, re.DOTALL | re.IGNORECASE)
        if actions_match:
            return actions_match.group(1)
        return None
    
    def parse_action_definition(self, action_text):
        """Parse individual action definition"""
        lines = action_text.strip().split('\n')
        if not lines:
            return None
            
        # Parse action header
        header_match = re.match(r'\s*(\w+)\s+is\s+an?\s+(.+?)(?:\s*$)', lines[0])
        if not header_match:
            return None
            
        action_name = header_match.group(1)
        action_type = header_match.group(2).strip()
        
        action_info = {
            'name': action_name,
            'type': action_type,
            'attributes': [],
            'parameters': [],
            'sections': {},
            'full_text': action_text
        }
        
        current_section = None
        section_content = []
        
        for line in lines[1:]:
            line = line.rstrip()
            if not line:
                continue
                
            # Check for attributes (single words at start of line)
            if re.match(r'^\s*\w+\s*$', line) and not line.strip().startswith('\t'):
                action_info['attributes'].append(line.strip())
                continue
                
            # Check for section headers
            section_match = re.match(r'^\s*([A-Z][a-zA-Z\s]*)\s*$', line)
            if section_match and not line.startswith('\t\t'):
                if current_section:
                    action_info['sections'][current_section] = '\n'.join(section_content)
                current_section = section_match.group(1).strip()
                section_content = []
                continue
                
            # Add content to current section
            if current_section:
                section_content.append(line)
        
        # Add final section
        if current_section and section_content:
            action_info['sections'][current_section] = '\n'.join(section_content)
            
        return action_info
    
    def parse_parameters(self, params_text):
        """Parse Parameters section"""
        parameters = []
        for line in params_text.split('\n'):
            param_match = re.match(r'\s*(\w+)\s+is\s+(.+)', line)
            if param_match:
                param_name = param_match.group(1)
                param_type = param_match.group(2).strip()
                parameters.append({'name': param_name, 'type': param_type})
        return parameters
    
    def analyze_file(self, file_path):
        """Analyze single BusinessClass file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            actions_section = self.extract_actions_section(content)
            if not actions_section:
                return
                
            # Split into individual actions
            action_blocks = re.split(r'\n(?=\s*\w+\s+is\s+an?\s+)', actions_section)
            
            for block in action_blocks:
                if not block.strip():
                    continue
                    
                action_info = self.parse_action_definition(block)
                if action_info:
                    self.actions_data[file_path.name].append(action_info)
                    self.action_types[action_info['type']] += 1
                    
                    for attr in action_info['attributes']:
                        self.action_attributes[attr] += 1
                    
                    # Parse parameters if present
                    if 'Parameters' in action_info['sections']:
                        params = self.parse_parameters(action_info['sections']['Parameters'])
                        action_info['parameters'] = params
                        for param in params:
                            self.parameter_types[param['type']] += 1
                    
                    # Store interesting patterns
                    if len(action_info['sections']) > 3:
                        self.action_patterns['complex_actions'].append(action_info)
                    if 'BOD' in block or 'trigger' in block.lower():
                        self.action_patterns['bod_integration'].append(action_info)
                    if 'confirmation required' in block.lower():
                        self.action_patterns['confirmation_actions'].append(action_info)
                        
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        total_files = len(self.actions_data)
        total_actions = sum(len(actions) for actions in self.actions_data.values())
        
        report = f"""=== COMPREHENSIVE ACTIONS ANALYSIS RESULTS ===

**ANALYSIS SUMMARY:**
- Total BusinessClass files analyzed: {len(self.find_businessclass_files())}
- Files with Actions: {total_files}
- Total Actions found: {total_actions}

**TOP ACTION TYPES BY FREQUENCY:**
"""
        
        for i, (action_type, count) in enumerate(self.action_types.most_common(10), 1):
            percentage = (count / total_actions * 100) if total_actions > 0 else 0
            report += f"{i}. {action_type}: {count} ({percentage:.1f}%)\n"
        
        report += "\n**MOST COMMON ACTION ATTRIBUTES:**\n"
        for attr, count in self.action_attributes.most_common(10):
            percentage = (count / total_actions * 100) if total_actions > 0 else 0
            report += f"- {attr}: {count} ({percentage:.1f}%)\n"
        
        report += "\n**PARAMETER TYPES ANALYSIS:**\n"
        for param_type, count in self.parameter_types.most_common(10):
            report += f"- {param_type}: {count}\n"
        
        # Add sample syntax for each action type
        report += "\n**COMPLETE ACTION TYPE SYNTAX SAMPLES:**\n\n"
        
        for action_type in self.action_types.most_common(8):
            type_name = action_type[0]
            # Find a good example of this action type
            example = None
            for file_actions in self.actions_data.values():
                for action in file_actions:
                    if action['type'] == type_name and len(action['sections']) > 0:
                        example = action
                        break
                if example:
                    break
            
            if example:
                report += f"**{type_name.upper()}:**\n```lpl\n{example['full_text'][:800]}{'...' if len(example['full_text']) > 800 else ''}\n```\n\n"
        
        # Add complex patterns
        if self.action_patterns['complex_actions']:
            report += "**COMPLEX ACTIONS WITH MULTIPLE SECTIONS:**\n"
            for action in self.action_patterns['complex_actions'][:3]:
                report += f"```lpl\n{action['full_text'][:600]}{'...' if len(action['full_text']) > 600 else ''}\n```\n\n"
        
        if self.action_patterns['bod_integration']:
            report += "**BOD INTEGRATION PATTERNS:**\n"
            for action in self.action_patterns['bod_integration'][:2]:
                report += f"```lpl\n{action['full_text'][:600]}{'...' if len(action['full_text']) > 600 else ''}\n```\n\n"
        
        return report
    
    def run_analysis(self):
        """Run complete analysis"""
        print("Finding BusinessClass files...")
        files = self.find_businessclass_files()
        print(f"Found {len(files)} BusinessClass files")
        
        print("Analyzing Actions sections...")
        for i, file_path in enumerate(files, 1):
            if i % 100 == 0:
                print(f"Processed {i}/{len(files)} files...")
            self.analyze_file(file_path)
        
        print("Generating report...")
        return self.generate_report()

if __name__ == "__main__":
    analyzer = ActionsAnalyzer("C:/Visual Basic Code/LPL Library/References/business class")
    report = analyzer.run_analysis()
    
    # Save report
    output_path = "C:/Visual Basic Code/LPL Library/Outputs/actions_analysis_report.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Analysis complete! Report saved to: {output_path}")
    print("\nSample findings:")
    print(report[:2000] + "..." if len(report) > 2000 else report)