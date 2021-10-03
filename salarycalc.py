import os

# To update this to pull from a CSV
tax_letters = {
    "L": "You’re entitled to the standard tax-free Personal Allowance",
    "M": "Marriage Allowance: you’ve received a transfer of 10% of your partner’s\n   Personal Allowance",
    "N": "Marriage Allowance: you’ve transferred 10% of your Personal Allowance\n   to your partner",
    "T": "Your tax code includes other calculations to work out your Personal Allowance",
    "0T": "Your Personal Allowance has been used up, or you’ve started a new job and\n    your employer does not have the details they need to give you a tax code",
    "BR": "All your income from this job or pension is taxed at the basic rate\n    (usually used if you’ve got more than one job or pension)",
    "D0": "All your income from this job or pension is taxed at the higher rate\n    (usually used if you’ve got more than one job or pension)",
    "D1": "All your income from this job or pension is taxed at the additional rate\n    (usually used if you’ve got more than one job or pension)",
    "NT": "You’re not paying any tax on this income",
    "S": "Your income or pension is taxed using the rates in Scotland",
    "S0T": "Your Personal Allowance (Scotland) has been used up, or you’ve started\n     a new job and your employer does not have the details they need to give you a tax code",
    "SBR": "All your income from this job or pension is taxed at the basic rate in\n     Scotland (usually used if you’ve got more than one job or pension)",
    "SD0": "All your income from this job or pension is taxed at the intermediate\n     rate in Scotland (usually used if you’ve got more than one job or pension)",
    "SD1": "All your income from this job or pension is taxed at the higher rate in\n     Scotland (usually used if you’ve got more than one job or pension)",
    "SD2": "All your income from this job or pension is taxed at the top rate in\n     Scotland (usually used if you’ve got more than one job or pension)",
    "C": "Your income or pension is taxed using the rates in Wales",
    "C0T": "Your Personal Allowance (Wales) has been used up, or you’ve started a\n     new job and your employer does not have the details they need to give you a tax code",
    "CBR": "All your income from this job or pension is taxed at the basic rate in\n     Wales (usually used if you’ve got more than one job or pension)",
    "CD0": "All your income from this job or pension is taxed at the higher rate in\n     Wales (usually used if you’ve got more than one job or pension)",
    "CD1": "All your income from this job or pension is taxed at the additional rate\n     in Wales (usually used if you’ve got more than one job or pension)"
    }

# To update this to pull from a CSV
default_tax_code = '1257L'

# To update this to pull from a CSV
tax_brackets = {
    'Personal Allowance': 12570,
    'Basic': [0, 0.2],
    'Higher': [50270, 0.4],
    'Additional': [150000, 0.45]
}

# To update this to pull from a CSV
nic_brackets = {
    'Lower': [9568, 0.12],
    'Higher': [50270, 0.02]
}

set_personal_allowance = tax_brackets['Personal Allowance']
basic_rate = tax_brackets['Basic'][1]
basic_cap = tax_brackets['Higher'][0]
higher_rate = tax_brackets['Higher'][1]
higher_cap = tax_brackets['Additional'][0]
additional_rate = tax_brackets['Additional'][1]

nic_lower_floor = nic_brackets['Lower'][0]
nic_lower_rate = nic_brackets['Lower'][1]
nic_higher_floor = nic_brackets['Higher'][0]
nic_higher_rate = nic_brackets['Higher'][1]

# Function for clearing screen
def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      os.system('clear')
   else:
      # for windows platfrom
      os.system('cls')

def get_gross_income():
    check = True

    while check:
        gross_income = input('Gross Income: £')

        if ',' in gross_income:
            gross_income = gross_income.replace(',', '')

        if '£' in gross_income:
            gross_income = gross_income.replace('£', '')
        
        try:
            gross_income = float(gross_income)
            check = False
        except:
            print('Invalid input. Please enter a number.')
    
    return gross_income

# Checking tax code contains a letter
def verify1(tax_code):
    tax_letter_index = ''
    # Checking input contains a letter
    for char in tax_code:
        if char.upper().isalpha():
            tax_letter_index = tax_code.index(char)
            # print('Passed letter check')
            break
    if tax_letter_index == '':
        return -1
    else:
        return tax_letter_index

# Checking if tax code exists
def verify2(tax_letter, tax_letters):
    if tax_letter in tax_letters.keys():
        return False
    elif tax_letter not in tax_letters.keys():
        return True

# Gets tax code from user input
def get_tax_code(tax_letters, gross_income):

    # All commented prints are for testing purposes 

    # Running validation on user input
    check1 = True
    check2 = True

    while check1 or check2:
        tax_code = input('Tax Code (Leave blank for default tax code): ')
        if tax_code == '':
            tax_code = default_tax_code
        # print('Tax Code after input:', tax_code)
        tax_letter_index = verify1(tax_code)
        if tax_letter_index != -1:
            check1 = False
            tax_letter = tax_code[tax_letter_index:].upper()
            # print('Tax Code after letter check:', tax_code)
            check2 = verify2(tax_letter, tax_letters)
            if check2:
                # print('Tax Code during dictionary match check (false):', tax_code)
                # print('Failed dictionary match check')
                print('Invalid input. Please enter your tax code.')
            # else:    
                # print('Tax Code during dictionary match check (true):', tax_code)
                # print('Passed dictionary match check')
                # print('Tax Code after dictionary match check:', tax_code)
                
        
        else:
            # print('Failed letter check')
            print('Invalid input. Please enter your tax code.')

    
    # Getting personal allowance from Tax Code
    personal_allowance = tax_code[:tax_letter_index]

    # Setting personal allowance exceptions for gross income over £100,000
    if gross_income > 100000:
        personal_allowance = set_personal_allowance - ((gross_income - 100000) / 2)

        if personal_allowance < 0:
            personal_allowance = 0

        if tax_letter == default_tax_code[tax_letter_index:]:
            tax_letter = '0T'

    if personal_allowance == '' or tax_letter == '0T':
        personal_allowance = 0
    else:
        personal_allowance = float(personal_allowance) * 10

    return personal_allowance, tax_letter

# Get pension, or don't
def get_pension(gross_income):
    check = True

    while check:
        pension_percent = input('Pension (Leave blank for 0%):    %\x1B[4D')
        
        if ',' in pension_percent:
            pension_percent = pension_percent.replace(',', '')

        if '£' in pension_percent:
            pension_percent = pension_percent.replace('£', '')
        
        if '%' in pension_percent:
            pension_percent = pension_percent.replace('%', '')

        if pension_percent == '':
            pension_percent = 0

        try:
            pension_percent = (float(pension_percent))/100
            check = False
        except:
            print('Invalid input. Please enter a number.')
    
    pension = gross_income * pension_percent
    return pension_percent, pension


# Calculating Tax
def calculate_tax(gross_income, personal_allowance, tax_letter, pension):
    
    if gross_income < (personal_allowance + pension) :
        taxable_income = 0
    else:
        taxable_income = gross_income - pension - personal_allowance
    

    if gross_income < basic_cap or tax_letter == 'BR':
        basic_tax = taxable_income * basic_rate
        higher_tax = 0
        additional_tax = 0
        tax = basic_tax

    elif gross_income < higher_cap:
        basic_tax = (basic_cap - set_personal_allowance) * basic_rate
        higher_tax = (taxable_income - basic_cap + set_personal_allowance) * higher_rate
        additional_tax = 0
        tax = basic_tax + higher_tax

    else: 
        basic_tax = (basic_cap - set_personal_allowance) * basic_rate
        higher_tax = (higher_cap - basic_cap + set_personal_allowance) * higher_rate
        additional_tax = (taxable_income - higher_cap) * additional_rate
        tax = basic_tax + higher_tax + additional_tax

    if tax_letter == 'D0':
        basic_tax = 0
        higher_tax = taxable_income * higher_rate
        additional_tax = 0
        tax = higher_tax

    if tax_letter == 'D1':
        basic_tax = 0
        higher_tax = 0
        additional_tax = taxable_income * additional_rate
        tax = additional_tax
        
    return taxable_income, basic_tax, higher_tax, additional_tax, tax

# Calculating National Insurance Contributions
def calculate_nic(gross_income):
    if gross_income < nic_lower_floor:
        lower_nic = 0
        higher_nic = 0
        nic = lower_nic + higher_nic
    elif gross_income < nic_higher_floor:
        lower_nic = (gross_income - nic_lower_floor) * nic_lower_rate
        higher_nic = 0
        nic = lower_nic + higher_nic
    else: 
        lower_nic = (nic_higher_floor - nic_lower_floor) * nic_lower_rate
        higher_nic = (gross_income - nic_higher_floor) * nic_higher_rate
        nic = lower_nic + higher_nic

    return lower_nic, higher_nic, nic

# Calculate Net Income
def calculate_net(gross_income, pension, tax, nic):
    net_income = gross_income - pension - tax - nic
    if net_income < 0:
        net_income = 0
    return net_income

# Formats outputted values to fit in the table
def get_formatted(table_values):
    for value in table_values:
        value.append(value[0]/12)
        value.append(value[0]/52)
        value.append((value[2]/5))
    converted_values = []
    i = 0
    for values in table_values:
        converted_values.append([])
        for value in values:
            a = '{:,.2f}'.format(round(value, 2))
            if len(a) < 12:
                len_diff = 12 - len(a)
                spacer = ' ' * len_diff
                converted = '{}{:,.2f}'.format(spacer, value)
            else:
                converted = '{:,.2f}'.format(value)
            converted_values[i].append(converted)
        i += 1
    return converted_values

def get_formatted_single(value):
    values = [value, value/12, value/52, value/5]
    converted_values_single = []
    i = 0
    for value in values:
        a = '{:,.2f}'.format(round(value, 2))
        if len(a) < 12:
            len_diff = 12 - len(a)
            spacer = ' ' * len_diff
            converted = '{}{:,.2f}'.format(spacer, value)
        else:
            converted = '{:,.2f}'.format(value)
        converted_values_single.append(converted)
    return converted_values_single

# Creates spacers and reformats values to expand the table if the output values are too long
def tableformatter(converted_values):

    spacertable = [[], [], [], []]    
    formatted_values = [[], [], [], []]
    
    # Goes through each column
    for i in range(len(converted_values[0])):

        max_diff = 0
        max_len = 12
        tablespacer = ''
        titlespacer = ''
        
        # Goes through each row in column
        for o in range(len(converted_values)):

            spacer = ''
            
            # Define 'formatted' in case value will fit inside of the provided table
            formatted = '£{}'.format(converted_values[o][i])
            if len(converted_values[o][i]) > 12:               
                len_diff = len(converted_values[o][i]) - 12
                if len_diff >= max_diff:
                    max_diff = len_diff
                    max_len = len(converted_values[o][i])
            if len(converted_values[o][i]) < max_len:
                len_diff = max_len - len(converted_values[o][i])
                spacer = ' ' * len_diff
                formatted = '£{}{}'.format(spacer, converted_values[o][i])
            formatted_values[i].append(formatted)

        tablespacer = '═' * (max_diff)
        titlespacer = ' ' * (max_diff)
        spacertable[i].append(tablespacer)
        spacertable[i].append(titlespacer)
    return spacertable, formatted_values

# Creates spacers and reformats values to expand the table if the output values are too long
def tableformatter_single(converted_values, converted_values_single):

    spacertable = [[], [], [], []]    
    formatted_values = []
    # Goes through each column
    for i in range(len(converted_values)-1):

        max_diff = 0
        max_len = 12
        tablespacer = ''
        titlespacer = ''
        

        spacer = ''
        
        # Define 'formatted' in case value will fit inside of the provided table
        formatted_table = '£{}'.format(converted_values[0][i])
        formatted = '£{}'.format(converted_values_single[i])
        if len(converted_values[0][i]) > 12:               
            len_diff = len(converted_values[0][i]) - 12
            if len_diff >= max_diff:
                max_diff = len_diff
                max_len = len(converted_values[0][i])
        if len(converted_values_single[i]) < max_len:
            len_diff = max_len - len(converted_values_single[i])
            spacer = ' ' * len_diff
            formatted = '£{}{}'.format(spacer, converted_values_single[i])
        formatted_values.append(formatted)

        tablespacer = '═' * (max_diff)
        titlespacer = ' ' * (max_diff)
        spacertable[i].append(tablespacer)
        spacertable[i].append(titlespacer)

    return formatted_values
    
# Restarts code or exits based on user input
def loop_or_close():
        question = str(input('Would you like to calculate another salary? (Y/N)\n')).upper()

        if question == 'Y' or question == 'y':
            salarycalc()
        elif question == 'N' or question == 'n':
            exit()

        # Error handling
        if not question.isalpha():
            print('\nInvalid input. Please type a letter.')
            loop_or_close()
        elif question != 'Y' or question != 'N':
            print('\nInvalid input. Please type \'Y\' or \'N\'.')
            loop_or_close()
            

# Main function, defined as function to allow for looping back to start
def salarycalc():
    screen_clear()
    
    # Defining gross_income
    gross_income = get_gross_income()
    
    # Pulling personal_allowance and tax_letter using previous functions
    personal_allowance, tax_letter = get_tax_code(tax_letters, gross_income)

    pension_percent, pension = get_pension(gross_income)

    # Pulling taxable_income and tax using previous functions 
    # Additional values to be used in a feature update
    taxable_income, basic_tax, higher_tax, additional_tax, tax = calculate_tax(gross_income, personal_allowance, tax_letter, pension)
    
    if tax_letter == 'NT':
        taxable_income = 0
        tax = 0
    
    # Pulling National Insurance Contributions from calculate_nic
    lower_nic, higher_nic, nic = calculate_nic(gross_income)
    
    # Pulling Net Income from calculate_net
    net_income = calculate_net(gross_income, pension, tax, nic)
    
    # Getting data ready to format for placement in ASCII table
    table_values = [[gross_income], [taxable_income], [tax], [nic], [net_income]]

    # Creating spacers and reformatting values if needed
    spacertable, formatted_values = tableformatter(get_formatted(table_values))

    # Defining values for ASCII table placement
    # To check if this can be automated
    ytas = spacertable[0][0]
    ytis = spacertable[0][1]
    gyic = formatted_values[0][0]
    tiyc = formatted_values[0][1]
    txyc = formatted_values[0][2]
    ncyc = formatted_values[0][3]
    niyc = formatted_values[0][4]

    mtas = spacertable[1][0]
    mtis = spacertable[1][1]
    gmic = formatted_values[1][0]
    timc = formatted_values[1][1]
    txmc = formatted_values[1][2]
    ncmc = formatted_values[1][3]
    nimc = formatted_values[1][4]

    wtas = spacertable[2][0]
    wtis = spacertable[2][1]
    gwic = formatted_values[2][0]
    tiwc = formatted_values[2][1]
    txwc = formatted_values[2][2]
    ncwc = formatted_values[2][3]
    niwc = formatted_values[2][4]

    dtas = spacertable[3][0]
    dtis = spacertable[3][1]
    gdic = formatted_values[3][0]
    tidc = formatted_values[3][1]
    txdc = formatted_values[3][2]
    ncdc = formatted_values[3][3]
    nidc = formatted_values[3][4]

    # For adding a pension row if user chooses to provide pension
    if pension == '' or pension == 0:
        pension_row = ''
    else:
        formatted_pension = tableformatter_single(get_formatted(table_values), get_formatted_single(pension))
        pnyc = formatted_pension[0]
        pnmc = formatted_pension[1]
        pnwc = formatted_pension[2]
        pndc = formatted_pension[3]
        pension_row = f"""
    ╠════════════════════╬═══════════════{ytas}╬═══════════════{mtas}╬═══════════════{wtas}╬═══════════════{dtas}╣
    ║ Pension            ║ {pnyc} ║ {pnmc} ║ {pnwc} ║ {pndc} ║"""

    if personal_allowance == 0:
        print('\nPersonal Allowance\nYou do not have a Personal Allowance.')
    else:
        print('\nPersonal Allowance\n£{:,.2f}'.format(personal_allowance))
    print('\nTax Letter\n{}: {}'.format(tax_letter, tax_letters[tax_letter]))

    print(f"""
                         ╔═══════════════{ytas}╦═══════════════{mtas}╦═══════════════{wtas}╦═══════════════{dtas}╗
                         ║ Yearly        {ytis}║ Monthly       {mtis}║ Weekly        {wtis}║ Daily         {dtis}║
    ╔════════════════════╬═══════════════{ytas}╬═══════════════{mtas}╬═══════════════{wtas}╬═══════════════{dtas}╣
    ║ Gross Income       ║ {gyic} ║ {gmic} ║ {gwic} ║ {gdic} ║{pension_row}
    ╠════════════════════╬═══════════════{ytas}╬═══════════════{mtas}╬═══════════════{wtas}╬═══════════════{dtas}╣
    ║ Taxable Income     ║ {tiyc} ║ {timc} ║ {tiwc} ║ {tidc} ║
    ╠════════════════════╬═══════════════{ytas}╬═══════════════{mtas}╬═══════════════{wtas}╬═══════════════{dtas}╣
    ║ Tax                ║ {txyc} ║ {txmc} ║ {txwc} ║ {txdc} ║
    ╠════════════════════╬═══════════════{ytas}╬═══════════════{mtas}╬═══════════════{wtas}╬═══════════════{dtas}╣
    ║ National Insurance ║ {ncyc} ║ {ncmc} ║ {ncwc} ║ {ncdc} ║
    ╠════════════════════╬═══════════════{ytas}╬═══════════════{mtas}╬═══════════════{wtas}╬═══════════════{dtas}╣
    ║ Net Income         ║ {niyc} ║ {nimc} ║ {niwc} ║ {nidc} ║
    ╚════════════════════╩═══════════════{ytas}╩═══════════════{mtas}╩═══════════════{wtas}╩═══════════════{dtas}╝
    """)

    fbtax = tableformatter_single(get_formatted(table_values), get_formatted_single(basic_tax))[0]
    fhtax = tableformatter_single(get_formatted(table_values), get_formatted_single(higher_tax))[0]
    fatax = tableformatter_single(get_formatted(table_values), get_formatted_single(additional_tax))[0]
    
    flnic = tableformatter_single(get_formatted(table_values), get_formatted_single(lower_nic))[0]
    fhnic = tableformatter_single(get_formatted(table_values), get_formatted_single(higher_nic))[0]

    input('Press enter for Tax and NIC breakdown\'s\n')
    print('Tax Breakdown\n=============')
    print(f'Basic Rate:         {fbtax}')
    print(f'Higher Rate:        {fhtax}')
    print(f'Additional Rate:    {fatax}')
    print('\nNIC Breakdown\n=============')
    print(f'Lower Rate:         {flnic}')
    print(f'Higher Rate:        {fhnic}\n')
    
    # Asks user if they want to calculate another salary or exit the program
    loop_or_close()

# Starting salarycalc function
salarycalc()