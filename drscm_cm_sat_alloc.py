import csv
import numpy

# Create CSV files with customer information and project allocation rule folder
drscm_cm_sat_alloc_file = 'drscm_cm_alloc_crit.csv'
drscm_cm_cust_data = 'customer_data.csv'

# Clear out the scratch file
tempfile = open('scratch.csv', "w+")
tempfile.truncate()
tempfile.close()

# Open files and create numpy arrays with (1) the allocation rules and (2) customer data
# !!!UPDATE: CONVERT THIS INTO A FUNCTION THAT LOADS A SPECIFIC TABLE FROM THE CLOUD SQL DATABASE
rules = numpy.array(list(csv.reader(open(drscm_cm_sat_alloc_file, "r"), delimiter=","))).astype(str)
cust_data = numpy.array(list(csv.reader(open(drscm_cm_cust_data, "r"), delimiter=","))).astype(str)

# Set up an multi-dimensional array that tracks customer assignments to projects as 1's
# !!!UPDATE: NEED TO REDUCE THE WIDTH OF ARRAY TO ONLY COUNT PROJECTS AND NOT TOTAL ROWS IN CRITERIA SHEET
cust_pass_array = numpy.zeros([cust_data[:, 1].size, rules[:, 3].size])

# Get the field names from the customer data sheet, which should match the comparison field in the rule list
rule_options = cust_data[0]

# Set up an array that holds the comparison field
fieldList = rules[:, 3]

# Generic iterator 'x' is used to iterate through the project rules (skips row 0).
x = 0
projectCount = 0
projectList = numpy.empty()
for rule in rules:
    if
projectName = rules[1, 1]

# Array to track the unallocated customers. Each rule iteration will use this array to set available customer list
cust_binary_unalloc = numpy.ones(cust_data[:, 1].size)

# Generate one-dimensional arrays of 1's and 0's
cust_binary_ones = numpy.ones(cust_data[:, 1].size)
cust_binary_zeros = numpy.zeros(cust_data[:, 1].size)
possibleCustomers = cust_binary_ones

# Create array used to track customer allocations (one column per project, one for all customers, one for unallocated)

for alloc in cust_assignments:
    cust_binary_unalloc = cust_binary_unalloc * numpy.logical_not(possibleCustomers)
possibleCustomers = cust_binary_unalloc
cust_assignments = numpy.zeros([cust_data[:, 1].size, rules[:, 3].size])


for selectedRule in rules:
    if x > 0:
        if projectName != selectedRule[1]:
            projectName = selectedRule[1]
            projectCount = projectCount + 1
            for alloc in cust_pass_array:
                cust_binary_unalloc = cust_binary_unalloc * numpy.logical_not(possibleCustomers)
            possibleCustomers = cust_binary_unalloc

        fieldSelected = fieldList[x]
        selectedRule_inputToTest = selectedRule[6]
        i = 0
        custDataFieldColumn = 0

        # Find the field in the customer data array that matches the current comparison field
        # !!!UPDATE: USE A DICTIONARY FOR THIS
        for custDataFieldHeadings in cust_data[0]:
            if custDataFieldHeadings == fieldSelected:
                custDataFieldColumn = cust_data[:, i]
            i = i + 1

        # Set the customer binary tracking array to 1 where a customer is to be allocated to the current project
        possibleCustomers = possibleCustomers * (custDataFieldColumn == selectedRule_inputToTest)
        cust_pass_array[:, projectCount] = possibleCustomers


    x = x + 1

print(cust_binary_unalloc)
numpy.savetxt('scratch.csv', cust_pass_array, delimiter=',')