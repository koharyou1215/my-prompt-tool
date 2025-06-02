import os
import streamlit as st
import json

# プリセットデータ (前回完成したコウさんの全タグ搭載版)
PROMPT_CATEGORIES = {
    "品質・テクニカル": {
        "masterpiece": "傑作",
        "best quality": "最高品質",
        "ultra detailed": "超高精細",
        "high resolution": "高解像度",
        "8K": "8K解像度",
        "ultra-high definition": "超高精細度",
        "ultra-detailed illustration": "超精密イラスト",
        "anime style": "アニメスタイル",
        "anime screen capture": "アニメスクリーンキャプチャ",
        "sharp focus": "シャープフォーカス",
        "cinematic lighting": "映画的照明",
        "natural light": "自然光",
        "high-definition lighting": "高精細照明",
        "vivid colors": "鮮やかな色彩",
        "smooth lines": "滑らかな線",
        "perfect anatomy": "完璧な解剖学",
        "intricate fabric details": "複雑な布地ディテール",
        "dramatic shadows": "劇的な影",
        "score_9": "スコア9",
        "score_8_up": "スコア8以上",
        "score_7_up": "スコア7以上",
        "source_anime": "アニメ風(ソースアニメ)",
        "dim lighting": "薄暗い照明"
    },
    "アングル・画角": {
        "straight-on": "真正面 ★",
        "front view": "正面構図",
        "symmetrical": "左右対称構図",
        "rotational symmetry": "回転対称（キャラ注意）",
        "back view": "背後構図（横顔映る）",
        "side view": "横構図",
        "from side": "横から ★",
        "from behind": "真後ろから ★",
        "from above": "斜め上から（見下ろし） ★",
        "from below": "斜め下から（見上げ） ★",
        "from outside": "屋外から室内を見る視点",
        "low angle": "ローアングル",
        "three-quarter view": "スリークォータービュー",
        "over-the-shoulder shot": "肩越しショット",
        "vanishing point": "消失点（パース強調）",
        "dutch angle": "ダッチアングル（斜め構図）",
        "upside-down": "上下逆構図",
        "perspective": "パース（手前強調） ★",
        "foreshortening": "遠近法（縮図法）",
        "close-up": "クローズアップ",
        "dynamic angle": "ダイナミックアングル",
        "intense angle": "迫力あるアングル（アップ多し）",
        "cinematic angle": "映画的アングル",
        "full body": "全身図 ★",
        "cowboy shot": "太ももまでの構図 ★",
        "multiple views": "複数視点（同キャラ別角度） ★",
        "face": "顔メイン",
        "profile": "横顔",
        "upper body": "上半身メイン ★",
        "lower body": "下半身メイン",
        "fisheye lens": "魚眼レンズ ★",
        "POV": "主観視点 ★",
        "pov_doorway": "ドア開けた瞬間の主観視点",
        "portrait": "ポートレート（頭部～肩）",
        "head out of frame": "顔フレームアウト",
        "feet out of frame": "足フレームアウト",
        "cropped legs": "脚途中切れ ★",
        "cropped torso": "胴体途中切れ ★",
        "cropped arms": "腕途中切れ ★",
        "cropped shoulders": "肩から上（浮遊感） ★",
        "cropped head": "頭部のみ（浮遊感） ★",
        "wide shot": "ワイドショット（遠景）",
        "very wide shot": "ベリーワイドショット（背景より遠く）",
        "in the distance": "○○ in the distance（遠景指定）",
        "panorama": "パノラマ（雄大背景）",
        "overlooking panorama view": "高所からの展望風景",
        "aerial view": "空中視点（監視カメラ風）",
        "establishing shot": "状況説明ショット",
        "extreme close-up": "超クローズアップ",
        "extreme long shot": "超ロングショット",
        "extreme perspective": "超パース",
        "eye level": "アイレベル（目の高さ）"
    },
    "視線": {
        "looking at viewer": "カメラ目線",
        "looking back": "振り向く",
        "looking down": "見下ろす（うつむく）",
        "looking up": "見上げる（顔上向き）",
        "looking up at viewer": "カメラを見上げる",
        "looking down at viewer": "カメラを見下ろす",
        "eye contact": "複数キャラで見つめ合う",
        "looking afar": "遠くを見つめる",
        "looking ahead": "前方を見つめる",
        "looking away": "向こうを向く（視線逸らし）",
        "looking to the side": "横を見る",
        "looking at another": "他の人/物を見る",
        "looking at (own) breasts": "自分の胸元を見る",
        "looking at mirror": "鏡を見る",
        "looking at phone": "スマホを見る",
        "looking outside": "屋内から外を見る",
        "looking over eyewear": "メガネ越しに見る（鼻眼鏡風）",
        "adjusting eyewear": "メガネの位置を直す"
    },
    "キャラクター設定（基本・体型・肌・頭身・年齢・種族）": {
        "1 girl": "一人の少女",
        "Mithra": "ミスラ（キャラ名/種族）",
        "elf ears": "エルフの耳",
        "small anime girl": "小さなアニメの女の子",
        "boy": "少年（teen顔立ち）",
        "woman": "女性（成人風）",
        "kawaii": "可愛らしい（目が大きく幼く）",
        "mature female": "熟女・人妻",
        "milf": "色気のあるママキャラ",
        "student": "中高生",
        "years old": "〇〇years old 年齢指定",
        "loli": "ロリ（顔立ち・身体）",
        "lolibaba": "ロリババア（のじゃロリ）",
        "age_difference": "年齢差のある二人",
        "child": "子供（小学生風）",
        "feminine boy": "男の娘風の顔立ち",
        "tom girl": "おてんば娘",
        "crossdressing": "異性装",
        "maid": "メイド（メイド服）",
        "miko": "巫女",
        "nun": "修道女",
        "witch": "魔女",
        "ninja": "忍者",
        "princess": "お姫様",
        "samurai": "侍",
        "elf": "エルフ（pointy earsで耳だけも）",
        "gyaru": "ギャル",
        "fair-skinned": "色白",
        "dark skin": "褐色肌",
        "tan": "日焼け肌",
        "pale skin": "青白い肌",
        "medium breasts": "中くらいの胸",
        "large breasts": "大きな胸",
        "small breasts": "小さな胸",
        "huge breasts": "巨乳",
        "flat chest": "平らな胸（貧乳）",
        "sagging breasts": "たるんだ胸",
        "curvy body": "曲線的な体つき",
        "slim body": "細身の体",
        "petite": "小柄",
        "muscular": "筋肉質（女性）",
        "abs": "腹筋",
        "wide hips": "広い腰",
        "thick thighs": "太い太もも",
        "bare legs": "素足",
        "skinny": "痩せ体型",
        "slim waist": "細いウエスト強調",
        "potbelly": "ぽっちゃり",
        "fat": "むちっとする",
        "plump": "はっきり太い",
        "shiny skin": "光沢肌（ハイライト大） ★",
        "oily skin": "オイルっぽい光沢肌",
        "glistening skin": "テカリ感肌",
        "gleaming skin": "光る肌（自然な反射光）",
        "black skin": "黒人風の肌",
        "wet": "濡れた肌",
        "furry": "ケモ（半人半獣、全身毛皮）",
        "kemomimi": "ケモ耳（ネコ耳より長め）",
        "kemono": "獣（ジャパリパーク風）",
        "animalization": "動物化（ガチケモ風）"
    },
    "髪（長さ・色・スタイル・髪質）": {
        "long hair": "長い髪",
        "very long hair": "とても長い髪",
        "blonde hair": "金髪",
        "brown hair": "茶髪",
        "black hair": "黒髪",
        "blue hair": "青髪",
        "pink hair": "ピンク髪",
        "silver hair": "銀髪",
        "red hair": "赤髪",
        "green hair": "緑髪",
        "purple hair": "紫髪",
        "twintails": "ツインテール",
        "ponytail": "ポニーテール",
        "hime cut": "姫カット",
        "braid": "三つ編み",
        "curly hair": "カーリーヘア（癖っ毛）",
        "wavy hair": "ウェーブヘア",
        "straight hair": "ストレートヘア",
        "flipped hair": "外ハネ",
        "dreadlocks": "横髪ドレッド",
        "ahoge": "アホ毛",
        "antenna hair": "アンテナヘア",
        "comb over": "なでつけた髪",
        "hair pulled back": "ひっつめ",
        "hair slicked back": "オールバック",
        "lone nape hair": "うなじの後れ毛",
        "bow-shaped hair": "髪リボン風結い",
        "braided bangs": "前髪編む（横髪編まれる）",
        "french braid": "フレンチブレイド",
        "crown braid": "クラウンブレイド",
        "single braid": "一つ結びおさげ",
        "multiple braids": "複数編み",
        "twin braids": "２つ編み",
        "low twin braids": "低い位置で２つ編み",
        "hair bun": "お団子ヘア",
        "braided bun": "編み込みお団子",
        "single hair bun": "一つお団子",
        "double bun": "二つお団子",
        "half updo": "ハーフアップ",
        "one side up": "ワンサイドアップ",
        "two side up": "両サイドアップ",
        "low-braided long hair": "低い位置で編んだ長髪",
        "low-tied long hair": "低い位置でまとめた長髪",
        "mizura": "みずら（水色和服副作用）",
        "multi-tied hair": "複数にまとめた髪",
        "nihongami": "日本髪（和風影響）",
        "high ponytail": "高い位置ポニーテール",
        "side ponytail": "サイドポニーテール",
        "low twintails": "低い位置ツインテール",
        "drill hair": "ドリルヘア",
        "twin drills": "ツインドリル",
        "hair flaps": "ヘアフラップ（猫耳風ハネ毛）",
        "messy hair": "癖っ毛（寝起き風）",
        "pointy hair": "突き出た髪型",
        "ringlets": "縦ロール",
        "hair down": "結ばない髪（ロング化）",
        "hair up": "アップヘア",
        "asymmetrical hair": "左右非対称ヘア",
        "blunt ends": "毛先ぱっつん",
        "multicolored hair": "マルチカラーヘア",
        "colored inner hair": "インナーカラー",
        "gradient hair": "グラデーションヘア",
        "rainbow hair": "虹色の髪",
        "split-color hair": "頭頂部二色分け髪",
        "streaked hair": "部分染め髪（メッシュ風）",
        "two-tone hair": "ツートーンヘア",
        "colored tips": "毛先だけ別色"
    },
    "表情・感情・口・舌・キス・成人向け表情": {
        "smile": "笑顔",
        "laughing": "笑っている",
        "sad face": "悲しい顔",
        "crying": "泣いている",
        "tears": "涙目",
        "angry face": "怒った顔",
        "blush": "赤面",
        "embarrassed": "恥ずかしい",
        "happy": "ハッピー（嬉しい）",
        "surprised": "驚いた顔",
        "shouting": "叫んでいる顔",
        "closed eyes": "目を閉じている",
        "open mouth": "口を開けている",
        "tongue out": "舌を出す",
        "ahegao": "アヘ顔",
        "flushed face": "赤ら顔",
        "head tilt": "首をかしげる",
        "covering own mouth": "自分の口を隠す。",
        "hand to own mouth": "口元に手をやる（考え事風）。",
        "finger to mouth": "唇に指（しーっ/指さし）。",
        "teeth": "歯を見せて笑う（Sっぽく）。",
        "fang": "牙（八重歯）。",
        "skin fang": "スキンファング（口ライン八重歯）。",
        "sharp teeth": "鋭い歯（ギザギザ）。",
        "round teeth": "丸い歯（上前歯まるく）。",
        "mouth hold": "何かを咥える。",
        "upper teeth": "上の歯を見せる。",
        "tongue": "舌（tongue outより大きく）。",
        "long tongue": "長い舌（モンスター風）。",
        "stick tongue out": "舌をとがらせて出す。",
        "chestnut mouth": "栗みたいな口。",
        "dot mouth": "ドット絵風の小さい口。",
        "heart-shaped mouth": "ハート形の口。",
        "rectangular mouth": "台形の口（驚き/栗口）。",
        "sideways mouth": "横顔から見える口（漫画的）。",
        "split mouth": "口の線が繋がらない描き方。",
        "square mouth": "四角い口（（・□・）ギャグ調）。",
        "triangle mouth": "三角の口（（・△・））。",
        "wavy mouth": "波打った口（あわわ…）。",
        "mouth pull": "いーっと口をひっぱる。",
        "drink": "飲み物を飲む。",
        "eating": "食べ物を食べる。",
        "kiss": "キスする。",
        "after kiss": "キス直後のとろけた表情。",
        "blowing kiss": "投げキス。",
        "french kiss": "舌を絡ませるキス。",
        "implied kiss": "キスの暗示。",
        "imminent kiss": "キス直前。",
        "incoming kiss": "カメラに向かってキス顔。",
        "indirect kiss": "間接キス。",
        "kiss_from_behind": "背後からのキス。",
        "pocky kiss": "ポッキーキス。",
        "cigarette kiss": "タバコキス。",
        "surprise kiss": "サプライズキス。",
        "tiptoe kiss": "つま先立ちキス。",
        "fucked silly": "アヘ顔（感じすぎバカ風）。",
        "sexual ecstasy": "性的絶頂表情。",
        "in heat": "興奮した表情（自然な感じ）。",
        "naughty face": "エロティックな表情（誘う笑み）。",
        "seductive smile": "誘うような笑顔。",
        "orgasm": "絶頂（sexual ecstasy類似）。",
        "blank eyes": "白目（黒目なし）。",
        "rolling eyes": "白目むく（黒目あり）。",
        "upturned eyes": "上目遣い（目がハートも）。",
        "crazy eyes": "狂った目つき。",
        "evil smile": "悪魔の笑み（眉V字）。",
        "drunked eyes": "酔った目つき（とろん）。",
        "aroused": "興奮した表情（快感耐え）。",
        "cross-eyed": "寄り目（縮瞳）。",
        "half-closed eyes": "半分閉じた目・薄目。",
        "saliva": "唾液。",
        "saliva trail": "唾液の橋。",
        "drooling": "よだれ。",
        "afterglow": "情事後の満足表情。"
    },
    "化粧・ギャル関連": {
        "makeup": "化粧（ランダム効果）。",
        "lipstick": "リップ（口紅）。",
        "faint lips": "かすかなリップ。",
        "eyeliner": "アイライナー。",
        "mascara": "マスカラ。",
        "eyeshadow": "アイシャドー。",
        "eyelashes": "アイラッシュ。",
        "fake eyelashes": "つけまつげ。",
        "short eyebrows": "短い眉（まろ眉小）。",
        "thick eyebrows": "太眉・まろ眉。",
        "hikimayu": "引き眉。",
        "lip balm": "リップバーム（メンターム）。",
        "lipgloss": "リップグロス。",
        "rouge (makeup)": "ルージュ（目じり赤）。",
        "fancy makeup": "ファンシーな化粧。",
        "sexy makeup": "セクシーな化粧。",
        "lips": "リップ（lipgloss類似）。",
        "applying makeup": "【動】メイクする。",
        "runny makeup": "メイク流れ。",
        "ganguro": "ガングロ。",
        "kogal": "コギャル。",
        "gyaru v": "ギャルピース。",
        "amesuku gyaru": "アメリカンスクール系ギャル。",
        "jirai kei": "地雷系ファッション。",
        "tanlines": "日焼け跡。"
    },
    "体全体ポーズ（立ち・アクション系）": {
        "standing": "立っている。",
        "standing at attention": "起立ポーズ。",
        "standing on one leg": "片足立ち。",
        "contrapposto": "コントラポスト。",
        "open stance": "脚肩幅開き（オープンスタンス）。",
        "arched back": "上半身のけぞる（崩壊注意）。",
        "bent over": "前屈。",
        "leaning back": "後ろにもたれる。",
        "leaning forward": "前にもたれる（前屈覗き込み）。",
        "slouching": "前かがみ（考え事風）。",
        "twisted torso": "腰をひねる。",
        "dynamic pose": "ダイナミックポーズ。",
        "facing viewer": "カメラに顔向ける ★",
        "facing away": "顔が向こう向く（後頭部）。",
        "acrobatic pose": "アクロバティックポーズ（新体操風）。",
        "aerial": "空中浮遊ポーズ。",
        "stylish pose": "スタイリッシュポーズ。",
        "upside-down face": "顔部分上下逆。",
        "singing": "歌う。",
        "dancing": "踊る。",
        "bowing": "お辞儀。",
        "tiptoes": "つま先立ち。",
        "heel up": "かかとを上げる。",
        "reclining": "リクライニング。",
        "stretching": "ストレッチ（体伸びる）。",
        "handstand": "逆立ち。",
        "yoga": "ヨガのポーズ。",
        "horse riding": "乗馬。",
        "against wall": "壁にもたれる。",
        "hand on wall": "壁に手をつく。",
        "kabedon": "壁ドン。",
        "against glass": "ガラスにもたれる。",
        "breasts on glass": "ガラスにおっぱい押し付け。",
        "hand on glass": "ガラスに手をつく。"
    },
    "座る・寝る・這うポーズ": {
        "sit": "座る。",
        "on side": "横向き寝・横座り。",
        "squatting": "しゃがむ（エロ蹲踞多し）。",
        "lying": "寝そべる。",
        "lie on your side": "添い寝風横寝。",
        "lie flat": "横になる（ベッド頭下多し）。",
        "on stomach": "うつ伏せ（状態起き）。",
        "prone": "うつ伏せ（寝てclowling近い）。",
        "the_pose": "うつ伏せ膝曲げ足ゆらゆら。",
        "on back": "仰向け。",
        "knees up": "体育座り。",
        "indian style": "あぐら。",
        "prostrate": "うつ伏せ（尻上下）。",
        "prostration": "土下座。",
        "butterfly sitting": "ちょうちょ座り。",
        "figure four sitting": "片足上げ椅子座り。",
        "seiza": "正座。",
        "wariza": "ぺたんこ座り。",
        "yokozuwari": "女座り・横座り。",
        "fetal position": "胎児ポーズ。",
        "sleepy": "眠そう（寝る）。",
        "kneeling": "ひざまずく。",
        "superhero landing": "ヒーロー着地。",
        "all fours": "四つん這い。",
        "crawling": "這いまわる。",
        "couple sitting": "カップル座り。"
    },
    "手・指・腕のポーズ／持つ・抱く・掴む": {
        "holding phone": "スマホを持つ。",
        "holding removed eyewear": "外した眼鏡を持つ。",
        "holding hand": "手を握る。",
        "holding another's wrist": "相手の手首を握る。",
        "group hug": "グループハグ。",
        "hug from behind": "後ろから抱きしめる。",
        "imminent hug": "抱きしめようとする。",
        "hug self": "自分を抱きしめる。",
        "incoming hug": "カメラに手を広げ抱きしめる。",
        "mutual hug": "二人で正面から抱きしめ合う。",
        "waist hug": "相手の腰に抱きつく。",
        "arm hug": "相手の腕に抱きつく。",
        "hugging another's leg": "相手の脚に抱きつく。",
        "hugging own legs": "自分の脚を抱える（体育座り）。",
        "arm grab": "腕をつかむ。",
        "ankle grab": "足首をつかむ。",
        "ass grab": "お尻をつかむ。",
        "grabbing another's breast": "相手の胸を揉む。",
        "guided breast grab": "胸を揉ませる。",
        "grabbing another's ear": "相手の耳をつかむ。",
        "face grab": "顔をつかむ。",
        "grabbing another's ass": "相手のお尻をつかむ。",
        "grabbing another's chin": "相手のあごをつかむ。",
        "grabbing another's foot": "相手の足をつかむ。",
        "grabbing another's hair": "相手の髪をつかむ。",
        "grabbing another's hand": "相手の手を握る。",
        "clothes grab": "服をつかむ。",
        "curtain grab": "カーテンをつかむ。",
        "collar grab": "首輪をつかむ。",
        "necktie grab": "ネクタイをつかむ。",
        "sheet grab": "シーツをつかむ。",
        "hand on own ear": "耳に手をやる。",
        "hand on another's head": "相手の頭に手を置く。",
        "hand on own head": "頭に手をやる。",
        "hand on own forehead": "額に手をやる。",
        "hand on another's face": "相手の顔に手を添える。",
        "hand on own face": "顔に手をやる（頬杖風）。",
        "hand on another's cheek": "相手の頬に手を添える。",
        "hand on own cheek": "頬に手をやる（頬杖風）。",
        "hand on headwear": "帽子を押さえる。",
        "hands on upper body": "胸元に手を置く。",
        "hand on own ass": "お尻に手をやる。",
        "hands on own hips": "腰に手を置く。",
        "hands on own knees": "膝に手を置く。",
        "hand between legs": "足の間に手を挟む。",
        "hands in pockets": "ポケットに手を入れる。",
        "handshake": "握手。",
        "hands together": "自分の手を合わせる（お祈り）。",
        "interlocked fingers": "恋人つなぎ。",
        "own hands clasped": "自分の手を握る（西洋風お祈り）。",
        "open hand": "開いた手。",
        "clenched hand": "握った手（こぶし）。",
        "raised fist": "こぶしを突き上げる。",
        "beckoning": "手招きする。",
        "hair twirling": "髪をいじる。",
        "reaching": "手を伸ばす（片手）。",
        "reaching towards viewer": "カメラに手を伸ばす（両手）。",
        "point at viewer": "カメラに指さす。",
        "between fingers": "〇〇 between fingers 指挟む。",
        "peace sign": "ピースサイン。",
        "thumbs up": "サムズアップ。",
        "hidden hands": "手で何かを隠す。",
        "detailed fingers": "詳細な指。",
        "shushing": "シーッ（唇に人差し指）。",
        "put index finger on mouth": "人差し指を口に当てる。",
        "put up index finger": "人差し指を立てる。",
        "arm support": "腕で体重支える。",
        "arms at sides": "両腕を自然に下ろす。",
        "arms raised in the air": "両手を空にバンザイ。",
        "arms behind back": "後ろ手。",
        "arms behind head": "頭の後ろで腕組む。",
        "headpat": "頭を撫でる。",
        "paw pose": "猫の手ポーズ。",
        "claw pose": "爪を立てるポーズ。",
        "open arms for viewer": "腕を広げ「抱っこして」。",
        "waving at viewer": "カメラに手を振る。",
        "salute": "敬礼。",
        "two-finger salute": "二本指敬礼（よっ）。",
        "spread arms": "両手を広げる。",
        "outstretched arms": "真横に両手広げる。",
        "crossed arms": "腕を組む。",
        "covering chest by hand": "手で胸を隠す。",
        "leaning on person": "相手にしなだれかかる。",
        "curtsey": "カーテシー（英国風挨拶）。",
        "shrugging": "肩をすくめる。",
        "v arms": "足間に両手挟む（可愛い）。",
        "w arms": "両手を上げる（わーい）。",
        "carry me": "小さい子を抱きかかえる。",
        "cupping hands": "手をお皿のようにする。",
        "double finger gun": "二丁拳銃ポーズ。",
        "fidgeting": "もじもじする。",
        "finger counting": "指で数える。",
        "finger frame": "指で四角作る。",
        "fist bump": "拳ぶつけ合う。",
        "heart hands": "両手でハート。",
        "heart hands duo": "二人でハート。",
        "heart hands trio": "三人でハート。",
        "high five": "ハイタッチ。",
        "horns pose": "つのポーズ。",
        "penetration gesture": "OKサインに指入れる。",
        "rabbit pose": "うさぎポーズ。",
        "shadow puppet": "影絵ポーズ（きつね）。",
        "steepled fingers": "両手指先合わせる。",
        "x arms": "手でバッテン。",
        "x fingers": "指でバッテン。"
    },
    "脚ポーズ": {
        "spread legs": "股を広げる（nsfw寄り）。",
        "legs apart": "立った状態で足を開く。",
        "legs together": "脚をそろえる。",
        "crossed legs": "脚を組む/交差させる。",
        "toe-point": "つま先をこちらに向ける。",
        "leg up": "片足を上げる。",
        "legs up": "両足を上にあげる。",
        "knees to chest": "体育座り風に膝抱える。",
        "leg lift": "開脚足上げ手で支える。",
        "trampling": "踏みつける。",
        "outstretched leg": "足カメラ手前に見切れる。",
        "standing split": "I字開脚。",
        "knees together feet apart": "膝つけ足先離す。",
        "pigeon-toed": "内股立ち。",
        "plantar flexion": "足の甲を伸ばす。"
    },
    "服装（一般・学生服・職業制服・コスプレ・スポーツ）": {
        "shirt": "シャツ",
        "collared shirt": "襟付きシャツ",
        "dress shirt": "ドレスシャツ",
        "t-shirt": "Tシャツ",
        "sweater": "セーター",
        "turtleneck sweater": "タートルネックセーター",
        "hoodie": "パーカー",
        "jacket": "ジャケット",
        "coat": "コート",
        "jeans": "ジーンズ",
        "pants": "パンツ（ズボン）",
        "shorts": "ショートパンツ",
        "short shorts": "ショートショーツ（ホットパンツ）",
        "skirt": "スカート",
        "flare skirt": "フレアスカート",
        "pleated skirt": "プリーツスカート",
        "layered skirt": "レイヤードスカート",
        "frilled skirt": "フリルスカート",
        "mini skirt": "ミニスカート",
        "micro mini skirt": "マイクロミニスカート",
        "pencil skirt": "ペンシルスカート",
        "A-line skirt": "Aラインスカート",
        "lace skirt": "レーススカート",
        "dress": "ドレス",
        "cardigan": "カーディガン",
        "tracksuit": "ジャージ上下",
        "school uniform": "学生服",
        "school uniform, collared shirt": "学生服（襟付きシャツ）",
        "school uniform, pleated skirt": "学生服（プリーツスカート）",
        "school uniform, blazer": "学生服（ブレザー）",
        "serafuku": "セーラー服",
        "serafuku, summer": "セーラー服（夏）",
        "serafuku, winter": "セーラー服（冬）",
        "school uniform, vest": "学生服とベスト",
        "school uniform, beige vest": "学生服とベージュベスト",
        "school gym uniform": "学校の体操服",
        "white gym uniform": "白い体操服",
        "gym uniform, shorts": "体操服（ショートパンツ）",
        "gym uniform, buruma": "体操服（ブルマ）",
        "school swimsuit": "スクール水着",
        "office lady uniform": "OL制服",
        "business suit": "ビジネススーツ",
        "office staff suit": "OLスーツ",
        "office worker": "OL（職業）",
        "female office worker": "女性会社員（職業）",
        "secretary": "秘書（職業）",
        "suit": "スーツ（職業）",
        "lab coat": "白衣（研究者等）",
        "doctor": "医師（職業）",
        "doctor coat": "ドクターコート",
        "nurse": "看護師（職業）",
        "white nurse": "白衣の看護師",
        "pink nurse": "ピンクのナース服",
        "teacher": "教師（職業）",
        "school teacher": "学校の先生（職業）",
        "police officer": "警察官（職業）",
        "police uniform": "警察官の制服",
        "military uniform": "軍服",
        "waitress": "ウェイトレス（職業）",
        "flight attendant": "客室乗務員（職業）",
        "undertaker": "葬儀屋（職業）",
        "maid outfit": "メイド服",
        "maid headdress": "メイドカチューシャ",
        "frill apron": "フリルエプロン",
        "french maid": "フレンチメイド",
        "idol costume": "アイドル衣装",
        "fantasy costume": "ファンタジー衣装",
        "magical girl costume": "魔法少女コスチューム",
        "blue magical girl costume": "青い魔法少女コスチューム",
        "wedding dress": "ウェディングドレス",
        "bunny girl suit": "バニーガールスーツ",
        "race queen costume": "レースクイーンコスチューム",
        "santa costume": "サンタクロース衣装",
        "sportswear": "スポーツウェア",
        "tennis wear": "テニスウェア",
        "tennis player": "テニスプレイヤー",
        "volleyball wear": "バレーボールウェア",
        "volleyball player": "バレーボールプレイヤー",
        "marathon wear": "マラソンウェア",
        "marathon runner": "マラソンランナー",
        "marathon wear, shorts": "マラソンウェア（ショーツ）",
        "cheerleader": "チアリーダー（役割/服装）",
        "cheerleader uniform": "チアリーダーユニフォーム",
        "cheerleader, frilled skirt": "チアリーダー（フリルスカート）",
        "cheerleader, separate": "チアリーダー（セパレート）",
        "figure skater": "フィギュアスケート選手",
        "figure skating costume": "フィギュアスケート衣装",
        "blouse": "ブラウス",
        "competition swimsuit": "競泳水着",
        "formal": "正装",
        "off-shoulder sweater": "肩出しセーター",
        "bag": "バッグ",
        "leotard": "レオタード",
        "chinese clothes": "チャイナ服",
        "collar": "首輪（SM風/動物風）",
        "buruma": "ブルマ",
        "red leather backpack": "ランドセル",
        "bunny girl": "バニーガール"
    },
    "下着・ナイトウェア・H衣装": {
        "lingerie": "ランジェリー",
        "bra": "ブラジャー",
        "panties": "パンティ",
        "thong": "ソング（Tバック）",
        "bikini": "ビキニ（水着/下着）",
        "micro bikini": "マイクロビキニ",
        "negligee": "ネグリジェ",
        "nightgown": "ナイトガウン",
        "pajamas": "パジャマ",
        "babydoll": "ベビードール",
        "bloomers (underwear)": "ブルーマーズ（下着風）",
        "fundoshi": "ふんどし",
        "embroidery": "刺繍（下着など）",
        "lace": "レース（下着など）",
        "lace-trimmed_bra": "レースつきブラ",
        "lace-trimmed_panty": "レースつきパンティ",
        "bustier": "ビスチェ",
        "camisole": "キャミソール",
        "fishnets": "網タイツ・網衣装",
        "garter straps": "ガーターストラップ",
        "garter belt": "ガーターベルト",
        "pantyhose": "パンスト",
        "panties under pantyhose": "パンスト下透けパンツ",
        "side-tie bikini bottom": "紐パン水着",
        "bondage outfit": "ボンデージ衣装",
        "nipple chain": "乳首チェーン",
        "gag": "さるぐつわ",
        "ball gag": "ボールギャグ",
        "tape gag": "口ガムテープ",
        "gag harness": "ギャグハーネス",
        "gimp suit": "ボンデージスーツ",
        "leash": "首紐・リード",
        "clitoris leash": "クリトリスリード",
        "rope": "麻縄（縛り）",
        "crotch rope": "股縄",
        "spreader bar": "強制開脚器",
        "riding crop": "乗馬用むち"
    },
    "衣装状態・着こなし・露出": {
        "open shirt": "開いたシャツ",
        "open clothes": "はだけた服",
        "torn clothes": "破れた服 ★",
        "wet clothes": "濡れた服",
        "see-through": "透けている服",
        "sheer fabric": "薄い生地の服",
        "damaged clothes": "傷ついた服",
        "ripped jeans": "破れたジーンズ",
        "off_shoulder": "オフショルダー",
        "shirt tucked in": "シャツをイン",
        "shirt untucked": "シャツを出す",
        "bare shoulders": "肩出し",
        "cleavage": "胸の谷間 ★",
        "exposed thighs and stomach": "太ももとお腹露出",
        "adjusting clothes": "ずれた服を直す。",
        "aside": "〇〇 aside 衣服ずらし",
        "pull": "〇〇 pull 衣服引っ張る",
        "grab": "〇〇 grab 衣服つかむ",
        "open": "〇〇 open 衣服前開き",
        "lift": "〇〇 lift 衣服持ち上げ",
        "tug": "〇〇 tug 服つかみ押し下げ",
        "down": "〇〇 down 服下げる",
        "wringing": "wringing〇〇 濡れ服しぼる",
        "covering privates": "局部隠す",
        "revealing clothes": "露出度の高い服",
        "see-through sleeves": "透け袖",
        "see-through shirt": "透けシャツ",
        "see-through cleavage": "透け谷間",
        "see-through dress": "透けドレス",
        "see-through legwear": "透けストッキング等",
        "see-through leotard": "透けレオタード",
        "see-through skirt": "透けスカート",
        "unbuttoned": "ボタン外す",
        "undressing": "【動】脱衣",
        "unfastened": "（縛った物）ほどく",
        "untied": "（結んだ物）ほどく",
        "unzipped": "ジッパー開けた服",
        "unzipping": "【動】ジッパー開ける",
        "strap pull": "ストラップ引っ張る",
        "strap slip": "ストラップ肩から落ちる",
        "armpits": "脇見せ",
        "shoulder cutout": "肩露出服",
        "sleeves rolled up": "袖まくり",
        "sleeveless": "ノースリーブ",
        "low-cut armhole": "腕繰り大きいノースリーブ風",
        "center opening": "胸～へそ露出服",
        "open collar": "開襟",
        "jacket, open": "ジャケット前開き",
        "shirt slip": "シャツ片方ずり落ち",
        "breastless clothes": "胸露出服",
        "breast out": "胸出し服",
        "bra lift": "ブラ上げて見せる",
        "no pant": "ノーパン",
        "no bra": "ノーブラ",
        "bra pull": "ブラ引っ張る",
        "topless": "トップレス",
        "cleavage cutout": "胸の谷間カット服",
        "sideboob": "横乳",
        "underboob": "下乳",
        "underboob cutout": "下乳カット服",
        "nippleless clothes": "乳首露出デザイン服",
        "nipples (visible)": "乳首見える",
        "back cutout": "背中開きデザイン",
        "backless outfit": "背中ほぼなし衣装",
        "midriff": "へそ出し ★",
        "sideless outfit": "横乳見せ衣装",
        "downblouse": "ブラウス下げ（半脱ぎ）",
        "hip vent": "袴腰帯脇隙間（春麗風）",
        "side slit": "サイドスリット（太もも露出）",
        "zettai ryouiki": "絶対領域 ★",
        "bottomless": "下半身何もなし",
        "skirt around one leg": "脱ぎかけスカート（片足）",
        "panty around one leg": "脱ぎかけパンツ（片足）",
        "skirt around ankles": "全脱ぎスカート（くるぶし周り）",
        "underwear only": "下着のみ",
        "taut shirt": "はちきれそうシャツ",
        "shirt partially tucked in": "部分タックイン",
        "tented shirt": "乳テント",
        "button gap": "パツパツボタン隙間チラ見え",
        "short sleeves": "半袖",
        "long sleeves": "長袖",
        "sleeves past wrists": "萌え袖（指先出る）",
        "sleeves past fingers": "余り袖（指先も隠れる）",
        "completely nude": "全裸",
        "half undress": "半脱ぎ"
    },
    "アクセサリー・靴・装飾品": {
        "hat": "帽子",
        "cap": "キャップ",
        "beret": "ベレー帽",
        "sun visor": "サンバイザー",
        "glasses": "メガネ",
        "sunglasses": "サングラス",
        "necklace": "ネックレス",
        "choker": "チョーカー",
        "earrings": "イヤリング/ピアス",
        "ring": "指輪",
        "bracelet": "ブレスレット",
        "gloves": "手袋",
        "belt (accessory)": "ベルト（装飾）",
        "scarf": "スカーフ",
        "navy scarf": "紺色スカーフ",
        "red scarf": "赤色スカーフ",
        "bow (accessory)": "リボン（アクセ）",
        "hair ribbon": "髪リボン",
        "tie": "ネクタイ",
        "bowtie": "蝶ネクタイ",
        "wings": "羽",
        "angel wings": "天使の羽",
        "devil wings": "悪魔の羽",
        "angel halo": "天使の輪",
        "devil horns": "悪魔の角",
        "animal ears": "動物の耳",
        "tail": "尻尾",
        "shoes": "靴",
        "sneakers": "スニーカー",
        "boots": "ブーツ",
        "western boots": "ウエスタンブーツ",
        "high heels": "ハイヒール",
        "loafers": "ローファー",
        "sandals": "サンダル",
        "slippers": "スリッパ",
        "socks": "靴下",
        "short socks": "短い靴下",
        "high socks": "ハイソックス",
        "long slouchy socks": "長いルーズソックス",
        "knee-high socks": "ニーハイソックス",
        "thighhighs": "サイハイソックス",
        "black pantyhose": "黒パンスト", # "pantyhose" もあるので、どちらか、または説明を工夫
        "fishnet tights": "網タイツ",
        "mask (face)": "マスク（顔）",
        "blindfold": "目隠し（一般）",
        "no eyewear": "裸眼",
        "removing eyewear": "眼鏡外す/ずらす",
        "piercing": "ピアス",
        "thighlet": "太ももアクセ",
        "pasties": "ニップレス",
        "frills": "フリル（衣装装飾）",
        "fur trimmed": "fur trimmed〇〇 ファー付き",
        "gathers": "ギャザー（肩ひだ飾り）",
        "gold trimmed": "gold trimmed〇〇 金縁取り",
        "lace trimmed": "lace trimmed〇〇 レース装飾",
        "ribbon trimmed": "ribbon trimmed〇〇 リボン装飾"
    },
    "NSFW（体位・玩具・性癖・その他）": {
        "nsfw": "NSFW（職場閲覧注意）",
        "obscene scenario": "わいせつなシナリオ",
        "BDSM": "BDSM",
        "bondage": "拘束",
        "shibari": "緊縛（日本式）",
        # "ropes": "ロープ（拘束具）", # "rope" で統一
        # "chains": "鎖（拘束具）", # "chain" で統一
        "star-shaped restraint": "星型拘束",
        "slime": "スライム",
        "slime tentacles": "スライム触手",
        "tentacles": "触手",
        "tentacles grabbing": "掴む触手",
        "prison clothes": "囚人服",
        "breast hold": "胸抱え（性的）",
        "ass focus": "尻に焦点",
        "upskirt": "スカートの中（アングル）",
        "missionary": "正常位",
        "cowgirl position": "騎乗位",
        "sex from behind": "バック",
        "doggystyle": "ドギースタイル",
        "top-down bottom-up": "トップダウンボトムアップ",
        "prone bone": "寝バック",
        "legs over head": "まんぐり返し",
        "full nelson": "フルネルソン体位",
        "mating press": "種付けプレス",
        "recumbent position": "臥位",
        "reverse cowgirl position": "逆騎乗位",
        "upright straddle": "対面座位",
        "suspended congress": "駅弁",
        "69": "シックスナイン",
        "amazon position": "アマゾン体位",
        "anvil position": "アンヴィル体位",
        "butt plug": "アナルプラグ",
        "dildo": "ディルドー",
        "double dildo": "双頭ディルドー",
        "dildo riding": "ディルドー騎乗",
        "prostate massager": "電マ（hitachi推奨）",
        "pump": "吸引機",
        "too many sex toys": "玩具にうずもれる",
        "vibrator": "バイブレータ",
        "hitachi magic wand": "日立マジックワンド",
        "remote control vibrator": "リモコンバイブ",
        "public vibrator": "公然バイブ",
        "vibrator under clothes": "服の下バイブ",
        "vibrator in leg garter": "足ガーターにバイブ",
        "vibrator in thighhighs": "サイハイにバイブ",
        "lotion": "ローション",
        "cheating (relationship)": "不倫",
        "interracial": "異人種間H",
        "rape": "強姦表現",
        "implied_sex": "SEX示唆",
        "under table": "テーブルの下プレイ",
        "group sex": "グループセックス",
        "gangbang": "輪姦",
        "female pervert": "痴女",
        "fake phone screenshot": "スマホ画面風自撮り",
        "lipstick ring": "ペニスに口紅痕",
        "peeping": "覗き",
        "livestream": "ライブストリーミング風",
        "hypnosis": "催眠効果",
        "heart-shaped pupils": "ハート目（催眠）",
        "empty eyes": "虚ろ目（催眠）",
        "expressionless": "無表情（催眠）",
        "corruption": "悪堕ち",
        "pink growing eyes": "ピンクに輝く瞳（催眠）",
        "pendulum": "ペンデュラム（催眠用振り子）",
        "spoken_question_mark": "「？」空中浮遊（催眠混乱）",
        "sweat": "汗ばんだ肌",
        "love juice": "愛液",
        "pussy juice stain": "愛液の染み",
        "steam": "吐息表現",
        "heavy breathing": "息切れ",
        "trembling": "ビクビク震える",
        "motion lines": "びくびく線",
        "public indecency": "露出プレイ",
        "mirror,smartphone": "鏡越しスマホ自撮り",
        "paizuri": "パイズリ",
        "cooperative paizuri": "協力パイズリ",
        "handsfree paizuri": "手放しパイズリ",
        "paizuri over clothes": "着衣パイズリ（服の上）",
        "paizuri under clothes": "着衣パイズリ（服の下）",
        "stealth paizuri": "隠れパイズリ",
        "straddling paizuri": "騎乗パイズリ",
        "thigh sex": "太ももズリ",
        "nipple tweak": "乳首いじり",
        "masturbation": "オナニー",
        "clothed masturbation": "着衣オナニー",
        "crotch rub": "股ズリ",
        "table humping": "机の角オナニー",
        "female masturbation": "女性オナニー",
        "mutual masturbation": "相互オナニー",
        "facesitting": "顔面騎乗",
        "fingering": "性器いじり",
        "anal fingering": "アナルいじり",
        "prostate milking": "搾乳（おっぱいから）",
        "fingering through clothes": "服の上からいじる",
        "fingering through panties": "パンツの上からいじる",
        "presenting": "H準備ポーズ",
        "M legs": "M字開脚",
        "V legs": "V字開脚",
        "pussy": "女性器見せ（vagina）",
        "spread own pussy": "くぱぁ（自分で広げる）",
        "anal": "アナル見せ（anus）",
        "groping": "愛撫（痴漢寄り）",
        "crotch grab": "股つかむ",
        "grabbing own breast": "自分でおっぱい掴む"
    },
    "戦闘・魔法": {
        "fighting stance": "ファイティングポーズ。",
        "sword guard stance": "刀構えポーズ。",
        "duel": "決闘（エフェクト）。",
        "clash": "クラッシュ（ヒットスパーク）。",
        "sparks": "スパーク（光弾ける）。",
        "fighting": "戦う（肉弾戦多し）。",
        "punching": "殴る・パンチ。",
        "kicking": "蹴る・キック。",
        "high kick": "ハイキック。",
        "wrestling": "レスリング（寝技多し）。",
        "slashing": "武器で切る（エフェクト）。",
        "holding weapon": "武器を持つ。",
        "rapid punches": "無数パンチ（北斗百裂拳風）。",
        "catfight": "キャットファイト（女子喧嘩）。",
        "pillow fight": "枕投げ。",
        "snowball fight": "雪合戦。",
        "magic": "魔法（光の玉多し）。",
        "energy": "エネルギー（オーラ風）。",
        "magic circle": "魔法陣（背景）。",
        "electrokinesis": "電気魔法。",
        "aura": "オーラ（体から光）。",
        "telekinesis": "テレキネシス（念動力）。",
        "levitation": "浮遊魔法（舞空術）。",
        "psychic": "サイキック（超能力）。",
        "floating clothes": "服が浮かぶ（魔法影響）。",
        "floating object": "物体浮遊。"
    },
    "背景・場所": {
        "indoors": "室内",
        "outdoors": "屋外",
        "room": "部屋",
        "bedroom": "寝室",
        "living room": "リビングルーム",
        "kitchen": "キッチン",
        "bathroom": "浴室",
        "school": "学校",
        "classroom": "教室",
        "gymnasium": "体育館",
        "rooftop": "屋上",
        "cityscape": "街並み",
        "street": "通り",
        "park": "公園",
        "forest": "森",
        "beach": "ビーチ",
        "ocean": "海",
        "mountains": "山",
        "sky": "空",
        "night sky": "夜空",
        "ruins": "廃墟",
        "dungeon": "ダンジョン",
        "dungeon wall": "ダンジョンの壁",
        "church": "教会",
        "stained glass": "ステンドグラス",
        "hot spring": "温泉",
        "shrine": "神社",
        "temple": "寺",
        "cafe": "カフェ",
        "library": "図書館",
        "bed": "ベッド",
        "pillow": "枕",
        "bed sheet": "シーツ",
        "sofa": "ソファ",
        "chair": "椅子",
        "table": "テーブル",
        "desk": "机",
        "window": "窓",
        "door": "ドア",
        "bathtub": "浴槽",
        "tile floor": "タイル床",
        "underground torture room": "地下拷問部屋",
        "prison": "牢獄",
        "room with Christmas tree": "クリスマスツリーのある部屋",
        "scenery": "美しい風景。",
        "scenic view": "美しい風景。",
        "magnificent view": "壮大な風景。"
    }
}

# 以降の Streamlit UIコードは変更なし (def save_presets から最後まで)
def save_presets(data):
    os.makedirs("presets", exist_ok=True)
    with open("presets/image_presets.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_presets():
    # PROMPT_CATEGORIES を確実にコピーして使う
    initial_categories = {k: v.copy() for k, v in PROMPT_CATEGORIES.items()}
    if os.path.exists("presets/image_presets.json"):
        with open("presets/image_presets.json", "r", encoding="utf-8") as f:
            try:
                loaded_data = json.load(f)
                # ここで initial_categories と loaded_data をマージするロジックも検討可能
                # 例えば、キーが重複する場合は loaded_data を優先するなど
                # 今回はシンプルに、ロードできたらそれを使う
                return loaded_data
            except json.JSONDecodeError:
                save_presets(initial_categories) 
                return initial_categories
    save_presets(initial_categories)
    return initial_categories

# --- UI設定 ---
st.set_page_config(layout="wide")
st.title("🎨 画像生成プロンプト生成ツール Ver.Complete (コウさん全タグ最終版！)")

# --- 初期化とデータロード ---
if 'categories_data' not in st.session_state:
    st.session_state.categories_data = load_presets()

# categories_data が辞書であることを保証 (古い形式のjsonを読み込んだ場合対策)
if not isinstance(st.session_state.categories_data, dict):
    st.warning("プリセットデータの形式が正しくありません。デフォルトデータで初期化します。")
    st.session_state.categories_data = {k: v.copy() for k, v in PROMPT_CATEGORIES.items()}
    save_presets(st.session_state.categories_data)


# --- 検索機能 ---
search_query = st.sidebar.text_input("全プリセット内を検索 ✨", key="main_search_query", placeholder="キーワードを入力...")

# categories は常に session_state から取得し、それを元にフィルタリング
master_categories_data = st.session_state.categories_data
categories_to_render = {} # 検索結果で実際に表示するカテゴリと項目

if search_query:
    search_query_lower = search_query.lower()
    for cat_name, presets in master_categories_data.items():
        # カテゴリ名自体がヒットするかどうか
        category_name_matches_search = search_query_lower in cat_name.lower()
        
        # カテゴリ内のプリセットを検索
        matching_presets_in_cat = {
            en_key: ja_desc for en_key, ja_desc in presets.items()
            if search_query_lower in en_key.lower() or search_query_lower in ja_desc.lower()
        }
        
        if category_name_matches_search or matching_presets_in_cat:
            # カテゴリ名がヒットした場合はそのカテゴリの全項目を表示
            # そうでなく、カテゴリ内の項目のみヒットした場合は、ヒットした項目のみ表示
            categories_to_render[cat_name] = presets if category_name_matches_search else matching_presets_in_cat
    
    if not categories_to_render:
        st.sidebar.caption("検索結果がありません。")
else:
    categories_to_render = master_categories_data
# --- 検索機能ここまで ---


st.sidebar.header("🔧 設定")

# 表示するカテゴリの選択肢 (検索結果で絞られたもの)
category_options_for_selector = list(categories_to_render.keys())

# session_state に保存されている選択カテゴリを、現在表示可能なカテゴリでフィルタリング
if 'selected_category_names_complete' not in st.session_state:
    st.session_state.selected_category_names_complete = category_options_for_selector # 初回は全て
else:
    st.session_state.selected_category_names_complete = [
        name for name in st.session_state.selected_category_names_complete if name in category_options_for_selector
    ]
    # フィルタの結果、選択が空になったが、選択肢自体はある場合は、表示可能なものを全部選択
    if not st.session_state.selected_category_names_complete and category_options_for_selector:
        st.session_state.selected_category_names_complete = category_options_for_selector


selected_category_names_display = st.sidebar.multiselect(
    "表示するカテゴリを選択", # ラベル変更
    options=category_options_for_selector, # 検索で絞られたカテゴリリスト
    default=st.session_state.selected_category_names_complete,
    key="category_selector_displayed" 
)
# マルチセレクトの選択状態を session_state に保存
st.session_state.selected_category_names_complete = selected_category_names_display


cols_num = st.sidebar.number_input("表示カラム数", min_value=1, max_value=10, value=4, key="column_selector_complete")
cols = st.columns(cols_num)
generated_prompt_parts = []

if 'category_selections_complete' not in st.session_state:
    st.session_state.category_selections_complete = {}

# メイン表示エリアのループ (st.session_state.selected_category_names_complete を使う)
# ただし、各カテゴリ内の項目は categories_to_render から取得する
for i, category_name in enumerate(st.session_state.selected_category_names_complete):
    if category_name in categories_to_render: # 選択されたカテゴリが、検索結果として表示すべきカテゴリに含まれているか
        with cols[i % cols_num]:
            st.subheader(f"🔖 {category_name}")
            
            # このカテゴリで表示すべきプリセットを取得 (検索結果で絞り込まれている可能性がある)
            presets_in_this_category_to_display = categories_to_render[category_name]
            options_in_category_display = list(presets_in_this_category_to_display.keys())
            
            # 前回の選択を復元 (このカテゴリ、この検索結果の中で有効なものだけ)
            default_selection_for_this_multiselect = []
            if category_name in st.session_state.category_selections_complete:
                default_selection_for_this_multiselect = [
                    opt for opt in st.session_state.category_selections_complete[category_name] 
                    if opt in options_in_category_display # 現在表示可能な選択肢に含まれるものだけ
                ]
            
            selected_options = st.multiselect(
                f"{category_name} から選択",
                options=options_in_category_display, 
                default=default_selection_for_this_multiselect,
                format_func=lambda x: f"{presets_in_this_category_to_display.get(x, x)} ({x})",
                key=f"multiselect_main_{category_name.replace(' ', '_').replace('・', '_').replace('(', '_').replace(')', '_').replace('/', '_')}_complete" 
            )
            generated_prompt_parts.extend(selected_options)
            st.session_state.category_selections_complete[category_name] = selected_options

st.subheader("✏️ カスタムプロンプト")
custom_prompt_input = st.text_area("自由記述欄（カンマ区切りで入力）", key="custom_prompt_text_area_complete")

if st.button("🛠️ プロンプト生成", key="generate_prompt_button_complete"):
    final_generated_prompt = ", ".join(filter(None, generated_prompt_parts))
    
    if custom_prompt_input:
        custom_parts = [p.strip() for p in custom_prompt_input.split(',') if p.strip()]
        if final_generated_prompt and custom_parts:
            final_generated_prompt += ", " + ", ".join(custom_parts)
        elif custom_parts:
            final_generated_prompt = ", ".join(custom_parts)
            
    st.subheader("🎯 生成されたプロンプト")
    st.code(final_generated_prompt, language="text")
    st.text_area("コピー用", final_generated_prompt, height=100, key="copy_area_generated_prompt_complete")

st.sidebar.header("💾 プリセット管理")
# categories_for_management は常にマスターデータを使う
categories_for_management = master_categories_data 

with st.sidebar.expander("新規プリセット追加/編集/削除"):
    edit_category_options = ["新しいカテゴリを作成"] + list(categories_for_management.keys())
    edit_category_name_selected = st.selectbox(
        "編集/追加先のカテゴリ名", 
        options=edit_category_options, 
        key="edit_cat_name_select_complete_manage",
        index=0 
    )
    
    actual_new_category_name = edit_category_name_selected
    if edit_category_name_selected == "新しいカテゴリを作成":
        actual_new_category_name = st.text_input("新しいカテゴリの実際の名前 (日本語)", key="actual_new_cat_name_input_complete_manage")

    new_preset_key = st.text_input("プリセットの英語キー", key="new_preset_key_input_complete_manage")
    new_preset_value_ja = st.text_input("プリセットの日本語訳", key="new_preset_value_ja_complete_manage")

    if st.button("プリセットを追加/更新", key="add_update_preset_button_complete_manage"):
        if actual_new_category_name and new_preset_key:
            # カテゴリリストの参照を categories_for_management (つまり master_categories_data) にする
            if edit_category_name_selected == "新しいカテゴリを作成":
                if not actual_new_category_name.strip():
                    st.error("新しいカテゴリ名が空です。入力してください。")
                elif actual_new_category_name not in categories_for_management:
                    categories_for_management[actual_new_category_name] = {}
                    # selected_category_names にも追加するが、これは表示上の選択なので、
                    # 次回のリロードで categories_for_selector に含まれればOK
                    if actual_new_category_name not in st.session_state.selected_category_names_complete:
                         st.session_state.selected_category_names_complete.append(actual_new_category_name)
                    st.success(f"新規カテゴリ「{actual_new_category_name}」を作成しました。")
            
            if actual_new_category_name in categories_for_management:
                categories_for_management[actual_new_category_name][new_preset_key] = new_preset_value_ja
                st.session_state.categories_data = categories_for_management 
                save_presets(st.session_state.categories_data) # 保存するのは更新されたマスターデータ
                st.success(f"「{actual_new_category_name}」に「{new_preset_key}」を追加/更新しました。")
                st.experimental_rerun()
            elif not (edit_category_name_selected == "新しいカテゴリを作成" and not actual_new_category_name.strip()):
                 st.error(f"カテゴリ「{actual_new_category_name}」の準備または選択に失敗しました。")
        else:
            st.error("カテゴリ名と英語キーを入力してください。")

    st.markdown("---")
    st.write("既存プリセットの削除:")
    delete_category_options_sidebar = list(categories_for_management.keys()) 
    if not delete_category_options_sidebar:
        st.caption("削除できるカテゴリがありません。")
    else:
        del_category_name = st.selectbox("削除するプリセットのカテゴリ名", delete_category_options_sidebar, key="del_cat_name_select_complete_del_manage", index=0 if delete_category_options_sidebar else None)
        if del_category_name and del_category_name in categories_for_management:
            del_preset_options = list(categories_for_management[del_category_name].keys())
            if not del_preset_options:
                st.caption(f"「{del_category_name}」には削除できるプリセットがありません。")
            else:
                del_preset_key = st.selectbox("削除するプリセットの英語キー", del_preset_options, key="del_preset_key_select_complete_del_manage", index=0 if del_preset_options else None)
                if del_preset_key and st.button(f"「{del_preset_key}」を「{del_category_name}」から削除", key=f"delete_preset_button_{del_category_name.replace(' ', '_')}_{del_preset_key.replace(' ', '_')}_complete_manage"):
                    if del_preset_key in categories_for_management[del_category_name]:
                        del categories_for_management[del_category_name][del_preset_key]
                        if not categories_for_management[del_category_name]: 
                            del categories_for_management[del_category_name]
                            st.session_state.selected_category_names_complete = [
                                name for name in st.session_state.selected_category_names_complete if name != del_category_name
                            ]
                        st.session_state.categories_data = categories_for_management 
                        save_presets(st.session_state.categories_data) # 更新されたマスターデータを保存
                        st.success(f"「{del_category_name}」から「{del_preset_key}」を削除しました。")
                        st.experimental_rerun()

if st.sidebar.button("現在の全プリセットをJSONファイルに保存", key="save_all_presets_to_file_button_complete"):
    save_presets(st.session_state.categories_data) # 保存するのは常にsession_stateの最新データ
    st.sidebar.success("現在の全プリセットを presets/image_presets.json に保存しました！")

if st.sidebar.button("【危険】全データを初期状態にリセット", type="primary", key="reset_to_default_button_complete"):
    default_categories_reset = {k: v.copy() for k, v in PROMPT_CATEGORIES.items()}
    st.session_state.categories_data = default_categories_reset
    st.session_state.selected_category_names_complete = list(default_categories_reset.keys())
    st.session_state.category_selections_complete = {} 
    save_presets(default_categories_reset) 
    st.sidebar.warning("全データを初期状態にリセットしました。")
    st.experimental_rerun()

st.markdown("---")
st.caption("Streamlit Prompt Tool - Kou-san Custom Edition (Search Enabled!)")
