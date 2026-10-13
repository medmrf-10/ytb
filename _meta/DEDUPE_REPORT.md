# تقرير إزالة التكرار وحل التعارضات (`DEDUPE_REPORT.md`)

> تاريخ التوليد: 2026-10-13 12:05:45  
> الحالة: مكتمل وحتمي — صادر عن أداة `tools/resolve.py` وفق قواعد وثيقة الخطة المعتمدة.

---

## 1. الملخص التنفيذي والأرقام القياسية

| المؤشر | القيمة | النسبة / الملاحظة |
|---|---:|---|
| إجمالي ملفات المحاضرات المدخلة | **8,595** | المخازن الخمسة (hw-tr 1,688 · hw-ls 1,845 · irth 1,047 · des-mut 2,729 · des-dur 1,286) |
| إجمالي الدروس الفريدة الناتجة | **4,049** | نسبة الانكماش: 52.9% |
| دروس بمعرّف يوتيوب (vid) | **3,670** | تطابق تام مع القياس الأساسي (F3: 3,670) |
| دروس بلا معرّف يوتيوب | **379** | تمايز نصوص ومحاضرات غير مرفوعة على يوتيوب |
| تكرارات متطابقة دُمجت | **4,546** | ملفات تكرار متطابق البايتات أو النص المطبَّع |
| حالات التعارض النصي الحقيقي | **43** | نفس الدرس بنصين مختلفين (تطابق تام مع F6: 43) |
| إسناد متنازع بين المشايخ | **88** | دروس ظهرت في سلاسل لشيوخ مختلفين (تطابق تام مع F7: 88) |
| تعدد السلاسل والصفوف | **294** | دروس شاركت في أكثر من صف (تطابق تام مع F7: 294) |

---

## 2. محاسبة المخازن ومصادر التكرار

| المخزن | المسار المصدر | إجمالي الملفات | البصمات الفريدة | الحجم (بايت) | الدروس الفائزة | ملفات مكررة مدمجة |
|---|---|---:|---:|---:|---:|---:|
| مطالعة (des-mut) | `des/mutalaa/data/txt` | 2,729 | 2,708 | 86,621,276 | 2,674 | 55 |
| دروس السلاسل (hw-ls) | `hawshat/playlists/lessons` | 1,845 | 1,841 | 96,915,794 | 223 | 1,622 |
| تفريغات هوشات (hw-tr) | `hawshat/transcripts` | 1,688 | 1,526 | 59,834,743 | 597 | 1,091 |
| دروس الشابكة (des-dur) | `des/durus/transcripts` | 1,286 | 1,286 | 38,152,933 | 10 | 1,276 |
| إرث النبوي (irth) | `irth/content/tube` | 1,047 | 1,047 | 50,632,511 | 545 | 502 |

> **المخازن الأكثر مساهمة في التكرار:**
> 1. **hw-ls**: 1,622 ملفاً مكرراً دُمج في نسخ أخرى.
> 1. **des-dur**: 1,276 ملفاً مكرراً دُمج في نسخ أخرى.
> 1. **hw-tr**: 1,091 ملفاً مكرراً دُمج في نسخ أخرى.
> 1. **irth**: 502 ملفاً مكرراً دُمج في نسخ أخرى.
> 1. **des-mut**: 55 ملفاً مكرراً دُمج في نسخ أخرى.

---

## 3. الملفات والمجموعات المستبعدة (بلا مقر في التفريغات)

| المجموعة / المسار | العدد | السبب | القرار |
|---|---:|---|---|
| `hawshat/irth-simulation/` | 379 | كلام عشوائي مُولَّد (Synthetic Text) لا يطابق أي محاضرة حقيقية | استبعاد نهائي |
| `hawshat/transcripts/maktaba/` | 17 | كتب ومتون مفرغة (ألفية، مراقي، أم البراهين) ملوثة بنصوص النموذج | استبعاد ككتب (قرار المالك Q3) |
| `hawshat/inbox/` | 94 | ملفات محاذاة فقط (align JSON) لسلاسل البوطي بلا نصوص تفريغ | تأجيل إلى طبقة المحاذاة (P9) |
| `des/shami/` | 295 | كوربوس كتب الشامي (كتب لا تفريغ صوتيات) | استبعاد كوربوس كتب |
| `des/nusus/` | 1,286 | نصوص كتب ومراجع تراثية | استبعاد كوربوس كتب |
| `des/kutub/` | 1 | كتب تراثية | استبعاد كوربوس كتب |
| `des/manzuma/` | 1,331 | شروح منظومات نصية | استبعاد كوربوس كتب |
| `des/jadid2/` | 1,507 | كوربوس إنجليزي ونصوص حديثة | استبعاد كوربوس كتب |

---

## 4. توزيع الدروس الفريدة لكل شيخ

| المعرّف (Slug) | الشيخ | الدروس الفريدة | نسبة المحتوى |
|---|---|---:|---:|
| `said-bouti` | سعيد رمضان البوطي | 1,012 | 25.0% |
| `adham-alasimi` | أدهم العاسمي | 452 | 11.2% |
| `habib-omar-ibn-hafiz` | الحبيب عمر بن حفيظ | 444 | 11.0% |
| `habib-ali-aljifri` | الحبيب علي الجفري | 442 | 10.9% |
| `bardouni-husaymi` | محمد البردوني الحسيمي | 390 | 9.6% |
| `ahmed-alsayed` | أحمد السيد | 284 | 7.0% |
| `ali-mahmoud-alomari` | علي محمود العمري | 236 | 5.8% |
| `dhaker-alhashimi` | ذاكر الهاشمي | 217 | 5.4% |
| `ali-gomaa` | علي جمعة | 215 | 5.3% |
| `fadhel-sulaiman` | فاضل سليمان | 89 | 2.2% |
| `mouloud-sariri` | مولود السريري | 87 | 2.1% |
| `saif-alasri` | سيف العصري | 56 | 1.4% |
| `aboubakr-almashhour` | أبو بكر المشهور | 39 | 1.0% |
| `muhammad-abdelwahid-hanbali` | محمد عبد الواحد الازهري الحنبلي | 38 | 0.9% |
| `ahmed-abdelmonem` | أحمد عبد المنعم | 20 | 0.5% |
| `hatem-alaouni` | حاتم العوني | 19 | 0.5% |
| `bensaib` | بن سايب | 8 | 0.2% |
| `unattributed` | unattributed | 1 | 0.0% |

---

## 5. جدول التعارضات النصية الحقيقية (الـ 43 درساً)

حُلت جميع الحالات الـ 43 بنظام الأولوية الحتمي: **الأحدث في git commit time** ثم **الأطول جسماً** ثم **أسبقية المخزن**، مع أرشفة النص الخاسر.

| # | معرّف الدرس (LID) | المسار الفائز | المخزن الفائز | سبب الفوز | عدد النسخ الخاسرة | مسار النسخة المؤرشفة | نسبة التشابه (Jaccard) |
|---|---|---|---|---|---:|---|---:|
| 1 | `yt:nqwovh99-p4` | `des/mutalaa/data/txt/786/002_الشيخ سارية الرفاعي ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` | `des-mut` | longer_body | 1 | `adham-alasimi/786/_variants/002_nqwovh99-p4.des-mut.txt` | 75.7% |
| 2 | `yt:3LQ1ywCHpJQ` | `des/mutalaa/data/txt/786/004_مقومات بناء الأوطان ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` | `des-mut` | longer_body | 1 | `adham-alasimi/786/_variants/004_3LQ1ywCHpJQ.des-mut.txt` | 75.5% |
| 3 | `yt:dMLjQ_LBlD0` | `des/mutalaa/data/txt/786/005_الغفلة عن شعبان ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` | `des-mut` | longer_body | 1 | `adham-alasimi/786/_variants/005_dMLjQ_LBlD0.des-mut.txt` | 71.7% |
| 4 | `yt:KJrhWu9iU0c` | `des/mutalaa/data/txt/789/011_كفُّ الأذى ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` | `des-mut` | longer_body | 1 | `adham-alasimi/789/_variants/011_KJrhWu9iU0c.des-mut.txt` | 92.3% |
| 5 | `yt:RvJ4f7hEP4U` | `des/mutalaa/data/txt/789/013_النظام والعمل التطوعي ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` | `des-mut` | longer_body | 1 | `adham-alasimi/789/_variants/013_RvJ4f7hEP4U.des-mut.txt` | 85.2% |
| 6 | `yt:0qLNRrKdS_g` | `des/mutalaa/data/txt/789/016_إلا الصوم فإنه لي ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` | `des-mut` | longer_body | 1 | `adham-alasimi/789/_variants/016_0qLNRrKdS_g.des-mut.txt` | 94.6% |
| 7 | `yt:AheJID8nwdc` | `des/mutalaa/data/txt/798/001_(4) شرح متن البناء في علم الصرف ｜ الشيخ أدهم العاسمي.txt` | `des-mut` | newest_commit | 1 | `adham-alasimi/798/_variants/001_AheJID8nwdc.des-dur.txt` | 78.8% |
| 8 | `yt:xc1_CuIWdI8` | `des/mutalaa/data/txt/798/003_(2) شرح متن البناء في علم الصرف ｜ الشيخ أدهم العاسمي.txt` | `des-mut` | newest_commit | 1 | `adham-alasimi/798/_variants/003_xc1_CuIWdI8.des-dur.txt` | 71.6% |
| 9 | `yt:qu3VtS1fXD4` | `des/mutalaa/data/txt/798/004_(1) شرح متن البناء في علم الصرف ｜ الشيخ أدهم العاسمي.txt` | `des-mut` | newest_commit | 1 | `adham-alasimi/798/_variants/004_qu3VtS1fXD4.des-dur.txt` | 79.2% |
| 10 | `yt:YFDcsg-_wJw` | `des/mutalaa/data/txt/661/041_خير القرون 40 ｜ صاحب السر رضي الله عنه ｜ أحمد السيد.txt` | `des-mut` | newest_commit | 1 | `ahmed-alsayed/661/_variants/041_YFDcsg-_wJw.hw-tr.txt` | 45.3% |
| 11 | `yt:wihglz3B8yo` | `des/mutalaa/data/txt/672/004_تدبّر سورة الأنفال 03 ｜ أحمد السيد.txt` | `des-mut` | newest_commit | 1 | `ahmed-alsayed/672/_variants/004_wihglz3B8yo.irth.txt` | 47.6% |
| 12 | `yt:zwOHopJzlDE` | `des/mutalaa/data/txt/672/006_تدبّر سورة الأنفال 05 ｜ أحمد السيد.txt` | `des-mut` | newest_commit | 1 | `ahmed-alsayed/672/_variants/006_zwOHopJzlDE.irth.txt` | 16.8% |
| 13 | `yt:AvYazyD8jII` | `des/mutalaa/data/txt/672/007_تدبّر سورة الأنفال 06 ｜ أحمد السيد.txt` | `des-mut` | newest_commit | 1 | `ahmed-alsayed/672/_variants/007_AvYazyD8jII.irth.txt` | 21.5% |
| 14 | `yt:Me3B0orykFA` | `irth/content/tube/tadabburElanfal-007/transcript.txt` | `irth` | newest_commit | 1 | `ahmed-alsayed/672/_variants/015_Me3B0orykFA.hw-tr.txt` | 68.3% |
| 15 | `yt:0BdXpeTyJT8` | `hawshat/transcripts/alsayed/mut-686/001_تدبر سورة التوبة 01 ｜ أحمد السيد.txt` | `hw-tr` | newest_commit | 1 | `ahmed-alsayed/686/_variants/001_0BdXpeTyJT8.hw-tr.txt` | 67.0% |
| 16 | `yt:qe4QqpJgF_U` | `des/mutalaa/data/txt/686/002_تدبر سورة التوبة 02 ｜ أحمد السيد.txt` | `des-mut` | newest_commit | 1 | `ahmed-alsayed/686/_variants/002_qe4QqpJgF_U.hw-tr.txt` | 67.2% |
| 17 | `yt:XfcCEEUaOxs` | `des/mutalaa/data/txt/686/003_تدبر سورة التوبة 03 ｜ أحمد السيد.txt` | `des-mut` | newest_commit | 1 | `ahmed-alsayed/686/_variants/003_XfcCEEUaOxs.hw-tr.txt` | 67.8% |
| 18 | `yt:iTXhqCP2-f0` | `des/mutalaa/data/txt/686/004_تدبر سورة التوبة 04 ｜ أحمد السيد.txt` | `des-mut` | newest_commit | 1 | `ahmed-alsayed/686/_variants/004_iTXhqCP2-f0.hw-tr.txt` | 56.8% |
| 19 | `yt:qQTNbtM-tuU` | `des/mutalaa/data/txt/686/006_تدبر سورة التوبة 06 ｜ أحمد السيد.txt` | `des-mut` | newest_commit | 2 | `ahmed-alsayed/686/_variants/006_qQTNbtM-tuU.hw-tr.txt` | 73.2% |
| 20 | `yt:HTKZgKsIPk8` | `hawshat/transcripts/alsayed/mut-686/007_تدبر سورة التوبة 07 ｜ أحمد السيد.txt` | `hw-tr` | newest_commit | 1 | `ahmed-alsayed/686/_variants/007_HTKZgKsIPk8.hw-tr.txt` | 51.2% |
| 21 | `yt:8w9oBYXruWo` | `irth/content/tube/alamriNasafiyya-014/transcript.txt` | `irth` | newest_commit | 1 | `ali-mahmoud-alomari/alamri-barahin-muqtatafat/_variants/018_8w9oBYXruWo.irth.txt` | 47.0% |
| 22 | `yt:--mO_oVFljU` | `des/mutalaa/data/txt/114/001_في رمضان ｜ الإنسانية قبل التدين ｜ الحبيب علي الجفري ｜ Humanity Before Religiosit.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/001_--mO_oVFljU.des-dur.txt` | 98.7% |
| 23 | `yt:-P9l5UEkz1s` | `des/mutalaa/data/txt/114/005_الإنسانية قبل التدين ｜ الحلقة 5 - هل للأخلاق والقيم صلة بالدين؟ ｜ علي الجفري ｜ E.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/005_-P9l5UEkz1s.des-dur.txt` | 70.0% |
| 24 | `yt:5ETQ9Z6j5Ns` | `des/mutalaa/data/txt/114/007_الإنسانية قبل التدين ｜ الحلقة 7 - كيف تؤثر المحبة في الإنسانية ｜ علي الجفري ｜ En.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/007_5ETQ9Z6j5Ns.des-dur.txt` | 87.1% |
| 25 | `yt:wW1_BVCu2A8` | `des/mutalaa/data/txt/114/008_الإنسانية قبل التدين ｜ حلقة 3 - كيف تتوافق رغبات الإنسان بالإنسانية ｜ علي الجفري.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/008_wW1_BVCu2A8.des-dur.txt` | 99.5% |
| 26 | `yt:7oDUfRE4rNw` | `des/mutalaa/data/txt/114/009_الإنسانية قبل التدين ｜ الحلقة 8 - محبة الله والنبي وأثرها  ｜ علي الجفري ｜ Englis.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/009_7oDUfRE4rNw.des-dur.txt` | 80.4% |
| 27 | `yt:nogkt3jTwrc` | `des/mutalaa/data/txt/114/010_الإنسانية قبل التدين ｜ الحلقة 9 - هل الولاء والبراء من الإسلام ｜ علي الجفري ｜ En.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/010_nogkt3jTwrc.des-dur.txt` | 74.2% |
| 28 | `yt:yeonqcnFR3o` | `des/mutalaa/data/txt/114/011_الإنسانية قبل التدين ｜ الحلقة 10 - إنسانية التعامل مع المخطئ ｜ علي الجفري ｜ Engl.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/011_yeonqcnFR3o.des-dur.txt` | 79.7% |
| 29 | `yt:RlEKVnSDL3g` | `des/mutalaa/data/txt/114/012_الإنسانية قبل التدين ｜ الحلقة 11 - كيف نتعامل مع جموح الشباب؟  ｜ علي الجفري ｜ En.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/012_RlEKVnSDL3g.des-dur.txt` | 83.1% |
| 30 | `yt:ZFdhS30B8fg` | `des/mutalaa/data/txt/114/014_الإنسانية قبل التدين ｜ الحلقة 13- إنسانية العفو والمسامحة  ｜ علي الجفري ｜ Englis.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/014_ZFdhS30B8fg.des-dur.txt` | 86.8% |
| 31 | `yt:qj-MafQroxQ` | `des/mutalaa/data/txt/114/015_الإنسانية قبل التدين ｜ الحلقة 14- إنسانية التعامل مع المذنب  ｜ علي الجفري ｜ Engl.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/015_qj-MafQroxQ.des-dur.txt` | 71.4% |
| 32 | `yt:sXP5SAFZSlM` | `des/mutalaa/data/txt/114/016_الإنسانية قبل التدين ｜ الحلقة 15- اضطراب الهوية الجنسية ｜ علي الجفري ｜ English S.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/016_sXP5SAFZSlM.des-dur.txt` | 81.4% |
| 33 | `yt:TepOiYnOCG0` | `des/mutalaa/data/txt/114/017_الإنسانية قبل التدين ｜ الحلقة 16- التعامل مع مخالف العقيدة ｜ علي الجفري ｜ Englis.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/017_TepOiYnOCG0.des-dur.txt` | 79.5% |
| 34 | `yt:vnUNfhSwrlU` | `des/mutalaa/data/txt/114/019_الإنسانية قبل التدين ｜ الحلقة 18- مفاهيم التعامل مع غير المسلمين ｜ علي الجفري ｜ .txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/019_vnUNfhSwrlU.des-dur.txt` | 74.3% |
| 35 | `yt:5PDX-VWIN0U` | `des/mutalaa/data/txt/114/020_الإنسانية قبل التدين ｜ الحلقة 19 - لا إنسانية في الفتنة الطائفية ｜ علي الجفري ｜ .txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/020_5PDX-VWIN0U.des-dur.txt` | 82.1% |
| 36 | `yt:9XOZMwf-2v0` | `des/mutalaa/data/txt/114/022_الإنسانية قبل التدين ｜ الحلقة 21 - الجهاد الحق ｜ علي الجفري ｜ English Subtitle.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/022_9XOZMwf-2v0.des-dur.txt` | 81.2% |
| 37 | `yt:bMQoeUePP2g` | `des/mutalaa/data/txt/114/025_الإنسانية قبل التدين ｜ الحلقة 24 - ثقافة الوقف ｜ علي الجفري ｜ English Subtitle.txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/025_bMQoeUePP2g.des-dur.txt` | 77.7% |
| 38 | `yt:TmLggAmX4sk` | `des/mutalaa/data/txt/114/026_الإنسانية قبل التدين ｜ الحلقة 25 - الحدود والقصاص وإنسانية العفو 1 ｜ علي الجفري .txt` | `des-mut` | newest_commit | 1 | `habib-ali-aljifri/114/_variants/026_TmLggAmX4sk.des-dur.txt` | 69.5% |
| 39 | `yt:hDdfJM78L5s` | `irth/content/tube/abdelwahidTawassul-001/transcript.txt` | `irth` | newest_commit | 1 | `muhammad-abdelwahid-hanbali/abdelwahid-tawassul/_variants/001_hDdfJM78L5s.hw-tr.txt` | 65.5% |
| 40 | `yt:Sqx-KSJzARA` | `irth/content/tube/abdelwahidTawassul-002/transcript.txt` | `irth` | newest_commit | 1 | `muhammad-abdelwahid-hanbali/abdelwahid-tawassul/_variants/002_Sqx-KSJzARA.hw-tr.txt` | 68.0% |
| 41 | `yt:WFLgTeRtEIo` | `irth/content/tube/abdelwahidTawassul-004/transcript.txt` | `irth` | newest_commit | 1 | `muhammad-abdelwahid-hanbali/abdelwahid-tawassul/_variants/004_WFLgTeRtEIo.hw-tr.txt` | 72.7% |
| 42 | `yt:vRhNirjptm0` | `irth/content/tube/abdelwahidTawassul-005/transcript.txt` | `irth` | newest_commit | 1 | `muhammad-abdelwahid-hanbali/abdelwahid-tawassul/_variants/005_vRhNirjptm0.hw-tr.txt` | 66.3% |
| 43 | `yt:x7hB5-Vp0HE` | `des/mutalaa/data/txt/403/041_39- فقه السيرة النبوية ｜ صلح الحديبية (2).txt` | `des-mut` | newest_commit | 1 | `said-bouti/403/_variants/041_x7hB5-Vp0HE.hw-ls.txt` | 44.0% |

### أكبر 5 حالات تعارض من حيث عدد النسخ والتباين
#### حالة 1: `yt:qQTNbtM-tuU`
- **الفائز:** `des/mutalaa/data/txt/686/006_تدبر سورة التوبة 06 ｜ أحمد السيد.txt` (des-mut) — الحجم: 29166 حرف — السبب: `newest_commit`
  - **خاسر:** `hawshat/transcripts/alsayed/mut-672/014_تدبر سورة التوبة 06 ｜ أحمد السيد.txt` (hw-tr) — الحجم: 29370 حرف — تشابه: 73.2% — يؤرشف في `ahmed-alsayed/686/_variants/006_qQTNbtM-tuU.hw-tr.txt`
  - **خاسر:** `hawshat/playlists/lessons/alsayed-mut-672/014.txt` (hw-ls) — الحجم: 29370 حرف — تشابه: 72.5% — يؤرشف في `ahmed-alsayed/686/_variants/006_qQTNbtM-tuU.hw-ls.txt`
#### حالة 2: `yt:nqwovh99-p4`
- **الفائز:** `des/mutalaa/data/txt/786/002_الشيخ سارية الرفاعي ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` (des-mut) — الحجم: 15580 حرف — السبب: `longer_body`
  - **خاسر:** `des/mutalaa/data/txt/789/012_الشيخ سارية الرفاعي ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` (des-mut) — الحجم: 15218 حرف — تشابه: 75.7% — يؤرشف في `adham-alasimi/786/_variants/002_nqwovh99-p4.des-mut.txt`
#### حالة 3: `yt:3LQ1ywCHpJQ`
- **الفائز:** `des/mutalaa/data/txt/786/004_مقومات بناء الأوطان ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` (des-mut) — الحجم: 7354 حرف — السبب: `longer_body`
  - **خاسر:** `des/mutalaa/data/txt/789/014_مقومات بناء الأوطان ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` (des-mut) — الحجم: 7181 حرف — تشابه: 75.5% — يؤرشف في `adham-alasimi/786/_variants/004_3LQ1ywCHpJQ.des-mut.txt`
#### حالة 4: `yt:dMLjQ_LBlD0`
- **الفائز:** `des/mutalaa/data/txt/786/005_الغفلة عن شعبان ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` (des-mut) — الحجم: 9543 حرف — السبب: `longer_body`
  - **خاسر:** `des/mutalaa/data/txt/789/015_الغفلة عن شعبان ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` (des-mut) — الحجم: 9272 حرف — تشابه: 71.7% — يؤرشف في `adham-alasimi/786/_variants/005_dMLjQ_LBlD0.des-mut.txt`
#### حالة 5: `yt:KJrhWu9iU0c`
- **الفائز:** `des/mutalaa/data/txt/789/011_كفُّ الأذى ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` (des-mut) — الحجم: 16556 حرف — السبب: `longer_body`
  - **خاسر:** `des/mutalaa/data/txt/786/001_كفُّ الأذى ⧸ خطبة الجمعة ⧸ الشيخ أدهم العاسمي.txt` (des-mut) — الحجم: 16523 حرف — تشابه: 92.3% — يؤرشف في `adham-alasimi/789/_variants/011_KJrhWu9iU0c.des-mut.txt`

---

## 6. جدول الإسناد المتنازع بين المشايخ (الـ 88 درساً)

الدروس التي وُجدت منسوبة لأكثر من شيخ في المخازن المصدر، مع القرار الآلي المعتمد (بادئة السلسلة الفائزة):

| # | معرّف الدرس (VID) | المشايخ المتنازعون | المسار المعتمد | الشيخ المعتمد |
|---|---|---|---|---|
| 1 | `wlK7z0JkemA` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/006_شرح المنهج  المنتخب ｜ دس77 ( ق123 الكتابة هل هي شراء رقبة أو شراء خدمة ) ｜ الشيخ.txt` | **`bardouni-husaymi`** |
| 2 | `q3xeK8QlmD4` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/002_شرح المنهج  المنتخب ｜ دس82 ( ق135كل ما أدى ثبوته إلى نفيه فنفيه أولى) ｜ الشيخ ال.txt` | **`bardouni-husaymi`** |
| 3 | `BjdQmTf4yDA` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/007_شرح المنهج  المنتخب ｜ دس76 ( ق121 مضمن الإقرار هل هو كصريحه ) ｜ الشيخ محمدالبردو.txt` | **`bardouni-husaymi`** |
| 4 | `2pDW0_AFw8A` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/008_شرح المنهج  المنتخب ｜ دس79 ( ق128 المعاملة بنقيض القصد) ｜ الشيخ البردوني.txt` | **`bardouni-husaymi`** |
| 5 | `efUGvLsW30E` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/004_شرح المنهج  المنتخب ｜ دس80 ( ق129 بقاء ما كان على ما كان - ق130الأصل لا يجتمع مع.txt` | **`bardouni-husaymi`** |
| 6 | `LTRdr-jG_oo` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/010_شرح المنهج  المنتخب ｜ دس74 ( ق113 العادة هل هي كالشاهد الواحد أو كالشاهدين ) ｜ ا.txt` | **`bardouni-husaymi`** |
| 7 | `OnIJviRxPx0` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/013_شرح المنهج  المنتخب ｜ دس 71 ( ق105 هل ظن الكمال كالتحقق أم لا   ) ｜ الشيخ محمد ا.txt` | **`bardouni-husaymi`** |
| 8 | `DXgieAwH75g` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/011_شرح المنهج  المنتخب ｜ دس73 ( ق111 إذا دار الملك بين أن يبطل جملة أو من وجه فالثا.txt` | **`bardouni-husaymi`** |
| 9 | `dLjq1H4nmBo` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/014_شرح المنهج  المنتخب ｜ دس 70 ( ق104 اشتراط ما لا يفيد هل يجب الوفاء به أم لا  ) ｜.txt` | **`bardouni-husaymi`** |
| 10 | `xVT8MNNfxlA` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/005_شرح المنهج  المنتخب ｜ دس78 ( ق127 إعطاء الموجود حكم المعدوم أو المعدوم حكم الموج.txt` | **`bardouni-husaymi`** |
| 11 | `CffvWa-67Zo` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/012_شرح المنهج  المنتخب ｜ دس 72 ( ق108 كل ما ينتقل ملكه بغير عوض يشترط فيه الحوز ) ｜.txt` | **`bardouni-husaymi`** |
| 12 | `VAvUv-DViA0` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/009_شرح المنهج  المنتخب ｜ دس75 ( ق115 الأرض هل هي مستهلكة أم مربية  ) ｜ الشيخ محمدال.txt` | **`bardouni-husaymi`** |
| 13 | `MrZY7-35aGU` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/003_شرح المنهج  المنتخب ｜ دس81 ( ق132 الضرورات تبيح المحظورات) ｜ الشيخ البردوني.txt` | **`bardouni-husaymi`** |
| 14 | `NcS9h3t4xgU` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/001_شرح المنهج  المنتخب ｜ دس83 ( ق136 الأص أن من أتلف مثليا فعليه مثله إلا في المصرا.txt` | **`bardouni-husaymi`** |
| 15 | `pSPTdf7gqNw` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/985/015_شرح المنهج  المنتخب ｜ دس 69 ( ق102 اشتراط ما يوجب الحكم خلافه هل يعتبر أم لا ) ｜.txt` | **`bardouni-husaymi`** |
| 16 | `بلا vid` | ali-gomaa · habib-ali-aljifri · habib-omar-ibn-hafiz | `des/mutalaa/data/txt/239/057_إيضاح أسرار علوم المقربين - الدرس السابع والخمسون - خطر الانسياق وراء الغضب.txt` | **`ali-gomaa`** |
| 17 | `KmUVqzXW38w` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/019_شرح الحكم ｜ دس19 ＂ ما أرادت همة سالك أن تقف عند ما كشف لها إلا نادته هواتف الحقي.txt` | **`ali-gomaa`** |
| 18 | `7jGV-waj_D8` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/016_شرح الحكم ｜ الدرس 16 ＂مما يدلك على وجود قهره سبحانه أن حجبك عنه بما ليس بموجود م.txt` | **`ali-gomaa`** |
| 19 | `FQP-lGAkSYs` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/014_شرح الحكم العطائية ｜ الدرس 14 ＂ الكون كله ظلمة و إنما أناره ظهور الحق فيه ＂ ｜ ال.txt` | **`ali-gomaa`** |
| 20 | `mVB0vEByBjo` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/007_شرح الحكم العطائية ｜ الدرس 7 ｜ الشيخ محمد البردوني الحسيمي.txt` | **`ali-gomaa`** |
| 21 | `wezbVCV6vqA` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/020_شرح الحكم ｜ دس20 ＂  طلبك منه اتهام له و طلبك له غيبة منك عنه   ＂ ｜ الشيخ محمد ال.txt` | **`ali-gomaa`** |
| 22 | `3buuhNKEg-0` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/013_شرح الحكم العطائية ｜ الدرس 13 ＂ كيف يشرق قلب صور الاكوان منطبعة في مرآته -تتمة- .txt` | **`ali-gomaa`** |
| 23 | `flt1OUzCyrQ` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/018_شرح الحكم ｜دس18-لا تطلب منه أن يخرجك من حالة ليستعملك فيما سواها إذ لو أرادك لاس.txt` | **`ali-gomaa`** |
| 24 | `W1MikGO_774` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/008_شرح الحكم العطائية ｜ الدرس 8＂ تنوعت أجناس الأعمال لتنوع واردات الأحوال＂｜ الشيخ م.txt` | **`ali-gomaa`** |
| 25 | `kINUd97QAAQ` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/009_شرح الحكم العطائية ｜ الدرس 9 ＂ الأعمال صور قائمة و أرواحها وجود السر الإخلاص فيه.txt` | **`ali-gomaa`** |
| 26 | `g17CMZMRsHM` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/010_شرح الحكم العطائية｜الدرس 10＂إدفن نفسك في أرض الخمول فما نبت مما لم يدفن لا يتم ن.txt` | **`ali-gomaa`** |
| 27 | `sF5frekLgqs` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/006_شرح الحكم العطائية ｜ الدرس 6 ｜ الشيخ محمد البردوني الحسيمي.txt` | **`ali-gomaa`** |
| 28 | `qo2PmzRA6R8` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/017_شرح الحكم ｜دس17 ＂ما ترك من الجهل شيئا من أراد أن يحدث في الوقت غير ما أظهره الله.txt` | **`ali-gomaa`** |
| 29 | `7kuwk6U53JU` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/012_شرح الحكم العطائية ｜الدرس 12 ＂ كيف يشرق قلب صور الاكوان منطبعة في مرآته＂｜ الشيخ .txt` | **`ali-gomaa`** |
| 30 | `BUVWvNsYcXk` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/005_شرح الحكم العطائية ｜ الدرس 5 ｜  الشيخ  محمد البردوني الحسيمي.txt` | **`ali-gomaa`** |
| 31 | `K4gyhA9b6mQ` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/001_شرح الحكم العطائية  ｜  الدرس 1 ｜ الشيخ محمدالبردوني الحسيمي.txt` | **`ali-gomaa`** |
| 32 | `ZUZSAtpR0Rk` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/015_شرح الحكم العطائية ｜ الدرس 15 ＂ الكون كله ظلمة و إنما أناره ظهور الحق فيه -تتمة-.txt` | **`ali-gomaa`** |
| 33 | `lIcplZ1zwgs` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/021_شرح الحكم ｜ دس21 ＂ ما من نفس تبديه إلا و له قدر فيك يمضيه ＂ ｜ الشيخ محمد البردون.txt` | **`ali-gomaa`** |
| 34 | `SJffj3xM0iE` | ali-gomaa · bardouni-husaymi | `des/mutalaa/data/txt/997/011_شرح الحكم العطائية ｜ الدرس 11 ｜ الشيخ محمد البردوني الحسيمي.txt` | **`ali-gomaa`** |
| 35 | `HGCLbQEc0Bw` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/001_شرح نظم الاستعارة  ｜ الدرس 11-الأخير- ( مجاز النسبة ) ｜  الشيخ محمد البردوني الح.txt` | **`bardouni-husaymi`** |
| 36 | `PMgNROSsp1U` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/003_شرح نظم الاستعارة  ｜ الدرس 9 (الاستعارة التخييلية) ｜  الشيخ محمد البردوني الحسيم.txt` | **`bardouni-husaymi`** |
| 37 | `iGtyX7H0KCc` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/007_شرح نظم الاستعارة  ｜ الدرس 4 (المجاز المرسل) ｜  الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 38 | `8IsPOzjH8Cc` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/008_شرح نظم الاستعارة  ｜ الدرس 3 (تعريف الحقيقة و المجاز و أقسامهما) ｜  الشيخ محمد ا.txt` | **`bardouni-husaymi`** |
| 39 | `bGWyXjYHRpc` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/004_شرح نظم الاستعارة  ｜ الدرس 8 (الاستعارة المكنية) ｜  الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 40 | `FZjcydhZmCQ` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/006_شرح نظم الاستعارة  ｜ الدرس 5 (أقسام الاستعارة) ｜  الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 41 | `kK_H7EbT5wU` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/009_شرح نظم الاستعارة  ｜ الدرس 2 ｜  الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 42 | `frWpEHIpXWg` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/002_شرح نظم الاستعارة  ｜ الدرس 10 ( المجاز المركب ) ｜  الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 43 | `WA1nWeDrQuI` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/010_شرح نظم الاستعارة  ｜ الدرس 1 ｜  الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 44 | `rSoPe6XEQZ4` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/990/005_شرح نظم الاستعارة  ｜ الدرس 7  ｜  الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 45 | `QICpLAntzak` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/010_شرح الرسالة العضدية ｜ الدرس 10 (قوله ＂ اللفظ قد يوضع لشخص بعينه＂ ) ｜ الشيخ محمد .txt` | **`bardouni-husaymi`** |
| 46 | `VLbwq2VCpvA` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/008_شرح الرسالة العضدية ｜ الدرس 8 (المقدمة-تتمة-) ｜ الشيخ محمد البردوني.txt` | **`bardouni-husaymi`** |
| 47 | `zISph8T35jY` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/013_شرح العضدية ｜ الدرس 13 (قوله ＂ تنبيه ما هو من هذا القبيل لا يفيد التشخص الا بقري.txt` | **`bardouni-husaymi`** |
| 48 | `iIAjq6G89tU` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/004_شرح الرسالة العضدية ｜ الدرس 4 (المقدمة-تتمة-) ｜ الشيخ محمد البردوني.txt` | **`bardouni-husaymi`** |
| 49 | `jzlRIRjwgAg` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/003_شرح الرسالة العضدية ｜ الدرس 3 (المقدمة-تتمة-) ｜ الشيخ محمد البردوني.txt` | **`bardouni-husaymi`** |
| 50 | `NstFsI0-q2c` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/021_شرح الرسالة العضدية ｜ الدرس 21 ( قوله ＂ التنبيه الرابع-تتمة- ＂ ) ｜ الشيخ  محمد ا.txt` | **`bardouni-husaymi`** |
| 51 | `C-zZjmsQ42c` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/018_شرح الرسالة العضدية ｜ الدرس 18 ( قوله ＂ التنبيه الثالت ＂ ) ｜ الشيخ  محمد البردون.txt` | **`bardouni-husaymi`** |
| 52 | `hnyjlmRqZSs` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/007_شرح الرسالة العضدية ｜ الدرس 7 (المقدمة-تتمة-) ｜ الشيخ محمد البردوني.txt` | **`bardouni-husaymi`** |
| 53 | `EUCaEqVHjaE` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/005_شرح الرسالة العضدية ｜ الدرس 5 (المقدمة-تتمة-) ｜ الشيخ محمد البردوني.txt` | **`bardouni-husaymi`** |
| 54 | `NKdexOMIMFQ` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/015_شرح الرسالة العضدية ｜ الدرس 15 (قوله ＂ و الأول إما ذات او حدث＂ ) ｜ الشيخ محمد ال.txt` | **`bardouni-husaymi`** |
| 55 | `6f5I17ekts8` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/022_شرح الرسالة العضدية ｜ الدرس 22 ( قوله＂ التنبيه الخامس و السادس و السابع و الثامن.txt` | **`bardouni-husaymi`** |
| 56 | `XrjsXuixjNo` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/017_شرح الرسالة العضدية ｜ الدرس 17 ( قوله ＂ الخاتمة تشتمل على تنبيهات ＂ ) ｜ الشيخ  م.txt` | **`bardouni-husaymi`** |
| 57 | `Cn2j0Uu9eQ4` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/002_شرح الرسالة العضدية ｜ الدرس 2 (المقدمة-تتمة-) ｜ الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 58 | `CYhdKfc60J8` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/020_شرح الرسالة العضدية ｜ الدرس 20 ( قوله ＂ التنبيه الرابع-تتمة- ＂ ) ｜ الشيخ  محمد ا.txt` | **`bardouni-husaymi`** |
| 59 | `e70rby6DcHM` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/009_شرح الرسالة العضدية ｜ الدرس 9 (المقدمة-تتمة-) ｜ الشيخ محمد البردوني.txt` | **`bardouni-husaymi`** |
| 60 | `pUyIKyYH2vQ` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/023_شرح الرسالة العضدية ｜ الدرس 23- الأخير- ( ＂ التنبيه التاسع ＂) ｜ الشيخ محمد البرد.txt` | **`bardouni-husaymi`** |
| 61 | `5_bUYZJrnHc` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/016_شرح الرسالة العضدية｜ الدرس 16 (قوله＂و الثاني مدلوله إما أن يكون معنى في غيره٠٠)｜.txt` | **`bardouni-husaymi`** |
| 62 | `eC_2EFV1iyo` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/019_شرح الرسالة العضدية ｜ الدرس 19 ( قوله ＂ التنبيه الرابع-تتمة- ＂ ) ｜ الشيخ  محمد ا.txt` | **`bardouni-husaymi`** |
| 63 | `CxhQ6xzPaJs` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/988/002_شرح رسالة ابن ابي زيد القيرواني ｜ الدرس الثاني｜ الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 64 | `DapjxZMbpQ0` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/012_شرح الرسالة العضدية ｜ الدرس 12 (قوله ＂ فالوضع كلي و الموضوع له مشخص＂ ) ｜ الشيخ م.txt` | **`bardouni-husaymi`** |
| 65 | `orKWplmdHvQ` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/001_شرح الرسالة العضدية ｜ الدرس 1 (المقدمة) ｜ الشيخ محمد البردوني الحسيمي.txt` | **`bardouni-husaymi`** |
| 66 | `1vljrtty2v0` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/011_شرح الرسالة العضدية ｜ الدرس 11 (قوله ＂ اللفظ قد يوضع لشخص بعينه-تتمة-＂ ) ｜ الشيخ.txt` | **`bardouni-husaymi`** |
| 67 | `5FjrC2zaLEI` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/006_شرح الرسالة العضدية ｜ الدرس 6 (المقدمة-تتمة-) ｜ الشيخ محمد البردوني.txt` | **`bardouni-husaymi`** |
| 68 | `ux_hocepN2o` | bardouni-husaymi · mouloud-sariri | `des/mutalaa/data/txt/992/014_شرح الرسالة العضدية ｜ الدرس 14 (قوله ＂ اللفظ مدلوله إما كلي أو جزئي＂ ) ｜ الشيخ م.txt` | **`bardouni-husaymi`** |
| 69 | `dSPmvIe1nkU` | adham-alasimi · habib-omar-ibn-hafiz | `des/mutalaa/data/txt/781/005_(05) عبد الله الذبيح وفداؤه ⧸ السيرة النبوية ⧸ الشيخ أدهم العاسمي.txt` | **`adham-alasimi`** |
| 70 | `PPuCtMciB54` | adham-alasimi · habib-omar-ibn-hafiz | `des/mutalaa/data/txt/781/011_(11) ختم النبوة ⧸ السيرة النبوية ⧸ الشيخ أدهم العاسمي.txt` | **`adham-alasimi`** |
| 71 | `idelHZln40Q` | adham-alasimi · habib-omar-ibn-hafiz | `des/mutalaa/data/txt/781/006_(06) من إرهاصات النبوة ⧸ السيرة النبوية ⧸ الشيخ أدهم العاسمي.txt` | **`adham-alasimi`** |
| 72 | `AdRtZheEDAo` | adham-alasimi · habib-omar-ibn-hafiz | `des/mutalaa/data/txt/781/002_(02) فوائد دراسة السيرة (2) ⧸ السيرة النبوية ⧸ الشيخ أدهم العاسمي.txt` | **`adham-alasimi`** |
| 73 | `mhCkLFoA3BY` | adham-alasimi · habib-omar-ibn-hafiz | `des/mutalaa/data/txt/781/021_(21) موقف السيدة خديجة من الوحي ⧸ السيرة النبوية ⧸ الشيخ أدهم العاسمي.txt` | **`adham-alasimi`** |
| 74 | `6IvAtp4ryjk` | adham-alasimi · habib-omar-ibn-hafiz | `des/mutalaa/data/txt/781/004_(04) قبل المبعث ⧸ الجزيرة العربية ⧸ السيرة النبوية ⧸ الشيخ أدهم العاسمي.txt` | **`adham-alasimi`** |
| 75 | `IyBHJgXnStg` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/014_شرح أم البراهين ｜ الدرس 23 ( قوله ＂ برهان وجود الله  ＂ ) ｜ الشيخ محمد البردوني.txt` | **`adham-alasimi`** |
| 76 | `vIJfI8ZeF58` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/007_شرح أم البراهين ｜ الدرس30(قوله＂برهان كون فعل الممكنات أو تركها جائزا في حقه سبحا.txt` | **`adham-alasimi`** |
| 77 | `f7mJVw-ZmAI` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/005_شرح أم البراهين ｜ الدرس 32 (  دليل جواز الأعراض البشرية في حق الأنبياء ) ｜ الشيخ.txt` | **`adham-alasimi`** |
| 78 | `PLbMPERpY1o` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/013_شرح أم البراهين ｜ الدرس 24 ( قوله ＂ برهان وجود الله-تتمة-  ＂ ) ｜ الشيخ محمد البر.txt` | **`adham-alasimi`** |
| 79 | `WTSHdqtmqhg` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/008_شرح أم البراهين ｜ الدرس29 (قوله ＂برهان وجوب اتصافه سبحانه بالقدرة و العلم و الحي.txt` | **`adham-alasimi`** |
| 80 | `FLSO3rKiHac` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/009_شرح أم البراهين ｜ الدرس 28 ( قوله ＂ برهان وجوب الوحدانية لله سبحانه-تتمة-  ＂ ) ｜.txt` | **`adham-alasimi`** |
| 81 | `MMU384FDL08` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/010_شرح أم البراهين ｜ الدرس 27 ( قوله ＂ برهان وجوب الوحدانية لله سبحانه  ＂ ) ｜ الشيخ.txt` | **`adham-alasimi`** |
| 82 | `fQcXFFmOLDo` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/003_شرح أم البراهين ｜ الدرس 33 ( معاني لا إله إلا الله ) ｜ الشيخ محمد البردوني.txt` | **`adham-alasimi`** |
| 83 | `LIzLYZFiUHA` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/006_شرح أم البراهين ｜ الدرس 31 ( قوله ＂ برهان وجوب صدق الانبياء ＂ ) ｜ الشيخ محمد الب.txt` | **`adham-alasimi`** |
| 84 | `lyo9ZjyeI2k` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/012_شرح أم البراهين ｜ الدرس 25 ( قوله ＂ برهان وجوب القدم لله سبحانه  ＂ ) ｜ الشيخ محم.txt` | **`adham-alasimi`** |
| 85 | `yD9ASBvTcSQ` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/002_شرح أم البراهين ｜ الدرس 35 ( معاني لا إله إلا الله-تتمة- ) ｜ الشيخ محمد البردوني.txt` | **`adham-alasimi`** |
| 86 | `lhtjluwWOS4` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/001_شرح أم البراهين ｜ الدرس 36 و الأخير ( معاني محمد رسول الله ) ｜ الشيخ محمد البردو.txt` | **`adham-alasimi`** |
| 87 | `bvfIiRJm20k` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/004_شرح أم البراهين ｜ الدرس 34 ( معاني لا إله إلا الله-تتمة- ) ｜ الشيخ محمد البردوني.txt` | **`adham-alasimi`** |
| 88 | `iaovSvOxzSU` | adham-alasimi · bardouni-husaymi | `des/mutalaa/data/txt/984/011_شرح أم البراهين ｜ الدرس 26 ( قوله ＂ برهان وجوب البقاء لله سبحانه  ＂ ) ｜ الشيخ مح.txt` | **`adham-alasimi`** |

---

## 7. تعدد السلاسل والصفوف (الـ 294 درساً)

دروس ظهرت في أكثر من سلسلة؛ تم توجيهها للسلسلة الرقمية القانونية المعتمدة مع تسجيل السلاسل الأخرى في حقل `also_in`:

- إجمالي الدروس المشتركة بين السلاسل: **294** درساً.
- قاعدة الحسم المطبقة: السلسلة بعد `canon()`، مع تفضيل صف المطالعة الرقمي على السلاسل القديمة، وتسجيل الباقي في بيانات الدرس الوصفية.

| عينة من الدروس المتعددة | السلاسل التي ظهر فيها | السلسلة الفائزة |
|---|---|---|
| `wlK7z0JkemA` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `q3xeK8QlmD4` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `BjdQmTf4yDA` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `2pDW0_AFw8A` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `efUGvLsW30E` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `LTRdr-jG_oo` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `OnIJviRxPx0` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `DXgieAwH75g` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `dLjq1H4nmBo` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `xVT8MNNfxlA` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `CffvWa-67Zo` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `VAvUv-DViA0` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `MrZY7-35aGU` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `NcS9h3t4xgU` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |
| `pSPTdf7gqNw` | bardouni-husaymi--bardouni-mut-985 · mouloud-sariri--37 | **`bardouni-husaymi--bardouni-mut-985`** |

---

## 8. الصفوف المصنوعة (Created Rows)

12 صفاً تم إنشاؤها وفق اصطلاح `gen_stats` لربط الصفوف غير المسجلة في `row_ids.json` القديم:

| الصف الأصلي | المعرّف القانوني المصنوع | الشيخ | اسم السلسلة |
|---|---|---|---|
| `36` | `mouloud-sariri--36` | `mouloud-sariri` | شرح الرسالة العضدية |
| `37` | `mouloud-sariri--37` | `mouloud-sariri` | شرح المنهج المنتخب (durus) |
| `40` | `mouloud-sariri--40` | `mouloud-sariri` | نظم الاستعارة |
| `112` | `habib-ali-aljifri--112` | `habib-ali-aljifri` | مقتطفات برنامج الإنسانية قبل التدين |
| `173` | `habib-omar-ibn-hafiz--173` | `habib-omar-ibn-hafiz` | مجلس قراءة السيرة النبوية - إرشادات السلوك |
| `344` | `said-bouti--bouti-khutab-2010` | `said-bouti` | خطب الجمعة لعام 2010 |
| `355` | `said-bouti--bouti-muqtatafat-ulum` | `said-bouti` | مقتطفات من سلسلة علوم القرآن الكريم |
| `743` | `adham-alasimi--743` | `adham-alasimi` | شرح العقيدة الصغرى (أم البراهين) |
| `871` | `ali-gomaa--871` | `ali-gomaa` | شرح الحكم العطائية | الأزهر الشريف |
| `985` | `bardouni-husaymi--bardouni-mut-985` | `bardouni-husaymi` | المنهج المنتخب |
| `995` | `bardouni-husaymi--10` | `bardouni-husaymi` | شرح منظومة الأجهوري (مدمج في 10) |

---

## 9. سلامة الجودة: الملفات الملوثة والقصيرة

- **ملفات ملوثة بتفكير النموذج (F11):** 18 ملفاً تم عزلها وترقيتها ببدائل سليمة كلما وُجدت.
- **ملفات قصيرة (< 300 حرف):** 31 ملفاً.

---

## 10. الفرق بين المانيفست الحي والمثبّت (F13)

تمت مقارنة `des/mutalaa/data/manifest.json` الحي مع `hawshat/playlists/data/mut_manifest.json` المثبّت:
- كلاهما يحتوي على **999** صفاً تماماً.
- كلاهما يحتوي على **2,729** درساً منجزاً تماماً.
- أول فرق عند البايت 216,711 في الصف **114**:
  - النسخة الحية (des): `الإنسانية قبل التدين (English Subtitle)`
  - النسخة المثبتة (hawshat): `الإنسانية قبل التدين‬⁩ - الحبيب علي الجفري English Subtitle`
- تم اعتماد النسخة الحية كمرجع رئيسي وفق الخطة.
