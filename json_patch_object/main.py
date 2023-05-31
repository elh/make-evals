import json
import random
import uuid
import jsonpatch
import string
import random
import argparse

# gross global
key_set = set()
key_format = "uuid"

# note: could allow for duplicates across objects to increase difficulty
def generate_key():
    while True:
        k = str(uuid.uuid4())
        if key_format == "short":
            k = k[:6]
        if k not in key_set:
            break
    key_set.add(k)
    return k

def generate_value():
    return random.randint(1, 1000)

def deep_get(v, *ks):
    for k in ks:
        try:
            v = v[k]
        except KeyError:
            return None
    return v

def generate_dict(num_keys, value_func):
    return {generate_key(): value_func() for _ in range(num_keys)}

def pick_path(d):
    if not isinstance(d, dict):
        return []
    k = random.choice(list(d.keys()) + [None])
    if k is None:
        return []
    return [k] + pick_path(d[k])

def pick_operation(d, path):
    path_str = "/".join(path)
    v = deep_get(d, *path)

    ops = ["add", "remove", "replace"]
    if not isinstance(v, dict):
        ops = ["remove", "replace"]
    op = random.choice(ops)

    if op == "add":
        return {
            "op": op,
            "path": "/" + path_str + "/" + generate_key(),
            "value": generate_value()
        }
    elif op == "remove":
        return {
            "op": op,
            "path": "/" + path_str
        }
    else:
        # make sure there is no nop generated which would create an ambiguous nop
        new_v = generate_value()
        while new_v == v:
            new_v = generate_value()
        return {
            "op": op,
            "path": "/" + path_str,
            "value": new_v
        }

def main():
    parser = argparse.ArgumentParser(description='Generate an eval for JSON Patching of nested objects.')
    parser.add_argument('--output', type=str, default="json_patch_object/file.jsonl", help='Output file')
    parser.add_argument('--n', type=int, default=100, help='Number of cases to create.')
    parser.add_argument('--key_format', type=str, default="uuid", help='key format: uuid or short')
    args = parser.parse_args()

    with open(args.output, "w") as f:
        for _ in range(args.n):
            # mutate globals
            global key_set
            global key_format
            key_set = set()
            key_format = args.key_format

            d = generate_dict(4, lambda: generate_dict(4, lambda: generate_dict(4, lambda: generate_value())))
            # d = generate_dict(2, lambda: generate_dict(2, lambda: generate_dict(2, lambda: generate_value())))
            # print(json.dumps(d, indent=2))

            path = []
            while len(path) == 0:
                path = pick_path(d)

            op = pick_operation(d, path)
            # print(op)

            patched = jsonpatch.apply_patch(d, [op])

            f.write(json.dumps({
                "input": [
                    {
                        "role": "system",
                        "content": f"Return a JSON Patch array with no additional commentary.\nReturn the minimal set of JSON Patch operations required; do not return ineffective or redundant operations.\nJSON Patch operations should be JSON objects with the keys \"op\", \"path\", and \"value\".\n\"op\" can be one of \"add\", \"remove\", or \"replace\".\n\"path\" is a JSON Pointer to the key in the base JSON to which the operation should be applied.\nIf the operation is \"add\" or \"replace\", \"value\" is the value to be added or replaced.\nIf the operation is \"remove\", \"value\" should be not included.\nReturn the JSON Patch array on a single line in the following format: [{{\"op\": \"replace\", \"path\": \"/95d90676-2b2e-4152-9b48-5238ca7019a9/38184eb5-03b9-4f3a-9546-c76d4bc141ef\", \"value\": 385}}]"
                    },
                    {
                        "role": "user",
                        "content": f"Return the minimal JSON Patch array that when applied to the following JSON object: {json.dumps(d)} will result in the following object: {json.dumps(patched)}"
                    }
                ],
                "ideal": json.dumps([op]),
            }) + "\n")

if __name__ == "__main__":
    main()
