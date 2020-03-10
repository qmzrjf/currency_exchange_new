CURR_USD, CURR_EUR = range(1, 3)
CURRENCY_CHOICES = (
    (CURR_USD, 'USD'),
    (CURR_EUR, 'EUR'),
)

SR_PRIVAT, SR_MONO, SR_VKUR, SR_OTP, SR_PUMB, SR_ALFA = range(1, 7)
SOURCE_CHOICES = (
    (SR_PRIVAT, 'PrivatBank'),
    (SR_MONO, 'MonoBank'),
    (SR_VKUR, 'Vkurse'),
    (SR_OTP, 'OTP'),
    (SR_PUMB, 'Pumb'),
    (SR_ALFA, 'Alfa'),

)

CURRENCY_CHOICES_DICT = {i[0]: i[1] for i in CURRENCY_CHOICES}
