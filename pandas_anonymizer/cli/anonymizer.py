#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


import argparse

import os

import numpy as np
import pandas as pd

#pd.set_option('max_rows', 10)
pd.set_option('expand_frame_repr', False)
pd.set_option('max_columns', 6)

from pandas_anonymizer import Anonymizer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input Excel or CSV file')
    parser.add_argument('-o', '--output', help='Output Excel or CSV file', default='')
    parser.add_argument('-l', '--locale', help='Faker locale', default='en_GB')
    parser.add_argument('-s', '--seed', help='Faker seed (use an integer to get same results)', default=None)
    args = parser.parse_args()

    short_file_name, file_extension = os.path.splitext(args.input)
    file_extension = file_extension.lower()
    allowed_file_extension = ['.xls', '.xlsx', '.csv']
    if file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(args.input)
    elif file_extension in ['.csv']:
        df = pd.read_csv(args.input)
    else:
        raise(NotImplementedError("Unsupported input file extension '%s' - it must be in %s" % (filext, allowed_fileext)))

    print("Original data:")
    print(df)

    anonymizer = Anonymizer(args.locale)
    anonymizer.seed(args.seed)
    df_anon = anonymizer.anonymize(df)

    print("")

    print("Anonymized data:")
    print(df_anon)

    if args.output == '':
        filename_out = short_file_name + '_anon' + file_extension
    else:
        filename_out = args.output
    short_file_name_out, file_extension_out = os.path.splitext(args.output)

    if file_extension in ['.xls', '.xlsx']:
        df_anon.to_excel(filename_out)
    elif file_extension in ['.csv']:
        df_anon.to_csv(filename_out, index=False)
    else:
        raise(NotImplementedError("Unsupported output file extension '%s' - it must be in %s" % (filext, allowed_fileext)))
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
