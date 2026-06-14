#!/usr/bin/env python3
"""Generate chinese-flashcards.apkg with audio from macOS TTS."""

import os
import subprocess
import genanki

VOICE = "Tingting"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(OUT_DIR, "_anki_audio")
APKG_PATH = os.path.join(OUT_DIR, "chinese-flashcards.apkg")

os.makedirs(AUDIO_DIR, exist_ok=True)

# ── deck data ──────────────────────────────────────────────────────────────────
deck_data = [
    ("的","de","possessive / modifying particle",[("我的书","wǒ de shū","my book"),("漂亮的花","piàoliang de huā","beautiful flower")]),
    ("一","yī","one",[("一起","yīqǐ","together"),("一个人","yī gè rén","one person / alone")]),
    ("是","shì","to be; yes",[("你是谁","nǐ shì shéi","who are you?"),("这是我的","zhè shì wǒ de","this is mine")]),
    ("在","zài","at; in; exist",[("在家","zài jiā","at home"),("他在哪里","tā zài nǎlǐ","where is he?")]),
    ("不","bù","not; no",[("不好意思","bù hǎoyìsi","excuse me / sorry"),("不客气","bù kèqi","you're welcome")]),
    ("了","le","completed action particle",[("吃了吗","chī le ma","have you eaten?"),("好了","hǎo le","done / okay")]),
    ("有","yǒu","to have; there is",[("我有时间","wǒ yǒu shíjiān","I have time"),("有没有","yǒu méiyǒu","do you have (any)?")]),
    ("和","hé","and; with; peace",[("你和我","nǐ hé wǒ","you and I"),("和平","hépíng","peace")]),
    ("人","rén","person; people",[("中国人","Zhōngguórén","Chinese person"),("好人","hǎorén","good person")]),
    ("这","zhè","this",[("这里","zhèlǐ","here"),("这个","zhège","this one")]),
    ("中","zhōng","middle; China",[("中国","Zhōngguó","China"),("中文","Zhōngwén","Chinese language")]),
    ("大","dà","big; large",[("大学","dàxué","university"),("大家","dàjiā","everyone")]),
    ("为","wèi / wéi","for; because of; act as",[("为什么","wèishéme","why?"),("因为","yīnwèi","because")]),
    ("上","shàng","up; on; above",[("上面","shàngmiàn","above / on top"),("上班","shàngbān","go to work")]),
    ("个","gè","general measure word",[("一个","yī gè","one (of something)"),("这个人","zhège rén","this person")]),
    ("国","guó","country; nation",[("国家","guójiā","country / nation"),("外国","wàiguó","foreign country")]),
    ("我","wǒ","I; me",[("我是学生","wǒ shì xuésheng","I am a student"),("我们","wǒmen","we / us")]),
    ("以","yǐ","with; by; in order to",[("可以","kěyǐ","can / may"),("以后","yǐhòu","after / later")]),
    ("要","yào","to want; need; will",[("我要去","wǒ yào qù","I want to go"),("需要","xūyào","to need")]),
    ("他","tā","he; him",[("他是谁","tā shì shéi","who is he?"),("他们","tāmen","they / them")]),
    ("时","shí","time; when",[("时间","shíjiān","time"),("有时候","yǒu shíhou","sometimes")]),
    ("来","lái","to come",[("来这里","lái zhèlǐ","come here"),("进来","jìnlái","come in")]),
    ("用","yòng","to use",[("使用","shǐyòng","to use"),("有用","yǒuyòng","useful")]),
    ("们","men","plural marker (我们)",[("我们","wǒmen","we"),("你们","nǐmen","you (plural)")]),
    ("生","shēng","life; birth; raw",[("学生","xuésheng","student"),("生日","shēngrì","birthday")]),
    ("到","dào","to arrive; to",[("到了","dào le","arrived"),("做到","zuòdào","to achieve")]),
    ("作","zuò","to do; make; work",[("工作","gōngzuò","work / job"),("作业","zuòyè","homework")]),
    ("地","de / dì","adverb particle; earth",[("慢慢地","mànmàn de","slowly"),("地方","dìfāng","place")]),
    ("于","yú","in; at; to",[("关于","guānyú","about / regarding"),("于是","yúshì","therefore")]),
    ("出","chū","to go out; exit",[("出去","chūqù","go out"),("出来","chūlái","come out")]),
    ("就","jiù","then; right away; just",[("就是","jiùshì","exactly / it is"),("马上就来","mǎshàng jiù lái","coming right away")]),
    ("分","fēn / fèn","to divide; minute; part",[("五分钟","wǔ fēnzhōng","five minutes"),("十分","shífēn","very / fully")]),
    ("对","duì","correct; toward; pair",[("对不起","duìbuqǐ","sorry"),("对了","duì le","that's right")]),
    ("成","chéng","to become; succeed",[("完成","wánchéng","to complete"),("成功","chénggōng","success")]),
    ("会","huì","can; meeting; will",[("我会说中文","wǒ huì shuō Zhōngwén","I can speak Chinese"),("开会","kāihuì","hold a meeting")]),
    ("可","kě","can; may; approve",[("可以","kěyǐ","can / may"),("可能","kěnéng","maybe / possible")]),
    ("主","zhǔ","main; host; owner",[("主人","zhǔrén","host / owner"),("主要","zhǔyào","main / primary")]),
    ("发","fā / fà","to send; develop; hair",[("发现","fāxiàn","to discover"),("发展","fāzhǎn","to develop")]),
    ("年","nián","year",[("今年","jīnnián","this year"),("新年","xīnnián","New Year")]),
    ("动","dòng","to move; action",[("动物","dòngwù","animal"),("运动","yùndòng","exercise / sport")]),
    ("同","tóng","same; together",[("同学","tóngxué","classmate"),("不同","bùtóng","different")]),
    ("工","gōng","work; labor; craft",[("工作","gōngzuò","work / job"),("工人","gōngrén","worker")]),
    ("也","yě","also; too",[("我也是","wǒ yě shì","me too"),("也许","yěxǔ","perhaps")]),
    ("能","néng","can; able; energy",[("可能","kěnéng","possible"),("能力","nénglì","ability")]),
    ("下","xià","down; below; next",[("下午","xiàwǔ","afternoon"),("下面","xiàmiàn","below / underneath")]),
    ("过","guò","to pass; cross; -ed",[("过来","guòlái","come over"),("过去","guòqù","the past / go over")]),
    ("子","zi / zǐ","child; noun suffix; son",[("孩子","háizi","child"),("桌子","zhuōzi","table")]),
    ("说","shuō","to speak; say",[("说话","shuōhuà","to talk"),("听说","tīngshuō","heard that / apparently")]),
    ("你","nǐ","you",[("你好","nǐ hǎo","hello"),("谢谢你","xièxie nǐ","thank you")]),
    ("种","zhǒng / zhòng","kind; to plant",[("各种","gèzhǒng","various kinds"),("种类","zhǒnglèi","type / category")]),
    ("面","miàn","face; surface; noodles",[("面条","miàntiáo","noodles"),("前面","qiánmiàn","in front")]),
    ("而","ér","and; but; yet",[("而且","érqiě","moreover / and also"),("然而","rán'ér","however")]),
    ("方","fāng","square; direction; method",[("地方","dìfāng","place"),("方法","fāngfǎ","method")]),
    ("后","hòu","behind; after; back",[("以后","yǐhòu","after / later"),("后面","hòumiàn","behind / in back")]),
    ("多","duō","many; much",[("多少","duōshao","how much / many?"),("很多","hěnduō","a lot")]),
    ("定","dìng","to fix; decide; sure",[("一定","yīdìng","certainly / definitely"),("决定","juédìng","to decide")]),
    ("行","xíng / háng","OK; walk; profession",[("行不行","xíng bu xíng","is it okay?"),("银行","yínháng","bank")]),
    ("学","xué","to study; learning",[("学习","xuéxí","to study / learn"),("大学","dàxué","university")]),
    ("法","fǎ","law; method; way",[("方法","fāngfǎ","method"),("法律","fǎlǜ","law")]),
    ("所","suǒ","place; that which",[("所以","suǒyǐ","therefore / so"),("所有","suǒyǒu","all / everything")]),
    ("民","mín","the people; citizen",[("人民","rénmín","the people"),("民族","mínzú","ethnic group / nation")]),
    ("得","de / dé / děi","particle; obtain; must",[("觉得","juéde","to feel / think"),("得到","dédào","to obtain")]),
    ("经","jīng","classic; pass through; manage",[("经常","jīngcháng","often"),("经济","jīngjì","economy")]),
    ("十","shí","ten",[("十分","shífēn","very / completely"),("十月","shíyuè","October")]),
    ("三","sān","three",[("三月","sānyuè","March"),("三角","sānjiǎo","triangle")]),
    ("之","zhī","of; it; classical marker",[("总之","zǒngzhī","in short"),("之后","zhīhòu","afterwards")]),
    ("进","jìn","to enter; advance",[("进来","jìnlái","come in"),("进步","jìnbù","progress")]),
    ("着","zhe / zháo / zhuó","ongoing action particle",[("看着","kàn zhe","looking at"),("等着","děng zhe","waiting")]),
    ("等","děng","to wait; etc.; rank",[("等一下","děng yīxià","wait a moment"),("等等","děngdeng","wait / hold on")]),
    ("没","méi / mò","not have; drowned",[("没有","méiyǒu","don't have / no"),("没关系","méiguānxi","it's okay / never mind")]),
    ("好","hǎo / hào","good; like",[("你好","nǐ hǎo","hello"),("好吃","hǎochī","delicious")]),
    ("家","jiā","home; family",[("回家","huíjiā","go home"),("家人","jiārén","family members")]),
    ("电","diàn","electricity; electric",[("电话","diànhuà","telephone"),("电脑","diànnǎo","computer")]),
    ("力","lì","power; strength",[("努力","nǔlì","to work hard"),("力量","lìliàng","strength / power")]),
    ("里","lǐ","inside; village; li (unit)",[("里面","lǐmiàn","inside"),("这里","zhèlǐ","here")]),
    ("如","rú","like; as if; such as",[("如果","rúguǒ","if"),("如何","rúhé","how / in what way")]),
    ("水","shuǐ","water",[("水果","shuǐguǒ","fruit"),("喝水","hē shuǐ","drink water")]),
    ("化","huà","to transform; -ize",[("变化","biànhuà","change"),("文化","wénhuà","culture")]),
    ("高","gāo","tall; high",[("高中","gāozhōng","high school"),("高兴","gāoxìng","happy")]),
    ("自","zì","self; from",[("自己","zìjǐ","oneself"),("自然","zìrán","nature / natural")]),
    ("二","èr","two",[("二月","èryuè","February"),("第二","dì'èr","second")]),
    ("理","lǐ","reason; manage; texture",[("道理","dàolǐ","reason / logic"),("理解","lǐjiě","to understand")]),
    ("起","qǐ","to rise; start",[("起来","qǐlái","get up / rise"),("一起","yīqǐ","together")]),
    ("小","xiǎo","small; little",[("小心","xiǎoxīn","be careful"),("小时","xiǎoshí","hour")]),
    ("物","wù","thing; object",[("动物","dòngwù","animal"),("食物","shíwù","food")]),
    ("现","xiàn","now; appear; cash",[("现在","xiànzài","now"),("发现","fāxiàn","to discover")]),
    ("实","shí","real; solid; fruit",[("其实","qíshí","actually"),("实在","shízài","really / indeed")]),
    ("加","jiā","to add; plus",[("加油","jiāyóu","cheer up / go!"),("增加","zēngjiā","to increase")]),
    ("量","liàng","quantity; measure",[("质量","zhìliàng","quality"),("数量","shùliàng","quantity / amount")]),
    ("都","dōu / dū","all; capital city",[("都是","dōu shì","are all"),("首都","shǒudū","capital city")]),
    ("两","liǎng / liàng","two; both; tael",[("两个","liǎng gè","two (of something)"),("两次","liǎng cì","twice")]),
    ("机","jī","machine; opportunity",[("手机","shǒujī","mobile phone"),("飞机","fēijī","airplane")]),
    ("当","dāng / dàng","when; ought; pawn",[("当然","dāngrán","of course"),("当时","dāngshí","at that time")]),
    ("使","shǐ","to make; use; envoy",[("使用","shǐyòng","to use"),("大使","dàshǐ","ambassador")]),
    ("点","diǎn","point; o'clock; a little",[("一点","yīdiǎn","a little"),("三点","sān diǎn","three o'clock")]),
    ("去","qù","to go",[("去哪里","qù nǎlǐ","where are you going?"),("出去","chūqù","go out")]),
    ("本","běn","root; origin; book",[("本来","běnlái","originally"),("日本","Rìběn","Japan")]),
    ("看","kàn","to look; watch",[("看书","kàn shū","read a book"),("看看","kànkan","take a look")]),
    ("天","tiān","sky; day; heaven",[("今天","jīntiān","today"),("天气","tiānqì","weather")]),
    ("心","xīn","heart; mind",[("小心","xiǎoxīn","be careful"),("开心","kāixīn","happy")]),
]

# ── audio helpers ──────────────────────────────────────────────────────────────
def audio_filename(tag):
    """Sanitise a string into a safe filename."""
    safe = "".join(c if c.isalnum() else "_" for c in tag)
    return f"zh_{safe}.m4a"

def generate_audio(text, out_path):
    if os.path.exists(out_path):
        return
    aiff = out_path.replace(".m4a", ".aiff")
    subprocess.run(["say", "-v", VOICE, "-o", aiff, "--", text],
                   check=True, capture_output=True)
    subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", aiff, out_path],
                   check=True, capture_output=True)
    os.remove(aiff)

# ── Anki model ─────────────────────────────────────────────────────────────────
MODEL_ID = 1_947_382_910
DECK_ID  = 1_947_382_911

CSS = """
@import url('https://cdn.jsdelivr.net/npm/lxgw-wenkai-webfont@1.7.0/style.css');

.card {
  font-family: system-ui, sans-serif;
  background: #f4efe6;
  color: #1c1917;
  text-align: center;
  padding: 2rem 1.5rem;
  max-width: 480px;
  margin: 0 auto;
}

.hanzi-front {
  font-family: 'LXGW WenKai', 'Kaiti SC', 'STKaiti', 'KaiTi', serif;
  font-size: 6rem;
  line-height: 1.1;
}

.hanzi-back {
  font-family: 'LXGW WenKai', 'Kaiti SC', 'STKaiti', 'KaiTi', serif;
  font-size: 3rem;
  margin-bottom: 0.25rem;
}

.pinyin {
  font-size: 1.75rem;
  font-weight: 600;
  color: #b91c1c;
  margin-bottom: 0.35rem;
  letter-spacing: 0.04em;
}

.meaning {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.rank {
  font-size: 0.8rem;
  color: #78716c;
  margin-bottom: 1rem;
}

hr { border: none; border-top: 1px solid rgba(28,25,23,0.1); margin: 0.75rem 0; }

.examples { text-align: left; }

.ex-row {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.6rem;
}

.ex-phrase {
  font-family: 'LXGW WenKai', 'Kaiti SC', 'STKaiti', 'KaiTi', serif;
  font-size: 1.4rem;
  line-height: 1.2;
  min-width: 4rem;
}

.ex-info { display: flex; flex-direction: column; gap: 0.1rem; padding-top: 0.1rem; }
.ex-pinyin { font-size: 0.9rem; color: #b91c1c; font-weight: 600; }
.ex-meaning { font-size: 0.85rem; color: #78716c; }
"""

FRONT_TMPL = "{{FrontSide}}" # unused — using separate q/a

model = genanki.Model(
    MODEL_ID,
    "Top 100 Chinese Characters",
    fields=[
        {"name": "Hanzi"},
        {"name": "Pinyin"},
        {"name": "Meaning"},
        {"name": "Rank"},
        {"name": "Examples"},
        {"name": "CharAudio"},
        {"name": "Ex1Audio"},
        {"name": "Ex2Audio"},
    ],
    templates=[{
        "name": "Recognition",
        "qfmt": '<div class="hanzi-front">{{Hanzi}}</div>',
        "afmt": """
<div class="hanzi-back">{{Hanzi}}</div>
<div class="pinyin">{{Pinyin}}</div>
<div class="meaning">{{Meaning}}</div>
<div class="rank">{{Rank}}</div>
{{CharAudio}}
<hr>
<div class="examples">{{Examples}}</div>
{{Ex1Audio}}{{Ex2Audio}}
""",
    }],
    css=CSS,
)

anki_deck = genanki.Deck(DECK_ID, "Top 100 Chinese Characters")

# ── build notes ────────────────────────────────────────────────────────────────
media_files = []

for i, (hanzi, pinyin, meaning, examples) in enumerate(deck_data, 1):
    rank = f"#{i} of 100"

    # Determine what to speak for the main character
    # (use first example phrase as context for multi-reading characters)
    char_speak_text = examples[0][0] if "/" in pinyin else hanzi

    # Audio filenames
    char_audio_file = audio_filename(f"char_{i:03d}_{hanzi}")
    ex1_audio_file  = audio_filename(f"ex1_{i:03d}_{examples[0][0]}")
    ex2_audio_file  = audio_filename(f"ex2_{i:03d}_{examples[1][0]}")

    char_audio_path = os.path.join(AUDIO_DIR, char_audio_file)
    ex1_audio_path  = os.path.join(AUDIO_DIR, ex1_audio_file)
    ex2_audio_path  = os.path.join(AUDIO_DIR, ex2_audio_file)

    print(f"[{i:3d}/100] {hanzi}  generating audio…")
    generate_audio(char_speak_text, char_audio_path)
    generate_audio(examples[0][0], ex1_audio_path)
    generate_audio(examples[1][0], ex2_audio_path)

    media_files += [char_audio_path, ex1_audio_path, ex2_audio_path]

    # Build examples HTML
    ex_html = ""
    for phrase, ex_pin, ex_mean in examples:
        ex_html += f"""
<div class="ex-row">
  <span class="ex-phrase">{phrase}</span>
  <span class="ex-info">
    <span class="ex-pinyin">{ex_pin}</span>
    <span class="ex-meaning">{ex_mean}</span>
  </span>
</div>"""

    note = genanki.Note(
        model=model,
        fields=[
            hanzi,
            pinyin,
            meaning,
            rank,
            ex_html,
            f"[sound:{char_audio_file}]",
            f"[sound:{ex1_audio_file}]",
            f"[sound:{ex2_audio_file}]",
        ],
    )
    anki_deck.add_note(note)

# ── package ────────────────────────────────────────────────────────────────────
pkg = genanki.Package(anki_deck)
pkg.media_files = media_files
pkg.write_to_file(APKG_PATH)

print(f"\nDone! Deck written to:\n  {APKG_PATH}")
print(f"  {len(media_files)} audio files included")
