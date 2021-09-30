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
    'Basic': [0, 0.2],
    'Higher': [50270, 0.4],
    'Additional': [150000, 0.45]
}

basic_rate = tax_brackets['Basic'][1]
basic_cap = tax_brackets['Higher'][0]
higher_rate = tax_brackets['Higher'][1]
higher_cap = tax_brackets['Additional'][0]
additional_rate = tax_brackets['Additional'][1]

print(basic_rate, higher_rate, additional_rate)
print(basic_cap, higher_cap)

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
    
    global personal_allowance
    personal_allowance = tax_code[:tax_letter_index]
    if personal_allowance == '':
        personal_allowance = 0
    else:
        personal_allowance = float(personal_allowance) * 10
    
    if gross_income > 100000:
        personal_allowance = 0
    
    global tax_letter
    tax_letter = tax_code[tax_letter_index:].upper()

def calculate_tax(gross_income, personal_allowance):
    global taxable_income
    taxable_income = gross_income - personal_allowance

    global tax
    global basic_tax
    global higher_tax
    global additional_tax

    if gross_income < basic_cap:
        basic_tax = taxable_income * basic_rate
        higher_tax = 0
        additional_tax = 0
        tax = basic_tax

    elif gross_income < higher_cap:
        basic_tax = basic_cap * basic_rate
        higher_tax = (taxable_income - higher_cap) * higher_rate
        additional_tax = 0
        tax = basic_tax + higher_tax

    else: 
        basic_tax = basic_cap * basic_rate
        higher_tax = (higher_cap - basic_cap) * higher_rate
        additional_tax = (gross_income - higher_cap) * additional_rate
        tax = basic_tax + higher_tax + additional_tax



def salarycalc():
    screen_clear()

    global gross_income
    gross_income = input('Gross Income: £')

    if ',' in gross_income:
        gross_income = gross_income.replace(',', '')

    if '£' in gross_income:
        gross_income = gross_income.replace('£', '')

    gross_income = float(gross_income)

    tax_code_seperator(get_tax_code())

    calculate_tax(gross_income, personal_allowance)

    print()

    if personal_allowance == 0:
        print('Personal Allowance\nYou do not have a Personal Allowance.')
    else:
        print('Personal Allowance\n£{:,.2f}'.format(personal_allowance))
    print('\nTax Letter\n{}: {}'.format(tax_letter, tax_letters[tax_letter]))
    print('\nTaxable Income\n£{:,.2f}'.format(taxable_income))
    print('\nBasic Tax\n£{:,.2f}'.format(basic_tax))
    print('\nHigher Tax\n£{:,.2f}'.format(higher_tax))
    print('\nAdditional Tax\n£{:,.2f}'.format(additional_tax))
    print('\nTax\n£{:,.2f}'.format(tax))

    input('\nPress any key to loop...\n')
    salarycalc()

salarycalc()