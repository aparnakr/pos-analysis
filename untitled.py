import csv

a = ['sg', '734']
with open('names.csv', 'w') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovelddy', 'last_name': 'Spadfm'})
    writer.writerow({'first_name': 'Wonderdddgul', 'last_name': 'Spam'})
    for i in range(2):
    	writer.writerow({'first_name': i, 'last_name': a[i]})


