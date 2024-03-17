#!/usr/bin/python
# -*- coding: utf-8 -*-

import jsonschema
import pandas as pd
import json
import os
import sys
import requests
from pathlib import Path
import pathlib
import glob
from flatten_json import flatten
import pyarrow.parquet as pq
import argparse
import urllib.parse
from json.decoder import JSONDecodeError


def main():
    with open('C:/Home/python/managed-etl-validation/schema.json', 'r') as schema:
        schema = json.load(schema)
        
    with open('C:/Home/python/managed-etl-validation/test.json', 'r') as event:
        event = json.load(event)
    
    runtimePath = Path(os.path.abspath(__file__))
    with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'w') as f:
        print('Validating Against OCSF event Class: ' + str(event['class_uid']), file=f)
        print('Validating Against OCSF Version: ' + str(event['metadata']['version']), file=f)
        print('Validating Against OCSF Profiles: ' + str(event['metadata']['profiles']), file=f)
        
    validator = jsonschema.Draft7Validator(schema)
    errors = validator.iter_errors(event)
    output = []
    for error in errors:
        output.append(str(error))
        
    # Print event data and validation errors
    with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
        print('\n------------------------------- INPUT RECORD ------------------------------\n', file=f)
        print(json.dumps(event, indent=6) + '\n', file=f)
    if output == []:
        with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
            print('\n---------------------------------- OUTPUT ---------------------------------' + '\n', file=f)
            print('VALID OCSF.', file=f)
            if str(event['class_uid']) == '2001':
                print("WARN: " + "OCSF event class: Security Findings (2001) is deprecated!", file=f)
            if str(event['class_uid']) == '4010':
                print("WARN: " + "OCSF event class: Network File Activity (4010) is deprecated!", file=f)
    else:
        with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
            print('\n---------------------------------- OUTPUT ---------------------------------' + '\n', file=f)
            print('INVALID OCSF.', file=f)
            if str(event['class_uid']) == '2001':
                print("WARN: " + "OCSF event class: Security Findings (2001) is deprecated!", file=f)
            if str(event['class_uid']) == '4010':
                print("WARN: " + "OCSF event class: Network File Activity (4010) is deprecated!", file=f)
            for i in output:
                print("\n---------------------------------------------------------------------------\n", file=f)
                print(i, file=f)
            print("\n---------------------------------------------------------------------------", file=f)
        
if __name__ == '__main__':
    main()