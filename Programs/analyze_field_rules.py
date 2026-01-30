import re

def analyze_field_rules(file_path):
    """Analyze Field Rules section from Account.businessclass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find Field Rules section
        field_rules_match = re.search(r'Field Rules\s*\n(.*?)(?=\n[A-Z][a-zA-Z\s]*\n|\nend\s|\Z)', content, re.DOTALL)
        
        if not field_rules_match:
            print("No Field Rules section found in Account.businessclass")
            return
        
        field_rules_content = field_rules_match.group(1)
        
        # Parse field rules
        rules = []
        current_rule = {}
        
        for line in field_rules_content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Field name (starts without tab)
            if not line.startswith('\t') and line:
                if current_rule:
                    rules.append(current_rule)
                current_rule = {'field': line, 'constraints': [], 'messages': []}
            
            # Constraint or message (starts with tab)
            elif line.startswith('\t'):
                clean_line = line.lstrip('\t')
                if clean_line.startswith('"') and clean_line.endswith('"'):
                    current_rule['messages'].append(clean_line[1:-1])
                else:
                    current_rule['constraints'].append(clean_line)
        
        if current_rule:
            rules.append(current_rule)
        
        # Display results
        print(f"FIELD RULES ANALYSIS - ACCOUNT.BUSINESSCLASS")
        print(f"=" * 50)
        print(f"Total Field Rules: {len(rules)}")
        print()
        
        for i, rule in enumerate(rules, 1):
            print(f"{i}. Field: {rule['field']}")
            if rule['constraints']:
                print(f"   Constraints: {', '.join(rule['constraints'])}")
            if rule['messages']:
                print(f"   Messages: {rule['messages']}")
            print()
        
        # Summary statistics
        constraint_types = {}
        for rule in rules:
            for constraint in rule['constraints']:
                constraint_type = constraint.split()[0] if constraint.split() else 'unknown'
                constraint_types[constraint_type] = constraint_types.get(constraint_type, 0) + 1
        
        print("CONSTRAINT TYPE SUMMARY:")
        for constraint_type, count in sorted(constraint_types.items()):
            print(f"  {constraint_type}: {count}")
        
        return rules
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error analyzing file: {e}")

if __name__ == "__main__":
    file_path = r"C:\Visual Basic Code\LPL Library\References\business class\Account.businessclass"
    analyze_field_rules(file_path)