def generate_set_action_knowledge():
    """Generate comprehensive Set Action knowledge for the knowledge base"""
    
    # Read the complete analysis
    try:
        with open(r"c:\lpl-library\Outputs\journalize_transactions_complete.txt", 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return "Analysis file not found"
    
    # Extract key patterns and generate knowledge
    knowledge_sections = []
    
    # Basic Set Action syntax
    knowledge_sections.append("""
=== SET ACTIONS SYNTAX ===

**BASIC SET ACTION STRUCTURE:**
```lpl
ActionName is a Set Action
    [restricted]
    Parameters
        ParameterName is DataType
            [default label is "Label"]
    Queue Mapping Fields
        FieldName1
        FieldName2
    Parameter Rules
        ParameterName
            [validation rules]
    Local Fields
        LocalFieldName is DataType
    Instance Selection
        where (conditions)
    Sort Order
        FieldName1
        FieldName2 [descending]
    Accumulators
        AccumulatorName
    Action Rules
        [Complex processing logic with nested Set Rules]
```

**SET ACTION COMPONENTS:**

1. **Parameters Section:**
   - Define input parameters for the Set Action
   - Each parameter has a type and optional default label
   - Support for complex business class types
   - Default value assignments

2. **Queue Mapping Fields:**
   - Specify fields used for queue processing
   - Enable parallel processing capabilities
   - Map to parameter fields for distribution

3. **Parameter Rules:**
   - Validation logic for parameters
   - Default value assignments
   - Required field constraints
   - Cross-parameter validation

4. **Local Fields:**
   - Temporary variables for processing
   - Complex data type support
   - View references and calculations
   - Accumulator variables

5. **Instance Selection:**
   - WHERE clause filtering
   - Complex boolean conditions
   - Parameter-based filtering
   - Multi-field criteria

6. **Sort Order:**
   - Field-based sorting
   - Ascending/descending options
   - Multi-level sorting
   - Performance optimization

7. **Accumulators:**
   - Automatic totaling fields
   - Debit/Credit separations
   - Currency amount totals
   - Units and quantity totals

8. **Action Rules:**
   - Complex nested processing logic
   - Set Rules for different groupings
   - Entrance and Exit Rules
   - Multi-level rule blocks
""")

    # Advanced patterns from JournalizeTransactions
    knowledge_sections.append("""
=== ADVANCED SET ACTION PATTERNS ===

**COMPLEX PARAMETER TYPES:**
```lpl
Parameters
    PrmEnterpriseGroup is a FinanceEnterpriseGroup
        default label is "FinanceEnterpriseGroup"
    PrmJournalizeGroup is a JournalizeGroup
        default label is "JournalizeGroup"
    PrmCurrencyTable is a CurrencyTable
        default label is "CurrencyTable"
    PrmJournalCreated is Boolean
        default label is "JournalCreated"
    PrmAccountingEntity is a AccountingEntity
        default label is "AccountingEntity"
    PrmClosePeriod is a GeneralLedgerClosePeriod
        default label is "ClosePeriod"
    PrmJournalControl is a GeneralLedgerJournalControl
        default label is "JournalControl"
    PrmBypassStructureRelationEdit is Boolean
        default label is "BypassStructureRelationEdit"
```

**QUEUE MAPPING FIELDS:**
```lpl
Queue Mapping Fields
    PrmAccountingEntity.PostingCategory
    PrmJournalCreated
```

**COMPLEX LOCAL FIELDS:**
```lpl
Local Fields
    LocalAccountingEntityJournalView is a GeneralLedgerJournalControl view
    LocalToAccountingEntityJournalView is a GeneralLedgerJournalControl view
    LocalTransactionView is a GeneralLedgerTransaction view
    LocalToTransactionView is a GeneralLedgerTransaction view
    LocalFrAccountingEntity is a AccountingEntity
    LocalPostingDate is Date
    LocalToAccountingEntity is a ToAccountingEntity
    LocalActionCurrencyCode is a Currency
    LocalActionTransactionDate is Date
    LocalActionAutoReverse is Boolean
    LocalTransactionAmountDr is an InternationalAmount
    LocalToFunctionalAmountDr is an InternationalAmount
    LocalToAlternateAmountDr is an InternationalAmount
```

**COMPREHENSIVE ACCUMULATORS:**
```lpl
Accumulators
    TransactionAmountDrTotal
    FunctionalAmountDrTotal
    AlternateAmountDrTotal
    AlternateAmount2DrTotal
    AlternateAmount3DrTotal
    AutoReverseAmountDrTotal
    ToFunctionalAmountDrTotal
    ToAlternateAmountDrTotal
    ToAlternateAmount2DrTotal
    ToAlternateAmount3DrTotal
    ToAutoReverseAmountDrTotal
    ProjectAmountDrTotal
    ReportAmount1DrTotal
    ReportAmount2DrTotal
    ReportAmount3DrTotal
    ReportAmount4DrTotal
    ReportAmount5DrTotal
    UnitsDrTotal
    AutoReverseUnitsDrTotal
    UnitsAmountTotal
    [Corresponding Cr (Credit) totals for each Dr (Debit) total]
```
""")

    # Nested Set Rules patterns
    knowledge_sections.append("""
=== NESTED SET RULES PATTERNS ===

**HIERARCHICAL SET RULES:**
Set Actions support complex nested Set Rules that process data at different grouping levels:

```lpl
Action Rules
    Empty Set Rules
    Set Rules
        Entrance Rules
            [Initialization logic]
        Exit Rules
            [Cleanup and finalization logic]
    
    AccountingEntity Set Rules
        Entrance Rules
            [Entity-level processing setup]
        Exit Rules
            [Entity-level processing completion]
    
    ZoneSystemKeyFields Set Rules
        Entrance Rules
            [Zone processing setup]
        Exit Rules
            [Zone processing completion]
    
    PostingDateJournalCodeKey Set Rules
        Entrance Rules
            [Journal creation and setup]
        Exit Rules
            [Journal finalization and release]
    
    FinanceCodeBlock.ToAccountingEntity Set Rules
        Entrance Rules
            [Inter-entity processing setup]
        Exit Rules
            [Inter-entity processing completion]
    
    CurrencyCode Set Rules
        Entrance Rules
            [Currency-specific processing]
        Exit Rules
            [Currency totaling and balancing]
    
    ZoneFields Set Rules
        Entrance Rules
            [Zone field processing setup]
        Exit Rules
            [Zone balancing and totaling]
    
    AutoReverse Set Rules
        Entrance Rules
            [Auto-reverse transaction setup]
        Exit Rules
            [Transaction creation and processing]
```

**SET RULE PROCESSING FLOW:**
1. **Empty Set Rules:** Handle cases where no records match criteria
2. **General Set Rules:** Overall processing initialization and cleanup
3. **Entity-Level Rules:** Process by accounting entity groupings
4. **Zone Rules:** Handle zone balancing and inter-entity transactions
5. **Journal Rules:** Create and manage journal controls
6. **Currency Rules:** Process currency-specific calculations
7. **Field-Level Rules:** Handle specific field groupings and calculations

**RULE BLOCK INCLUDES:**
```lpl
include UpdateInterEntityZoneAmounts
include CreateFromInterEntityTransaction
include CreateToInterEntityTransaction
include UpdateZoneTotals
include AssignInterEntityCodeBlockDefaults
```
""")

    # Generate complete knowledge
    complete_knowledge = '\n'.join(knowledge_sections)
    
    return complete_knowledge

def update_knowledge_base(new_knowledge):
    """Update the Knowledge.txt file with new Set Action knowledge"""
    
    try:
        with open(r"c:\lpl-library\Knowledge.txt", 'r', encoding='utf-8') as f:
            current_knowledge = f.read()
    except FileNotFoundError:
        current_knowledge = ""
    
    # Add new Set Actions section
    updated_knowledge = current_knowledge + "\n\n" + new_knowledge
    
    with open(r"c:\lpl-library\Knowledge.txt", 'w', encoding='utf-8') as f:
        f.write(updated_knowledge)
    
    return "Knowledge base updated successfully"

# Main execution
if __name__ == "__main__":
    print("Generating Set Action knowledge for knowledge base...")
    
    knowledge = generate_set_action_knowledge()
    
    if isinstance(knowledge, str) and knowledge.startswith("Analysis file"):
        print(f"Error: {knowledge}")
    else:
        # Save the generated knowledge
        with open(r"c:\lpl-library\Outputs\set_action_knowledge.txt", 'w', encoding='utf-8') as f:
            f.write("SET ACTION KNOWLEDGE FOR LPL KNOWLEDGE BASE\n")
            f.write("=" * 60 + "\n")
            f.write(knowledge)
        
        # Update the main knowledge base
        result = update_knowledge_base(knowledge)
        
        print("Set Action knowledge generated and saved to:")
        print("- c:\\lpl-library\\Outputs\\set_action_knowledge.txt")
        print(f"- Knowledge base update: {result}")
        
        print("\nKey knowledge areas added:")
        print("- Basic Set Action syntax structure")
        print("- Advanced parameter and field patterns")
        print("- Complex accumulator definitions")
        print("- Nested Set Rules hierarchical processing")
        print("- Queue Mapping Fields for parallel processing")
        print("- Parameter Rules for validation")
        print("- Multi-level rule block patterns")