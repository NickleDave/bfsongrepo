"""Make .tar.gz archives
containing audio and annotations
from Bengalese Finch Song Repository dataset.

Command-line options allow selecting
which audio and annotation format to put
in the archives.
"""
import argparse
import pathlib
import tarfile

import tqdm


BIRD_IDS = [
    'bl26lb16',
    'gr41rd51',
    'gy6or6',
    'or60yw70',
]

DEFAULT_DATASET_ROOT = pathlib.Path(
    '~/Documents/data/vocal/BFSongRepo'
).expanduser()


def tar_audio_annot(dataset_root,
                    tar_dst,
                    audio_ext='.cbin',
                    annot_ext='.not.mat',
                    dry_run=False,
                    skip_exists=False):
    dataset_root = pathlib.Path(dataset_root).expanduser().resolve()
    if not dataset_root.exists():
        raise NotADirectoryError(
            f'Dataset root not found: {dataset_root}'
        )
    tar_dst = pathlib.Path(tar_dst).expanduser().resolve()
    if not tar_dst.exists():
        raise NotADirectoryError(
            f'.tar destination root not found: {tar_dst}'
        )

    for bird_id in BIRD_IDS:
        print(f'converting data for bird: {bird_id}')
        bird_dir = dataset_root / bird_id

        date_dirs = [
            date_dir
            for date_dir in bird_dir.iterdir()
            if date_dir.is_dir()
            ]
        for date_dir in date_dirs:
            print(
                f'Archiving: {date_dir}'
                )

            archive_name = f'sober.repo1.{bird_dir.name}.{date_dir.name}{audio_ext}{annot_ext}.tar.gz'
            archive_path = tar_dst / archive_name
            print(
                f'will create archive: {archive_path}'
            )

            if not dry_run:
                if skip_exists:
                    if archive_path.exists():
                        print('Archive exists already, skipping.')

                audio_paths = sorted(date_dir.glob(f'*{audio_ext}'))
                if audio_ext == '.cbin':
                    # we need to get .rec ("record") files,
                    # in addition to .cbin audio files
                    # since the .rec files have the sampling rate
                    # and are used by `evfuncs.load_cbin` to load .cbin audio
                    audio_paths.extend(
                        sorted(date_dir.glob('*.rec'))
                    )
                annot_paths = sorted(date_dir.glob(f'*{annot_ext}'))

                tar = tarfile.open(archive_path, 'w:gz')
                try:
                    print("Adding audio paths to archive.")
                    pbar = tqdm.tqdm(audio_paths)
                    for audio_path in pbar:
                        pbar.set_description(
                            f'Adding: {audio_path.name}'
                        )
                        arcname = str(audio_path).replace(str(dataset_root) + '/', '')
                        tar.add(name=audio_path, arcname=arcname)
                    print("Adding annotation paths to archive.")
                    pbar = tqdm.tqdm(annot_paths)
                    for annot_path in pbar:
                        arcname = str(annot_path).replace(str(dataset_root) + '/', '')
                        tar.add(name=annot_path, arcname=arcname)
                        pbar.set_description(
                            f'Adding: {annot_path.name}'
                        )
                finally:
                    tar.close()


def main(dataset_root=DEFAULT_DATASET_ROOT,
         tar_dst=DEFAULT_DATASET_ROOT,
         audio_annot_type='cbin-notmat',
         dry_run=False,
         skip_exists=False):
    if audio_annot_type not in {'cbin-notmat', 'wav-csv'}:
        raise ValueError(
            "audio_annot_type must be one of: {'cbin-notmat', 'wav-csv'} "
            f"but was: {audio_annot_type}"
        )
    if audio_annot_type == 'cbin-notmat':
        audio_ext = '.cbin'
        annot_ext = '.not.mat'
    elif audio_annot_type == 'wav-csv':
        audio_ext = '.wav'
        annot_ext = '.csv'

    tar_audio_annot(dataset_root, tar_dst,
                    audio_ext, annot_ext,
                    dry_run, skip_exists)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset-root',
        default=DEFAULT_DATASET_ROOT,
        help=('root of Bengalese Finch Song Repository dataset'
              f'Default is: {DEFAULT_DATASET_ROOT}')
    )
    parser.add_argument(
        '--tar-dst',
        default=DEFAULT_DATASET_ROOT,
        help=('Destination where .tar.gz files should be saved. '
              f'Default is: {DEFAULT_DATASET_ROOT}')
    )
    parser.add_argument(
        '--audio-annot-type',
        default='cbin-notmat',
        choices={'cbin-notmat', 'wav-csv'},
        help=("Type of audio and annotation files to put in tar. "
              "One of {'cbin-notmat', 'wav-csv'}")
    )
    parser.add_argument(
        '--dry-run',
        action='store_true'
    )
    parser.add_argument(
        '--skip-exists',
        action='store_true'
    )
    return parser


parser = get_parser()
args = parser.parse_args()
main(
    dataset_root=args.dataset_root,
    tar_dst=args.tar_dst,
    audio_annot_type=args.audio_annot_type,
    dry_run=args.dry_run,
    skip_exists=args.skip_exists,
)
