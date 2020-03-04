#Dictionary CSV code

with open(drscm_cm_sat_alloc_file, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        print(f'\t{row["Project"]} works in the {row["Criteria"]} department, and was born in {row["Input 1"]}.')
        line_count += 1
    print(f'Processed {line_count} lines.')


with open(drscm_cm_cust_data, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        print(row["Project"])





        for i in range(1, projectRules.index.size):
            criteria = selectedSubs[ruleCriteria.loc['FICO Score']] = '700'
            criteria2 = selectedSubs[ruleCriteria.iloc[1]] == 'Queue'
            criteria3 = selectedSubs[ruleCriteria.iloc[2]] == 'NYSEG'
            criteria4 = selectedSubs[ruleCriteria.iloc[3]] == '1'
            criteria5 = selectedSubs[ruleCriteria.iloc[4]] == 'E'
            criteria6 = criteria & criteria2 & criteria3 & criteria4 & criteria5
            passedSubs = selectedSubs[criteria6]

    passedSubs.to_csv('scratch.csv')


        criteria = criteria & selectedSubs[ruleCriteria.iloc[i]] == projectRules.iloc[i,5]
        passedSubs = selectedSubs[criteria]



# query code

column = ruleCriteria.iloc[:, 0].astype(str).values.tolist()
equal = ruleCondition.iloc[:, 0].astype(str).values.tolist()
inputs = ruleInputs.iloc[:, 0].astype(str).values.tolist()

query = ' & '.join(f'{i} {j} {k}' for i, j, k in zip(column, equal, inputs))
print(selectedSubs.query(query))


# selection code that reduces the list

for i in range(0, projectRules.index.size):

    if ruleCondition.iloc[i]['Condition'] == '==':
        criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']] == projectRules.iloc[i]['Input 1']
        selectedSubs = selectedSubs[criteria]
    if ruleCondition.iloc[i]['Condition'] == '>':
        criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int).values > int(
            projectRules.iloc[i]['Input 1'])
        selectedSubs = selectedSubs[criteria]
    if ruleCondition.iloc[i]['Condition'] == '<':
        criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int).values < int(
            projectRules.iloc[i]['Input 1'])
        selectedSubs = selectedSubs[criteria]
    if ruleCondition.iloc[i]['Condition'] == '>=':
        criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int).values >= int(
            projectRules.iloc[i]['Input 1'])
        selectedSubs = selectedSubs[criteria]
    if ruleCondition.iloc[i]['Condition'] == '<=':
        criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int).values <= int(
            projectRules.iloc[i]['Input 1'])
        selectedSubs = selectedSubs[criteria]
    if ruleCondition.iloc[i]['Condition'] == '!=':
        criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int).values != int(
            projectRules.iloc[i]['Input 1'])
        selectedSubs = selectedSubs[criteria]
