import csv

with open('not_another_salad.tsv','r') as tsvin, open('notAnotherSalad.json', 'w') as jsonOut:
    tsvin = csv.reader(tsvin, delimiter='\t')
    pk = 1
    jsonOut.write('[\n')
    for row in tsvin:
        if row[0] == '':
            pass
        else:
            jsonOut.write('    {\n')
            jsonOut.write('        "model": "pages.restaurant",\n')
            jsonOut.write('        "pk": ' + str(pk) + ',\n')
            pk += 1
            jsonOut.write('        "fields": {\n')
            jsonOut.write('            "name": "' +str(row[0])+'",\n')
            jsonOut.write('            "address": "' +str(row[1])+'",\n')
            if row[2] == '':
                jsonOut.write('            "phone": "N/A",\n')
            else:
                jsonOut.write('            "phone": "' +str(row[2])+'",\n')
            if row[2] == '':
                jsonOut.write('            "menu": "N/A",\n')
            else:
                jsonOut.write('            "menu": "' +str(row[3])+'",\n')
            jsonOut.write('            "description": "' +str(row[4])+'"\n')
            jsonOut.write('        }\n')
            jsonOut.write('    },\n')
    jsonOut.write(']\n')
