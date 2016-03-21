"""
Assessment history parser
File: 'br63trf.nicrt4wb'
"""
from struct import Struct, calcsize
from csv import DictWriter
from sys import stdin, stdout

layout = '5s 5s 1s 7s 2s 9s 6x 6x 1s 5x 25x 25x 25x 25x 25x 5x 4x 1x 9x 9x 9x 9x 11x 9s 9s 9s 9s 11s 2x'

header = ['STREET_CODE', 'HOUSE_NUMBER', 'SUFFIX', 'UNIT_NUMBER', 'CERT_YEAR', 'ACCOUNT_NUMBER', 'ACTION_CODE', 'CERTIFIED_TAXABLE_LAND', 'CERTIFIED_TAXABLE_BUILD', 'CERTIFIED_EXEMPT_LAND', 'CERTIFIED_EXEMPT_BUILDING', 'MARKET_VALUE']

output_header = ['RECORD_ID', 'PROPERTY_ID', 'ACCOUNT_NUMBER', 'CERT_YEAR', 'MARKET_VALUE', 'CERTIFIED_TAXABLE_LAND', 'CERTIFIED_TAXABLE_BUILD', 'CERTIFIED_EXEMPT_LAND', 'CERTIFIED_EXEMPT_BUILDING']

numeric_fields = ['CERTIFIED_TAXABLE_LAND', 'CERTIFIED_TAXABLE_BUILD', 'CERTIFIED_EXEMPT_LAND', 'CERTIFIED_EXEMPT_BUILDING', 'MARKET_VALUE']

def are_all_chars(input, char):
  return input == len(input) * char

# Prepare CSV output to stdout
writer = DictWriter(stdout, fieldnames=output_header, extrasaction='ignore')
writer.writeheader()

parse = Struct(layout).unpack_from
struct_length = calcsize(layout)

for line in stdin.readlines():
  # Ensure string length is what deconstructer expects
  if len(line) != struct_length:
    line = '{:<{}s}'.format(line, struct_length)

  # Deconstruct fixed-width string
  row = parse(line)

  # Trim whitespace in each field
  row = [field.strip() for field in row]

  # Convert to dict using header
  row = dict(zip(header, row))

  # Filter out records where action code is not 'A'
  if row['ACTION_CODE'] != 'A':
    continue

  # Use full certification year instead of last 2 chars
  if row['CERT_YEAR']:
    row['CERT_YEAR'] = '20' + row['CERT_YEAR']

  # Enforce numeric fields
  for field in numeric_fields:
    row[field] = int(row[field])

  # Unit numbers should be padded with leading zeros or empty
  if are_all_chars(row['UNIT_NUMBER'], '0'):
    row['UNIT_NUMBER'] = ''
  else:
    row['UNIT_NUMBER'] = row['UNIT_NUMBER'].zfill(7)

  # Construct property id from street code + house number + suffix + unit
  row['PROPERTY_ID'] = '{0}{1}{2}{3}'.format(row['STREET_CODE'], row['HOUSE_NUMBER'], row['SUFFIX'], row['UNIT_NUMBER'])

  # Construct unique record id from property id + certification year
  row['RECORD_ID'] = '{0}{1}'.format(row['PROPERTY_ID'], row['CERT_YEAR'])

  # Filter out 
  writer.writerow(row)