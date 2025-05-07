import os
import zlib
import argparse
import re
from PyInstaller.archive.readers import ZlibArchiveReader, CArchiveReader


def parse_pyc(input_file, output_file, module_name):
    print(f'👀 Trying to process {input_file}')
    try:
        archive = ZlibArchiveReader(input_file)     
        for name, (typecode, foo, bar) in archive.toc.items():
            if module_name.lower() in name.lower():
                offset = foo
                lenght = bar
    except Exception as e:
        print(f'😿 No success: {e}')

    if offset:
        print(f'🤞 {module_name} found: offset:{offset}, lenght:{lenght}')
    else:
        print(f'😿 No success: {module_name} no found')

    with open(input_file, "rb") as foo:
        foo.seek(offset)
        data = foo.read(lenght)
    try:
        dec = re.findall(rb"[ -~]{4,}", zlib.decompress(data))
        with open(output_file, "w") as foo:
            for s in dec:
                foo.write(s.decode('utf-8', errors='ignore') + '\n')
        print(f'🥳 Remotely python-related strings written in {output_file}')
    except Exception as e:
        print(f'😿 No success: {e}')


def parse_args():
    parser = argparse.ArgumentParser(
                    prog='pyz-parser.py',
                    description='Tries to parse module from pyz files if nothing else works.',
                    epilog='Assault coded tool, use and develop at your own risk.')
    parser.add_argument('-i', '--input', required=True, help='Input pyz file.')
    parser.add_argument('-o', '--output', required=True, help='File to write strings carved from pyz files...')
    parser.add_argument('-m', '--module', required=True, help='Name of the module you want to dump')
    return parser.parse_args()


def main():
    args = parse_args()
    parse_pyc(args.input, args.output, args.module)
    
if __name__=='__main__':
    main()
    