from nepali_tithi_miti.calendar import ad_to_bs, bs_to_ad, get_today_nepali_date


def test_ad_to_bs_uses_nepali_datetime():
    result = ad_to_bs("2026-06-13")

    assert result.output_date == "2083-02-30"
    assert result.source == "nepali-datetime"
    assert result.confidence == "high"


def test_bs_to_ad_uses_nepali_datetime():
    result = bs_to_ad("2083-02-30")

    assert result.output_date == "2026-06-13"
    assert result.source == "nepali-datetime"
    assert result.confidence == "high"


def test_today_returns_bs_date():
    result = get_today_nepali_date()

    assert result["ad_today"]
    assert result["bs_today"]
    assert result["conversion_source"] == "nepali-datetime"
    assert result["conversion_confidence"] == "high"
