import datetime
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(
    page_title="Налоговое планирование",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

:root {
    --primary-color: #1e3a8a;
    --background-color: #ffffff;
    --secondary-background-color: #f8fafc;
    --text-color: #000000;
}

html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Montserrat', sans-serif !important;
    background-color: #ffffff !important;
    color: #000000 !important;
}

[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
    background-color: #f8fafc !important;
    border-right: 1px solid #cbd5e1 !important;
    color: #000000 !important;
}

h1, h2, h3, h4, h5, h6, p, span, div, label, li, td, th, a, small {
    color: #000000 !important;
    font-family: 'Montserrat', sans-serif !important;
}

/* Кнопки (обычные, secondary, primary, download, +/- в number_input) */
button,
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"],
[data-testid="stDownloadButton"] button,
[data-testid="stNumberInputStepUp"],
[data-testid="stNumberInputStepDown"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #94a3b8 !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

button:hover,
[data-testid="baseButton-secondary"]:hover,
[data-testid="baseButton-primary"]:hover,
[data-testid="stDownloadButton"] button:hover,
[data-testid="stNumberInputStepUp"]:hover,
[data-testid="stNumberInputStepDown"]:hover {
    background-color: #e2e8f0 !important;
    color: #000000 !important;
    border-color: #64748b !important;
}

button:focus,
button:active,
[data-testid="baseButton-secondary"]:focus,
[data-testid="baseButton-primary"]:focus,
[data-testid="stNumberInputStepUp"]:focus,
[data-testid="stNumberInputStepDown"]:focus {
    background-color: #dbeafe !important;
    color: #000000 !important;
    border-color: #1e3a8a !important;
    box-shadow: none !important;
}

/* Иконки и SVG внутри всех кнопок и полей ввода */
button svg,
button svg path,
[data-testid="stNumberInputStepUp"] svg,
[data-testid="stNumberInputStepDown"] svg,
[data-testid="stNumberInputStepUp"] svg path,
[data-testid="stNumberInputStepDown"] svg path,
[data-baseweb="select"] svg,
[data-baseweb="select"] svg path,
[data-testid="stExpander"] svg,
[data-testid="stExpander"] svg path {
    fill: #000000 !important;
    color: #000000 !important;
    stroke: #000000 !important;
}

/* Поля ввода: NumberInput, TextInput, DateInput, Selectbox */
input,
textarea,
[data-baseweb="input"],
[data-baseweb="input"] > div,
[data-baseweb="base-input"],
[data-baseweb="select"] > div,
[data-testid="stNumberInput"] div[data-baseweb="input"],
[data-testid="stDateInput"] div[data-baseweb="input"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    border-color: #cbd5e1 !important;
}

input:hover,
input:focus,
[data-baseweb="input"]:hover,
[data-baseweb="input"]:focus-within,
[data-baseweb="select"] > div:hover {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    border-color: #1e3a8a !important;
}

/* Выпадающие списки и всплывающий календарь */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"],
ul[role="listbox"],
[data-testid="stSelectboxVirtualDropdown"],
div[data-baseweb="calendar"],
div[data-baseweb="calendar"] * {
    background-color: #ffffff !important;
    color: #000000 !important;
}

li[role="option"],
[data-testid="stSelectboxVirtualDropdown"] li,
div[role="gridcell"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}

li[role="option"]:hover,
li[role="option"][aria-selected="true"],
[data-testid="stSelectboxVirtualDropdown"] li:hover,
div[role="gridcell"]:hover {
    background-color: #e2e8f0 !important;
    color: #000000 !important;
}

div[role="gridcell"][aria-selected="true"] {
    background-color: #dbeafe !important;
    color: #000000 !important;
    font-weight: 700 !important;
}

/* Вкладки (Tabs) */
[data-baseweb="tab-list"] {
    background-color: #ffffff !important;
    border-bottom: 2px solid #cbd5e1 !important;
}

[data-baseweb="tab"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: none !important;
}

[data-baseweb="tab"]:hover {
    background-color: #f1f5f9 !important;
    color: #000000 !important;
}

[data-baseweb="tab"][aria-selected="true"] {
    background-color: #f8fafc !important;
    color: #000000 !important;
    font-weight: 700 !important;
    border-bottom: 3px solid #1e3a8a !important;
}

/* Сворачиваемые блоки (Expander) */
[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary:hover {
    background-color: #f8fafc !important;
    color: #000000 !important;
}

/* Карточки метрик */
.kpi-card {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 8px;
}

.kpi-title {
    font-size: 12px;
    font-weight: 600;
    color: #334155 !important;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 6px;
}

.kpi-value {
    font-size: 20px;
    font-weight: 700;
    color: #000000 !important;
    font-variant-numeric: tabular-nums;
}

.kpi-sub {
    font-size: 11px;
    color: #475569 !important;
    margin-top: 4px;
}

/* Горизонтальная матрица */
.matrix-wrap {
    overflow-x: auto;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    background-color: #ffffff;
}

table.plan-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    font-variant-numeric: tabular-nums;
    background-color: #ffffff;
}

table.plan-table th {
    background-color: #f1f5f9;
    color: #000000 !important;
    font-weight: 700;
    padding: 10px 8px;
    border: 1px solid #cbd5e1;
    text-align: center;
    white-space: nowrap;
}

table.plan-table th.row-header {
    text-align: left;
    min-width: 230px;
    position: sticky;
    left: 0;
    z-index: 2;
    background-color: #f1f5f9;
}

table.plan-table td {
    padding: 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
    min-width: 155px;
    background-color: #ffffff;
    color: #000000 !important;
}

table.plan-table td.row-label {
    font-weight: 600;
    background-color: #f8fafc;
    position: sticky;
    left: 0;
    z-index: 1;
    min-width: 230px;
}

table.plan-table td.cell-sale-zero {
    background-color: #f0fdf4 !important;
}

table.plan-table td.cell-sale-tax {
    background-color: #fffbeb !important;
}

table.plan-table tr.summary-row td {
    background-color: #f1f5f9 !important;
    font-weight: 700;
    border-top: 2px solid #94a3b8;
}

.cell-line-main {
    font-weight: 700;
    font-size: 12px;
    color: #000000 !important;
}

.cell-line-sub {
    font-size: 11px;
    color: #334155 !important;
    margin-top: 2px;
}

.cell-line-tax {
    font-size: 11px;
    font-weight: 600;
    color: #000000 !important;
    margin-top: 2px;
}

/* Предупреждения и инфо-блоки */
[data-testid="stAlert"] {
    background-color: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    color: #000000 !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

YEARS = list(range(2026, 2036))
UNIT_PRICE_START = 1000.0


def fmt_num(val: float) -> str:
    return f"{int(round(val)):,}".replace(",", " ")


def fmt_float(val: float, digits: int = 2) -> str:
    return f"{val:,.{digits}f}".replace(",", " ")


def get_min_iis_years(open_date: datetime.date) -> int:
    y = open_date.year
    if y <= 2026:
        return 5
    elif y == 2027:
        return 6
    elif y == 2028:
        return 7
    elif y == 2029:
        return 8
    elif y == 2030:
        return 9
    return 10


def full_years_between(start_dt: datetime.date, end_dt: datetime.date) -> int:
    if end_dt <= start_dt:
        return 0
    years = end_dt.year - start_dt.year
    if (end_dt.month, end_dt.day) < (start_dt.month, start_dt.day):
        years -= 1
    return max(0, years)


def calc_ndfl_2027(taxable_addition: float, prev_base: float):
    if taxable_addition <= 0:
        return 0.0, "налогооблагаемая база равна 0 руб., налог = 0 руб."
    brackets = [
        (2_400_000.0, 0.13, "13%"),
        (5_000_000.0, 0.15, "15%"),
        (20_000_000.0, 0.18, "18%"),
        (50_000_000.0, 0.20, "20%"),
        (float("inf"), 0.22, "22%"),
    ]
    tax_total = 0.0
    details = []
    cur_start = prev_base
    cur_end = prev_base + taxable_addition
    low_bound = 0.0
    for high_bound, rate, rate_lbl in brackets:
        seg_start = max(cur_start, low_bound)
        seg_end = min(cur_end, high_bound)
        if seg_end > seg_start:
            chunk = seg_end - seg_start
            chunk_tax = chunk * rate
            tax_total += chunk_tax
            details.append(
                f"по {rate_lbl} облагается {fmt_num(chunk)} руб. (налог {fmt_num(chunk_tax)} руб.)"
            )
        low_bound = high_bound
    return tax_total, ", ".join(details)


def compute_xirr(cashflows):
    if not cashflows or len(cashflows) < 2:
        return 0.0
    has_pos = any(cf > 0 for _, cf in cashflows)
    has_neg = any(cf < 0 for _, cf in cashflows)
    if not (has_pos and has_neg):
        return 0.0
    t0 = min(dt for dt, _ in cashflows)
    days = [(dt - t0).days / 365.0 for dt, _ in cashflows]
    amounts = [cf for _, cf in cashflows]

    def npv(rate):
        if rate <= -0.9999:
            return float("inf")
        return sum(a / ((1.0 + rate) ** t) for a, t in zip(amounts, days))

    low, high = -0.95, 5.0
    for _ in range(120):
        mid = (low + high) / 2.0
        val = npv(mid)
        if abs(val) < 1e-4:
            return mid * 100.0
        if val > 0:
            low = mid
        else:
            high = mid
    return ((low + high) / 2.0) * 100.0


st.title("Налоговое планирование")
st.caption("Индивидуальная модель управления капиталом: комбинация контуров ИИС-3 и ОПИФ ЛДВ (шкала НДФЛ 2027 года)")

with st.sidebar:
    st.header("Параметры портфеля")
    total_capital = st.number_input(
        "Общий капитал (руб.)",
        min_value=1_000_000,
        max_value=100_000_000_000,
        value=300_000_000,
        step=10_000_000,
        format="%d"
    )
    annual_return_pct = st.number_input(
        "Ожидаемая доходность (% годовых)",
        min_value=0.0,
        max_value=100.0,
        value=14.0,
        step=0.5,
        format="%.1f"
    )
    annual_return = annual_return_pct / 100.0

    st.subheader("Распределение по счетам (%)")
    w_iis1 = st.number_input("Доля ИИС-3 №1 (%)", min_value=0.0, max_value=100.0, value=11.0, step=1.0, format="%.1f")
    w_iis2 = st.number_input("Доля ИИС-3 №2 (%)", min_value=0.0, max_value=100.0, value=11.0, step=1.0, format="%.1f")
    w_iis3 = st.number_input("Доля ИИС-3 №3 (%)", min_value=0.0, max_value=100.0, value=11.0, step=1.0, format="%.1f")
    w_ldv = max(0.0, round(100.0 - (w_iis1 + w_iis2 + w_iis3), 2))
    st.markdown(f"**Доля ОПИФ ЛДВ:** {w_ldv:.1f}%")

    if w_iis1 + w_iis2 + w_iis3 > 100.0:
        st.error("Сумма долей ИИС-3 превышает 100%.")

    with st.expander("Даты открытия счетов", expanded=True):
        d_iis1 = st.date_input("Дата открытия ИИС-3 №1", value=datetime.date(2025, 12, 1))
        d_iis2 = st.date_input("Дата открытия ИИС-3 №2", value=datetime.date(2025, 12, 1))
        d_iis3 = st.date_input("Дата открытия ИИС-3 №3", value=datetime.date(2025, 12, 1))
        d_ldv = st.date_input("Дата покупки паев ОПИФ ЛДВ", value=datetime.date(2026, 1, 15))

cap_iis1 = total_capital * (w_iis1 / 100.0)
cap_iis2 = total_capital * (w_iis2 / 100.0)
cap_iis3 = total_capital * (w_iis3 / 100.0)
cap_ldv = total_capital * (w_ldv / 100.0)

pools = [
    {
        "id": "iis1",
        "label": f"ИИС-3 №1 (откр. {d_iis1.strftime('%d.%m.%Y')})",
        "short_label": "ИИС-3 №1",
        "contour": "IIS3",
        "open_date": d_iis1,
        "min_years": get_min_iis_years(d_iis1),
        "start_cap": cap_iis1,
        "units": int(round(cap_iis1 / UNIT_PRICE_START)),
    },
    {
        "id": "iis2",
        "label": f"ИИС-3 №2 (откр. {d_iis2.strftime('%d.%m.%Y')})",
        "short_label": "ИИС-3 №2",
        "contour": "IIS3",
        "open_date": d_iis2,
        "min_years": get_min_iis_years(d_iis2),
        "start_cap": cap_iis2,
        "units": int(round(cap_iis2 / UNIT_PRICE_START)),
    },
    {
        "id": "iis3",
        "label": f"ИИС-3 №3 (откр. {d_iis3.strftime('%d.%m.%Y')})",
        "short_label": "ИИС-3 №3",
        "contour": "IIS3",
        "open_date": d_iis3,
        "min_years": get_min_iis_years(d_iis3),
        "start_cap": cap_iis3,
        "units": int(round(cap_iis3 / UNIT_PRICE_START)),
    },
    {
        "id": "ldv",
        "label": f"ОПИФ ЛДВ (покупка {d_ldv.strftime('%d.%m.%Y')})",
        "short_label": "ОПИФ ЛДВ",
        "contour": "LDV",
        "open_date": d_ldv,
        "min_years": 3,
        "start_cap": cap_ldv,
        "units": int(round(cap_ldv / UNIT_PRICE_START)),
    },
]

if "sales_plan" not in st.session_state:
    st.session_state.sales_plan = {p["id"]: {y: 0 for y in YEARS} for p in pools}

for p in pools:
    if p["id"] not in st.session_state.sales_plan:
        st.session_state.sales_plan[p["id"]] = {y: 0 for y in YEARS}
    for y in YEARS:
        if y not in st.session_state.sales_plan[p["id"]]:
            st.session_state.sales_plan[p["id"]][y] = 0


def run_optimizer():
    new_plan = {p["id"]: {y: 0 for y in YEARS} for p in pools}
    iis_pools = [p for p in pools if p["contour"] == "IIS3" and p["units"] > 0]
    iis_pools_sorted = sorted(iis_pools, key=lambda x: (x["open_date"].year + x["min_years"], x["id"]))

    used_iis_years = set()
    terminal_year = YEARS[-1]
    last_iis_close_year = None

    for p in iis_pools_sorted:
        eligible_years = [
            y for y in YEARS
            if full_years_between(p["open_date"], datetime.date(y, 12, 25)) >= p["min_years"]
        ]
        chosen_y = None
        for y in eligible_years:
            if y not in used_iis_years:
                chosen_y = y
                used_iis_years.add(y)
                break
        if chosen_y is None and eligible_years:
            chosen_y = eligible_years[-1]
        if chosen_y is not None:
            new_plan[p["id"]][chosen_y] = p["units"]
            if last_iis_close_year is None or chosen_y > last_iis_close_year:
                last_iis_close_year = chosen_y

    if last_iis_close_year is not None:
        terminal_year = last_iis_close_year

    ldv_pool = next(p for p in pools if p["id"] == "ldv")
    rem_ldv = ldv_pool["units"]
    for y in YEARS:
        if rem_ldv <= 0 or y > terminal_year:
            break
        deal_dt = datetime.date(y, 12, 25)
        held_years = full_years_between(ldv_pool["open_date"], deal_dt)
        if y == terminal_year:
            new_plan["ldv"][y] = rem_ldv
            rem_ldv = 0
        elif held_years >= 3:
            limit_rub = 3_000_000.0 * held_years
            t_growth = max(0.0, (deal_dt - ldv_pool["open_date"]).days / 365.0)
            price_y = UNIT_PRICE_START * ((1.0 + annual_return) ** t_growth)
            gain_per_unit = price_y - UNIT_PRICE_START
            if gain_per_unit > 0:
                optimal_units = int(math.floor(limit_rub / gain_per_unit))
                sell_u = min(rem_ldv, max(0, optimal_units))
                new_plan["ldv"][y] = sell_u
                rem_ldv -= sell_u

    st.session_state.sales_plan = new_plan
    for p in pools:
        for y in YEARS:
            w_key = f"inp_{p['id']}_{y}"
            if w_key in st.session_state:
                st.session_state[w_key] = new_plan[p["id"]][y]


def reset_plan():
    st.session_state.sales_plan = {p["id"]: {y: 0 for y in YEARS} for p in pools}
    for p in pools:
        for y in YEARS:
            w_key = f"inp_{p['id']}_{y}"
            if w_key in st.session_state:
                st.session_state[w_key] = 0


col_btn1, col_btn2, col_btn3 = st.columns([2, 1.5, 4.5])
with col_btn1:
    if st.button("Оптимизировать налоговый план", use_container_width=True):
        run_optimizer()
with col_btn2:
    if st.button("Очистить график продаж", use_container_width=True):
        reset_plan()

with st.expander("Как работает кнопка «Оптимизировать налоговый план»", expanded=False):
    rules_text = chr(10).join([
        "- **Цель:** Снизить эффективную ставку налога до минимума за счет полной выборки доступных льгот и полностью реализовать портфель к моменту закрытия последнего счета ИИС-3.",
        "- **Контур ИИС-3:** Счета закрываются по одному в календарный год сразу после достижения минимального срока владения (5-10 лет в зависимости от года открытия) для ежегодного использования вычета 30 000 000 руб.",
        "- **Контур ОПИФ ЛДВ:** Начиная с 3-го полного года владения ежегодно продается объем паев, прибыль по которому полностью перекрывается вычетом ЛДВ (3 000 000 руб. x полные годы владения). В год закрытия последнего ИИС-3 реализуется весь остаток бумаг.",
    ])
    st.markdown(rules_text)

# Движок расчета
rem_units = {p["id"]: p["units"] for p in pools}
matrix_cells = {p["id"]: {} for p in pools}
yearly_summary = {}
deals_records = []
log_lines = []
cashflows = []

for p in pools:
    if p["units"] > 0:
        cashflows.append((p["open_date"], -float(p["units"] * UNIT_PRICE_START)))

for y in YEARS:
    deal_dt = datetime.date(y, 12, 25)
    log_lines.append(f"=== ГОД {y} (Дата оценки и сделок: {deal_dt.strftime('%d.%m.%Y')}) ===")
    acc_tax_base_year = 0.0
    iis_deduction_used_year = 0.0

    y_gross_out = 0.0
    y_gain_before = 0.0
    y_deduction = 0.0
    y_base_after = 0.0
    y_tax = 0.0
    y_tax_no_benefit = 0.0
    y_end_value = 0.0
    any_deal_in_year = False

    for p in pools:
        t_growth = max(0.0, (deal_dt - p["open_date"]).days / 365.0)
        price_y = UNIT_PRICE_START * ((1.0 + annual_return) ** t_growth)
        avail_u = rem_units[p["id"]]
        req_u = int(st.session_state.sales_plan[p["id"]].get(y, 0))
        sell_u = min(avail_u, max(0, req_u))

        if sell_u > 0:
            any_deal_in_year = True
            is_full = (sell_u == avail_u)
            sale_type_str = "ПОЛНАЯ" if is_full else "ЧАСТИЧНАЯ"
            revenue = sell_u * price_y
            cost = sell_u * UNIT_PRICE_START
            gain = max(0.0, revenue - cost)
            held_years = full_years_between(p["open_date"], deal_dt)

            deduction = 0.0
            deduction_note = ""
            if p["contour"] == "IIS3":
                if not is_full:
                    deduction_note = "Льгота ИИС-3 не применена: продана только часть бумаг (требуется полное закрытие счета)."
                elif held_years < p["min_years"]:
                    deduction_note = f"Льгота ИИС-3 не применена: прошло {held_years} полн. лет из требуемых {p['min_years']} лет."
                else:
                    avail_iis_lim = max(0.0, 30_000_000.0 - iis_deduction_used_year)
                    deduction = min(gain, avail_iis_lim)
                    iis_deduction_used_year += deduction
                    deduction_note = (
                        f"ИИС-3 закрыт полностью. Срок: {held_years} полн. лет (>= {p['min_years']}). "
                        f"Доступный годовой лимит: {fmt_num(avail_iis_lim)} руб. Применен вычет: {fmt_num(deduction)} руб."
                    )
            else:
                if held_years < 3:
                    deduction_note = f"ЛДВ не применена: срок владения {held_years} полн. лет (требуется >= 3 лет)."
                else:
                    ldv_lim = 3_000_000.0 * held_years
                    deduction = min(gain, ldv_lim)
                    deduction_note = (
                        f"ЛДВ применена (срок {held_years} полн. лет сохранен при обмене ОПИФ). "
                        f"Лимит пула: 3 000 000 x {held_years} = {fmt_num(ldv_lim)} руб. Применен вычет: {fmt_num(deduction)} руб."
                    )

            base_after = max(0.0, gain - deduction)
            tax_paid, tax_detail = calc_ndfl_2027(base_after, acc_tax_base_year)
            tax_no_ben, _ = calc_ndfl_2027(gain, acc_tax_base_year)
            acc_tax_base_year += base_after

            rem_units[p["id"]] -= sell_u
            net_cash = revenue - tax_paid
            if net_cash > 0:
                cashflows.append((deal_dt, net_cash))

            eff_rate = (tax_paid / gain * 100.0) if gain > 0 else 0.0

            y_gross_out += revenue
            y_gain_before += gain
            y_deduction += deduction
            y_base_after += base_after
            y_tax += tax_paid
            y_tax_no_benefit += tax_no_ben

            rem_val_after = rem_units[p["id"]] * price_y
            y_end_value += rem_val_after

            matrix_cells[p["id"]][y] = {
                "is_sale": True,
                "revenue": revenue,
                "gain": gain,
                "base_after": base_after,
                "tax": tax_paid,
                "rem_val": rem_val_after,
                "sell_u": sell_u,
            }

            deals_records.append({
                "Год": y,
                "Счет": p["short_label"],
                "Тип сделки": sale_type_str,
                "Продано (шт.)": sell_u,
                "Выручка (руб.)": round(revenue),
                "База ДО льготы (руб.)": round(gain),
                "Вычет (руб.)": round(deduction),
                "База ПОСЛЕ льготы (руб.)": round(base_after),
                "Налог (руб.)": round(tax_paid),
                "Эфф. ставка (%)": round(eff_rate, 2),
                "Налог без льготы (руб.)": round(tax_no_ben),
            })

            log_lines.append(f"  [{p['label']} | {sale_type_str} ПРОДАЖА]")
            log_lines.append(
                f"   1. Объем: продано {fmt_num(sell_u)} шт. (остаток: {fmt_num(rem_units[p['id']])} шт.). "
                f"Цена на {deal_dt.strftime('%d.%m.%Y')}: 1000.00 x (1 + {annual_return_pct:.1f}%)^{t_growth:.2f} = {fmt_float(price_y, 2)} руб."
            )
            log_lines.append(
                f"   2. Финансовый результат: Выручка {fmt_num(revenue)} руб. - Затраты {fmt_num(cost)} руб. = База ДО льготы {fmt_num(gain)} руб."
            )
            log_lines.append(f"   3. Расчет льготы: {deduction_note}")
            log_lines.append(
                f"   4. База ПОСЛЕ льготы: {fmt_num(gain)} - {fmt_num(deduction)} = {fmt_num(base_after)} руб."
            )
            log_lines.append(
                f"   5. Расчет НДФЛ (шкала 2027 г. 13%-22%, накопленная база до сделки: {fmt_num(acc_tax_base_year - base_after)} руб.): "
                f"{tax_detail}. Итого налог = {fmt_num(tax_paid)} руб."
            )
            log_lines.append(
                f"   6. Эффективная ставка по пулу: {eff_rate:.2f}%. Налог без льготы: {fmt_num(tax_no_ben)} руб."
            )
        else:
            cur_val = avail_u * price_y
            cur_gain = max(0.0, cur_val - avail_u * UNIT_PRICE_START)
            y_end_value += cur_val
            matrix_cells[p["id"]][y] = {
                "is_sale": False,
                "cur_val": cur_val,
                "cur_gain": cur_gain,
            }

    if not any_deal_in_year:
        log_lines.append("  Сделок по продаже бумаг в этом году не запланировано.")

    y_net_out = y_gross_out - y_tax
    y_eff_rate = (y_tax / y_gain_before * 100.0) if y_gain_before > 0 else 0.0
    yearly_summary[y] = {
        "gross_out": y_gross_out,
        "net_out": y_net_out,
        "gain_before": y_gain_before,
        "deduction": y_deduction,
        "base_after": y_base_after,
        "tax": y_tax,
        "tax_no_benefit": y_tax_no_benefit,
        "eff_rate": y_eff_rate,
        "end_value": y_end_value,
    }

# Учет нереализованного остатка на конец 2035 года для корректного XIRR
final_end_val = yearly_summary[YEARS[-1]]["end_value"]
cf_for_xirr = list(cashflows)
if final_end_val > 0:
    cf_for_xirr.append((datetime.date(YEARS[-1], 12, 25), final_end_val))
net_cagr_pct = compute_xirr(cf_for_xirr)

tot_net_out = sum(yearly_summary[y]["net_out"] for y in YEARS)
tot_gain_before = sum(yearly_summary[y]["gain_before"] for y in YEARS)
tot_tax = sum(yearly_summary[y]["tax"] for y in YEARS)
tot_tax_no_ben = sum(yearly_summary[y]["tax_no_benefit"] for y in YEARS)
tot_saved = max(0.0, tot_tax_no_ben - tot_tax)
avg_eff_rate = (tot_tax / tot_gain_before * 100.0) if tot_gain_before > 0 else 0.0

# Верхняя панель KPI
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Выведено чистыми</div>'
        f'<div class="kpi-value">{fmt_num(tot_net_out)} руб.</div>'
        f'<div class="kpi-sub">Остаток в 2035 г.: {fmt_num(final_end_val)} руб.</div></div>',
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Налоговая экономия</div>'
        f'<div class="kpi-value">{fmt_num(tot_saved)} руб.</div>'
        f'<div class="kpi-sub">Без льгот налог: {fmt_num(tot_tax_no_ben)} руб.</div></div>',
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Эффективная ставка</div>'
        f'<div class="kpi-value">{avg_eff_rate:.2f}%</div>'
        f'<div class="kpi-sub">От реализованной прибыли</div></div>',
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Уплачено налога</div>'
        f'<div class="kpi-value">{fmt_num(tot_tax)} руб.</div>'
        f'<div class="kpi-sub">По шкале 2027 г. (13%-22%)</div></div>',
        unsafe_allow_html=True,
    )
with k5:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">Чистый CAGR (XIRR)</div>'
        f'<div class="kpi-value">{net_cagr_pct:.2f}%</div>'
        f'<div class="kpi-sub">После уплаты всех налогов</div></div>',
        unsafe_allow_html=True,
    )

tab1, tab2, tab3, tab4 = st.tabs([
    "1. План по годам (Матрица)",
    "2. Управление продажами",
    "3. Графики для клиента",
    "4. Проверка расчетов (Лог)",
])

with tab1:
    st.subheader("Горизонтальная матрица стратегии (2026–2035)")
    html_parts = ['<div class="matrix-wrap"><table class="plan-table"><thead><tr>']
    html_parts.append('<th class="row-header">Счет / Контур</th>')
    for y in YEARS:
        html_parts.append(f"<th>{y} г.</th>")
    html_parts.append("<th>Итого за 10 лет</th></tr></thead><tbody>")

    for p in pools:
        html_parts.append("<tr>")
        html_parts.append(
            f'<td class="row-label">{p["label"]}<br>'
            f'<span style="font-weight:400;font-size:11px;">Старт: {fmt_num(p["start_cap"])} руб. ({fmt_num(p["units"])} шт.)</span></td>'
        )
        p_tot_rev = 0.0
        p_tot_gain = 0.0
        p_tot_tax = 0.0
        for y in YEARS:
            c = matrix_cells[p["id"]][y]
            if c["is_sale"]:
                p_tot_rev += c["revenue"]
                p_tot_gain += c["gain"]
                p_tot_tax += c["tax"]
                td_cls = "cell-sale-zero" if c["tax"] == 0 else "cell-sale-tax"
                cell_html = (
                    f'<td class="{td_cls}">'
                    f'<div class="cell-line-main">Вывод: {fmt_num(c["revenue"])}</div>'
                    f'<div class="cell-line-sub">Доход: {fmt_num(c["gain"])}</div>'
                    f'<div class="cell-line-tax">База п/л: {fmt_num(c["base_after"])} | Налог: {fmt_num(c["tax"])}</div>'
                    f"</td>"
                )
            else:
                cell_html = (
                    f"<td>"
                    f'<div class="cell-line-main">{fmt_num(c["cur_val"])}</div>'
                    f'<div class="cell-line-sub">Доход: {fmt_num(c["cur_gain"])}</div>'
                    f"</td>"
                )
            html_parts.append(cell_html)

        html_parts.append(
            f'<td style="background-color:#f8fafc;">'
            f'<div class="cell-line-main">Вывод: {fmt_num(p_tot_rev)}</div>'
            f'<div class="cell-line-sub">Доход: {fmt_num(p_tot_gain)}</div>'
            f'<div class="cell-line-tax">Налог: {fmt_num(p_tot_tax)}</div>'
            f"</td></tr>"
        )

    # Итоговый подвал таблицы
    html_parts.append('<tr class="summary-row"><td class="row-label">Итого по году</td>')
    for y in YEARS:
        s = yearly_summary[y]
        html_parts.append(
            f"<td>"
            f'<div class="cell-line-main">Чистыми: {fmt_num(s["net_out"])}</div>'
            f'<div class="cell-line-sub">База п/л: {fmt_num(s["base_after"])}</div>'
            f'<div class="cell-line-tax">Налог: {fmt_num(s["tax"])} ({s["eff_rate"]:.2f}%)</div>'
            f"</td>"
        )
    html_parts.append(
        f"<td>"
        f'<div class="cell-line-main">Чистыми: {fmt_num(tot_net_out)}</div>'
        f'<div class="cell-line-sub">Доход: {fmt_num(tot_gain_before)}</div>'
        f'<div class="cell-line-tax">Налог: {fmt_num(tot_tax)} ({avg_eff_rate:.2f}%)</div>'
        f"</td></tr></tbody></table></div>"
    )
    st.markdown("".join(html_parts), unsafe_allow_html=True)

with tab2:
    st.subheader("Ручное управление продажами бумаг (в штуках)")
    selected_year = st.selectbox("Выберите год для редактирования продаж", YEARS, index=4)
    deal_dt_sel = datetime.date(selected_year, 12, 25)

    # Расчет доступного остатка к выбранному году
    avail_before_sel = {p["id"]: p["units"] for p in pools}
    for y_prev in YEARS:
        if y_prev >= selected_year:
            break
        for p in pools:
            sold_prev = min(avail_before_sel[p["id"]], int(st.session_state.sales_plan[p["id"]][y_prev]))
            avail_before_sel[p["id"]] -= sold_prev

    for p in pools:
        t_g = max(0.0, (deal_dt_sel - p["open_date"]).days / 365.0)
        pr_sel = UNIT_PRICE_START * ((1.0 + annual_return) ** t_g)
        max_u = avail_before_sel[p["id"]]
        held_y = full_years_between(p["open_date"], deal_dt_sel)

        c1, c2, c3, c4 = st.columns([3, 2, 1.5, 2.5])
        with c1:
            st.markdown(f"**{p['label']}**")
            st.caption(f"Доступно: {fmt_num(max_u)} шт. | Цена пая: {fmt_float(pr_sel, 2)} руб. | Срок: {held_y} полн. лет")
        with c2:
            cur_val_inp = min(max_u, int(st.session_state.sales_plan[p["id"]][selected_year]))
            new_u = st.number_input(
                f"Продать (шт.) — {p['short_label']}",
                min_value=0,
                max_value=max(0, max_u),
                value=cur_val_inp,
                step=100,
                key=f"inp_{p['id']}_{selected_year}",
                label_visibility="collapsed",
            )
            st.session_state.sales_plan[p["id"]][selected_year] = int(new_u)
        with c3:
            if st.button("Весь пул", key=f"all_{p['id']}_{selected_year}", use_container_width=True):
                st.session_state.sales_plan[p["id"]][selected_year] = max_u
                st.rerun()
        with c4:
            est_rev = new_u * pr_sel
            est_gain = max(0.0, est_rev - new_u * UNIT_PRICE_START)
            st.markdown(f"Выручка: **{fmt_num(est_rev)} руб.**")
            st.caption(f"Прибыль до льготы: {fmt_num(est_gain)} руб.")
        st.divider()

with tab3:
    st.subheader("Визуализация стратегии для клиента")
    df_chart = pd.DataFrame({
        "Год": [str(y) for y in YEARS],
        "Вывод чистыми (млн руб.)": [yearly_summary[y]["net_out"] / 1e6 for y in YEARS],
        "Эффективная ставка (%)": [yearly_summary[y]["eff_rate"] for y in YEARS],
        "Налог по схеме (млн руб.)": [yearly_summary[y]["tax"] / 1e6 for y in YEARS],
        "Налог без льгот (млн руб.)": [yearly_summary[y]["tax_no_benefit"] / 1e6 for y in YEARS],
        "Освобождено льготой (млн руб.)": [yearly_summary[y]["deduction"] / 1e6 for y in YEARS],
        "База после льготы (млн руб.)": [yearly_summary[y]["base_after"] / 1e6 for y in YEARS],
    })

    # График 1: Денежный поток и эффективная ставка
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(
        go.Bar(
            x=df_chart["Год"],
            y=df_chart["Вывод чистыми (млн руб.)"],
            name="Вывод чистыми (млн руб.)",
            marker_color="#1e3a8a",
        ),
        secondary_y=False,
    )
    fig1.add_trace(
        go.Scatter(
            x=df_chart["Год"],
            y=df_chart["Эффективная ставка (%)"],
            name="Эффективная ставка налога (%)",
            mode="lines+markers",
            line=dict(color="#b45309", width=3),
            marker=dict(size=8),
        ),
        secondary_y=True,
    )
    fig1.update_layout(
        title=dict(text="Ежегодный вывод средств и эффективная налоговая ставка", font=dict(color="#000000", size=16)),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Montserrat", color="#000000"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(color="#000000"), bgcolor="#ffffff"),
        hoverlabel=dict(bgcolor="#ffffff", font=dict(color="#000000")),
    )
    fig1.update_xaxes(title_text="Год", title_font=dict(color="#000000"), tickfont=dict(color="#000000"), gridcolor="#e2e8f0")
    fig1.update_yaxes(title_text="Вывод чистыми (млн руб.)", title_font=dict(color="#000000"), tickfont=dict(color="#000000"), gridcolor="#e2e8f0", secondary_y=False)
    fig1.update_yaxes(title_text="Ставка налога (%)", title_font=dict(color="#000000"), tickfont=dict(color="#000000"), secondary_y=True)
    st.plotly_chart(fig1, use_container_width=True)

    # График 2: Сравнение налогов
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df_chart["Год"],
        y=df_chart["Налог без льгот (млн руб.)"],
        name="Налог на обычном счете (млн руб.)",
        marker_color="#94a3b8",
    ))
    fig2.add_trace(go.Bar(
        x=df_chart["Год"],
        y=df_chart["Налог по схеме (млн руб.)"],
        name="Налог по стратегии ИИС-3 + ЛДВ (млн руб.)",
        marker_color="#15803d",
    ))
    fig2.update_layout(
        barmode="group",
        title=dict(text="Сравнение налоговой нагрузки по годам", font=dict(color="#000000", size=16)),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Montserrat", color="#000000"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(color="#000000"), bgcolor="#ffffff"),
        hoverlabel=dict(bgcolor="#ffffff", font=dict(color="#000000")),
    )
    fig2.update_xaxes(title_text="Год", title_font=dict(color="#000000"), tickfont=dict(color="#000000"), gridcolor="#e2e8f0")
    fig2.update_yaxes(title_text="Сумма налога (млн руб.)", title_font=dict(color="#000000"), tickfont=dict(color="#000000"), gridcolor="#e2e8f0")
    st.plotly_chart(fig2, use_container_width=True)

    # График 3: Утилизация льгот
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=df_chart["Год"],
        y=df_chart["Освобождено льготой (млн руб.)"],
        name="Прибыль, освобожденная от налога (млн руб.)",
        marker_color="#16a34a",
    ))
    fig3.add_trace(go.Bar(
        x=df_chart["Год"],
        y=df_chart["База после льготы (млн руб.)"],
        name="Налогооблагаемый остаток (млн руб.)",
        marker_color="#d97706",
    ))
    fig3.update_layout(
        barmode="stack",
        title=dict(text="Структура реализованной прибыли (льгота против налоговой базы)", font=dict(color="#000000", size=16)),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Montserrat", color="#000000"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(color="#000000"), bgcolor="#ffffff"),
        hoverlabel=dict(bgcolor="#ffffff", font=dict(color="#000000")),
    )
    fig3.update_xaxes(title_text="Год", title_font=dict(color="#000000"), tickfont=dict(color="#000000"), gridcolor="#e2e8f0")
    fig3.update_yaxes(title_text="Прибыль (млн руб.)", title_font=dict(color="#000000"), tickfont=dict(color="#000000"), gridcolor="#e2e8f0")
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("Детальный протокол математического аудита")
    if deals_records:
        st.dataframe(pd.DataFrame(deals_records), use_container_width=True, hide_index=True)

    full_log_text = chr(10).join(log_lines)
    st.download_button(
        label="Скачать лог расчетов (UTF-8 .txt)",
        data=full_log_text.encode("utf-8"),
        file_name="single_investor_tax_audit.txt",
        mime="text/plain; charset=utf-8",
    )
    st.text_area("Текстовый лог расчетов", value=full_log_text, height=450)
