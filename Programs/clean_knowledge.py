import re

def clean_knowledge_file():
    """Remove all UNKNOWN.BUSINESSCLASS entries from Knowledge.txt"""
    
    # Read the file
    with open(r"C:\Visual Basic Code\LPL Library\Knowledge.txt", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match UNKNOWN.BUSINESSCLASS entries
    pattern = r'=== LOCAL FIELDS ANALYSIS - UNKNOWN\.BUSINESSCLASS ===\r?\n\r?\n\*\*No Local Fields section found\*\*\r?\n'
    
    # Remove all matches
    cleaned_content = re.sub(pattern, '', content)
    
    # Write back to file
    with open(r"C:\Visual Basic Code\LPL Library\Knowledge.txt", 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print("Removed all UNKNOWN.BUSINESSCLASS entries from Knowledge.txt")

if __name__ == "__main__":
    clean_knowledge_file()