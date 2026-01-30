import re

def analyze_conditions_section(file_path):
    """Analyze the Conditions section of an LPL BusinessClass file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find Conditions section
        conditions_match = re.search(r'\tConditions\s*\n(.*?)(?=\n\t[A-Z]|\Z)', content, re.DOTALL)
        
        if not conditions_match:
            return "No Conditions section found in Account.businessclass"
        
        conditions_content = conditions_match.group(1)
        
        # Parse individual conditions with their definitions
        condition_blocks = re.findall(r'\t\t([^\n\t]+)\n((?:\t\t\t[^\n]*\n?)*)', conditions_content)
        conditions = []
        for name, definition in condition_blocks:
            clean_def = re.sub(r'\n\t\t\t', ' ', definition.strip())
            conditions.append((name, clean_def))
        
        result = f"=== CONDITIONS SECTION ANALYSIS - ACCOUNT.BUSINESSCLASS ===\n\n"
        result += f"Total Conditions: {len(conditions)}\n\n"
        
        for i, (name, definition) in enumerate(conditions, 1):
            result += f"{i}. **{name.strip()}**\n"
            if definition:
                result += f"   {definition}\n"
            result += "\n"
        
        return result
        
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error analyzing file: {str(e)}"

# Analyze Account.businessclass
file_path = r"C:\Visual Basic Code\LPL Library\References\business class\Account.businessclass"
analysis = analyze_conditions_section(file_path)
print(analysis)

# Save analysis to output file
output_path = r"C:\Visual Basic Code\LPL Library\Outputs\account_conditions_analysis.txt"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(analysis)

print(f"\nAnalysis saved to: {output_path}")