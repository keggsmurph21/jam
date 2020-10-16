nested = {
    "json": ["rigid", "better for data interchange"],
    "toml": ["simple and readable", "easier to implement"],
    "yaml": ["slim and flexible", "better for configuration"],
    "object": {
        "key": "value",
        "array": [{"null_value": None}, {"boolean": True}, {"integer": 1}],
    },
    "paragraph": "Blank lines denote\nparagraph breaks\n",
    "content": "Or we\ncan auto\nconvert line breaks\nto save space",
}

flatter = {
    "json": ["rigid", "better for data interchange"],
    "toml": ["simple and readable", "easier to implement"],
    "yaml": ["slim and flexible", "better for configuration"],
    "object": {
        "key": "value",
        "array": "omitted",
    },
    "paragraph": "Blank lines denote\nparagraph breaks\n",
    "content": "Or we\ncan auto\nconvert line breaks\nto save space",
}
