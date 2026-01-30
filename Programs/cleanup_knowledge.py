#!/usr/bin/env python3
"""
Script to clean up Knowledge.txt by removing '**No Local Fields section found**' entries.
"""

def cleanup_knowledge_file():
    """Remove all instances of '**No Local Fields section found**' from Knowledge.txt"""
    
    # File paths
    input_file = r"c:\Visual Basic Code\LPL Library\Knowledge.txt"
    output_file = r"c:\Visual Basic Code\LPL Library\Outputs\Knowledge_cleaned.txt"
    
    try:
        # Read the file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences before cleanup
        target_text = "**No Local Fields section found**"
        original_count = content.count(target_text)
        
        # Remove all instances of the target text
        cleaned_content = content.replace(target_text, "")
        
        # Clean up any extra blank lines that might be left
        # Replace multiple consecutive newlines with just two (to maintain section separation)
        import re
        cleaned_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_content)
        
        # Write the cleaned content to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        # Also overwrite the original file
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"Cleanup completed successfully!")
        print(f"Removed {original_count} instances of '{target_text}'")
        print(f"Original file updated: {input_file}")
        print(f"Backup saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find the file {input_file}")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    cleanup_knowledge_file()