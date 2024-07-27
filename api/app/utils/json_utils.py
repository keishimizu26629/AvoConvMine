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
