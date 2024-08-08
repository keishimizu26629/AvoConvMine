def flatten_json(data, prefix=''):
    items = []
    for key, value in data.items():
        new_key = f"{prefix}{key}".replace('_', ' ')
        if isinstance(value, dict):
            items.extend(flatten_json(value, f"{new_key} ").items())
        elif isinstance(value, list):
            items.append((new_key, ' '.join(map(str, value))))
        else:
            items.append((new_key, str(value)))
    return dict(items)

def flatten_json_with_prefix(data, prefix=''):
    result = {}
    for key, value in data.items():
        new_key = f"{prefix}{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten_json_with_prefix(value, f"{new_key}_"))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    result.update(flatten_json_with_prefix(item, f"{new_key}_{i}_"))
                else:
                    result[f"{new_key}_{i}"] = item
        else:
            result[new_key] = value
    return result
