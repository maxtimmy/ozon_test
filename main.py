import requests


u = 'https://akabab.github.io/superhero-api/api/all.json'


# берет рост героя
def ht(a):

    b = a.get('appearance', {}).get('height', [])

    if len(b) < 2:
        return 0

    c = b[1]

    if c == '-' or c == '':
        return 0

    if 'meters' in c:
        return int(float(c.replace(' meters', '')) * 100)

    if 'cm' in c:
        try:
            return int(c.replace(' cm', ''))
        except ValueError:
            raise ValueError('height error')

    raise ValueError('height error')


# смотрит есть ли работа
def wk(a):
    b = a.get('work', {}).get('occupation', '')

    if b == '-' or b.strip() == '':
        return False

    return True


# ищет героя
def fd(g, j):
    if type(g) != str:
        raise TypeError('gender error')

    if type(j) != bool:
        raise TypeError('work error')

    if g != 'Male' and g != 'Female':
        raise ValueError('gender error')

    r = requests.get(u)
    r.raise_for_status()

    d = r.json()

    m = None
    z = 0

    for a in d:
        b = a.get('appearance', {}).get('gender')

        if b != g:
            continue

        if wk(a) != j:
            continue

        try:
            c = ht(a)
        except ValueError:
            continue

        if c > z:
            z = c
            m = a


    return m


if __name__ == '__main__':
    print(fd('Male', True))
