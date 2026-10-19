# ytb — المستودع الموحّد لتفريغات ومحاذاة الدروس العلمية

المستودع الرسمي الموحّد لجميع النصوص المفرّغة (`.txt`) وملفات المحاذاة الصوتية بالكلمة والثانية (`.align.json`) والبيانات الوصفية (`.meta.json`) وفق هيكلة `cheikh` القياسية.

---

## 1. الإحصاءات العامة

- **المشايخ ذوو المحتوى الفعلي:** 24 شيخاً
- **السلاسل المفرّغة:** 369 سلسلة
- **الدروس المفرّغة نصياً (`.txt`):** 6,345 درساً
- **الدروس المحاذاة صوتياً (`.align.json`):** 964 درساً
- **إجمالي الحجم النصي:** 148,859,137 حرفاً

---

## 2. جدول المشايخ

| # | الشيخ | المعرّف (`Slug`) | السلاسل | الدروس المفرغة (`.txt`) | الدروس المحاذاة (`.align.json`) | المجلد |
|---:|---|---|---:|---:|---:|---|
| 1 | محمد سعيد رمضان البوطي | `said-bouti` | 34 | 1,165 | 132 | [`said-bouti/`](./said-bouti/) |
| 2 | محمد متولي الشعراوي | `sharawi` | 48 | 648 | 45 | [`sharawi/`](./sharawi/) |
| 3 | أدهم العاسمي | `adham-alasimi` | 29 | 546 | 36 | [`adham-alasimi/`](./adham-alasimi/) |
| 4 | أحمد السيد | `ahmed-alsayed` | 34 | 483 | 122 | [`ahmed-alsayed/`](./ahmed-alsayed/) |
| 5 | الحبيب علي الجفري | `habib-ali-aljifri` | 23 | 471 | 22 | [`habib-ali-aljifri/`](./habib-ali-aljifri/) |
| 6 | فاضل السامرائي | `fadhel-samarrai` | 42 | 460 | 244 | [`fadhel-samarrai/`](./fadhel-samarrai/) |
| 7 | الحبيب عمر بن حفيظ | `habib-omar-ibn-hafiz` | 15 | 450 | 24 | [`habib-omar-ibn-hafiz/`](./habib-omar-ibn-hafiz/) |
| 8 | ذاكر الهاشمي | `dhaker-alhashimi` | 20 | 348 | 26 | [`dhaker-alhashimi/`](./dhaker-alhashimi/) |
| 9 | محمد البردوني الحسيمي | `bardouni-husaymi` | 16 | 343 | 61 | [`bardouni-husaymi/`](./bardouni-husaymi/) |
| 10 | علي جمعة | `ali-gomaa` | 14 | 276 | 27 | [`ali-gomaa/`](./ali-gomaa/) |
| 11 | علي محمود العمري | `ali-mahmoud-alomari` | 18 | 241 | 15 | [`ali-mahmoud-alomari/`](./ali-mahmoud-alomari/) |
| 12 | مولود السريري | `mouloud-sariri` | 17 | 214 | 36 | [`mouloud-sariri/`](./mouloud-sariri/) |
| 13 | علي هاني العقرباوي | `ali-hani-aqrabawi` | 14 | 197 | 36 | [`ali-hani-aqrabawi/`](./ali-hani-aqrabawi/) |
| 14 | أيمن عبد الرحيم | `ayman-abdelrahim` | 20 | 130 | 104 | [`ayman-abdelrahim/`](./ayman-abdelrahim/) |
| 15 | معاذ سعيد حوى | `maath-hawa` | 7 | 92 | 23 | [`maath-hawa/`](./maath-hawa/) |
| 16 | فاضل سليمان | `fadhel-sulaiman` | 3 | 89 | 0 | [`fadhel-sulaiman/`](./fadhel-sulaiman/) |
| 17 | سيف العصري | `saif-alasri` | 1 | 56 | 0 | [`saif-alasri/`](./saif-alasri/) |
| 18 | أبو بكر المشهور | `aboubakr-almashhour` | 6 | 39 | 0 | [`aboubakr-almashhour/`](./aboubakr-almashhour/) |
| 19 | محمد عبد الواحد الحنبلي | `muhammad-abdelwahid-hanbali` | 1 | 38 | 0 | [`muhammad-abdelwahid-hanbali/`](./muhammad-abdelwahid-hanbali/) |
| 20 | أحمد عبد المنعم | `ahmed-abdelmonem` | 1 | 20 | 0 | [`ahmed-abdelmonem/`](./ahmed-abdelmonem/) |
| 21 | حاتم العوني | `hatem-alaouni` | 3 | 19 | 0 | [`hatem-alaouni/`](./hatem-alaouni/) |
| 22 | سعيد الكملي | `said-kamali` | 1 | 11 | 11 | [`said-kamali/`](./said-kamali/) |
| 23 | بن صايب | `bensaib` | 1 | 8 | 0 | [`bensaib/`](./bensaib/) |
| 24 | دروس غير منسوبة | `unattributed` | 1 | 1 | 0 | [`unattributed/`](./unattributed/) |

> التفاصيل الكاملة لكل سلسلة داخل كل شيخ موجودة في [`COVERAGE.md`](./COVERAGE.md) وفي [`catalog.json`](./catalog.json).

---

## 3. هيكل المستودع القياسي

```text
ytb/
  README.md                       # الواجهة الرئيسية والإحصاءات العامة
  COVERAGE.md                     # تقرير التغطية التفصيلي لكل شيخ وسلسلة
  catalog.json                    # الفهرس المركزي المهيكل
  <sheikh-slug>/                  # مجلد الشيخ + _sheikh.json + _index.json
    <s_code>/                     # مجلد السلسلة القياسي (مثل s001) + _meta.json + _index.json
      <NNN>_<vid>.txt             # النص العربي المطهّر للمحاضرة
      <NNN>_<vid>.align.json      # المحاذاة الصوتية الدقيقة (كلمة بكلمة بالثانية)
      <NNN>_<vid>.meta.json       # البيانات الوصفية للمحاضرة
  tools/                          # أدوات الفهرسة والتحقق (build_index.py)
  _meta/                          # سجلات الجرد والتحقق المرجعية
```
