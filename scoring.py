"""User-provided image scoring; not a validated diagnostic instrument."""
SYMPTOMS = (
    ('안면홍조', 4), ('발한', 2), ('불면증', 2), ('신경질', 2),
    ('우울증', 1), ('현기증(어지럼증)', 1), ('피로감', 1), ('두통', 1),
    ('관절 / 근육통', 1), ('가슴두근거림', 1), ('질 건조감', 1),
)
LEVELS = ('없다', '약간', '보통', '심함')
MAX_SCORE = 51

def calculate(answers):
    if len(answers) != len(SYMPTOMS) or any(type(x) is not int or x not in range(4) for x in answers):
        raise ValueError('11개 문항에 모두 응답해주세요.')
    return sum(value * weight for value, (_, weight) in zip(answers, SYMPTOMS))
