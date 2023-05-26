import json
import random
import uuid
import jsonpatch

N = 100

def deep_get(v, *ks):
    for k in ks:
        try:
            v = v[k]
        except KeyError:
            return None
    return v

def generate_dict(num_keys, value_func):
    return {str(uuid.uuid4()): value_func() for _ in range(num_keys)}

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
            "path": "/" + path_str + "/" + str(uuid.uuid4()),
            "value": random.randint(1, 1000)
        }
    elif op == "remove":
        return {
            "op": op,
            "path": "/" + path_str
        }
    else:
        return {
            "op": op,
            "path": "/" + path_str,
            "value": random.randint(1, 1000)
        }

def main():
    with open("json_patch_object/file.jsonl", "w") as f:
        for _ in range(N):
            d = generate_dict(3, lambda: generate_dict(3, lambda: generate_dict(3, lambda: random.randint(1, 1000))))

            path = []
            while len(path) == 0:
                path = pick_path(d)

            op = pick_operation(d, path)

            patched = jsonpatch.apply_patch(d, [op])

            f.write(json.dumps({
                "input": [
                    {
                        "role": "system",
                        "content": f"Return a JSON Patch array with no additional commentary. Return the minimal set of JSON Patch operations required; do not return ineffective or redundant operations. Return the JSON Patch array on a single line in the following format: [{{\"op\": \"replace\", \"path\": \"/95d90676-2b2e-4152-9b48-5238ca7019a9/38184eb5-03b9-4f3a-9546-c76d4bc141ef\", \"value\": 385}}]"
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
