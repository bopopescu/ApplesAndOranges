def get_display(key, list):
    d = dict(list)
    if key in d:
        return d[key]
    return None