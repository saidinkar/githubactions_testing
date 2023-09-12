def maybe_to_tuple(anything):
    if anything is None:
        return ()

    if isinstance(anything, tuple):
        return anything

    if isinstance(anything, list):
        return tuple(anything)

    return (anything,)


def maybe_to_list(anything):
    if anything is None:
        return []

    if isinstance(anything, list):
        return anything

    if isinstance(anything, tuple):
        return list(anything)

    return [anything]


def __clean_helper(data):
    if not isinstance(data, dict):
        return data

    return dict((k, __clean_helper(v)) for k, v in data.items() if v is not None)


def clean(anything):
    if anything is None:
        return {}

    if not isinstance(anything, dict):
        raise Exception("dict expected.")

    return __clean_helper(anything)


def compact(d):
    return {k: v for k, v in d.items() if v is not None}
