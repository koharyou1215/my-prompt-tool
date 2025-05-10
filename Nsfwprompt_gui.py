import os
import streamlit as st
import json

# プリセットデータ
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
        "anime screen capture": "アニメのスクリーンキャプチャ",
        "sharp focus": "鋭い集中力 (シャープフォーカス)",
        "cinematic lighting": "映画的な照明",
        "natural light": "自然光",
        "high-definition lighting": "高精細な照明",
        "vivid colors": "鮮やかな色彩",
        "smooth lines": "滑らかな線",
        "perfect anatomy": "完璧な解剖学",
        "intricate fabric details": "複雑な布地のディテール",
        "dramatic shadows": "劇的な影",
        "score_9": "スコア9",
        "score_8_up": "スコア8以上",
        "score_7_up": "スコア7以上",
        "source_anime": "アニメ風 (ソース:アニメ)",
        "dim lighting": "薄暗い照明"
    },
    "キャラクター基本": {
        "1 girl": "一人の少女",
        "Mithra": "ミスラ (キャラクター名/種族)",
        "elf ears": "エルフの耳",
        "small anime girl": "小さなアニメの女の子"
    },
    "髪型・髪色": {
        "long hair": "長い髪",
        "very long hair": "とても長い髪",
        "short hair": "短い髪",
        "medium hair": "ミディアムヘア",
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
        "bob cut": "ボブカット",
        "hime cut": "姫カット",
        "braid": "三つ編み",
        "curly hair": "カーリーヘア",
        "wavy hair": "ウェーブヘア",
        "straight hair": "ストレートヘア"
    },
    "体型・肌": {
        "fair-skinned": "色白",
        "dark skin": "褐色肌",
        "tan": "日焼け肌",
        "pale skin": "青白い肌",
        "medium breasts": "中くらいの胸",
        "large breasts": "大きな胸",
        "small breasts": "小さな胸",
        "huge breasts": "巨乳",
        "flat chest": "平らな胸",
        "sagging breasts:1.2": "たるんだ胸 (強調1.2)",
        "curvy body": "曲線的な体つき",
        "slim body": "細身の体",
        "petite": "小柄な",
        "muscular": "筋肉質な",
        "abs": "腹筋",
        "wide hips": "広い腰",
        "thick thighs": "太い太もも",
        "bare legs": "素足" # 追加
    },
    "表情・感情": {
        "smile": "笑顔",
        "laughing": "笑っている",
        "sad face": "悲しい顔",
        "crying": "泣いている",
        "tears": "涙目",
        "angry face": "怒った顔",
        "blush": "赤面",
        "embarrassed:1.5": "恥ずかしい (強調1.5)",
        "happy": "ハッピー (嬉しい)",
        "surprised": "驚いた顔",
        "shouting": "叫んでいる顔",
        "closed eyes": "目を閉じている",
        "open mouth": "口を開けている",
        "tongue out": "舌を出している",
        "ahegao": "アヘ顔",
        "flushed face": "赤ら顔",
        "head tilt": "首をかしげる"
    },
    "服装一般 (Apparel - General)": {
        "shirt": "シャツ",
        "collared shirt": "襟付きシャツ", # 学生服と区別するため汎用として
        "dress shirt": "ドレスシャツ", # 追加
        "t-shirt": "Tシャツ",
        "sweater": "セーター",
        "turtleneck sweater": "タートルネックセーター", # 追加
        "hoodie": "パーカー",
        "jacket": "ジャケット", # 追加 (学生服と区別)
        "coat": "コート", # 追加
        "jeans": "ジーンズ",
        "pants": "パンツ (ズボン)",
        "shorts": "ショートパンツ (一般)",
        "short shorts": "ショートショーツ (ホットパンツ)", # 追加
        "skirt": "スカート (一般)",
        "flare skirt": "フレアスカート", # 追加
        "pleated skirt": "プリーツスカート (一般)", # 追加 (学生服と区別)
        "layered skirt": "レイヤードスカート", # 追加
        "frilled skirt": "フリルスカート (一般)", # 追加 (チア等と区別)
        "mini skirt": "ミニスカート",
        "micro mini skirt": "マイクロミニスカート", # micro mini -> micro mini skirt
        "pencil skirt": "ペンシルスカート", # 追加
        "A-line skirt": "Aラインスカート", # 追加
        "lace skirt": "レーススカート", # 追加
        "dress": "ドレス (一般)",
        "cardigan": "カーディガン",
        "tracksuit": "ジャージ上下"
    },
    "学生服・体操服 (School Uniforms & Gym Clothes)": { # 名称変更
        "school uniform": "学生服",
        "school uniform, collared shirt": "学生服 (襟付きシャツ)",
        "school uniform, pleated skirt": "学生服 (プリーツスカート)",
        "school uniform, blazer": "学生服 (ブレザー)", # blazer (school) から変更
        "serafuku": "セーラー服",
        "serafuku, summer": "セーラー服 (夏服)",
        "serafuku, winter": "セーラー服 (冬服)",
        "school uniform, vest": "学生服とベスト",
        "school uniform, beige vest": "学生服とベージュのベスト",
        "school gym uniform": "学校の体操服", # school gym clothes, suitも同義として集約
        "white gym uniform": "白い体操服",
        "gym uniform, shorts": "体操服 (ショートパンツ)",
        "gym uniform, buruma": "体操服 (ブルマ)",
        "school swimsuit": "スクール水着"
    },
    "職業制服・その他制服 (Work & Other Uniforms)": {
        "office lady uniform": "OL制服",
        "business suit": "ビジネススーツ",
        "office staff suit": "OLスーツ", # 追加
        "office worker": "OL (職業指定)", # 追加
        "female office worker": "女性会社員 (職業指定)", # 追加
        "secretary": "秘書 (職業指定)", # 追加
        "suit": "スーツ (職業)",
        "lab coat": "白衣 (研究者等)",
        "doctor": "医師 (職業指定)", # 追加
        "doctor coat": "ドクターコート (医師の白衣)", # 追加
        "nurse": "看護師 (職業指定)", # 追加
        "white nurse": "白衣の看護師", # 追加
        "pink nurse": "ピンクのナース服", # 追加
        "teacher": "教師 (職業指定)", # 追加
        "school teacher": "学校の先生 (職業指定)", # 追加
        "police officer": "警察官 (職業指定)", # police uniformと関連
        "police uniform": "警察官の制服",
        "military uniform": "軍服",
        "waitress": "ウェイトレス (職業指定)", # 追加
        "flight attendant": "客室乗務員 (職業指定)", # 追加
        "undertaker": "葬儀屋 (職業指定)" # 追加
    },
    "コスプレ衣装 (Cosplay Outfits)": {
        "maid outfit": "メイド服", # maidと同義集約
        "maid headdress": "メイドカチューシャ", # アクセにもあるがセットとして
        "frill apron": "フリルエプロン", # アクセにもあるがセットとして
        "french maid": "フレンチメイド",
        "miko": "巫女", # japanese shrine miko, shrine maiden を集約
        "idol costume": "アイドル衣装",
        "nun": "修道女", # nun outfit を集約
        "fantasy costume": "ファンタジー衣装",
        "magical girl costume": "魔法少女のコスチューム",
        "blue magical girl costume": "青い色の魔法少女のコスチューム",
        "wedding dress": "ウェディングドレス",
        "bunny girl suit": "バニーガールスーツ",
        "race queen costume": "レースクイーンのコスチューム",
        "santa costume": "サンタクロースの衣装"
    },
    "スポーツウェア (Sportswear)": { # 新設カテゴリ
        "sportswear": "スポーツウェア (総称)",
        "tennis wear": "テニスウェア", # 追加
        "tennis player": "テニスプレイヤー (役割)", # 追加
        "volleyball wear": "バレーボールウェア", # volleyball ware -> wear, 追加
        "volleyball player": "バレーボールプレイヤー (役割)", # 追加
        "marathon wear": "マラソンウェア", # 追加
        "marathon runner": "マラソンランナー (役割)", # 追加
        "marathon wear, shorts": "マラソンウェア (ショートパンツ)", # 追加
        "cheerleader": "チアリーダー (役割/服装)", # 追加
        "cheerleader uniform": "チアリーダーのユニフォーム",
        "cheerleader, frilled skirt": "チアリーダー (フリルスカート)", # 追加
        "cheerleader, separate": "チアリーダー (セパレート)", # 追加
        "figure skater": "フィギュアスケート選手 (役割/服装)", # 追加
        "figure skating costume": "フィギュアスケートコスチューム" # 追加
    },
    "下着・ナイトウェア (Lingerie & Nightwear)": {
        "lingerie": "ランジェリー",
        "bra": "ブラジャー",
        "panties": "パンティ",
        "thong": "ソング (Tバック)",
        "bikini": "ビキニ (水着・下着)",
        "micro bikini": "マイクロビキニ",
        "negligee": "ネグリジェ",
        "nightgown": "ナイトガウン",
        "pajamas": "パジャマ",
        "babydoll": "ベビードール",
        "bloomers (underwear)": "ブルーマーズ (下着風)",
        "fundoshi": "ふんどし"
    },
    "衣装状態・着こなし (Clothing Details & Condition)": {
        "open shirt": "開いたシャツ",
        "open clothes": "はだけた服",
        "torn clothes": "破れた服",
        "wet clothes": "濡れた服",
        "see-through": "透けている服",
        "sheer fabric": "薄い生地の服",
        "damaged clothes": "傷ついた服",
        "ripped jeans": "破れたジーンズ",
        "off_shoulder": "オフショルダー",
        "shirt tucked in": "シャツをインする",
        "shirt untucked": "シャツを出す",
        "bare shoulders": "肩出し",
        "cleavage": "胸の谷間",
        "exposed thighs and stomach": "露出した太ももとお腹"
    },
    "アクセサリー・靴・装飾品 (Accessories, Footwear & Ornaments)": {
        "hat": "帽子",
        "cap": "キャップ",
        "beret": "ベレー帽",
        "sun visor": "サンバイザー", # 追加
        "glasses": "メガネ",
        "sunglasses": "サングラス",
        "necklace": "ネックレス",
        "choker": "チョーカー",
        "earrings": "イヤリング/ピアス",
        "ring": "指輪",
        "bracelet": "ブレスレット",
        "gloves": "手袋",
        "belt (accessory)": "ベルト (装飾)", # belt から変更
        "scarf": "スカーフ",
        "navy scarf": "紺色のスカーフ",
        "red scarf": "赤色のスカーフ",
        "bow (accessory)": "リボン (アクセサリー)",
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
        "shoes": "靴 (総称)",
        "sneakers": "スニーカー",
        "boots": "ブーツ",
        "western boots": "ウエスタンブーツ",
        "high heels": "ハイヒール",
        "loafers": "ローファー", # 追加
        "sandals": "サンダル",
        "slippers": "スリッパ",
        "socks": "靴下 (一般)",
        "short socks": "短い靴下",
        "high socks": "ハイソックス", # 追加
        "long slouchy socks": "長いルーズソックス", # 追加
        "knee-high socks": "ニーハイソックス",
        "thighhighs": "サイハイソックス",
        "pantyhose": "パンティストッキング",
        "black pantyhose": "黒のパンティストッキング", # 追加
        "fishnet tights": "網タイツ", # 追加
        "zettai ryoiki": "絶対領域",
        "garter belt": "ガーターベルト",
        "mask (face)": "マスク (顔)", # mask から変更
        "blindfold": "目隠し (一般)"
    },
    "ポーズ・動作 (Pose & Action)": {
        # 立ちポーズ
        "standing": "立っている",
        "contrapposto": "コントラポスト",
        "leaning forward": "前かがみ",
        "arched back": "背中を反らす",
        "looking back": "振り返る",
        "leaning back (standing)": "後ろにもたれる (立位)",
        "standing against the wall": "壁にもたれて立つ",
        "standing on one leg": "片足立ち",
        "leg up (standing)": "足を上げる (立位)",
        "fighting pose": "ファイティングポーズ",
        "fighting stance": "構えのポーズ",
        # 座りポーズ
        "sitting": "座っている",
        "seiza": "正座",
        "wariza": "割座",
        "sitting with hands between legs": "脚の間に手を置いて座る",
        "sitting sideways": "横座り (yokozuwari)",
        "hugging own legs": "自分の脚を抱える (体育座り風)",
        "hugging own feet": "自分の足を抱える",
        "indian style sitting": "あぐら",
        "squatting": "しゃがむ",
        "on one knee": "片膝立ち",
        "kneeling": "両膝立ち",
        "crossed legs (sitting)": "脚を組んで座る",
        "spread legs (sitting)": "開脚して座る",
        "leaning back (sitting)": "後ろにもたれて座る",
        "straddling": "またがる (straddle, sit astride)",
        "dogeza": "土下座",
        # 四つん這い系
        "on all fours": "四つん這い",
        "crawling": "這う",
        # 手・腕のポーズ
        "peace sign": "ピースサイン",
        "double peace sign": "ダブルピース",
        "thumbs up": "サムズアップ",
        "finger pointing": "指差し",
        "praying hands": "祈りのポーズ",
        "chin rest": "頬杖",
        "hands making heart": "手でハートを作る",
        "waving hand": "手を振る",
        "salute": "敬礼",
        "paw pose": "猫の手ポーズ",
        "claw pose": "爪を立てるポーズ",
        "one hand on hip": "片手を腰に",
        "hands on hips": "両手を腰に",
        "hands on chest": "胸に手を置く",
        "reaching out": "手を伸ばす",
        "hands in pockets": "ポケットに手を入れる",
        "crossed arms": "腕を組む",
        "arm up": "片腕を上げる",
        "arms up": "両腕を上げる",
        "arms behind back": "腕を後ろに組む",
        "arms behind head": "頭の後ろで腕を組む",
        "spread arms": "両腕を広げる",
        "arm support": "腕で体を支える",
        # 寝ポーズ
        "lying on back": "仰向けに寝る",
        "lying on stomach": "うつ伏せに寝る",
        "lying on side": "横向きに寝る",
        "sleeping": "寝ている",
        "fetal position": "胎児のポーズ",
        "legs up (lying)": "脚を上げる (寝ながら)",
        "spread legs, legs up (lying)": "開脚して脚を上げる (寝ながら)",
        # 動作
        "walking": "歩いている",
        "running": "走っている",
        "jumping": "ジャンプしている",
        "dancing": "踊っている",
        "singing": "歌っている",
        # その他
        "selfie pose": "自撮りポーズ",
        "dynamic pose": "ダイナミックなポーズ",
        "acrobatic pose": "アクロバティックなポーズ",
    },
    "背景・場所 (Setting & Location)": {
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
        "church": "教会", # 追加
        "stained glass": "ステンドグラス", # 追加
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
        "underground torture room": "地下の拷問部屋",
        "prison": "牢獄",
        "room with Christmas tree": "クリスマスツリーのある部屋"
    },
    "NSFW・その他特殊指定": {
        "nsfw": "NSFW (職場閲覧注意)",
        "obscene scenario": "わいせつなシナリオ",
        "BDSM": "BDSM",
        "bondage": "拘束",
        "shibari": "緊縛 (日本式緊縛)",
        "ropes": "ロープ (拘束具)",
        "chains": "鎖 (拘束具)",
        "handcuffs": "手錠",
        "gagged": "猿ぐつわをされた",
        "blindfolded (nsfw context)": "目隠し (NSFW文脈)",
        "restrained": "拘束されている (一般)",
        "star-shaped restraint": "星型に拘束",
        "slime": "スライム",
        "slime tentacles": "スライムの触手",
        "tentacles": "触手",
        "tentacles grabbing": "掴む触手",
        "prison clothes": "囚人服",
        "breast hold": "胸を抱える (セクシャルな文脈)",
        "ass focus": "尻に焦点",
        "upskirt": "スカートの中 (アングル)",
        "panty shot": "パンチラ"
    }
}

def save_presets(data):
    os.makedirs("presets", exist_ok=True)
    with open("presets/image_presets.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_presets():
    if os.path.exists("presets/image_presets.json"):
        with open("presets/image_presets.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                save_presets(PROMPT_CATEGORIES) 
                return PROMPT_CATEGORIES
    save_presets(PROMPT_CATEGORIES)
    return PROMPT_CATEGORIES

# UI設定
st.set_page_config(layout="wide")
st.title("🎨 画像生成プロンプト生成ツール Ver.4 (スポーツウェアカテゴリ追加)")

if 'categories_data' not in st.session_state:
    st.session_state.categories_data = load_presets()

categories = st.session_state.categories_data

st.sidebar.header("🔧 設定")
if 'selected_category_names' not in st.session_state:
    st.session_state.selected_category_names = list(categories.keys())

selected_category_names = st.sidebar.multiselect(
    "使用するカテゴリを選択",
    list(categories.keys()),
    default=st.session_state.selected_category_names,
    key="category_selector"
)
st.session_state.selected_category_names = selected_category_names

cols_num = st.sidebar.number_input("表示カラム数", min_value=1, max_value=5, value=3, key="column_selector")
cols = st.columns(cols_num)
generated_prompt_parts = []

if 'category_selections' not in st.session_state:
    st.session_state.category_selections = {}

for i, category_name in enumerate(selected_category_names):
    if category_name in categories:
        with cols[i % cols_num]:
            st.subheader(f"🔖 {category_name}")
            options_in_category = list(categories[category_name].keys())
            default_selection = st.session_state.category_selections.get(category_name, [])
            
            selected_options = st.multiselect(
                f"{category_name} から選択",
                options=options_in_category,
                default=default_selection,
                format_func=lambda x: f"{x} ({categories[category_name].get(x, '')})",
                key=f"multiselect_{category_name.replace(' ', '_')}" # キーに空白が含まれないように
            )
            generated_prompt_parts.extend(selected_options)
            st.session_state.category_selections[category_name] = selected_options

st.subheader("✏️ カスタムプロンプト")
custom_prompt_input = st.text_area("自由記述欄（追加したいプロンプトをカンマ区切りで入力）", key="custom_prompt_text_area_v4")

if st.button("🛠️ プロンプト生成", key="generate_prompt_button_v4"):
    final_generated_prompt = ", ".join(filter(None, generated_prompt_parts))
    
    if custom_prompt_input:
        custom_parts = [p.strip() for p in custom_prompt_input.split(',') if p.strip()]
        if final_generated_prompt and custom_parts:
            final_generated_prompt += ", " + ", ".join(custom_parts)
        elif custom_parts:
            final_generated_prompt = ", ".join(custom_parts)
            
    st.subheader("🎯 生成されたプロンプト")
    st.code(final_generated_prompt, language="text")
    st.text_area("コピー用", final_generated_prompt, height=100, key="copy_area_generated_prompt_v4")

st.sidebar.header("💾 プリセット管理")
with st.sidebar.expander("新規プリセット追加/編集/削除"):
    edit_category_name = st.selectbox(
        "編集/追加先のカテゴリ名", 
        ["新しいカテゴリを作成"] + list(categories.keys()), 
        key="edit_cat_name_select_v4"
    )
    
    actual_new_category_name = edit_category_name
    if edit_category_name == "新しいカテゴリを作成":
        actual_new_category_name = st.text_input("新しいカテゴリの実際の名前 (日本語)", key="actual_new_cat_name_input_v4")

    new_preset_key = st.text_input("プリセットの英語キー", key="new_preset_key_input_v4")
    new_preset_value_ja = st.text_input("プリセットの日本語訳", key="new_preset_value_ja_input_v4")

    if st.button("プリセットを追加/更新", key="add_update_preset_button_v4"):
        if actual_new_category_name and new_preset_key:
            if actual_new_category_name not in categories and edit_category_name == "新しいカテゴリを作成":
                if not actual_new_category_name.strip(): # 空のカテゴリ名は許可しない
                    st.error("新しいカテゴリ名が空です。入力してください。")
                else:
                    categories[actual_new_category_name] = {}
            
            if actual_new_category_name in categories:
                categories[actual_new_category_name][new_preset_key] = new_preset_value_ja
                st.session_state.categories_data = categories
                save_presets(categories)
                st.success(f"「{actual_new_category_name}」に「{new_preset_key}」を追加/更新しました。")
                st.experimental_rerun()
            elif edit_category_name == "新しいカテゴリを作成" and not actual_new_category_name.strip():
                pass # エラーメッセージは上で表示済み
            else:
                 st.error(f"カテゴリ「{actual_new_category_name}」の準備に失敗しました。")
        else:
            st.error("カテゴリ名と英語キーを入力してください。")

    st.markdown("---")
    st.write("既存プリセットの削除:")
    del_category_options = list(categories.keys())
    if not del_category_options:
        st.caption("削除できるカテゴリがありません。")
    else:
        del_category_name = st.selectbox("削除するプリセットのカテゴリ名", del_category_options, key="del_cat_name_select_v4", index=0 if del_category_options else None)
        if del_category_name and del_category_name in categories:
            del_preset_options = list(categories[del_category_name].keys())
            if not del_preset_options:
                st.caption(f"「{del_category_name}」には削除できるプリセットがありません。")
            else:
                del_preset_key = st.selectbox("削除するプリセットの英語キー", del_preset_options, key="del_preset_key_select_v4", index=0 if del_preset_options else None)
                if st.button(f"「{del_preset_key}」を削除", key=f"delete_preset_button_{del_preset_key.replace(' ', '_')}"): # キーに空白が含まれないように
                    if del_preset_key in categories[del_category_name]:
                        del categories[del_category_name][del_preset_key]
                        if not categories[del_category_name]:
                            del categories[del_category_name]
                            st.session_state.selected_category_names = [cn for cn in st.session_state.selected_category_names if cn != del_category_name]
                        st.session_state.categories_data = categories
                        save_presets(categories)
                        st.success(f"「{del_category_name}」から「{del_preset_key}」を削除しました。")
                        st.experimental_rerun()

if st.sidebar.button("現在の全プリセットを保存", key="save_all_presets_button_v4"):
    save_presets(categories)
    st.sidebar.success("現在の全プリセットを presets/image_presets.json に保存しました！")

if st.sidebar.button("デフォルトプリセットにリセット", key="reset_to_default_button_v4"):
    st.session_state.categories_data = PROMPT_CATEGORIES.copy()
    st.session_state.selected_category_names = list(PROMPT_CATEGORIES.keys())
    st.session_state.category_selections = {}
    save_presets(PROMPT_CATEGORIES)
    st.sidebar.info("プリセットをデフォルトにリセットしました。")
    st.experimental_rerun()