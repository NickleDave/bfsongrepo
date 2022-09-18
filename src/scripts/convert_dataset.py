import argparse
import pathlib

import crowsetta
import soundfile


BIRD_IDS = [
    'bl26lb16',
    'gr41rd51',
    'gy6or6',
    'or60yw70',
]

DEFAULT_DATASET_ROOT = pathlib.Path('~/Documents/data/vocal/bfsongrepo').expanduser()


def convert(dataset_root):
    for bird_id in BIRD_IDS:
        print(f'converting data for bird: {bird_id}')
        bird_dir = dataset_root / bird_id
        date_dirs = [
            date_dir 
            for date_dir in bird_dir.iterdir()
            if date_dir.isdir()
            ]
        

def main(dataset_root=DEFAULT_DATASET_ROOT):
    convert(dataset_root)

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset-root',
        default=DEFAULT_DATASET_ROOT,
        help=''
    )