#!/usr/bin/env python
"""
ccsv2mongo
Utility to convert a CSV file to a MongoDB JSON dump.

Copyright 2015 Sam Saint-Pettersen.
Licensed under the MIT/X11 License.

Use -h switch for usage information.
"""
import sys
import csv
import os
import re
import argparse

signature = 'ccsv2mongo 1.0.2 (https://github.com/stpettersens/ccsv2mongo)'

def displayVersion():
	print('\n' + signature)

def displayInfo():
	print(__doc__)

def ccsv2mongo(file, out, separator, mongotypes, array, verbose, version, info):

	if len(sys.argv) == 1:
		displayInfo()
		sys.exit(0)

	if file == None and out == None:
		if verbose == False and version == True and info == False:
			displayVersion()

		elif verbose == False and version == False and info == True:
			displayInfo()

		sys.exit(0)

	if out == None: out = re.sub('.csv', '.json', file)

	if file.endswith('.csv') == False:
		print('Input file is not a CSV file.')
		sys.exit(1)

	if out.endswith('.json') == False:
		print('Output file is not a JSON file.')
		sys.exit(1)

	if mongotypes == None: mongotypes = True

	if array == None: array = False

	head, tail = os.path.split(file)
	collection = re.sub('.csv', '', tail)

	if separator == None: separator = ','

	fields = []
	rows = []
	with open(file, 'r') as csvfile:
		f = csv.reader(csvfile, delimiter=separator)
		headers = True
		for row in f:
			if headers:
				fields = separator.join(row).split(separator)
				headers = False
			else:
				rows.append(row)

		csvfile.close()

	fn = len(fields)
	inserts = []
	x = 0
	for row in rows:

		for value in rows[x]:

			tvalue = re.sub('\.', '', value)

			if tvalue.isdigit() == False:

				if value.startswith('ObjectId('):
					value = re.sub('ObjectId\(|\)', '', value)
					if mongotypes:
						value = '{"$oid":"' + value + '"}'
					else:
						value = '"' + value + '"'

				pattern = re.compile('\d{4}\-\d{2}\-\d{2}')
				if pattern.match(value) and mongotypes:
					value = '{"$date":"' + value + '"}'

				pattern = re.compile('true|false|null', re.IGNORECASE)
				if pattern.match(value):
					value = value

				else: value = '"' + value + '"'

			if len(value) > 0: inserts.append(value)

		x = x + 1

	records = []
	rrecords = []
	inserts = ['@@'.join(inserts[i:i+fn]) for i in range(0, len(inserts), fn)]

	for insert in inserts:
		records = insert.split('@@')
		x = 0

		a_fields = []
		for record in records:
			for field in fields:
				a_fields.append(field)

		for record in records:
			r = '"' + a_fields[x] + '":' + record
			r = re.sub('\'', '"', r)
			rrecords.append(r)
			x = x + 1

	rrecords = ['@@'.join(rrecords[i:i+fn]) for i in range(0, len(rrecords), fn)]

	if verbose:
		print('\nGenerating MongoDB JSON dump file: \'{0}\' from\nCSV file: \'{1}\'\n'
		.format(out, file))

	f = open(out, 'w')
	ac = ''
	if array:
		ac = ','
		f.write('[\n')

	x = 0
	for record in rrecords:
		record = re.sub('@@', ',', record)
		record = re.sub('\"{', '{', record)
		record = re.sub('}\"', '}', record)
		if x == len(rrecords) - 1: ac = ''
		record = '{' + record + '}' + ac
		f.write(record + '\n')
		x = x + 1

	if array: f.write(']\n')

	f.close()


# Handle any command line arguments.
parser = argparse.ArgumentParser(description='Utility to convert a CSV file to a MongoDB JSON dump.')
parser.add_argument('-f', '--file', action='store', dest='file', metavar="FILE")
parser.add_argument('-o', '--out', action='store', dest='out', metavar="OUT")
parser.add_argument('-s', '--separator', action='store', dest='separator', metavar="SEPARATOR")
parser.add_argument('-n', '--no-mongo-types', action='store_false', dest='mongotypes')
parser.add_argument('-a', '--array', action='store_true', dest='array')
parser.add_argument('-l', '--verbose', action='store_true', dest='verbose')
parser.add_argument('-v', '--version', action='store_true', dest='version')
parser.add_argument('-i', '--info', action='store_true', dest='info')
argv = parser.parse_args()

ccsv2mongo(argv.file, argv.out, argv.separator, argv.mongotypes, argv.array, argv.verbose, argv.version, argv.info)
