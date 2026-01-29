
# для чисел от 100 до 1000, поиск числа Армстронга 
# (также самовлюблённое число, совершенный цифровой инвариант; англ. pluperfect digital invariant, PPDI)
def pluperfect_digital_invariant(num: int) -> bool:
    ppdi = False
    low = num % 10
    mid = num // 10 % 10
    high = num // 100
    if num == low ** 3 + mid ** 3 + high ** 3:
        ppdi = True
    return ppdi
