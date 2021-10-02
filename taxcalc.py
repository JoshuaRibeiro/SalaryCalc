import os

alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

tax_letters = {
    "L": "You’re entitled to the standard tax-free Personal Allowance",
    "M": "Marriage Allowance: you’ve received a transfer of 10% of your partner’s Personal Allowance",
    "N": "Marriage Allowance: you’ve transferred 10% of your Personal Allowance to your partner",
    "T": "Your tax code includes other calculations to work out your Personal Allowance",
    "0T": "Your Personal Allowance has been used up, or you’ve started a new job and your employer does not have the details they need to give you a tax code",
    "BR": "All your income from this job or pension is taxed at the basic rate (usually used if you’ve got more than one job or pension)",
    "D0": "All your income from this job or pension is taxed at the higher rate (usually used if you’ve got more than one job or pension)",
    "D1": "All your income from this job or pension is taxed at the additional rate (usually used if you’ve got more than one job or pension)",
    "NT": "You’re not paying any tax on this income",
    "S": "Your income or pension is taxed using the rates in Scotland",
    "S0T": "Your Personal Allowance (Scotland) has been used up, or you’ve started a new job and your employer does not have the details they need to give you a tax code",
    "SBR": "All your income from this job or pension is taxed at the basic rate in Scotland (usually used if you’ve got more than one job or pension)",
    "SD0": "All your income from this job or pension is taxed at the intermediate rate in Scotland (usually used if you’ve got more than one job or pension)",
    "SD1": "All your income from this job or pension is taxed at the higher rate in Scotland (usually used if you’ve got more than one job or pension)",
    "SD2": "All your income from this job or pension is taxed at the top rate in Scotland (usually used if you’ve got more than one job or pension)",
    "C": "Your income or pension is taxed using the rates in Wales",
    "C0T": "Your Personal Allowance (Wales) has been used up, or you’ve started a new job and your employer does not have the details they need to give you a tax code",
    "CBR": "All your income from this job or pension is taxed at the basic rate in Wales (usually used if you’ve got more than one job or pension)",
    "CD0": "All your income from this job or pension is taxed at the higher rate in Wales (usually used if you’ve got more than one job or pension)",
    "CD1": "All your income from this job or pension is taxed at the additional rate in Wales (usually used if you’ve got more than one job or pension)"
    }

tax_brackets = {
    'Personal Allowance': 12570,
    'Basic': [0, 0.2],
    'Higher': [50270, 0.4],
    'Additional': [150000, 0.45]
}

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

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      os.system('clear')
   else:
      # for windows platfrom
      os.system('cls')

def get_tax_code():
    tax_code = input('Tax Code: ')
    print('Tax Code after input:', tax_code)
    # Checking input contains a letter
    tax_letter_index = ''

    for char in tax_code:
        if char.upper() in alpha:
            tax_letter_index = tax_code.index(char)
            print('Passed letter check')
            break
    
    if tax_letter_index == '':
        print('Failed letter check')
        print('Invalid input. Please enter your tax code.')
        get_tax_code()

    print('Tax Code after letter check:', tax_code)

    tax_letter = tax_code[tax_letter_index:].upper()

    # Checking input has a key match in the tax_letters dictionary
    if tax_letter not in tax_letters.keys():
        print('Tax Code during dictionary match check (false):', tax_code)
        print('Failed dictionary match check')
        print('Invalid input. Please enter your tax code.')
        get_tax_code()
    elif tax_letter in tax_letters.keys():
        print('Tax Code during dictionary match check (true):', tax_code)
        print('Passed dictionary match check')
        
    print('Tax Code after dictionary match check:', tax_code)

    return tax_code

def tax_code_seperator(tax_code):
    for char in tax_code:
        if char.upper() in alpha:
            tax_letter_index = tax_code.index(char)
            print('Passed letter check')
            break

    tax_letter = tax_code[tax_letter_index:].upper()

    # Getting personal allowance from Tax Code
    personal_allowance = tax_code[:tax_letter_index]
    if personal_allowance == '':
        personal_allowance = 0
    else:
        personal_allowance = int(personal_allowance) * 10

    # Setting personal allowance exceptions for gross income over £100,000
    if gross_income > 100000:
        personal_allowance = set_personal_allowance - ((gross_income - 100000) / 2)
        if personal_allowance < 0:
            personal_allowance = 0
            
    print('Personal Allowance:', personal_allowance)
    print('Tax Letter:', tax_letter)
    
    return personal_allowance, tax_letter

def calculate_tax(gross_income, personal_allowance):
    global taxable_income
    if gross_income < personal_allowance:
        taxable_income = 0
    else:
        taxable_income = gross_income - personal_allowance

    if gross_income < basic_cap:
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
        additional_tax = (gross_income - higher_cap) * additional_rate
        tax = basic_tax + higher_tax + additional_tax

    return taxable_income, basic_tax, higher_tax, additional_tax, tax

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

def calculate_net(gross_income, tax, nic):
    net_income = gross_income - tax - nic
    return net_income

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
            a = '{:,.2f}'.format(value)
            if len(a) < 12:
                len_diff = 12 - len(a)
                spacer = ' ' * len_diff
                converted = '{}{:,.2f}'.format(spacer, value)
            else:
                converted = '{:,.2f}'.format(value)
            converted_values[i].append(converted)
        i += 1
    return converted_values

def tableformatter(converted_values):

    spacertable = [[], [], [], []]    
    formatted_values = [[], [], [], []]

    for i in range(len(converted_values[0])):

        max_diff = 0
        max_len = 12
        tablespacer = ''
        titlespacer = ''

        for o in range(len(converted_values)):

            spacer = ''
            
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

def loop_or_close():
        question = input('\nWould you like to calculate another salary? (Y/N)\n')
        check = False
        if question.upper() not in alpha:
            print('Invalid input. Please type \'Y\' or \'N\'.')
            loop_or_close()
        if question is 'Y' or 'N':
            check = True
        if check is False:
            print('Invalid input. Please type \'Y\' or \'N\'.')
            loop_or_close()
        if question == 'Y' or question == 'y':
            salarycalc()
        if question == 'N' or question == 'n':
            exit()

def salarycalc():
    screen_clear()

    global gross_income
    gross_income = input('Gross Income: £')

    if ',' in gross_income:
        gross_income = gross_income.replace(',', '')

    if '£' in gross_income:
        gross_income = gross_income.replace('£', '')

    gross_income = float(gross_income)

    personal_allowance, tax_letter = tax_code_seperator(get_tax_code())
    print(personal_allowance, tax_letter)

    taxable_income, basic_tax, higher_tax, additional_tax, tax = calculate_tax(gross_income, personal_allowance)

    if tax_letter == 'NT':
        taxable_income = 0
        tax = 0

    lower_nic, higher_nic, nic = calculate_nic(gross_income)

    net_income = calculate_net(gross_income, tax, nic)

    table_values = [[gross_income], [taxable_income], [tax], [nic], [net_income]]

    spacertable, formatted_values = tableformatter(get_formatted(table_values))

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

    pension = ''

    if personal_allowance == 0:
        print('Personal Allowance\nYou do not have a Personal Allowance.')
    else:
        print('Personal Allowance\n£{:,.2f}'.format(personal_allowance))
    print('\nTax Letter\n{}: {}'.format(tax_letter, tax_letters[tax_letter]))
    # print('\nTaxable Income\n£{:,.2f}'.format(taxable_income))
    # print('\nBasic Tax\n£{:,.2f}'.format(basic_tax))
    # print('\nHigher Tax\n£{:,.2f}'.format(higher_tax))
    # print('\nAdditional Tax\n£{:,.2f}'.format(additional_tax))
    # print('\nTax\n£{:,.2f}'.format(tax))
    # print('\nNational Insurance\n£{:,.2f}'.format(nic))
    # print('\nNet Income\n£{:,.2f}'.format(net_income))



    print(f"""
                         ╔═══════════════{ytas}╦═══════════════{mtas}╦═══════════════{wtas}╦═══════════════{dtas}╗
                         ║ Yearly        {ytis}║ Monthly       {mtis}║ Weekly        {wtis}║ Daily         {dtis}║
    ╔════════════════════╬═══════════════{ytas}╬═══════════════{mtas}╬═══════════════{wtas}╬═══════════════{dtas}╣
    ║ Gross Income       ║ {gyic} ║ {gmic} ║ {gwic} ║ {gdic} ║{pension}
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

    loop_or_close()


salarycalc()