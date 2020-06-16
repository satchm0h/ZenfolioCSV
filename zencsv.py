#!/usr/local/bin/python3
import os
import csv
import argparse

FIELD_NAMES = ['File Name', 'Title', 'Caption', 'Copyright', 'Alt attribute',
               'Keywords', 'Zenfolio Photo ID [DO NOT EDIT]']


def main(options):

    print(f'Zenfolio CSV: {options.zen_csv}')
    print(f'   Proof CSV: {options.proof_csv}')
    print(f'  Output CSV: {options.output_csv}')

    if not os.path.isfile(options.zen_csv):
        print(f"\nERROR: Unable to locate file: {options.zen_csv}")
    if not os.path.isfile(options.proof_csv):
        print(f"\nERROR: Unable to locate file: {options.proof_csv}")

    proofs = transform_proofs(options.proof_csv)
    # print(f'{proofs}')
    zen_rows = read_csv(options.zen_csv)
    # print(f"\n{zen_rows}")
    for row in zen_rows:
        if row['File Name'] in proofs:
            row['Keywords'] = f"{proofs[row['File Name']]['num']},{proofs[row['File Name']]['first']},{proofs[row['File Name']]['last']},{proofs[row['File Name']]['fullname']},{proofs[row['File Name']]['email']}"
        else:
            print(
                f'WARNING: Unable to find proof data for Zenfolio File Name: {row["File Name"]}')

    with open(options.output_csv, 'w') as fh:
        writer = csv.DictWriter(fh, FIELD_NAMES)
        writer.writeheader()
        writer.writerows(zen_rows)
    print("DONE\n")


def transform_proofs(proof_csv):
    rval = {}
    with open(proof_csv) as fh:
        rows = csv.DictReader(fh)
        for row in rows:
            for image in ['Image1', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Image9', 'Image10', 'Image11', 'Image12', 'Image13', 'Image14', 'Image15', 'Image16', 'Image17', 'Image18']:
                if image in row and row[image] != '':
                    rval[row[image]] = {
                        'first': row['Keyword1'],
                        'last': row['Keyword2'],
                        'fullname': row['Keyword3'],
                        'email': row['Keyword4'],
                        'num': row['Keyword5']
                    }
    return rval


def read_csv(csv_file):
    rval = []
    with open(csv_file, encoding="utf-8-sig") as fh:
        rows = csv.DictReader(fh)
        for row in rows:
            rval.append(row)
    return rval


def get_args():
    '''Handle command-line arguments. Returns argparse object (See argparse)'''

    parser = argparse.ArgumentParser(
        description='Update Zenfolio CSV with custom proof keywords'
    )
    parser.add_argument(
        '-D, --Debug',
        action='store_true',
        dest='debug',
        help='Debug: Log moar stuff'
    )

    parser.add_argument(
        'zen_csv',
        help='Zenfolio CSV path'
    )

    parser.add_argument(
        'proof_csv',
        help='Custom Proof CSV path'
    )

    parser.add_argument(
        'output_csv',
        help='Output CSV pat'
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(get_args())
