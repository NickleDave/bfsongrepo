"""script to download Bengalese Finch Song Repository dataset from Figshare
https://figshare.com/articles/dataset/Bengalese_Finch_song_repository/4805749
"""
from __future__ import annotations
import argparse
import json
import pathlib
import shutil
import sys
import time
import urllib.request
import warnings


DATASET_JSON_URL = "https://raw.githubusercontent.com/NickleDave/bfsongrepo/main/data/dataset.json"


def get_dataset_json() -> dict:
    """get a dict containing download urls for dataset files from the github url for a raw .json file"""
    with urllib.request.urlopen(DATASET_JSON_URL) as response:
        return json.load(response)


def reporthook(count, block_size, total_size):
    """hook for urlretrieve that gives us a simple progress report
    https://blog.shichao.io/2012/10/04/progress_speed_indicator_for_urlretrieve_in_python.html
    """
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def download_dataset(download_urls_by_bird_ID: dict,
                     bfsongrepo_dir: pathlib.Path) -> None:
    """download the dataset, given a dict of download urls"""
    tar_dir = bfsongrepo_dir / "tars"
    tar_dir.mkdir()
    # top-level keys are bird ID: bl26lb16, gr41rd51, ...
    for bird_id, tars_dict in download_urls_by_bird_ID.items():
        print(
            f'Downloading .tar files for bird: {bird_id}'
        )
        # bird ID -> dict where keys are .tar.gz filenames mapping to download url + MD5 hash
        for tar_name, url_md5_dict in tars_dict.items():
            print(
                f'Downloading tar: {tar_name}'
            )
            download_url = url_md5_dict['download']
            filename = tar_dir / tar_name
            urllib.request.urlretrieve(download_url, filename, reporthook)
            print('\n')


def extract_tars(bfsongrepo_dir: pathlib.Path) -> None:
    tar_dir = bfsongrepo_dir / "tars"  # made by download_dataset function
    tars = sorted(tar_dir.glob('*.tar.gz'))
    for tar_path in tars:
        print(
            f"\nunpacking: {tar_path}"
        )

        shutil.unpack_archive(
            filename=tar_path,
            extract_dir=bfsongrepo_dir,
            format="gztar"
        )


def main(dst : str | pathlib.Path,
         audio_annot_type: str) -> None:
    """main function that downloads and extracts entire dataset"""
    dst = pathlib.Path(dst).expanduser().resolve()
    if not dst.is_dir():
        raise NotADirectoryError(
            f"Value for 'dst' argument not recognized as a directory: {dst}"
        )
    bfsongrepo_dir = dst / 'bfsongrepo'
    if bfsongrepo_dir.exists():
        warnings.warn(
            f"Directory already exists: {bfsongrepo_dir}\n"
            "Will download and write over any existing files. Press Ctrl-C to stop."
        )

    try:
        bfsongrepo_dir.mkdir(exist_ok=True)
    except PermissionError as e:
        raise PermissionError(
            f"Unable to create directory in 'dst': {dst}\n"
            "Please try running with 'sudo' on Unix systems or as Administrator on Windows systems.\n"
            "If that fails please download files manually from Figshare:\n"
            "https://figshare.com/articles/dataset/Bengalese_Finch_song_repository/4805749"
        ) from e

    print(
        f'Downloading Bengalese Finch Song Repository to: {bfsongrepo_dir}'
    )
    dataset_json = get_dataset_json()
    # top-level keys are audio + annot: either 'cbin-notmat' or 'wav-simpleseq'
    download_urls_by_bird_ID = dataset_json[audio_annot_type]
    download_dataset(download_urls_by_bird_ID, bfsongrepo_dir)
    extract_tars(bfsongrepo_dir)


def get_parser():
    """get ArgumentParser used to parse command-line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dst',
        default='.',
        help=("Destination where dataset should be downloaded. "
              "Default is '.', i.e., current working directory "
              "from which this script is run.'")
    )
    parser.add_argument(
        '--audio-annot-type',
        default='cbin-notmat',
        choices={'cbin-notmat', 'wav-csv'},
        help=("Type of audio and annotation files to put in tar. "
              "One of {'cbin-notmat', 'wav-csv'}")
    )
    return parser


parser = get_parser()
args = parser.parse_args()
main(dst=args.dst,
     audio_annot_type=args.audio_annot_type
)
