"""Convert Bengalese Finch Song Repository dataset 
from .cbin audio and .not.mat annotation files 
to .wav audio files and .csv annotation files in 'simple-seq' format"""
import argparse
import pathlib

import crowsetta
import evfuncs
import numpy as np
import soundfile
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


def convert(dataset_root, dst):
    dataset_root = pathlib.Path(dataset_root).expanduser().resolve()
    if not dataset_root.exists():
        raise NotADirectoryError(
            f'Dataset root not found: {dataset_root}'
        )
    dst = pathlib.Path(dst).expanduser().resolve()
    dst.mkdir(exist_ok=True)
    print(
        f'Destination for converted audio and annotation: {dst}'
    )

    for bird_id in BIRD_IDS:
        print(f'converting data for bird: {bird_id}')
        bird_dir = dataset_root / bird_id
        dst_bird_dir = dst / bird_dir.name
        dst_bird_dir.mkdir(exist_ok=True)

        date_dirs = [
            date_dir 
            for date_dir in bird_dir.iterdir()
            if date_dir.is_dir()
            ]
        for date_dir in date_dirs:
            print(
                f'Converting day: {date_dir}'
                )
            dst_date_dir = dst_bird_dir / date_dir.name
            dst_date_dir.mkdir(exist_ok=True)

            print('Converting .cbin audio to .wav format')
            cbin_paths = sorted(date_dir.glob('*.cbin'))
            pbar = tqdm.tqdm(cbin_paths)
            for cbin_path in pbar:
                pbar.set_description(
                    f'Converting: {cbin_path.name}'
                )
                # https://stackoverflow.com/a/42544738/4906855
                audio, sampfreq = evfuncs.load_cbin(cbin_path)
                audio = audio.astype(np.float64) / 32768.0
                wav_dst = dst_date_dir / f"{cbin_path.name.replace('.cbin', '')}.wav"
                soundfile.write(file=wav_dst, data=audio, samplerate=sampfreq)

            print('Converting .not.mat annotations to simple-seq .csv format')
            notmat_paths = sorted(date_dir.glob('*.not.mat'))
            pbar = tqdm.tqdm(notmat_paths)
            for notmat_path in pbar:
                pbar.set_description(
                    f'Converting: {notmat_path.name}'
                )
                notmat = crowsetta.formats.seq.NotMat.from_file(notmat_path)
                csv_dst = dst_date_dir / f"{notmat_path.name.replace('cbin.not.mat', 'wav.csv')}"
                simpleseq = crowsetta.formats.seq.SimpleSeq(
                    onsets_s=notmat.onsets,
                    offsets_s=notmat.offsets,
                    labels=notmat.labels,
                    annot_path=csv_dst,  # required arg, use destination file as dummy
                )

                simpleseq.to_file(csv_dst)


def main(dataset_root=DEFAULT_DATASET_ROOT,
         dst=DEFAULT_DATASET_ROOT):
    convert(dataset_root, dst)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset-root',
        default=DEFAULT_DATASET_ROOT,
        help=('root of Bengalese Finch Song Repository dataset' 
              f'Default is: {DEFAULT_DATASET_ROOT}')
    )
    parser.add_argument(
        '--dst',
        default=DEFAULT_DATASET_ROOT,
        help=('Destination where converted files should be saved. '
              f'Default is: {DEFAULT_DATASET_ROOT}')
    )
    return parser


parser = get_parser()
args = parser.parse_args()
main(
    dataset_root=args.dataset_root,
    dst=args.dst
)
