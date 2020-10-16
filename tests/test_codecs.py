from typing import Any

import pytest

from jam import Decoder
from jam import Encoder
from jam import decode_json, encode_json
from jam import decode_toml, encode_toml
from jam import decode_yaml, encode_yaml
from jam import Obj
from test_data import nested, flatter


def roundtrip(data: Any, decoder: Decoder, encoder: Encoder) -> None:
    obj = Obj(data)
    s = obj.encode(encoder, 2, False)
    assert data == decoder(s)


def test_json() -> None:
    roundtrip(nested, decode_json, encode_json)


def test_toml() -> None:
    with pytest.raises(AssertionError):
        roundtrip(nested, decode_toml, encode_toml)
    roundtrip(flatter, decode_toml, encode_toml)


def test_yaml() -> None:
    roundtrip(nested, decode_yaml, encode_yaml)
