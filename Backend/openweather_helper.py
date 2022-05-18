
def float_range(start, stop, increment):
    while start < stop:  # and not math.isclose(start, stop): Py>3.5
        yield start
        start += increment


def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int(n/precision+correction) * precision


def round_to_5(n):
    return round_to(n, 0.5)


def round_viewport(viewport):
    result = {'lat1': round_to_5(viewport['lat1']),
              'lon1': round_to_5(viewport['lon1']),
              'lat2': round_to_5(viewport['lat2']),
              'lon2': round_to_5(viewport['lon2']),
              'interval': round_to_5(viewport['interval'])}
    return result
