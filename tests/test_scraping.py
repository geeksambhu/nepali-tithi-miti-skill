from datetime import date

from nepali_tithi_miti.hamropatro import (
    parse_hamropatro_home_today,
    parse_month_html,
    parse_nepali_calendar_current_html,
    parse_nepali_patro_today_html,
)


def test_parse_hamropatro_home_today_block():
    html = """
    <html><body>
    <div>३० जेठ २०८३, शनिवार</div>
    <div>अधिक जेठ कृष्ण त्रयोदशी</div>
    <div>पञ्चाङ्ग: सुकर्मा गर कृत्तिका</div>
    <div>दिउँसोको १२:५७:१३</div>
    <div>Jun 13, 2026</div>
    </body></html>
    """

    day = parse_hamropatro_home_today(html)

    assert day is not None
    assert day.bs_date == "2083-02-30"
    assert day.ad_date == "2026-06-13"
    assert day.tithi_np == "अधिक जेठ कृष्ण त्रयोदशी"
    assert day.panchang == "सुकर्मा गर कृत्तिका"
    assert day.yoga == "सुकर्मा"
    assert day.karana == "गर"
    assert day.nakshatra == "कृत्तिका"


def test_parse_hamropatro_home_today_block_with_extra_lines():
    html = """
    <html><body>
    <nav>Hamro Patro</nav>
    <div>३० जेठ २०८३, शनिवार</div>
    <div>अधिक जेठ कृष्ण त्रयोदशी</div>
    <div>पञ्चाङ्ग: सुकर्मा गर कृत्तिका</div>
    <div>दिउँसोको १२ : ५७ : १३</div>
    <div>weather widget</div>
    <div>Jun 13, 2026</div>
    </body></html>
    """

    day = parse_hamropatro_home_today(html)

    assert day is not None
    assert day.bs_date == "2083-02-30"
    assert day.ad_date == "2026-06-13"
    assert day.tithi_np == "अधिक जेठ कृष्ण त्रयोदशी"
    assert day.panchang == "सुकर्मा गर कृत्तिका"


def test_parse_hamropatro_home_today_block_with_split_panchang():
    html = """
    <html><body>
    <div>३० जेठ २०८३, शनिवार</div>
    <div>अधिक जेठ कृष्ण त्रयोदशी</div>
    <div>पञ्चाङ्ग:</div>
    <div>सुकर्मा गर कृत्तिका</div>
    <div>दिउँसोको १२ : ५७ : १३</div>
    <div>Jun 13, 2026</div>
    </body></html>
    """

    day = parse_hamropatro_home_today(html)

    assert day is not None
    assert day.bs_date == "2083-02-30"
    assert day.tithi_np == "अधिक जेठ कृष्ण त्रयोदशी"
    assert day.panchang == "सुकर्मा गर कृत्तिका"


def test_parse_hamropatro_month_grid_block():
    html = """
    <html><body>
    <div>३० जेठ २०८३, शनिवार</div>
    <div>June 13, 2026</div>
    <div>अधिक जेठ कृष्ण त्रयोदशी</div>
    <div>पञ्चाङ्ग: सुकर्मा गर कृत्तिका</div>
    </body></html>
    """

    days = parse_month_html(html, 2083, 2, "https://www.hamropatro.com/calendar/2083/2")

    assert len(days) == 1
    assert days[0].bs_date == "2083-02-30"
    assert days[0].ad_date == "2026-06-13"
    assert days[0].tithi_np == "अधिक जेठ कृष्ण त्रयोदशी"


def test_parse_nepali_calendar_current_page_block():
    html = """
    <html><body>
    <h5>Jestha 2083</h5>
    <h5>May/Jun 2026</h5>
    <div>१८</div>
    <div>Jun 1</div>
    <div>प्रतिपदा</div>
    <div>३०</div>
    <div>13</div>
    <div>त्रयोदशी</div>
    </body></html>
    """

    day = parse_nepali_calendar_current_html(html, date(2026, 6, 13))

    assert day is not None
    assert day.bs_date == "2083-02-30"
    assert day.ad_date == "2026-06-13"
    assert day.tithi_np == "त्रयोदशी"


def test_parse_nepali_patro_today_block():
    html = """
    <html><body>
    <div>३० शनिवार</div>
    <div>13 June, 2026</div>
    <h2>जेठ, २०८३</h2>
    <div>ने.सं. ११४६, अनलागा</div>
    <div>अधिक ज्येष्ठ कृष्ण त्रयोदशी</div>
    <div>12:58:08</div>
    <div>PM</div>
    </body></html>
    """

    day = parse_nepali_patro_today_html(html, date(2026, 6, 13))

    assert day is not None
    assert day.bs_date == "2083-02-30"
    assert day.ad_date == "2026-06-13"
    assert day.weekday_np == "शनिवार"
    assert day.tithi_np == "अधिक ज्येष्ठ कृष्ण त्रयोदशी"
