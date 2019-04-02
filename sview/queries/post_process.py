def as_multiline_graph_data(data, time_key, val_key, group_by):
    tmp = {}
    result = []
    groups = set()

    for i in data:
        if not i[time_key] in tmp:
            tmp[i[time_key]] = {}

        tmp[i[time_key]][i[group_by]] = i[val_key]
        groups.add(i[group_by])

    # Simply make one "official" order of the grouped variable for the rest of function
    groups = [g for g in groups]

    for key in sorted(tmp):
        item_dict = {
            time_key: key,
        }
        for i, g in enumerate(groups):
            item_dict[i] = tmp[key][g] if g in tmp[key] else 0
        result.append(item_dict)

    return {
        "labels": groups,
        "ykeys": [i for i in range(len(groups))],
        "data": result,
    }


def as_map_data(data, key_key, val_key):
    return {i[key_key]: i[val_key] for i in data}
