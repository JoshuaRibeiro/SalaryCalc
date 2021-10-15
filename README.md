# SalaryCalc
SalaryCalc has 2 applets:

    Calculate take home pay from gross annual income
    Calculate gross annual income from a desired monthly income

Feature set

    Choose between the 6 latest tax years, and specify pension contributions and tax code (optional)
    
    Generate ASCII table with yearly, monthly, weekly, and daily values for Gross Income, Pension (if applicable),
    Taxable Income, Tax, National Insurance Contributions, and Net Income
    
    Expandable ASCII table based on value size (if len(value) > 12: expand column)
    
    Export ASCII table in CSV format
    
    Output a breakdown showing how much is paid in each tax bracket based off of the input
    
Reversing Tax
  
    Reversing tax uses an algorithm to adjust gross_income proportionately until we retrieve the desired output.
    
