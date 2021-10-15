# SalaryCalc
View breakdown of the code here: https://medium.com/@joshuaribeiro1996/

SalaryCalc has 2 applets:

    Calculate take home pay from gross annual income
    Calculate gross annual income from a desired monthly income

Feature set

    Choose between the 6 latest tax years, and specify pension % and tax code (optional)
    
    Generate ASCII table with yearly, monthly, weekly, and daily values for Gross Income,
    Taxable Income, Tax, National Insurance Contributions, and Net Income
    
    Table includes pension row only if pension % is above 0
    
    Columns expand based on value sizes (if len(value) > 12: expand column)
    
    Option to export output in CSV format
    
    Output a breakdown showing how much is paid in each tax bracket based off of the input
    
Reversing tax uses an algorithm to adjust gross income proportionately until the desired output is retrieved.

