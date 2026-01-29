import pytest

import num_utils

def test_sum():
    assert sum([1,2,3]) == 6

# примеры чисел Армстронга -- 153, 370, 371
@pytest.mark.parametrize("num", [153, 370, 371])
def test_pluperfect_digital_invariant(num):
    assert num_utils.pluperfect_digital_invariant(num)

