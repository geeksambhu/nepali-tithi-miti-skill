from nepali_tithi_miti.parsing import parse_ymd, to_ascii_digits, to_devanagari_digits

def test_digit_conversion():
    assert to_devanagari_digits("2083-02-18") == "२०८३-०२-१८"
    assert to_ascii_digits("२०८३-०२-१८") == "2083-02-18"

def test_parse_ymd():
    assert parse_ymd("2083/02/18") == (2083, 2, 18)
    assert parse_ymd("२०८३-०२-१८") == (2083, 2, 18)
