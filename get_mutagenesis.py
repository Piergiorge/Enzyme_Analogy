import json
import requests
import sys

"""This code is using the Python standard library's json, requests, and sys modules to retrieve data from the EBI API 
and parse the data into a tab-separated format. """

requestURL = "https://www.ebi.ac.uk/proteins/api/mutagenesis?offset=0&size=100&accession=P06213%2CP05067%2CO00291"

r = requests.get(requestURL, headers={"Accept": "application/json"})

if not r.ok:
    r.raise_for_status()
    sys.exit()

responseBody = r.text

# parse the JSON data
data = json.loads(responseBody)

output = open('table_mut.tsv', 'w')

output.write('Taxid\taccession\ttype\tdescription\talternativeSequence\tbegin\tend\turl\n')
if data and 'features' in data[0]:
    for feature in data[0].get('features'):
        taxid = data[0].get('taxid', 'ND')
        accession = data[0].get('accession', 'ND')
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
