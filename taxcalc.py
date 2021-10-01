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
    input_check = False
    for letter in alpha:
        if letter in tax_code:
            input_check = True
    if input_check == False:
        print('Invalid Input. Please enter a valid Tax Code.')
        get_tax_code()
    return tax_code

def tax_code_seperator(tax_code):
    for char in tax_code:
        if char.upper() in alpha:
            tax_letter_index = tax_code.index(char)
            break
    
    personal_allowance = tax_code[:tax_letter_index]
    if personal_allowance == '':
        personal_allowance = 0
    else:
        personal_allowance = float(personal_allowance) * 10

    if gross_income > 100000:
        personal_allowance = set_personal_allowance - ((gross_income - 100000) / 2)
        if personal_allowance < 0:
            personal_allowance = 0
    
    tax_letter = tax_code[tax_letter_index:].upper()

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
                converted = '£{}{:,.2f}'.format(spacer, value)
            else:
                converted = '£{:,.2f}'.format(value)
            converted_values[i].append(converted)
        i += 1
    return converted_values

def loop_or_close():
        question = input('\nWould you like to calculate another salary? (Y/N)\n')
        check = False
        if question.upper() not in alpha:
            print('Invalid input. Please type \'Y\' or \'N\'.')
            loop_or_close()
        if question.upper() is 'Y' or 'N':
            check = True
        if check is False:
            print('Invalid input. Please type \'Y\' or \'N\'.')
            loop_or_close
        if question.upper() is 'Y':
            salarycalc()
        if question.upper() is 'N':
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

    taxable_income, basic_tax, higher_tax, additional_tax, tax = calculate_tax(gross_income, personal_allowance)

    if tax_letter == 'NT':
        taxable_income = 0
        tax = 0

    lower_nic, higher_nic, nic = calculate_nic(gross_income)

    net_income = calculate_net(gross_income, tax, nic)

    table_values = [[gross_income], [taxable_income], [tax], [nic], [net_income]]
    print()

    converted_values = get_formatted(table_values)
    
    gyic = converted_values[0][0]
    gmic = converted_values[0][1]
    gwic = converted_values[0][2]
    gdic = converted_values[0][3]

    tiyc = converted_values[1][0]
    timc = converted_values[1][1]
    tiwc = converted_values[1][2]
    tidc = converted_values[1][3]

    txyc = converted_values[2][0]
    txmc = converted_values[2][1]
    txwc = converted_values[2][2]
    txdc = converted_values[2][3]

    ncyc = converted_values[3][0]
    ncmc = converted_values[3][1]
    ncwc = converted_values[3][2]
    ncdc = converted_values[3][3]

    niyc = converted_values[4][0]
    nimc = converted_values[4][1]
    niwc = converted_values[4][2]
    nidc = converted_values[4][3]

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



    print("""
                         ╔═══════════════╦═══════════════╦═══════════════╦═══════════════╗
                         ║ Yearly        ║ Monthly       ║ Weekly        ║ Daily         ║
    ╔════════════════════╬═══════════════╬═══════════════╬═══════════════╬═══════════════╣
    ║ Gross Income       ║ {} ║ {} ║ {} ║ {} ║
    ╠════════════════════╬═══════════════╬═══════════════╬═══════════════╬═══════════════╣
    ║ Taxable Income     ║ {} ║ {} ║ {} ║ {} ║
    ╠════════════════════╬═══════════════╬═══════════════╬═══════════════╬═══════════════╣
    ║ Tax                ║ {} ║ {} ║ {} ║ {} ║
    ╠════════════════════╬═══════════════╬═══════════════╬═══════════════╬═══════════════╣
    ║ National Insurance ║ {} ║ {} ║ {} ║ {} ║
    ╠════════════════════╬═══════════════╬═══════════════╬═══════════════╬═══════════════╣
    ║ Net Income         ║ {} ║ {} ║ {} ║ {} ║
    ╚════════════════════╩═══════════════╩═══════════════╩═══════════════╩═══════════════╝
    """.format(
        gyic, gmic, gwic, gdic, 
        tiyc, timc, tiwc, tidc, 
        txyc, txmc, txwc, txdc,
        ncyc, ncmc, ncwc, ncdc,
        niyc, nimc, niwc, nidc
        ))

    loop_or_close()


salarycalc()