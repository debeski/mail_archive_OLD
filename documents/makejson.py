import json

data = [
    {
        "sentence": "رسالة في سنة 2020 بخصوص ... وارده من مركز تنمية الصادرات",
        "labels": ["O", "O", "O", "B-YEAR", "B-KEY", "I-KEY", "B-INC", "O", "B-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "قرار صادر في 2014 من الوزير سهيل ابوشيحه يتكلم عن ...",
        "labels": ["B-DEC", "I-DEC", "O", "B-YEAR", "O", "B-MIN", "I-MIN", "I-MIN", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "كل البريد الوارد من شهر مارس 2019 الى شهر سبتمبر 2021",
        "labels": ["O", "B-INC", "I-INC", "O", "O", "B-MONTH", "B-YEAR", "O", "O", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "مذكرة داخلية بتاريخ 18-10-2015 من مكتب الشؤون القانونية الى ادارة الموارد البشرية",
        "labels": ["B-INT", "I-INT", "O", "B-DATE", "O", "B-DEPT", "I-DEPT", "I-DEPT", "O", "B-DEPT", "I-DEPT", "I-DEPT"]
    },
    {
        "sentence": "كتاب صادر بتاريخ 20 يوليو 2011 بشأن ...",
        "labels": ["B-OUT", "I-OUT", "O", "B-DAY", "B-MONTH", "B-YEAR", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "رساله رقمها 1-7-101 في سنة 2010",
        "labels": ["O", "O", "B-NUM", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "كتاب رقمه 3122 سنة 2014",
        "labels": ["O", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": "منشور رقم 18 في شهر 8",
        "labels": ["O", "O", "B-NUM", "O", "O", "B-MONTH"]
    },
    {
        "sentence": "مذكرة رقمها 340 في يونيو",
        "labels": ["B-INT", "O", "B-NUM", "O", "B-MONTH"]
    },
    {
        "sentence": "مستند رقمه 1/7/4275 في 2019",
        "labels": ["O", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": "كتاب صادر رقمه 7-1-3457 في سنة 2007",
        "labels": ["B-OUT", "I-OUT", "O", "B-NUM", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "رسالة بخصوص ... بين سنة 2010 و 2015",
        "labels": ["O", "B-KEY", "I-KEY", "O", "O", "B-YEAR", "O", "B-YEAR"]
    },
    {
        "sentence": "قرار من محمد الحويج بحكومة الوحدة الوطنية بخصوص ...",
        "labels": ["B-DEC", "O", "B-MIN", "I-MIN", "B-GOV", "I-GOV", "I-GOV", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "رساله جايه من وزارة المالية لمكتب المتابعة في شهر 7 سنة 2022",
        "labels": ["B-INC", "I-INC", "O", "B-AFFT", "I-AFFT", "B-DEPT", "I-DEPT", "O", "O", "B-MONTH", "O", "B-YEAR"]
    },
    {
        "sentence": "رساله طالعه من ادارة الشؤون الادارية والمالية ماشيا للهيئة العامة للمعلومات بخصوص ...",
        "labels": ["B-OUT", "I-OUT", "O", "B-DEPT", "I-DEPT", "I-DEPT", "I-DEPT", "B-OUT", "B-AFFT", "I-AFFT", "I-AFFT", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي حاجه تتكلم على ... من سنة 2000 الى 2009",
        "labels": ["O", "O", "O", "B-KEY", "I-KEY", "O", "O", "B-YEAR", "O", "B-YEAR"]
    },
    {
        "sentence": "قرار رقم 54 لسنة 2006",
        "labels": ["B-DEC", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": "كتاب وارد مسجل برقم 289 سنه 2023",
        "labels": ["B-INC", "I-INC", "O", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": "رساله صادره برقم 374 لسنه 2018",
        "labels": ["B-OUT", "I-OUT", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": "كتاب صادر يحمل رقم 0943 في 2011",
        "labels": ["B-OUT", "I-OUT", "O", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": "مذكرة داخلية عندها رقم 3892 في سنة 2021",
        "labels": ["B-INT", "I-INT", "O", "O", "B-NUM", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "قرار صادر برقم 1027 سنه 1998",
        "labels": ["B-DEC", "I-DEC", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": "قرار وزير رقمه 1432 في 2020",
        "labels": ["B-DEC", "I-DEC", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": " قرار وزاري رقمه 652 لسنة 2012",
        "labels": ["B-DEC", "I-DEC", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": "قرار الوزير 931 في سنة 2007",
        "labels": ["B-DEC", "I-DEC", "B-NUM", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "قرار وكيل يحمل رقم 392 صادر في سنة 2014",
        "labels": ["B-DEC", "I-DEC", "O", "O", "B-NUM", "O", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "قرار رقم 214 بتاريخ 14-2-2011",
        "labels": ["B-DEC", "O", "B-NUM", "O", "B-DATE"]
    },
    {
        "sentence": "صادر رقم 628 يوم 12-3-2005",
        "labels": ["B-OUT", "O", "B-NUM", "O", "B-DATE"]
    },
    {
        "sentence": "وارد رقمه 5439 بتاريخ 8-8-2016",
        "labels": ["B-INC", "O", "B-NUM", "O", "B-DATE"]
    },
    {
        "sentence": "مستند رقمه 1724 يوم 19-4-2024",
        "labels": ["O", "O", "B-NUM", "O", "B-DATE"]
    },
    {
        "sentence": "كتاب رقم 1-4-3395 تاريخه 3-10-2010",
        "labels": ["O", "O", "B-NUM", "O", "B-DATE"]
    },
    {
        "sentence": "مذكرة رقمها 86 تاريخها 22-11-2001",
        "labels": ["B-INT", "O", "B-NUM", "O", "B-DATE"]
    },
    {
        "sentence": "رساله رقم 7654-4-1 في يوم 4-10-2019",
        "labels": ["O", "O", "B-NUM", "O", "O", "B-DATE"]
    },
    {
        "sentence": "قرار 117 بتاريخ 17-7-2007",
        "labels": ["B-DEC", "B-NUM", "O", "B-DATE"]
    },
    {
        "sentence": "رسالة صادره برقم 514 في سنة 2015 بخصوص مركز تنمية الصادرات",
        "labels": ["B-OUT", "I-OUT", "O", "B-NUM", "O", "O", "B-YEAR", "B-KEY", "I-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "رسالة وارده برقم 514 في سنة 2015 من مركز تنمية الصادرات",
        "labels": ["B-INC", "I-INC", "O", "B-NUM", "O", "O", "B-YEAR", "O", "B-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "كتاب صادر من وزارة الزراعة على موضوع ...",
        "labels": ["B-OUT", "I-OUT", "O", "B-AFFT", "I-AFFT", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "كتاب وارد جاي من وزارة الزراعة على موضوع ...",
        "labels": ["B-INC", "I-INC", "I-INC", "O", "B-AFFT", "I-AFFT", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اعطيني اي رساله بخصوص ...",
        "labels": ["O", "O", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي قرار بشأن وزارة المالية في عام 2016",
        "labels": ["O", "DEC", "B-KEY", "I-KEY", "I-KEY", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "جميع القرارات الصادرة في آخر شهرين",
        "labels": ["O", "B-DEC", "I-DEC", "O", "B-MONTH", "I-MONTH"]
    },
    {
        "sentence": "بريد طالع من قسم شؤون الموظفين بتاريخ 15 3",
        "labels": ["B-OUT", "I-OUT", "O", "B-DEPT", "I-DEPT", "I-DEPT", "O", "B-DAY", "B-MONTH"]
    },
    {
        "sentence": "قرار صادر بتاريخ 7 سبتمبر من سنة 2011",
        "labels": ["B-DEC", "I-DEC", "O", "B-DAY", "B-MONTH", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "اعطيني كل الرسائل الصادرة في النصف الثاني من عام 2023",
        "labels": ["O", "O", "B-OUT", "B-OUT", "O", "B-PERIOD", "I-PERIOD", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "اي حاجة صدرت بين تاريخ 15-10-2021 و 15-11-2021",
        "labels": ["O", "O", "B-OUT", "O", "O", "B-DATE", "O", "B-DATE"]
    },
    {
        "sentence": "كل الرسائل الواردة في الربع الاول من عام 2020",
        "labels": ["O", "B-INC", "B-INC", "O", "B-PERIOD", "I-PERIOD", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "الرسايل الصادرة في الفترة من 1 يناير 2019 الى 31 سبتمبر 2019",
        "labels": ["B-OUT", "B-OUT", "O", "O", "O", "B-DAY", "B-MONTH", "B-YEAR", "O", "B-DAY", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "الرسائل اللي صدرت في اول ثلاث شهور من هذه السنه",
        "labels": ["O", "O", "B-OUT", "O", "B-PERIOD", "I-PERIOD", "I-PERIOD", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "كل الرسائل الصادره في 2024 حتى الآن",
        "labels": ["O", "B-OUT", "B-OUT", "O", "B-YEAR", "O", "B-DAY"]
    },
    {
        "sentence": "جميع القرارات من يناير حتى مارس 2024",
        "labels": ["O", "B-DEC", "O", "B-MONTH", "O", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "كتاب يحمل رقم 548 بشان ...",
        "labels": ["O", "O", "O", "B-NUM", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي حاجه طالعه من الوزاره في يوم 23 شهر 7",
        "labels": ["O", "O", "B-OUT", "O", "O", "O", "O", "B-DAY", "O", "B-MONTH"]
    },
    {
        "sentence": "البريد الوارد من رقم 25 الى 66 في سنة 2013",
        "labels": ["B-INC", "I-INC", "O", "O", "B-NUM", "O", "B-NUM", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "طلعلي كل الرسايل الصادره من مكتب العلامات التجارية في شهر 12 عام 2023",
        "labels": ["O", "O", "B-OUT", "I-OUT", "O", "B-DEPT", "I-DEPT", "I-DEPT", "O", "O", "B-MONTH", "O", "B-YEAR"]
    },
    {
        "sentence": "كل المستندات الصادرة من ادارة التجارة الخارجية في سنة 2012",
        "labels": ["O", "B-OUT", "I-OUT", "O", "B-DEPT", "I-DEPT", "I-DEPT", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "كل البريد الموجه الى مركز المعلومات والتوثيق الاقتصادي",
        "labels": ["O", "B-OUT", "I-OUT", "O", "B-AFFT", "I-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "كل الكتابات الصادرة من مشروع ليبيا الغد 15-12-2024",
        "labels": ["O", "B-OUT", "I-OUT", "O", "B-AFFT", "I-AFFT", "I-AFFT", "B-DATE"]
    },
    {
        "sentence": "قرار في سنة 2014 يخصوص الهيكل التنظيمي من الوزير احمد الكوشلي بحكومة الانقاذ",
        "labels": ["B-DEC", "O", "O", "B-YEAR", "B-KEY", "I-KEY", "I-KEY", "O", "B-MIN", "I-MIN", "I-MIN", "B-GOV", "I-GOV"]
    },
    {
        "sentence": "القرارات متع الوزير علي القطراني",
        "labels": ["B-DEC", "O", "B-MIN", "I-MIN", "I-MIN"]
    },
    {
        "sentence": "كل المراسلات المتعلقة ب ...",
        "labels": ["O", "O", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي رسالة تتعلق ب ...",
        "labels": ["O", "O", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي كتاب يحمل رقم 777 في سنة 2011",
        "labels": ["O", "O", "O", "O", "B-NUM", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "جميع قرارات محمد الحويج في الحكومة الليبية المؤقتة",
        "labels": ["O", "B-DEC", "B-MIN", "I-MIN", "O", "B-GOV", "I-GOV", "I-GOV"]
    },
    {
        "sentence": "كل قرار من مصطفى ابوفناس في حكومة الانقاذ الوطني",
        "labels": ["O", "B-DEC", "O", "B-MIN", "I-MIN", "O", "B-GOV", "I-GOV", "I-GOV"]
    },
    {
        "sentence": "اي قرار من الوزير سليمان العجيلي في فترة مابين شهر اكتوبر وشهر ديسمبر لسنة 2018",
        "labels": ["O", "B-DEC", "O", "B-MIN", "I-MIN", "I-MIN", "O", "O", "O", "O", "B-MONTH", "O", "B-MONTH", "O", "B-YEAR"]
    },
    {
        "sentence": "قرارات اللجنة الشعبية العامة في اخر 3 اشهر من سنة 2007",
        "labels": ["B-DEC", "B-GOV", "I-GOV", "I-GOV", "O", "B-PERIOD", "I-PERIOD", "I-PERIOD", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "رسالة من الوزير بشأن احالة مشروع قرار",
        "labels": ["O", "O", "B-DEPT", "B-KEY", "I-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "منشور من الوزير بتاريخ فبراير 2023 بشان ...",
        "labels": ["O", "O", "B-DEPT", "O", "B-MONTH", "B-YEAR", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "كتاب صادر في يوم 24 من شهر سبتمبر بخصوص تعميم على الهيئات والمراكز والجهات التابعة",
        "labels": ["B-OUT", "I-OUT", "O", "O", "B-DAY", "O", "O", "B-MONTH", "B-KEY", "I-KEY", "I-KEY", "I-KEY", "I-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "قرار من الوزير الطيب الصافي به مرفقات",
        "labels": ["B-DEC", "O", "B-MIN", "I-MIN", "I-MIN", "O", "O"]
    },
    {
        "sentence": "كل القرارات من الوزير علي العيساوي التي بها ملف مرفق",
        "labels": ["O", "B-DEC", "O", "B-MIN", "I-MIN", "I-MIN", "O", "O", "O", "O"]
    },
    {
        "sentence": "اي كتاب صادر او وارد ليس به ملف pdf",
        "labels": ["O", "B-OUT", "I-OUT", "O", "B-INC", "O", "O", "O", "O"]
    },
    {
        "sentence": "اي كتاب صادر او وارد مافيشي ملف pdf",
        "labels": ["O", "B-OUT", "I-OUT", "O", "B-INC", "O", "O", "O"]
    },
    {
        "sentence": "اي كتاب صادر او وارد مافيش معاه ملف pdf",
        "labels": ["O", "B-OUT", "I-OUT", "O", "B-INC", "O", "O", "O", "O"]
    },
    {
        "sentence": "اي كتاب وارد يتحدث عن ...",
        "labels": ["O", "B-INC", "I-INC", "B-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "داخلي بشان اجهزة كمبيوتر مستعارة",
        "labels": ["B-INT", "B-KEY", "I-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "مذكرة داخليه تتكلم على ...",
        "labels": ["B-INT", "I-INT", "B-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "اي وثيقه وارده الى الوزارة فيها كلمة ...",
        "labels": ["O", "B-INC", "I-INC", "O", "O", "B-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "اي كتاب صادر من مكتب العلامات التجارية فيه كلمات ...",
        "labels": ["O", "B-OUT", "I-OUT", "O", "B-DEPT", "I-DEPT", "I-DEPT", "B-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "رسالة بخصوص ... جايه من مراقبة الاقتصاد مصراتة",
        "labels": ["O", "B-KEY", "I-KEY", "B-INC", "O", "B-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "كتاب بخصوص ... ماشي لمراقبة الاقتصاد بنغازي",
        "labels": ["O", "B-KEY", "I-KEY", "B-OUT", "B-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "طلعلي قرارات الوزير مصطفى بوفناس في الحكومة الليبية الانتقالية",
        "labels": ["O", "B-DEC", "B-MIN", "I-MIN", "I-MIN", "O", "B-GOV", "I-GOV", "I-GOV"]
    },
    {
        "sentence": "قرار مدايراته الحكومة الليبية المؤقتة",
        "labels": ["O", "O", "B-GOV", "I-GOV", "I-GOV"]
    },
    {
        "sentence": "طلع لي اي حاجه من وقت اللجنة الشعبية العامة فيها ...",
        "labels": ["O", "O", "O", "O", "O", "O", "B-GOV", "I-GOV", "I-GOV", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اعطيني كل الرسائل المتعلقة بمراقبات الاقتصاد والتجارة",
        "labels": ["O", "O", "O", "B-KEY", "I-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "كل المستندات الصادرة عن شبكة ليبيا للتجارة",
        "labels": ["O", "B-OUT", "I-OUT", "O", "B-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "الرسايل الوارده من مركز المعلومات والتوثيق الصناعي",
        "labels": ["B-INC", "I-INC", "O", "B-AFFT", "I-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "كل البريد الموجه الى مركز المعلومات والتوثيق الاقتصادي",
        "labels": ["O", "B-OUT", "I-OUT", "O", "B-AFFT", "I-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "شوف لي اي حاجه ليها علاقه ب ...",
        "labels": ["O", "O", "O", "O", "O", "B-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "كل البريد الوارد الى مكتب الوزير في الشهر الماضي",
        "labels": ["O", "B-INC", "I-INC", "O", "B-DEPT", "I-DEPT", "O", "B-MONTH", "I-MONTH"]
    },
    {
        "sentence": "كل المناشير المعممه من وزارة المالية بخصوص ...",
        "labels": ["O", "O", "O", "O", "B-AFFT", "I-AFFT", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "رسالة طالعة من ادارة الشؤون الادارية والمالية",
        "labels": ["O", "B-OUT", "O", "B-DEPT", "I-DEPT", "I-DEPT", "I-DEPT"]
    },
    {
        "sentence": "كل الرسائل التي تحمل الارقام المتسلسلة من 100 الى 200 في سنة 2020",
        "labels": ["O", "O", "O", "O", "O", "O", "O", "B-NUM", "O", "B-NUM", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "رسالة وارده رقم 504 ورساله رقم 102",
        "labels": ["B-INC", "I-INC", "O", "B-NUM", "O", "O", "B-NUM"]
    },
    {
        "sentence": "جميع القرارات التي تحمل رقم 749 من سنة 2015 الى سنة 2024",
        "labels": ["O", "B-DEC", "O", "O", "O", "B-NUM", "O", "O", "B-YEAR", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "مذكرة داخلية بعد 2022 بشان ...",
        "labels": ["B-INT", "I-INT", "O", "B-YEAR", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي شي ورد في شهر يناير في سنة 2005",
        "labels": ["O", "O", "B-INC", "O", "O", "B-MONTH", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "كل ما صدر في شهر فبراير من سنة 2017",
        "labels": ["O", "O", "B-OUT", "O", "O", "B-MONTH", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "اي حاجه طلعت شهر مارس لسنة 2009",
        "labels": ["O", "O", "B-OUT", "O", "B-MONTH", "O", "B-YEAR"]
    },
    {
        "sentence": "كل البريد الداخلي في ابريل لسنة 1997",
        "labels": ["O", "B-INT", "I-INT", "O", "B-MONTH", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "البريد الوارد في شهر مايو سنة 2020",
        "labels": ["B-INC", "I-INC", "O", "O", "B-MONTH", "O", "B-YEAR"]
    },
    {
        "sentence": "اي شي صدر شهر يونيو 2015",
        "labels": ["O", "O", "B-OUT", "O", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "كل ما ورد شهر يوليو في سنة 2003",
        "labels": ["O", "O", "B-INC", "O", "B-MONTH", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "اي حاجه داخليه في اغسطس 2011",
        "labels": ["O", "O", "B-INT", "O", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "كل القرارات في شهر سبتمبر في 1999",
        "labels": ["O", "B-DEC", "O", "O", "B-MONTH", "O", "B-YEAR"]
    },
    {
        "sentence": "كل قرارات شهر اكتوبر 2018",
        "labels": ["O", "B-DEC", "O", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "المذكرات الداخليه في نوفمبر سنة 2024",
        "labels": ["B-INT", "I-INT", "O", "B-MONTH", "O", "B-YEAR"]
    },
    {
        "sentence": "كل ما صدر من قرارات في شهر ديسمبر سنة 2014",
        "labels": ["O", "O", "O", "O", "B-DEC", "O", "O", "B-MONTH", "O", "B-YEAR"]
    },
    {
        "sentence": "رساله جايه لمكتب المراجعة الداخلية تاريخها 20-10-2015",
        "labels": ["B-INC", "I-INC", "B-DEPT", "I-DEPT", "I-DEPT", "O", "B-DATE"]
    },
    {
        "sentence": "كل البريد الوارد من المؤسسة الوطنية للنفط",
        "labels": ["O", "B-INC", "I-INC", "O", "B-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "قرار رقمه 111 بشان تنظيم ...",
        "labels": ["B-DEC", "O", "B-NUM", "B-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "اي ورقه بها كلمة ...",
        "labels": ["O", "O", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي حاجه تتعلق بمكتب الوزير وتاريخها 27 اغسطس 2007",
        "labels": ["O", "O", "B-KEY", "I-KEY", "I-KEY", "O", "B-DAY", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "مراسلات حكومة الوحدة الوطنية بخصوص ...",
        "labels": ["O", "B-GOV", "I-GOV", "I-GOV", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "كل قرارات الوزير عبد القادر البدري",
        "labels": ["O", "B-DEC", "B-MIN", "I-MIN", "I-MIN", "I-MIN"]
    },
    {
        "sentence": "اي كتاب صادر يتعلق بالوزير محمد الحويج",
        "labels": ["O", "B-OUT", "I-OUT", "B-KEY", "I-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "اي منشور من الوزير في سنة 2017",
        "labels": ["O", "O", "O", "B-DEPT", "O", "O", "B-YEAR"]
    },
    {
        "sentence": "طلعلي اي كتاب يتعلق بموضوع ...",
        "labels": ["O", "O", "O", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "كل القرارات اللي اتخذت بشان ...",
        "labels": ["O", "B-DEC", "O", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي رساله تحتوي على ...",
        "labels": ["O", "O", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي رسالة مذكور فيها ...",
        "labels": ["O", "O", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي حاجه تخص ...",
        "labels": ["O", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "اي قرار صادر من مكتب الوزير في 15 يناير 2023",
        "labels": ["O", "B-DEC", "I-DEC", "O", "B-DEPT", "I-DEPT", "O", "B-DAY", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "كل الرسائل الواردة من اللجنة العليا للتعليم",
        "labels": ["O", "B-INC", "I-INC", "O", "B-AFFT", "I-AFFT", "I-AFFT"]
    },
    {
        "sentence": "قرار رقم 999 لسنة 2022 بشأن ...",
        "labels": ["O", "O", "B-NUM", "O", "B-YEAR", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "كتاب صادر بتاريخ 5 ابريل 2021",
        "labels": ["B-OUT", "I-OUT", "O", "B-DAY", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "كل القرارات التي صدرت في شهر سبتمبر 2019",
        "labels": ["O", "B-DEC", "O", "O", "O", "O", "B-MONTH", "B-YEAR"]
    },
    {
        "sentence": "رسالة من مكتب الشؤون الخارجية بشأن ...",
        "labels": ["O", "O", "B-DEPT", "I-DEPT", "I-DEPT", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "قرار وزاري رقم 12 لسنة 2010",
        "labels": ["B-DEC", "I-DEC", "O", "B-NUM", "O", "B-YEAR"]
    },
    {
        "sentence": "مذكرة داخلية بتاريخ 15-12-2020",
        "labels": ["B-INT", "I-INT", "O", "B-DATE"]
    },
    {
        "sentence": "كل الرسائل المتعلقة بمكتب الوزير",
        "labels": ["O", "O", "O", "B-DEPT", "I-DEPT"]
    },
    {
        "sentence": "اي قرار صادر عن الوزير علي الرضا",
        "labels": ["O", "B-DEC", "I-DEC", "O", "B-MIN", "I-MIN", "I-MIN"]
    },
    {
        "sentence": "الكتب الواردة من وزارة التخطيط لعام 2023",
        "labels": ["B-INC", "I-INC", "O", "B-AFFT", "I-AFFT", "O", "B-YEAR"]
    },
    {
        "sentence": "قرار رقم 45 لسنة 2021 يتعلق بـ ...",
        "labels": ["B-DEC", "O", "B-NUM", "O", "B-YEAR", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "كتب واردة من وزارة الثقافة بشأن ...",
        "labels": ["B-INC", "I-INC", "O", "B-AFFT", "I-AFFT", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "رسالة من مكتب الوزير تتعلق بمواضيع ...",
        "labels": ["O", "O", "B-DEPT", "I-DEPT", "O", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "أي مستند يحمل رقم 88",
        "labels": ["O", "O", "O", "O", "B-NUM"]
    },
    {
        "sentence": "مذكرة تتعلق بمركز البحوث والتنمية",
        "labels": ["B-INT", "B-KEY", "I-KEY", "I-KEY", "I-KEY"]
    },
    {
        "sentence": "كل المستندات الواردة من وزراة الداخلية",
        "labels": ["O", "B-INC", "I-INC", "O", "B-AFFT", "I-AFFT"]
    },
    {
        "sentence": "أي كتاب من وزير الصحة بشأن ...",
        "labels": ["O", "O", "O", "B-AFFT", "I-AFFT", "B-KEY", "I-KEY"]
    },
    {
        "sentence": "رسالة واردة برقم 305",
        "labels": ["B-INC", "I-INC", "O", "B-NUM"]
    },
    {
        "sentence": "كل الوثائق المتعلقة بمكتب التخطيط",
        "labels": ["O", "O", "B-KEY", "I-KEY", "I-KEY"]
    }
]

# Save to JSON file
with open('training_data.json', 'w', encoding='utf-8') as f:
    json.dump({"data": data}, f, ensure_ascii=False, indent=4)

