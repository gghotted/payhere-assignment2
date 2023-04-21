from jamo import hangul_to_jamo, jamo_to_hcj


def convert_to_chosung(s: str):
    result = ""
    for c in s:
        """
        초성, 중성, 종성으로 분리
        """
        jamo = hangul_to_jamo(c)

        """
        U+11xx -> U+3xxx
        """
        hcj = jamo_to_hcj(jamo)

        chosung = next(hcj)
        result += chosung

    return result
