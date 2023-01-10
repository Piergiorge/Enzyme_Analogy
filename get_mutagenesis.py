import json
import requests
import sys

"""This code is using the Python standard library's json, requests, and sys modules to retrieve data from the EBI API 
and parse the data into a tab-separated format. """


accessions = [
    'P06213',
    'A0JNW5',
    'A0JP26',
    'A0PK11',
    'A1A4S6',
    'A1A519',
    'A1L190',
    'A1L3X0',
    'A1X283',
]
accessions = ",".join(accessions)
accessions = accessions.replace(',', '%2C')
requestURL = f"https://www.ebi.ac.uk/proteins/api/mutagenesis?offset=0&size=100&accession={accessions}"
r = requests.get(requestURL, headers={"Accept": "application/json"})

if not r.ok:
    r.raise_for_status()
    sys.exit()

responseBody = r.text

# parse the JSON data
data = json.loads(responseBody)
print(responseBody)

output = open('table_mut.tsv', 'w')

output.write('Taxid\taccession\ttype\tdescription\talternativeSequence\tbegin\tend\turl\n')
for d in data:
    features = d.get('features')
    if features:
        for feature in features:
            taxid = d.get('taxid', 'ND')
            accession = d.get('accession', 'ND')
            charact = feature.get('type', 'ND')
            description = feature.get('description', 'ND')
            alternativeSequence = feature.get('alternativeSequence', 'ND')
            begin = feature.get('begin', 'ND')
            end = feature.get('end', 'ND')
            evidences = feature.get('evidences')
            url = evidences[0].get('source').get('url')
            output_string = f"{taxid}\t{accession}\t{charact}\t{description}\t{alternativeSequence}\t{begin}\t{end}\t{url}\n"
            output.write(output_string)
output.close()
