# Blacklitt-Debanjan_Kartikeya

# Which Momentum Actually Works?

**Price, volume and delivery momentum signals on NSE equities**

Blacklitt × PGDBA Live Quant Research · Project 02
Debanjan Manna & Kartikeya Vadlamani · PGDBA 2026–28 (IIM Calcutta · ISI Kolkata · IIT Kharagpur)


---

## The question

Which way of measuring momentum (price, volume or delivery %, over daily, weekly or monthly lookbacks) best predicts an NSE stock's return over the next 1–2 weeks and 1–2 months?

---

## Project status

| Stage | Status |
|---|---|
| 1. Data collection (NSE full bhavcopy scraper) | ✅ Done |
| 2. Preprocessing (cleaning, corporate-action adjustment) | 🔜 Next |
| 3. Signal construction | ⏳ Planned |
| 4. Evaluation and backtesting | ⏳ Planned |
| 5. Dashboard | ⏳ Planned |

---

## Data collection

The scraper downloads NSE's daily **full bhavcopy with delivery data** (`sec_bhavdata_full`) from the NSE archives.



How it works:

- **Caching:** a file that already exists is never downloaded again, so the script can be rerun safely.
- **Holidays:** NSE returns `404` for days with no trading, and those days are skipped.
- **Retries:** failed requests are retried up to 4 times, waiting 1, 2, 4 and 8 seconds.
- **Rate limiting:** a 1-second pause after each download avoids being blocked by NSE.

---

## The data

Each file holds one trading day, with one row per security. Its columns are:

| Column | Meaning |
|---|---|
| `SYMBOL` | NSE ticker |
| `SERIES` | `EQ` = normal equity; `BE`/`BZ` = trade-for-trade |
| `DATE1` | Trade date (`DD-Mon-YYYY`) |
| `PREV_CLOSE`, `OPEN_PRICE`, `HIGH_PRICE`, `LOW_PRICE`, `LAST_PRICE`, `CLOSE_PRICE` | Prices (₹) |
| `AVG_PRICE` | Volume-weighted average price |
| `TTL_TRD_QNTY` | Total traded quantity |
| `TURNOVER_LACS` | Traded value (₹ lakh) |
| `NO_OF_TRADES` | Number of trades |
| `DELIV_QTY` | Deliverable quantity |
| `DELIV_PER` | Delivery % |

Delivery % is the share of traded quantity that was actually taken into demat accounts rather than squared off within the day:

---

## Next step: preprocessing

1. **Normalise:** strip spaces from column names and values, convert `-` to `NaN`, and parse dates.
2. **Filter:** keep `EQ` series. Exclude `BE`/`BZ` rows from delivery signals, because delivery is compulsory in those series and their delivery % is about 100% by rule.
3. **Adjust for corporate actions:** rescale prices and volumes from before splits and bonuses so they are comparable with later data:

4. **Quality checks:** no duplicate (date, symbol) rows, `DELIV_QTY ≤ TTL_TRD_QNTY`, and any one-day move above 35% flagged for review.
5. **Store:** load the cleaned panel into PostgreSQL for signal construction.

---

## Team

- **Debanjan Manna** · [LinkedIn](https://www.linkedin.com/in/debanjanmanna/) 
- **Kartikeya Vadlamani** · [LinkedIn](https://www.linkedin.com/in/kartikeya-vadlamani-403631247/)
