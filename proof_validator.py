import argparse
import os
import pathlib
import sys
from src import Validator

"""
Script for Classic statements proof validation
Command line interface is implemented for your own convenience
@author: 'Kudriavtsev Eduard' (@edkudriavtsev)
Be warned: Using this code as a substitute for your own work in ITMO's Labs in Math Logic is considered plagiarism and
may result in you being expelled. 
"""


def file_exists(filename: str | None) -> bool:
    return filename is None or pathlib.Path(filename).exists()


def subdirectory_exists(filename: str | None) -> bool:
    return filename is None or pathlib.Path(filename).parent.exists()


def main():
    parser = argparse.ArgumentParser(
        prog="Proof validator",
        description="Validate your classic statement proof here"
    )
    parser.add_argument('-in', '--input_file', default="in.txt")
    parser.add_argument('-out', '--output_file', default=None)
    arguments = parser.parse_args()
    in_file = arguments.input_file
    if in_error := (not file_exists(in_file)):
        print(f"Error: file {in_file} does not exist", file=sys.stderr)
    out_file = arguments.output_file
    if out_error := (not subdirectory_exists(out_file)):
        print(f"Error: output file {out_file}: cannot find subdirectories", file=sys.stderr)
    if not in_error and not out_error:
        Validator.validate(in_file, out_file)
    input("Press Enter to finish...")


if __name__ == '__main__':
    main()
