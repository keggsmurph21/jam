"""
Convert a file from {format1} to {format2}.

The {formatN} is determined by (1) the "--to" or "--from" argument,
or, if not given, the filename of the <input> or <output> argument.
"""
from pathlib import Path
from typing import Optional
from typing import Sequence

import argparse
import sys

from . import decode_json, encode_json
from . import decode_toml, encode_toml
from . import decode_yaml, encode_yaml
from . import Obj
from . import Registry


def get_extension(filename: str) -> str:
    """
    Get the extension from a filename.  We drop the first char b/c
    it's always a '.' char.
    """
    return Path(filename).suffix[1:]


def main(argv: Optional[Sequence[str]] = None) -> None:
    registry = Registry()
    registry.put("json", (decode_json, encode_json))
    registry.put("toml", (decode_toml, encode_toml))
    registry.put("yaml", (decode_yaml, encode_yaml))

    parser = argparse.ArgumentParser(
        "jam",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input",
        type=argparse.FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="The file to be parsed as {format1}",
    )
    parser.add_argument(
        "output",
        type=argparse.FileType("w"),
        nargs="?",
        default=sys.stdout,
        help="The file to be generated in {format2}",
    )
    parser.add_argument(
        "-f",
        "--from",
        dest="decoder",
        choices=registry.codecs,
        help="Format of <input>.  If not given, guessed based on extension of <input>.",
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="encoder",
        choices=registry.codecs,
        help="Format of <output>.  If not given, guessed based on extension of <output>",
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        default=2,
        help="Number of spaces to indent, for formats that support it",
    )
    parser.add_argument(
        "-s",
        "--sort-keys",
        action="store_true",
        help="Whether to sort map keys, for formats that support it",
    )
    args = parser.parse_args(argv)

    if not args.decoder and args.input is sys.stdin:
        raise ValueError("Can't infer input encoding! You must either set <input> or --from")
    if not args.encoder and args.output is sys.stdout:
        raise ValueError("Can't infer output encoding! You must either set <output> or --to")

    input_ext = get_extension(args.input.name)
    decoder, _ = registry.get(args.decoder or input_ext)
    decoded = Obj.decode(decoder, args.input)

    output_ext = get_extension(args.output.name)
    _, encoder = registry.get(args.encoder or output_ext)
    encoded = decoded.encode(encoder, args.indent, args.sort_keys)

    args.output.write(encoded.read())


if __name__ == "__main__":
    main()
