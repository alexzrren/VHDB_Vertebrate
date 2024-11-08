import sys
import os
from pathlib import Path
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="VHDB Vertebrate Virus Mapper")
    
    # 可选参数 --cores/-c，输入整数，默认值为4
    parser.add_argument(
        '-c', '--cores',
        type=int,
        default=4,
        help="Max threads for executing workflow [default: 4]"
    )

    # 必要参数 --input/-i，输入一个必须存在的文件
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help="Input table"
    )

    # 必要参数 --output，输入一个必须具有可写权限的路径
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help="Output path"
    )

    # 可选flag参数 -d/--dry-run，逻辑值
    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help="Dry-run"
    )
    
    parser.add_argument(
        '-r', '--readnum',
        type=int,
        default=2,
        help="Minimum readnum threshold [default: 2]"
    )

    return parser


def validate_args(args):
    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"Input file '{args.input}' not found")


    output_dir = os.path.dirname(args.output) or '.'
    if not os.access(output_dir, os.W_OK):
        raise PermissionError(f"Output path '{output_dir}' not writeable")


def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        validate_args(args)
    except (FileNotFoundError, PermissionError) as e:
        parser.error(str(e))
        
    script_root = Path(__file__).parent
    summarize_script = script_root/'scripts/summarize.py'
    infotable = script_root/'db_file/vhdb_info.csv'
    bowtie2_index = script_root/'bowtie2_index/vhdb_vert_ani90rep'
    
    snakemake_runcommand = ' '.join([
        'snakemake',
        f'--cores {args.cores}',
        '--config',
        f'input_table={args.input}',
        f'outdir={args.output}',
        f'index={bowtie2_index}',
        f'summarize_script={str(summarize_script)}',
        f'readnum_cutoff={args.readnum}',
        f'infotable={str(infotable)}'
    ])
    print(snakemake_runcommand)
    
    if args.dry_run:
        os.system(snakemake_runcommand + ' --dry-run')
    else:    
        os.system(snakemake_runcommand)


if __name__ == "__main__":
    main()


