import os, csv, sys
from datetime import datetime

annual_allowance=0

with open('CSVs/taxletters.csv', mode='r', encoding='utf-8-sig', newline='') as infile:
    reader = csv.reader(infile)
    for rows in reader:
        tax_letters = dict((rows[0],rows[1]) for rows in reader)

with open('CSVs/tax_years.csv', mode='r', encoding='utf-8-sig') as infile:
    reader = csv.reader(infile)
    for rows in reader:
        tax_years = dict((rows[0],[rows[1], rows[2]]) for rows in reader)

def get_tax_year():
    check = True
    print('List of available tax years\n')
    i = 0
    while i+2 < (len(tax_years)-1):
        key1 = list(tax_years)[i]
        val1 = tax_years[key1][0]
        i += 3
        key2 = list(tax_years)[i]
        val2 = tax_years[key2][0]
        i -= 2
        print(f'    [{key1}] {val1}             [{key2}] {val2}')
    
    print('\nPlease choose an option from the above\n\n')

    while check:
        print('\033[1A                    \033[K')
        choice = input('\033[1A\033[K')

        try:
            checkChoice = int(choice)
            if checkChoice in range(1,len(tax_years)+1):
                check = False
                screen_clear()
                print(f'Calculating salary based on the tax year {tax_years[choice][0]}\n')
        except:
            print('\033[3A\033[KInvalid input. Please enter a number between 1 - 6.\n\n')
        finally:
            pass

    return tax_years[choice][1]

def get_tax_brackets(tax_year):

    with open(f'CSVs/{tax_year}', mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            brackets = dict((rows[0],[rows[1],rows[2]]) for rows in reader)

    global default_tax_code
    default_tax_code = brackets['default'][0]
    global set_personal_allowance
    set_personal_allowance = int(brackets['personal_allowance'][0])
    global basic_rate, basic_cap
    basic_rate, basic_cap = float(brackets['tax_basic'][1]), int(brackets['tax_higher'][0])
    global higher_rate, higher_cap
    higher_rate, higher_cap = float(brackets['tax_higher'][1]), int(brackets['tax_additional'][0])
    global additional_rate
    additional_rate = float(brackets['tax_additional'][1])

    global nic_lower_floor
    nic_lower_floor = int(brackets['nic_lower'][0])
    global nic_lower_rate
    nic_lower_rate = float(brackets['nic_lower'][1])
    global nic_higher_floor
    nic_higher_floor = int(brackets['nic_higher'][0])
    global nic_higher_rate
    nic_higher_rate = float(brackets['nic_higher'][1])

    global annual_allowance
    annual_allowance = int(brackets['annual_allowance'][0])
    global minimum_allowance
    minimum_allowance = int(brackets['minimum_allowance'][0])
    global threshold_cap
    threshold_cap = int(brackets['threshold'][0])
    global adjusted_cap
    adjusted_cap = int(brackets['adjusted'][0])

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
    print('Gross Income')
    gross_income = input('£')
    while check:
        if ',' in gross_income:
            gross_income = gross_income.replace(',', '')

        if '£' in gross_income:
            gross_income = gross_income.replace('£', '')
            
        try:
            gross_income = float(gross_income)
            if gross_income > 999999999999:
                print('\033[2A\033[KGross Income                             \n£{:,.2f}\n'.format(round(gross_income, 2)))
                print('WARNING: This program has the capacity to produce a table using any value provided\nto it. However, as the table expands based off of the length of the value, the\namount you have entered may cause the table to be too large for your screen.\n')
                contCheck = True
                print('Are you sure you would like to continue? (Y/N)')
                while contCheck:
                    choice = input('').upper()
                    if choice == 'Y':
                        print('\033[1A\033[KY\n')
                        contCheck = False
                        check = False
                    elif choice == 'N':
                        print('\033[1A\033[KN\n')
                        loop_or_close()
                    else:
                        print('\033[2A\033[KInvalid input. Are you sure you would like to continue? (Y/N)')
            else:
                check = False
                print('\033[2A\033[KGross Income                             \n£{:,.2f}\n'.format(round(gross_income, 2)))
        except:
            print('\033[2A\033[KYour input contained letters. Please enter your Gross Annual Income.\n                                                 ')
            gross_income = input('\033[1A\033[K£')

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
def get_tax_code(tax_letters):

    # All commented prints are for testing purposes 

    # Running validation on user input
    check1 = True
    check2 = True
    
    print('Tax Code (Leave blank for default tax code)')
    tax_code = input('')
    while check1 or check2:
        if tax_code == '':
            tax_code = default_tax_code
        
        tax_letter_index = verify1(tax_code)
        if tax_letter_index != -1:
            check1 = False
            tax_letter = tax_code[tax_letter_index:].upper()
            if len(tax_code[:tax_letter_index]) > 4:
                print('\033[2A\033[KTax Code can not contain more than 4 numbers.\n                                      ')
                tax_code = input('\033[1A\033[K')
            else:
                # print('Tax Code after letter check:', tax_code)
                check2 = verify2(tax_letter, tax_letters)
                if check2:
                    print('\033[2A\033[KProvided Tax Code does not exist.\n                                      ')
                    tax_code = input('\033[1A\033[K')
        else:
            print('\033[2A\033[KProvided Tax Code does not exist.\n                                       ')
            tax_code = input('\033[1A\033[K')

    print('\033[3A\033[K                                                            ')

    return tax_code, tax_letter_index

def tax_code_seperator(gross_income, tax_code, tax_letter_index, total_pension = 0):
    # Getting personal allowance from Tax Code
    personal_allowance = float(tax_code[:tax_letter_index]) * 10
    tax_letter = tax_code[tax_letter_index:].upper()
    
    # Setting personal allowance exceptions for gross income over £100,000
    if gross_income - total_pension > 100000:
        personal_allowance = personal_allowance - ((gross_income - 100000 - total_pension) / 2)

        if personal_allowance < 0:
            personal_allowance = 0
            if tax_letter == default_tax_code[tax_letter_index:]:
                tax_letter = '0T'
        else:
            if tax_letter == default_tax_code[tax_letter_index:]:
                tax_letter = 'L'

    if personal_allowance == '':
        personal_allowance = 0
    
    return personal_allowance, tax_letter

# Get pension, or don't
def get_pension():
    check = True

    print('Pension (Leave blank for 0%)')
    pp_display = input()
    while check:
        if ',' in pp_display:
            pp_display = pp_display.replace(',', '')

        if '£' in pp_display:
            pp_display = pp_display.replace('£', '')
        
        if '%' in pp_display:
            pp_display = pp_display.replace('%', '')

        if pp_display == '':
            pp_display = 0

        try:
            pension_percent = (int(pp_display))/100
            pp_display = round(int(pp_display), 0)
            if pp_display >= 100:
                print('\033[2A\033[KMust be less than 100%. Please enter pension%, or leave blank for 0%.\n                                            ')
                pp_display = input('\033[1A\033[K')
            else:
                check = False
        except ValueError:
            try:
                pension_percent = (float(pp_display))/100
                pp_display = round(float(pp_display), 1)
                if pp_display >= 100:
                    print('\033[2A\033[KMust be less than 100%. Please enter pension%, or leave blank for 0%.\n                                            ')
                    pp_display = input('\033[1A\033[K')
                else:
                    check = False
            except:
                print('\033[2A\033[KMust be a number. Please enter pension%, or leave blank for 0%.\n                                            ')
                pp_display = input('\033[1A\033[K')

    print('\033[2A\033[KPension Contributions\n                                            ')
    print(f'\033[1A\033[K{pp_display}%\n')
    
    return pension_percent

def calculate_total_pension(gross_income, pension_percent):
    return gross_income * pension_percent

def get_monthly_income():
    check = True
    print('Monthly Income after tax')
    monthly_income = input('£')
    while check:
        if ',' in monthly_income:
            monthly_income = monthly_income.replace(',', '')

        if '£' in monthly_income:
            monthly_income = monthly_income.replace('£', '')
            
        try:
            monthly_income = float(monthly_income)
            if monthly_income > 999999999999:
                print('\033[2A\033[KMonthly Income                             \n£{:,.2f}\n'.format(round(monthly_income, 2)))
                print('WARNING: This program has the capacity to produce a table using any value provided\nto it. However, as the table expands based off of the length of the value, the\namount you have entered may cause the table to be too large for your screen.\n')
                contCheck = True
                print('Are you sure you would like to continue? (Y/N)')
                while contCheck:
                    choice = input('').upper()
                    if choice == 'Y':
                        print('\033[1A\033[KY\n')
                        contCheck = False
                        check = False
                    elif choice == 'N':
                        print('\033[1A\033[KN\n')
                        loop_or_close()
                    else:
                        print('\033[2A\033[KInvalid input. Are you sure you would like to continue? (Y/N)')
            else:
                check = False
                print('\033[2A\033[KMonthly Income                             \n£{:,.2f}\n'.format(round(monthly_income, 2)))
        except:
            print('\033[2A\033[KYour input contained letters. Please enter your Gross Annual Income.\n                                                 ')
            monthly_income = input('\033[1A\033[K£')

    return monthly_income

# Calculating Tax
def calculate_tax(gross_income, personal_allowance, tax_letter, total_pension, threshold_income=0, pension_allowance=annual_allowance):
    
    if threshold_income > 0:
        pass
    else: 
        personal_allowance = 0
    global deductable_pension
    if total_pension > pension_allowance:
        deductable_pension = total_pension + pension_allowance
    else:
        deductable_pension = total_pension

    if gross_income < (personal_allowance + total_pension) :
        taxable_income = 0
    else:
        taxable_income = gross_income - total_pension - personal_allowance
    
    if taxable_income < basic_cap or tax_letter == 'BR':
        basic_tax = taxable_income * basic_rate
        higher_tax = 0
        additional_tax = 0
        tax = basic_tax

    elif taxable_income < higher_cap:
        basic_tax = basic_cap * basic_rate
        higher_tax = (taxable_income - basic_cap) * higher_rate
        additional_tax = 0
        tax = basic_tax + higher_tax

    else: 
        basic_tax = (basic_cap) * basic_rate
        higher_tax = (higher_cap - basic_cap) * higher_rate
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

def calculate_threshold_income(net_income, total_pension, deductable_pension):
    return (net_income - total_pension) + deductable_pension

def calculate_adjusted_income(net_income, deductable_pension):
    return (net_income + deductable_pension)

def calculate_annual_allowance(threshold_income, adjusted_income):
    if threshold_income < threshold_cap:
        adjusted_annual_allowance = annual_allowance
    elif adjusted_income < adjusted_cap:
        adjusted_annual_allowance = annual_allowance
    else:
        adjusted_annual_allowance = annual_allowance - ((annual_allowance - adjusted_cap) / 2)
    if adjusted_annual_allowance < minimum_allowance:
        adjusted_annual_allowance = minimum_allowance
    
    return adjusted_annual_allowance

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
    values = [value, value/12, value/52, (value/52)/5]
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

def export_csv(tablevalues, pension):

    check = True

    while check:
        question = str(input('Would you like to export this salary as a CSV? (Y/N)\n')).upper()
        if question == 'Y' or question == 'N':
            check = False
        # Error handling
        elif not question.isalpha():
            print('\nInvalid input. Please type a letter.')
        elif question != 'Y' or question != 'N':
            print('\nInvalid input. Please type \'Y\' or \'N\'.')

    if question == 'Y' or question == 'y':

        tabletitles = ['Gross Income', 'Taxable Income', 'Tax', 'National Insurance', 'Net Income']

        if pension > 0:
            tablevalues.insert(1, [float(pension)])
            tablevalues[1].extend([pension/12, pension/52, (pension/52)/5])
            tabletitles.insert(1, 'Pension')

        # Defining file name with a root name of 'SalaryCalc_' and appending
        # the current date and time
        file_name = 'SalaryCalc_'
        file_name += datetime.today().strftime('%Y-%m-%d_%H%M%S') 

        # Get dir of current file
        absolutepath = os.path.abspath(__file__)

        # Get working directory
        fileDirectory = os.path.dirname(absolutepath)

        # Get parent directory
        parentDirectory = os.path.dirname(fileDirectory)

        if not os.path.exists(f"{parentDirectory}\\Exports"):
            os.mkdir(f"{parentDirectory}\\Exports")
        
        with open(f"{parentDirectory}\\Exports\\{file_name}.csv", mode='w', newline='') as csv_file:
            fieldnames = ['','Yearly', 'Monthly', 'Weekly', 'Daily']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(len(tablevalues)):
                writer.writerow({'': tabletitles[i], 'Yearly': f"£{round(tablevalues[i][0], 2)}", 'Monthly': f"£{round(tablevalues[i][1], 2)}", 'Weekly': f"£{round(tablevalues[i][2], 2)}", 'Daily': f"£{round(tablevalues[i][3], 2)}"})
        
        print(f'\nCSV Generated\n\n{parentDirectory}\Exports\\{file_name}.csv\n')

    elif question == 'N' or question == 'n':
        loop_or_close()

# Restarts code or exits based on user input
def loop_or_close():
    question = str(input('Would you like to calculate another salary? (Y/N)\n')).upper()

    if question == 'Y' or question == 'y':
        user_choice()
    elif question == 'N' or question == 'n':
        exit()

    # Error handling
    if not question.isalpha():
        print('\nInvalid input. Please type a letter.')
        loop_or_close()
    elif question != 'Y' or question != 'N':
        print('\nInvalid input. Please type \'Y\' or \'N\'.')
        loop_or_close()

# Calculate tax from gross income
def salarycalc():
    screen_clear()
    
    # Pulling tax brackets from CSVs
    get_tax_brackets(get_tax_year())

    # Defining gross_income
    gross_income = get_gross_income()
    
    # Defining pension amount
    total_pension = calculate_total_pension(gross_income, get_pension())

    # Getting tax code
    tax_code, tax_letter_index = get_tax_code(tax_letters)

    # Pulling personal_allowance and tax_letter using previous functions
    personal_allowance, tax_letter = tax_code_seperator(gross_income, tax_code, tax_letter_index, total_pension)

    # Pulling taxable_income and tax using previous functions 
    taxable_income, basic_tax, higher_tax, additional_tax, tax = calculate_tax(gross_income, personal_allowance, tax_letter, total_pension)
    
    if tax_letter == 'NT':
        taxable_income = 0
        tax = 0
    
    # Pulling National Insurance Contributions from calculate_nic
    lower_nic, higher_nic, nic = calculate_nic(gross_income)
    
    # Pulling Net Income from calculate_net
    net_income = calculate_net(gross_income, total_pension, tax, nic)

    threshold_income = calculate_threshold_income(net_income, total_pension, deductable_pension)

    adjusted_income = calculate_adjusted_income(net_income, deductable_pension)

    pension_allowance = calculate_annual_allowance(threshold_income, adjusted_income)

    taxable_income, basic_tax, higher_tax, additional_tax, tax = calculate_tax(gross_income, personal_allowance, tax_letter, total_pension, threshold_income, pension_allowance)
    
    # Pulling Net Income from calculate_net
    net_income = calculate_net(gross_income, total_pension, tax, nic)

    # Getting data ready to format for placement in ASCII table
    table_values = [[gross_income], [taxable_income], [tax], [nic], [net_income]]

    final_output(list(table_values), int(personal_allowance), basic_tax, higher_tax, additional_tax, lower_nic, higher_nic, tax_letter, total_pension)

# calculate required income from monthly income
def requiredincome():
    screen_clear()
    get_tax_brackets(get_tax_year())
    monthly_income = get_monthly_income()
    net_annual = int(monthly_income*12)
    gross_income = monthly_income*12

    # Defining pension amount
    pension_percent = get_pension()

    tax_code, tax_letter_index = get_tax_code(tax_letters)
    
    net_income = -1 
    
    # Defining gross_income
    while not net_annual-0.05 <= net_income <= net_annual+0.05:
        total_pension = calculate_total_pension(gross_income, pension_percent)
        # Pulling personal_allowance and tax_letter using previous functions
        personal_allowance, tax_letter = tax_code_seperator(gross_income, tax_code, tax_letter_index, total_pension)

        # Pulling taxable_income and tax using previous functions 
        taxable_income, basic_tax, higher_tax, additional_tax, tax = calculate_tax(gross_income, personal_allowance, tax_letter, total_pension)
        
        # Pulling National Insurance Contributions from calculate_nic
        lower_nic, higher_nic, nic = calculate_nic(gross_income)
        
        # Pulling Net Income from calculate_net
        net_income = calculate_net(gross_income, total_pension, tax, nic)
        threshold_income = calculate_threshold_income(net_income, total_pension, deductable_pension)
        adjusted_income = calculate_adjusted_income(net_income, deductable_pension)
        pension_allowance = calculate_annual_allowance(threshold_income, adjusted_income)
        taxable_income, basic_tax, higher_tax, additional_tax, tax = calculate_tax(gross_income, personal_allowance, tax_letter, total_pension, threshold_income, pension_allowance)
        net_income = calculate_net(gross_income, total_pension, tax, nic)
        net_monthly = round(net_income / 12, 2)

        r_adjuster = 0.5
        v_adjuster = 0.01

        while not net_annual - r_adjuster <= net_income <= net_annual + r_adjuster:
            r_adjuster *= 10
            v_adjuster *= 10
        
        if net_income < net_annual:
            gross_income += v_adjuster
        else:
            gross_income += v_adjuster
    
    # Getting data ready to format for placement in ASCII table
    table_values = [[gross_income], [taxable_income], [tax], [nic], [net_income]]

    final_output(list(table_values), int(personal_allowance), basic_tax, higher_tax, additional_tax, lower_nic, higher_nic, tax_letter, total_pension)

def final_output(table_values, personal_allowance, basic_tax, higher_tax, additional_tax, lower_nic, higher_nic, tax_letter, pension):  
       
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
        print('Personal Allowance                                          \nYou do not have a Personal Allowance.\n')
    else:
        print('Personal Allowance                                          \n£{:,.2f}\n'.format(personal_allowance))
    print(f'Tax Letter: {tax_letter}\n{tax_letters[tax_letter]}')

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
    
    export_csv(table_values, pension)
    # Asks user if they want to calculate another salary or exit the program
    loop_or_close()

# User choice between salary calc or required income
def user_choice():
    screen_clear()
    print('What would you like to do today?')
    print()
    print('     [1] Input annual income, calculate Tax and Net Income.')
    print('     [2] Input monthly income, calculate annual income.\n')
    print('Please choose 1 or 2\n')
    check = True
    while check:
        print('\033[1A                    \033[K')
        choice = input('\033[1A\033[K')
        try:
            choice = int(choice)
            if choice in [1, 2]:
                check = False
            else:
                print('\033[2A\033[KInvalid input. Please enter a number between 1 - 2.\n                      ')
        except Exception as error:
            print(f'\033[2A\033[K{error}Invalid input. Please enter a number.\n                    ')
    if choice == 1:
        check = False
        final_output(salarycalc())
    elif choice == 2:
        final_output(requiredincome())

user_choice()