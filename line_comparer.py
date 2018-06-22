"""Compare lines.
"""

import os
import argparse

def detect_malformed(lines:[str] or str) -> [([str], [int], [int])]:
    """Yield pairs (lines, malformed indexes, maxlen) found in given lines"""
    if isinstance(lines, str): lines = lines.splitlines(False)
    def line_blocks(lines):
        block = []
        for line in map(str.strip, lines):
            if not line:  # empty line
                yield block
                block = []
            else:
                block.append(line)
        if block: yield block
    def values_from_line(line:str) -> [int]:
        return tuple(line.strip().split())
    for block in line_blocks(lines):
        values = tuple(map(values_from_line, block))
        distribution, maxlens = distribution_from_block(values)
        bad_indexes = tuple(idx for idx, count in enumerate(distribution) if count > 1)
        yield (values, bad_indexes, maxlens)

def distribution_from_block(block:[(object)]) -> (object):
    """Return a list giving number of different values found
    for each index of each line of the block, and a list givin the maximum
    length of string representation of all objects for each column.

    >>> distribution_from_block(((1, 2), (1, 2)))
    ((1, 1), (1, 1))
    >>> distribution_from_block(((1, 2), (11, 22)))
    ((2, 2), (2, 2))
    >>> distribution_from_block(((11, 2), (11, 3)))
    ((1, 2), (2, 1))
    >>> distribution_from_block(((1, 2, 3, 20), (1, 2, 3, 4), (11, 2, 4, 30)))
    ((2, 1, 2, 3), (2, 1, 1, 2))

    """
    readers = [iter(line) for line in block]
    return tuple(zip(*tuple(
        (len(set(values)), max(map(lambda v: len(str(v)), values)))
        for values in zip(*readers)
    )))


def show_malformed(malformeds:[([str], [int], [int])], colors:bool=True):
    "Print given malformed data"
    if colors:
        from colorama import init, Fore, Back, Style
        init()  # make color working, even on Windows
        RED, GREEN, END = Fore.RED, Fore.GREEN, Style.RESET_ALL
    else:
        RED, GREEN, END = '', '', ''
    for block, badvalues, maxlens in malformeds:
        if badvalues:  # there is errors
            for line in block:
                for idx, (value, maxlen) in enumerate(zip(line, maxlens)):
                    toprint = str(value).rjust(maxlen)
                    if idx in badvalues:
                        print(RED + toprint + END, end=' ')
                    else:
                        print(toprint, end=' ')
                print()
            print(RED + 'BAD!' + END)
        else:  # no error, it's ok
            print('\n'.join(map(' '.join, block)))
            print(GREEN + 'OK!' + END)
        print()


def cli_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', type=existant_file,
                        help='file containing the lines to compare')
    parser.add_argument('--no-colors', action='store_true',
                        help='Do not print colors')
    return parser.parse_args()

def existant_file(filepath:str) -> str:
    """Argparse type, raising an error if given file does not exists"""
    if not os.path.exists(filepath):
        raise argparse.ArgumentTypeError("file {} doesn't exists".format(filepath))
    return filepath


if __name__ == '__main__':
    args = cli_args()
    with open(args.infile) as fd:
        show_malformed(detect_malformed(fd), colors=not args.no_colors)
