def get_vecs(data: str, separator: str = ";"):
    lines = data.splitlines(keepends=False)
    res = []
    for i in lines:
        tmp = i.split(sep=separator)
        valid = True
        dim = []
        for v in tmp:
            try:
                dim.append(float(v))
            except ValueError:
                valid = False
        if valid:
            res.append(dim)
    return res
