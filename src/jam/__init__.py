from io import StringIO
from typing import Any
from typing import Callable
from typing import Dict
from typing import IO
from typing import Sequence
from typing import Tuple

import json
import toml
import yaml


Decoder = Callable[[IO[str]], Any]
Encoder = Callable[[Any, IO[str], int, bool], None]
Codec = Tuple[Decoder, Encoder]


class Obj:
    def __init__(self, obj: Any):
        self._obj = obj

    @classmethod
    def decode(cls, decoder: Decoder, fp: IO[str]) -> "Obj":
        return cls(decoder(fp))

    def encode(self, encoder: Encoder, indent: int, sort_keys: bool) -> IO[str]:
        s = StringIO()
        encoder(self._obj, s, indent, sort_keys)
        s.seek(0)
        return s


def decode_json(fp: IO[str]) -> Any:
    return json.load(fp)


def encode_json(obj: Obj, fp: IO[str], indent: int, sort_keys: bool) -> None:
    json.dump(obj, fp, indent=indent, sort_keys=sort_keys)


def decode_toml(fp: IO[str]) -> Any:
    return toml.load(fp)


def encode_toml(obj: Obj, fp: IO[str], indent: int, sort_keys: bool) -> None:
    # NOTE: "indent" and "sort_keys" are ignored!  Also, TOML only supports
    #       serializing objects of type Mapping[str, Any], so let's enforce
    #       that.
    #
    #       There's other stuff that we should enforce (no deeply nested objects,
    #       for example), but .... we'll just elide over that for now.  Just
    #       beware that TOML isn't as flexible as JSON/YAML.
    if not isinstance(obj, dict):
        raise TypeError(f'Can only encode Mapping[str, Any], not "{type(obj).__name__}"!')
    validated_obj = {str(k): v for k, v in obj.items()}
    toml.dump(validated_obj, fp)


def decode_yaml(fp: IO[str]) -> Any:
    return yaml.safe_load(fp)


def encode_yaml(obj: Obj, fp: IO[str], indent: int, sort_keys: bool) -> None:
    yaml.safe_dump(obj, fp, indent=indent, sort_keys=sort_keys)


class Registry:
    def __init__(self) -> None:
        self._codecs: Dict[str, Codec] = {}

    def put(self, name: str, codec: Codec) -> None:
        assert name not in self._codecs
        self._codecs[name] = codec

    def get(self, name: str) -> Codec:
        if name not in self._codecs:
            raise ValueError(f'Unknown codec: "{name}"')
        return self._codecs[name]

    @property
    def codecs(self) -> Sequence[str]:
        return list(self._codecs.keys())
