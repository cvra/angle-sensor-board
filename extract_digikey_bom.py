#!/usr/bin/env python3

import collections
import xml.etree.ElementTree as ET
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", required=True)
parser.add_argument("--output", "-o", type=argparse.FileType('w'), required=True)
parser.add_argument("--quantity", "-q", type=int, default=1)
args = parser.parse_args()

tree = ET.parse(args.input)
root = tree.getroot()

customer_refs = {}
digikey_refs = {}

for component in root.find('components').findall("comp"):
    ref = component.attrib['ref']
    value = component.find('value').text
    footprint = component.find('footprint').text

    customer_refs[(footprint, value)] = customer_refs.get((footprint, value), []) + [ref]

    fields = component.find("fields")
    if not fields:
        continue

    for f in fields.findall("field"):
        if f.attrib['name'] == 'digikey#':
            digikey = f.text
            digikey_refs[(footprint, value)] = digikey

fieldnames = ['digikey', 'ref', 'qty']
writer = csv.DictWriter(args.output, fieldnames=fieldnames)
writer.writeheader()

results = {}
for key, refs in customer_refs.items():
    try:
        digikey = digikey_refs[key]
    except KeyError:
        print("No reference for {}".format(key))
        continue

    writer.writerow({'digikey': digikey, 'ref': ",".join(refs), 'qty': len(refs) * args.quantity})
