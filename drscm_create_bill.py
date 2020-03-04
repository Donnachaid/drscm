import csv

#Clean import of CSV file, removing commas from any fields

drscm_cm_data_file = 'drscm_cm_data.csv'
drscm_cm_data_file_TEMP = 'drscm_cm_data_TEMP.csv'
drscm_cm_data_file_VALIDATED = 'drscm_cm_data_VALIDATED.csv'

with open(drscm_cm_data_file, "rt") as csvfile, open(drscm_cm_data_file_TEMP, "wt", newline='') as outfile:
    reader = csv.reader(csvfile)
    writer = csv.writer(outfile)
    for row in reader:
        writer.writerow(item.replace(",", "") for item in row)

csvfile.close()
outfile.close()


with open(drscm_cm_data_file_TEMP, "rt") as csvfile, open(drscm_cm_data_file_VALIDATED, "wt", newline='') as outfile:
    reader = csv.reader(csvfile)
    writer = csv.writer(outfile)
    for row in reader:
        writer.writerow(item.replace("$", "") for item in row)

csvfile.close()
outfile.close()

tempfile = open('drscm_cm_data_TEMP.csv', "w")
tempfile.truncate()
tempfile.close()