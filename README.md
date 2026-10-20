# ytb — المستودع الموحّد لتفريغات ومحاذاة الدروس العلمية

المستودع الرسمي الموحّد لجميع النصوص المفرّغة (`.txt`) وملفات المحاذاة الصوتية بالكلمة والثانية (`.align.json`) والبيانات الوصفية (`.meta.json`) وفق هيكلة `cheikh` القياسية.

---

## 1. الإحصاءات العامة

- **المشايخ ذوو المحتوى الفعلي:** 25 شيخاً
- **السلاسل المفرّغة:** 386 سلسلة
- **الدروس المفرّغة نصياً (`.txt`):** 6,589 درساً
- **الدروس المحاذاة صوتياً (`.align.json`):** 1,828 درساً
- **إجمالي الحجم النصي:** 156,209,589 حرفاً

---

## 2. جدول المشايخ

| # | الشيخ | المعرّف (`Slug`) | السلاسل | الدروس المفرغة (`.txt`) | الدروس المحاذاة (`.align.json`) | المجلد |
|---:|---|---|---:|---:|---:|---|
| 1 | محمد سعيد رمضان البوطي | `said-bouti` | 34 | 1,165 | 177 | [`said-bouti/`](./said-bouti/) |
| 2 | محمد متولي الشعراوي | `sharawi` | 48 | 648 | 232 | [`sharawi/`](./sharawi/) |
| 3 | أدهم العاسمي | `adham-alasimi` | 29 | 546 | 55 | [`adham-alasimi/`](./adham-alasimi/) |
| 4 | أحمد السيد | `ahmed-alsayed` | 34 | 483 | 194 | [`ahmed-alsayed/`](./ahmed-alsayed/) |
| 5 | الحبيب علي الجفري | `habib-ali-aljifri` | 23 | 471 | 30 | [`habib-ali-aljifri/`](./habib-ali-aljifri/) |
| 6 | فاضل السامرائي | `fadhel-samarrai` | 42 | 460 | 333 | [`fadhel-samarrai/`](./fadhel-samarrai/) |
| 7 | الحبيب عمر بن حفيظ | `habib-omar-ibn-hafiz` | 15 | 450 | 56 | [`habib-omar-ibn-hafiz/`](./habib-omar-ibn-hafiz/) |
| 8 | ذاكر الهاشمي | `dhaker-alhashimi` | 20 | 348 | 73 | [`dhaker-alhashimi/`](./dhaker-alhashimi/) |
| 9 | محمد البردوني الحسيمي | `bardouni-husaymi` | 16 | 343 | 89 | [`bardouni-husaymi/`](./bardouni-husaymi/) |
| 10 | علي جمعة | `ali-gomaa` | 14 | 276 | 51 | [`ali-gomaa/`](./ali-gomaa/) |
| 11 | محمد الحسن الددو | `daddo` | 17 | 244 | 92 | [`daddo/`](./daddo/) |
| 12 | علي محمود العمري | `ali-mahmoud-alomari` | 18 | 241 | 59 | [`ali-mahmoud-alomari/`](./ali-mahmoud-alomari/) |
| 13 | مولود السريري | `mouloud-sariri` | 17 | 214 | 87 | [`mouloud-sariri/`](./mouloud-sariri/) |
| 14 | علي هاني العقرباوي | `ali-hani-aqrabawi` | 14 | 197 | 100 | [`ali-hani-aqrabawi/`](./ali-hani-aqrabawi/) |
| 15 | أيمن عبد الرحيم | `ayman-abdelrahim` | 20 | 130 | 119 | [`ayman-abdelrahim/`](./ayman-abdelrahim/) |
| 16 | معاذ سعيد حوى | `maath-hawa` | 7 | 92 | 70 | [`maath-hawa/`](./maath-hawa/) |
| 17 | فاضل سليمان | `fadhel-sulaiman` | 3 | 89 | 0 | [`fadhel-sulaiman/`](./fadhel-sulaiman/) |
| 18 | سيف العصري | `saif-alasri` | 1 | 56 | 0 | [`saif-alasri/`](./saif-alasri/) |
| 19 | أبو بكر المشهور | `aboubakr-almashhour` | 6 | 39 | 0 | [`aboubakr-almashhour/`](./aboubakr-almashhour/) |
| 20 | محمد عبد الواحد الحنبلي | `muhammad-abdelwahid-hanbali` | 1 | 38 | 0 | [`muhammad-abdelwahid-hanbali/`](./muhammad-abdelwahid-hanbali/) |
| 21 | أحمد عبد المنعم | `ahmed-abdelmonem` | 1 | 20 | 0 | [`ahmed-abdelmonem/`](./ahmed-abdelmonem/) |
| 22 | حاتم العوني | `hatem-alaouni` | 3 | 19 | 0 | [`hatem-alaouni/`](./hatem-alaouni/) |
| 23 | سعيد الكملي | `said-kamali` | 1 | 11 | 11 | [`said-kamali/`](./said-kamali/) |
| 24 | بن صايب | `bensaib` | 1 | 8 | 0 | [`bensaib/`](./bensaib/) |
| 25 | دروس غير منسوبة | `unattributed` | 1 | 1 | 0 | [`unattributed/`](./unattributed/) |

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
