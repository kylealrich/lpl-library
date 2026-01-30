import os
import re

def get_detailed_analysis(class_name, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        local_fields_match = re.search(r'Local Fields\s*\n(.*?)(?=\n\w|\nEnd|\Z)', content, re.DOTALL)
        
        if not local_fields_match:
            return None
        
        local_fields_content = local_fields_match.group(1)
        field_pattern = r'\t([A-Za-z_][A-Za-z0-9_]*)\s+is\s+(.*?)(?=\n\t[A-Za-z_]|\n\w|\Z)'
        
        fields = []
        for match in re.finditer(field_pattern, local_fields_content, re.DOTALL):
            field_name = match.group(1)
            field_definition = match.group(2).strip()
            
            # Classify field type
            definition_lower = field_definition.lower()
            if 'derivedfield' in definition_lower:
                field_type = 'DerivedField'
            elif ' set' in definition_lower:
                field_type = 'Set'
            elif 'relation' in definition_lower:
                field_type = 'Relation'
            elif 'messagefield' in definition_lower:
                field_type = 'MessageField'
            else:
                field_type = 'Reference'
            
            fields.append({
                "name": field_name,
                "type": field_type,
                "definition": field_definition[:100] + "..." if len(field_definition) > 100 else field_definition
            })
        
        return fields
    except Exception as e:
        return None

# Analyze top classes
base_dir = r"c:\Visual Basic Code\LPL Library\References\business class"
top_classes = [
    "SourcingEvent", "RecurringJournalControl", "StudentActivityBankTransaction",
    "BudgetChangeOrder", "CashLedgerBatchApproval", "CashLedgerElectronicFundsTransferTransaction",
    "FinanceDimension2", "FranchiseSales", "GeneralLedgerCalendarPeriod", "KitchenOrder"
]

print("=== DETAILED LOCAL FIELDS ANALYSIS ===\n")

for class_name in top_classes:
    file_path = os.path.join(base_dir, f"{class_name}.businessclass")
    if os.path.exists(file_path):
        fields = get_detailed_analysis(class_name, file_path)
        if fields:
            print(f"**{class_name} ({len(fields)} fields):**")
            for field in fields:
                print(f"- {field['name']} ({field['type']}): {field['definition']}")
            print()

# Common patterns analysis
print("=== COMMON LOCAL FIELD PATTERNS ===")
patterns = {
    "BOD Integration": ["BOD", "FSM", "Inbound", "Outbound"],
    "Error Handling": ["Error", "Message", "Exception"],
    "Validation": ["Valid", "Check", "Verify"],
    "Configuration": ["Config", "Parameter", "Setting"],
    "Relationships": ["Rel", "relation", "set"],
    "Derived Logic": ["Derived", "Calculate", "Count"]
}

for pattern_name, keywords in patterns.items():
    print(f"- {pattern_name}: Fields containing {', '.join(keywords)}")

print("\n=== FIELD TYPE CHARACTERISTICS ===")
print("- Reference: Direct references to other BusinessClass entities")
print("- Set: Collections of related records with filtering")
print("- DerivedField: Computed fields with conditional logic")
print("- Relation: One-to-one or one-to-many relationships")
print("- MessageField: UI feedback and notification fields")