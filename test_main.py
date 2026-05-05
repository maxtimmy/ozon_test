import main
import pytest
from unittest.mock import patch


# делает героя
def mk(n, g, h, w):
    return {
        'name': n,
        'appearance': {
            'gender': g,
            'height': ['0', str(h) + ' cm']
        },
        'work': {
            'occupation': w
        }
    }


class Rsp:
    pass


# ответ апишки
def rs(d):
    r = Rsp()
    r.d = d
    r.raise_for_status = lambda: None
    r.json = lambda: r.d

    return r


# подмена апи
def pt(d):
    return patch('main.requests.get', return_value=rs(d))


# мужик работает
@pytest.mark.positive
def t1():
    r = main.fd('Male', True)

    assert r['name'] == 'Utgard-Loki'


# мужик не мужик мужик не работает
@pytest.mark.positive
def t2():
    r = main.fd('Male', False)

    assert r['name'] == 'Ymir'


# женщина работает?
@pytest.mark.positive
def t3():
    r = main.fd('Female', True)

    assert r['name'] == 'Giganta'


# женщина не работает??
@pytest.mark.positive
def t4():
    r = main.fd('Female', False)

    assert r['name'] == 'Ardina'


# запрос был
@pytest.mark.positive
def t5():
    d = [
        mk('a', 'Male', 180, 'job')
    ]

    x = []

    def gg(c):
        x.append(c)
        return rs(d)

    with patch('main.requests.get', gg):
        main.fd('Male', True)

    assert x[0] == main.u

# вернул пол
@pytest.mark.positive
def t6():
    r = main.fd('Male', True)

    assert r['appearance']['gender'] == 'Male'


# вернул работу
@pytest.mark.positive
def t7():
    r = main.fd('Female', True)

    assert main.wk(r) is True


# вернул рост
@pytest.mark.positive
def t8():
    r = main.fd('Male', False)

    assert main.ht(r) > 0


# нет) нет ничего
@pytest.mark.negative
def t9():
    d = [
        mk('a', 'Male', 180, 'job')
    ]

    with pt(d):
        r = main.fd('Female', False)

    assert r is None


# нет роста
@pytest.mark.negative
def ta():
    d = {
        'appearance': {
            'height': ['-', '-']
        }
    }

    assert main.ht(d) == 0


# нет работы
@pytest.mark.negative
def tb():
    d = {
        'work': {
            'occupation': '   '
        }
    }

    assert main.wk(d) is False


# кривой герой
@pytest.mark.negative
def tc():
    d = [
        {
            'name': 'bad',
            'work': {
                'occupation': 'job'
            }
        },
        mk('ok', 'Male', 190, 'job')
    ]

    with pt(d):
        r = main.fd('Male', True)

    assert r['name'] == 'ok'


# пол сломался
@pytest.mark.negative
def td():
    with pytest.raises(ValueError, match='gender error'):
        main.fd('Robot', True)


# работа сломалась
@pytest.mark.negative
def te():
    with pytest.raises(TypeError, match='work error'):
        main.fd('Male', 'yes')


# работа числом
@pytest.mark.negative
def tf():
    with pytest.raises(TypeError, match='work error'):
        main.fd('Female', 1)
