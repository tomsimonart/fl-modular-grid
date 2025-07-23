#!/usr/bin/env python3
import re
import xml.etree.ElementTree as ET

def rewrite_file(input_path, output_path):
    pattern = re.compile(r'^(\s*)(\d+):')
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            match = pattern.match(line)
            if match:
                indent, num = match.groups()
                new_num = int(num) - 32
                new_line = f"{indent}{new_num}:" + line[match.end():]
                outfile.write(new_line)
            else:
                outfile.write(line)

# Write the mapping.py file with -32 offset
# rewrite_file('Intech/mapping_old.py', 'Intech/mapping.py')

# Write the fl studio mapping with -32 offset

def rewrite_fl_mapping(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    modif = 0
    for elem in root.iter("link"):
        ctrlparam = elem.find('ctrlparam')
        if ctrlparam is not None:
            ctrlparam.text = str(int(ctrlparam.text) - 32)
            modif += 1
    # Write output
    tree.write(output_file)
    print(f"Wrote {modif} modified elements to {output_file}")

# Modify the XML for port 13
# rewrite_fl_mapping(
#     r"C:\Users\tomsi\Documents\Image-Line\FL Studio\Settings\Mapping\Generic\local\Port 13_old.flmapping",
#     r"C:\Users\tomsi\Documents\Image-Line\FL Studio\Settings\Mapping\Generic\local\Port 13.flmapping"
# )