import csv
import numpy as np
import pandas as pd

# Create CSV files with customer information and project allocation rule folder
drscm_cm_sat_alloc_file = 'drscm_cm_alloc_crit.csv'
drscm_cm_cust_data = 'customer_data.csv'

# Clear out the scratch file
tempfile = open('scratch.csv', "w+")
tempfile.truncate()
tempfile.close()

# Variable names
projectNameColumn = 'Project'
projectRankColumn = 'Rank'
projectCriteriaColumn = 'Criteria'
projectConditionColumn = 'Condition'
projectInputsColumn = 'Input 1'
projectInputCountColumn = 'Input Count'

rules = pd.read_csv(drscm_cm_sat_alloc_file, index_col=0)
subData = pd.read_csv(drscm_cm_cust_data, index_col=0)
rules = rules.dropna(subset=[projectNameColumn])
rules = rules.sort_values(by=[projectRankColumn])
project_list = rules[projectNameColumn].unique()
rules.set_index(projectNameColumn)

for project in project_list:
    projectRules = rules[rules[projectNameColumn] == project].astype(object)
    ruleCriteria = projectRules[[projectCriteriaColumn]]
    ruleCondition = projectRules[[projectConditionColumn]]
    ruleInputs = projectRules[[projectInputsColumn]]
    ruleInputCount = projectRules[[projectInputCountColumn]]
    selectedSubs = subData[ruleCriteria['Criteria'].unique()]
    booleanSubs = pd.DataFrame(index=range(selectedSubs.index.size), columns=range(1)).fillna(1)

    def bool_provider(subBase, boolMask):
        #print(subBase)
        return np.multiply(subBase, boolMask)

    for i in range(0, projectRules.index.size):

        # Implementation to match customers to each project where a rule can be defined by only one test (i.e. "> 700 FICO")
        if ruleInputCount.iloc[i]['Input Count'] == 1:
            if ruleCondition.iloc[i]['Condition'] == '==':
                criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']] == projectRules.iloc[i]['Input 1']
                booleanSubs = booleanSubs.apply(lambda x: bool_provider(x.values, criteria.values))
            if ruleCondition.iloc[i]['Condition'] == '>':
                criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int) > int(projectRules.iloc[i]['Input 1'])
                booleanSubs = booleanSubs.apply(lambda x: bool_provider(x.values, criteria.values))
            if ruleCondition.iloc[i]['Condition'] == '<':
                criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int) < int(projectRules.iloc[i]['Input 1'])
                booleanSubs = booleanSubs.apply(lambda x: bool_provider(x.values, criteria.values))
            if ruleCondition.iloc[i]['Condition'] == '>=':
                criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int) >= int(projectRules.iloc[i]['Input 1'])
                booleanSubs = booleanSubs.apply(lambda x: bool_provider(x.values, criteria.values))
            if ruleCondition.iloc[i]['Condition'] == '<=':
                criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int) <= int(projectRules.iloc[i]['Input 1'])
                booleanSubs = booleanSubs.apply(lambda x: bool_provider(x.values, criteria.values))
            if ruleCondition.iloc[i]['Condition'] == '!=':
                criteria = selectedSubs[ruleCriteria.iloc[i]['Criteria']].astype(int) != int(projectRules.iloc[i]['Input 1'])
                booleanSubs = booleanSubs.apply(lambda x: bool_provider(x.values, criteria.values))

        if ruleInputCount.iloc[i]['Input Count'] > 1:

            # Implementation to match customers to each project where a rule requires more than one test (i.e. "Service Class = 1 or 8")
            ruleTestBox = pd.DataFrame(index=range(selectedSubs.index.size), columns=range(ruleInputCount.iloc[i]['Input Count']))
            for x in range(0, ruleInputCount.iloc[i]['Input Count']):
                inputLoc = 'Input ' + str(x + 1)
                if ruleCondition.iloc[i]['Condition'] == '==':
                    ruleTestBox.iloc[:, x] = selectedSubs[selectedSubs[[ruleCriteria.iloc[i]['Criteria']]] == str(int(projectRules.iloc[i][inputLoc]))][ruleCriteria.iloc[i]['Criteria']].tolist()
                if ruleCondition.iloc[i]['Condition'] == '>':
                    ruleTestBox.iloc[:, x] = selectedSubs[selectedSubs[[ruleCriteria.iloc[i]['Criteria']]].astype(int).values > int(projectRules.iloc[i]['Input 1'])][ruleCriteria.iloc[i]['Criteria']].tolist()
                if ruleCondition.iloc[i]['Condition'] == '<':
                    ruleTestBox.iloc[:, x] = selectedSubs[selectedSubs[[ruleCriteria.iloc[i]['Criteria']]].astype(int).values < int(projectRules.iloc[i]['Input 1'])][ruleCriteria.iloc[i]['Criteria']].tolist()
                if ruleCondition.iloc[i]['Condition'] == '>=':
                    ruleTestBox.iloc[:, x] = selectedSubs[selectedSubs[[ruleCriteria.iloc[i]['Criteria']]].astype(int).values >= int(projectRules.iloc[i]['Input 1'])][ruleCriteria.iloc[i]['Criteria']].tolist()
                if ruleCondition.iloc[i]['Condition'] == '<=':
                    ruleTestBox.iloc[:, x] = selectedSubs[selectedSubs[[ruleCriteria.iloc[i]['Criteria']]].astype(int).values <= int(projectRules.iloc[i]['Input 1'])][ruleCriteria.iloc[i]['Criteria']].tolist()
                if ruleCondition.iloc[i]['Condition'] == '!=':
                    ruleTestBox.iloc[:, x] = selectedSubs[selectedSubs[[ruleCriteria.iloc[i]['Criteria']]].astype(int).values != str(int(projectRules.iloc[i]['Input 1']))][ruleCriteria.iloc[i]['Criteria']].tolist()
            ruleTestBoxPass = ruleTestBox.fillna(0)
            ruleTestBoxPass = ruleTestBoxPass.loc[:] != 0
            ruleTestBoxPass = ruleTestBoxPass.any(axis='columns')
            booleanSubs = bool eanSubs.apply(lambda x: bool_provider(x.values, ruleTestBoxPass.values))

subNames = selectedSubs[booleanSubs.values == True]
subNames.to_csv('scratch.csv')