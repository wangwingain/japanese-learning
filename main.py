from js import document, window
from pyodide.ffi import create_proxy
import random
from time import time

# 獲取主容器
main_container = document.getElementById('main-container')
loading_div = document.getElementById('loading')

# ========== 資料定義 ==========
RAW_TEXTS = {
    4: "あ い う え お か き く け こ さ し す せ そ た ち つ て と な に ぬ ね の は ひ ふ へ ほ ま み む め も や ゆ よ ら り る れ ろ わ を ん",
    5: "ア イ ウ エ オ カ キ ク ケ コ サ シ ス セ ソ タ チ ツ テ ト ナ ニ ヌ ネ ノ ハ ヒ フ ヘ ホ マ ミ ム メ モ ヤ ユ ヨ ラ リ ル レ ロ ワ ヲ ン",
    6: "が ぎ ぐ げ ご ざ じ ず ぜ ぞ だ ぢ づ で ど ば び ぶ べ ぼ ぱ ぴ ぷ ぺ ぽ ガ ギ グ ゲ ゴ ザ ジ ズ ゼ ゾ ダ ヂ ヅ デ ド バ ビ ブ ベ ボ パ ピ プ ペ ポ",
    7: "きゃ きゅ きょ しゃ しゅ しょ ちゃ ちゅ ちょ にゃ にゅ にょ ひゃ ひゅ ひょ みゃ みゅ みょ りゃ りゅ りょ ぎゃ ぎゅ ぎょ じゃ じゅ じょ びゃ びゅ びょ ぴゃ ぴゅ ぴょ キャ キュ キョ シャ シュ ショ チャ チュ チョ ニャ ニュ ニョ ヒャ ヒュ ヒョ ミャ ミュ ミョ リャ リュ リョ ギャ ギュ ギョ ジャ ジュ ジョ ビャ ビュ ビョ ピャ ピュ ピョ"
}

BASE_CHINESE = {
    'あ': '阿', 'い': '依', 'う': '烏', 'え': '欸', 'お': '喔',
    'か': '卡', 'き': 'ki', 'く': '哭', 'け': 'k', 'こ': '摳',
    'さ': '撒', 'し': '西', 'す': '蘇', 'せ': 'se', 'そ': '搜',
    'た': '他', 'ち': '奇', 'つ': '次', 'て': '貼', 'と': '托',
    'な': '那', 'に': '尼', 'ぬ': '努', 'ね': '內', 'の': '諾',
    'は': '哈、挖', 'ひ': 'hi', 'ふ': '呼', 'へ': '嘿', 'ほ': '齁',
    'ま': '媽', 'み': '咪', 'む': '姆', 'め': '梅', 'も': '摸',
    'や': '雅', 'ゆ': 'yu', 'よ': '優',
    'ら': '拉', 'り': '哩', 'る': '魯', 'れ': '勒', 'ろ': '囉',
    'わ': '挖', 'を': '窩、喔', 'ん': '恩',
    'が': '嘎', 'ぎ': 'gi', 'ぐ': '咕', 'げ': '給', 'ご': '勾',
    'ざ': '扎', 'じ': '吉', 'ず': '祖', 'ぜ': '賊', 'ぞ': 'zo',
    'だ': '達', 'ぢ': '低', 'づ': '督', 'で': 'de', 'ど': '都',
    'ば': '巴', 'び': '比', 'ぶ': '布', 'べ': '北', 'ぼ': '波',
    'ぱ': '趴', 'ぴ': '匹', 'ぷ': '普', 'ぺ': '佩', 'ぽ': '坡',
    'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
    'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
    'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
    'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
    'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
    'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
    'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
    'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
    'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
    'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
    'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
    'キャ': 'kya', 'キュ': 'kyu', 'キョ': 'kyo',
    'シャ': 'sha', 'シュ': 'shu', 'ショ': 'sho',
    'チャ': 'cha', 'チュ': 'chu', 'チョ': 'cho',
    'ニャ': 'nya', 'ニュ': 'nyu', 'ニョ': 'nyo',
    'ヒャ': 'hya', 'ヒュ': 'hyu', 'ヒョ': 'hyo',
    'ミャ': 'mya', 'ミュ': 'myu', 'ミョ': 'myo',
    'リャ': 'rya', 'リュ': 'ryu', 'リョ': 'ryo',
    'ギャ': 'gya', 'ギュ': 'gyu', 'ギョ': 'gyo',
    'ジャ': 'ja', 'ジュ': 'ju', 'ジョ': 'jo',
    'ビャ': 'bya', 'ビュ': 'byu', 'ビョ': 'byo',
    'ピャ': 'pya', 'ピュ': 'pyu', 'ピョ': 'pyo'
}

BASE_ROMAJI = {
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha、wa', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'を': 'wo、o', 'ん': 'n',
    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
    'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
    'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
    'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
    'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
    'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
    'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
    'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
    'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
    'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
    'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
    'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
    'キャ': 'kya', 'キュ': 'kyu', 'キョ': 'kyo',
    'シャ': 'sha', 'シュ': 'shu', 'ショ': 'sho',
    'チャ': 'cha', 'チュ': 'chu', 'チョ': 'cho',
    'ニャ': 'nya', 'ニュ': 'nyu', 'ニョ': 'nyo',
    'ヒャ': 'hya', 'ヒュ': 'hyu', 'ヒョ': 'hyo',
    'ミャ': 'mya', 'ミュ': 'myu', 'ミョ': 'myo',
    'リャ': 'rya', 'リュ': 'ryu', 'リョ': 'ryo',
    'ギャ': 'gya', 'ギュ': 'gyu', 'ギョ': 'gyo',
    'ジャ': 'ja', 'ジュ': 'ju', 'ジョ': 'jo',
    'ビャ': 'bya', 'ビュ': 'byu', 'ビョ': 'byo',
    'ピャ': 'pya', 'ピュ': 'pyu', 'ピョ': 'pyo'
}

# 解析文字庫為列表
library_words = {}
for key in RAW_TEXTS:
    library_words[key] = RAW_TEXTS[key].split()

# ========== 強化補全 ==========
def ensure_all_words_covered():
    all_words = set()
    for words in library_words.values():
        all_words.update(words)

    kata_to_hira = {}
    for code in range(0x3041, 0x3097):
        hira = chr(code)
        kata = chr(code + 0x60)
        kata_to_hira[kata] = hira

    for word in all_words:
        if word not in BASE_CHINESE:
            if len(word) == 1 and '\u30a0' <= word <= '\u30ff':
                hira = kata_to_hira.get(word)
                if hira and hira in BASE_CHINESE:
                    BASE_CHINESE[word] = BASE_CHINESE[hira]
                else:
                    BASE_CHINESE[word] = word
            else:
                BASE_CHINESE[word] = word

        if word not in BASE_ROMAJI:
            if len(word) == 1 and '\u30a0' <= word <= '\u30ff':
                hira = kata_to_hira.get(word)
                if hira and hira in BASE_ROMAJI:
                    BASE_ROMAJI[word] = BASE_ROMAJI[hira]
                else:
                    BASE_ROMAJI[word] = word
            else:
                BASE_ROMAJI[word] = word

ensure_all_words_covered()

# ========== 狀態管理 ==========
library_status = {4: True, 5: False, 6: False, 7: False}
pronunciation_status = {'chinese': False, 'romaji': False}
pronunciation_locked = False
last_click_time = 0
current_word = 'あ'

# 儲存對話框引用
dialogs = {}
contents = {}

# ========== 電腦版配置 ==========
desktop_config = {
    1: {'left': '38%', 'top': '10%', 'width': '36%', 'height': '54%', 'font_size': '230px'},
    2: {'left': '75%', 'top': '20%', 'width': '23%', 'height': '18%', 'font_size': '76px'},
    3: {'left': '75%', 'top': '40%', 'width': '23%', 'height': '18%', 'font_size': '76px'},
    4: {'left': '1%', 'top': '83%', 'width': '8%', 'height': '14%', 'icon': '平假', 'icon_size': '24px'},
    5: {'left': '10%', 'top': '83%', 'width': '8%', 'height': '14%', 'icon': '片假', 'icon_size': '24px'},
    6: {'left': '19%', 'top': '83%', 'width': '8%', 'height': '14%', 'icon': '濁音', 'icon_size': '24px'},
    7: {'left': '28%', 'top': '83%', 'width': '8%', 'height': '14%', 'icon': '拗音', 'icon_size': '24px'},
    8: {'left': '59%', 'top': '70%', 'width': '15%', 'height': '27%', 'font_size': '40px'},
    9: {'left': '75%', 'top': '70%', 'width': '15%', 'height': '27%', 'font_size': '40px'}
}

# ========== 手機版配置 (已更新) ==========
mobile_config = {
    1: {'font_size': '90px', 'icon': None},
    2: {'font_size': '30px', 'icon': None},
    3: {'font_size': '30px', 'icon': None},
    4: {'icon': '平假名', 'icon_size': '14px'},
    5: {'icon': '片假名', 'icon_size': '14px'},
    6: {'icon': '濁音', 'icon_size': '14px'},
    7: {'icon': '拗音', 'icon_size': '14px'},
    8: {'font_size': '18px'},
    9: {'font_size': '18px'}
}

# ========== 基礎配置 ==========
base_config = {
    1: {'class': 'dialog-1', 'is_clickable': False},
    2: {'class': 'dialog-2', 'is_clickable': False},
    3: {'class': 'dialog-3', 'is_clickable': False},
    4: {'class': 'dialog-4', 'is_clickable': True, 'icon': '平假'},
    5: {'class': 'dialog-5', 'is_clickable': True, 'icon': '片假'},
    6: {'class': 'dialog-6', 'is_clickable': True, 'icon': '濁音'},
    7: {'class': 'dialog-7', 'is_clickable': True, 'icon': '拗音'},
    8: {'class': 'dialog-8', 'is_clickable': True},
    9: {'class': 'dialog-9', 'is_clickable': True}
}

# ========== 輔助函數：創建對話框 ==========
def create_dialog(dialog_id, base_config):
    config = base_config.copy()
    
    width = window.innerWidth
    is_mobile = width <= 567
    
    if is_mobile:
        if dialog_id in mobile_config:
            mobile_settings = mobile_config[dialog_id]
            if 'font_size' in mobile_settings:
                config['font_size'] = mobile_settings['font_size']
            if 'icon' in mobile_settings:
                config['icon'] = mobile_settings['icon']
            if 'icon_size' in mobile_settings:
                config['icon_size'] = mobile_settings['icon_size']
    else:
        if dialog_id in desktop_config:
            config.update(desktop_config[dialog_id])
    
    dialog = document.createElement('div')
    dialog.id = f'dialog-{dialog_id}'
    dialog.className = f'dialog {config["class"]}'
    
    if not is_mobile:
        if 'left' in config:
            dialog.style.left = config['left']
        if 'top' in config:
            dialog.style.top = config['top']
        if 'width' in config:
            dialog.style.width = config['width']
        if 'height' in config:
            dialog.style.height = config['height']
    
    if config.get('is_clickable', False):
        dialog.className += ' clickable'

    content_div = document.createElement('div')
    content_div.id = f'content-{dialog_id}'
    content_div.className = 'display-content'
    if 'font_size' in config:
        content_div.style.fontSize = config['font_size']
    dialog.appendChild(content_div)

    if dialog_id in [4, 5, 6, 7]:
        icon_div = document.createElement('div')
        icon_div.className = 'library-icon'
        icon_div.textContent = config['icon']
        if 'icon_size' in config:
            icon_div.style.fontSize = config['icon_size']
        content_div.appendChild(icon_div)
    elif dialog_id == 8:
        content_div.textContent = '讀音'
    elif dialog_id == 9:
        content_div.textContent = '下一個'

    if is_mobile:
        create_mobile_layout(dialog, dialog_id)
    else:
        main_container.appendChild(dialog)
    
    return dialog, content_div

# ========== 手機版布局 ==========
def create_mobile_layout(dialog, dialog_id):
    if dialog_id == 1:
        main_container.innerHTML = ''
        main_container.appendChild(dialog)
    elif dialog_id == 2:
        if not document.getElementById('pronunciation-row'):
            row = document.createElement('div')
            row.id = 'pronunciation-row'
            row.className = 'pronunciation-row'
            main_container.appendChild(row)
        row = document.getElementById('pronunciation-row')
        row.appendChild(dialog)
    elif dialog_id == 3:
        row = document.getElementById('pronunciation-row')
        if row:
            row.appendChild(dialog)
    elif dialog_id in [4, 5, 6, 7]:
        if not document.getElementById('library-grid'):
            grid = document.createElement('div')
            grid.id = 'library-grid'
            grid.className = 'library-grid'
            main_container.appendChild(grid)
        grid = document.getElementById('library-grid')
        grid.appendChild(dialog)
    elif dialog_id in [8, 9]:
        if not document.getElementById('action-row'):
            row = document.createElement('div')
            row.id = 'action-row'
            row.className = 'action-row'
            main_container.appendChild(row)
        row = document.getElementById('action-row')
        row.appendChild(dialog)

# ========== 建立所有對話框 ==========
for dialog_id in range(1, 10):
    dialog, content = create_dialog(dialog_id, base_config[dialog_id])
    dialogs[dialog_id] = dialog
    contents[dialog_id] = content

if loading_div:
    loading_div.style.display = 'none'

# ========== 更新文字庫視覺狀態 ==========
def update_library_appearance():
    for lib_id in [4, 5, 6, 7]:
        dialog = dialogs[lib_id]
        if library_status[lib_id]:
            dialog.classList.remove('library-off')
        else:
            dialog.classList.add('library-off')

# ========== 更新顯示 ==========
def update_displays():
    contents[1].textContent = current_word
    show_pronunciation = pronunciation_locked or pronunciation_status['chinese'] or pronunciation_status['romaji']
    
    if show_pronunciation and current_word in BASE_CHINESE:
        contents[2].textContent = BASE_CHINESE[current_word]
    else:
        contents[2].textContent = ''
    if show_pronunciation and current_word in BASE_ROMAJI:
        contents[3].textContent = BASE_ROMAJI[current_word]
    else:
        contents[3].textContent = ''

    update_library_appearance()

    if pronunciation_locked:
        contents[8].textContent = '鎖定'
        dialogs[8].classList.add('locked')
    else:
        if pronunciation_status['chinese'] or pronunciation_status['romaji']:
            contents[8].textContent = '隱藏'
        else:
            contents[8].textContent = '讀音'
        dialogs[8].classList.remove('locked')

def update_current_word(force=False):
    global current_word
    available_words = []
    for lib_id in [4, 5, 6, 7]:
        if library_status[lib_id]:
            available_words.extend(library_words[lib_id])
    if not available_words:
        current_word = ''
        return
    if not force and current_word in available_words:
        return
    else:
        current_word = random.choice(available_words)

# ========== 事件處理 ==========
def on_library_click(lib_id):
    def handler(event):
        global library_status
        library_status[lib_id] = not library_status[lib_id]
        update_current_word(force=False)
        update_displays()
        print(f'文字庫 {lib_id} 狀態: {"開啟" if library_status[lib_id] else "關閉"}')
    return handler

def on_pronunciation_click(event):
    global last_click_time, pronunciation_locked, pronunciation_status
    current_time = time() * 1000
    time_diff = current_time - last_click_time
    if time_diff < 300:
        pronunciation_locked = not pronunciation_locked
        if pronunciation_locked:
            pronunciation_status['chinese'] = True
            pronunciation_status['romaji'] = True
        else:
            pronunciation_status['chinese'] = False
            pronunciation_status['romaji'] = False
        print(f'讀音鎖定: {"開啟" if pronunciation_locked else "關閉"}')
    else:
        if not pronunciation_locked:
            if pronunciation_status['chinese'] or pronunciation_status['romaji']:
                pronunciation_status['chinese'] = False
                pronunciation_status['romaji'] = False
            else:
                pronunciation_status['chinese'] = True
                pronunciation_status['romaji'] = True
            print(f'讀音顯示: {"開啟" if pronunciation_status["chinese"] else "關閉"}')
    last_click_time = current_time
    update_displays()

def on_next_click(event):
    global pronunciation_status, pronunciation_locked
    if not pronunciation_locked:
        pronunciation_status['chinese'] = False
        pronunciation_status['romaji'] = False
    update_current_word(force=True)
    update_displays()
    print(f'更換文字為: {current_word}')

# ========== 綁定事件 ==========
dialogs[4].addEventListener('click', create_proxy(on_library_click(4)))
dialogs[5].addEventListener('click', create_proxy(on_library_click(5)))
dialogs[6].addEventListener('click', create_proxy(on_library_click(6)))
dialogs[7].addEventListener('click', create_proxy(on_library_click(7)))
dialogs[8].addEventListener('click', create_proxy(on_pronunciation_click))
dialogs[9].addEventListener('click', create_proxy(on_next_click))

# ========== 初始化 ==========
current_word = random.choice(library_words[4])
update_library_appearance()
update_displays()

print('=' * 50)
print('王又贏學日文五十音 - 響應式版')
print('電腦版：絕對定位自由布局')
print('手機版：垂直 Flex 布局，完全獨立')
print('點擊文字庫可開關（關閉時變暗淡），點擊8讀音可切換/鎖定，點擊9下一個隨機換字')
print('鎖定狀態下（雙擊8），9不會關閉讀音，8會變亮')
print('=' * 50)
print(f'當前螢幕尺寸: {window.innerWidth} x {window.innerHeight}')
print(f'當前模式: {"手機版" if window.innerWidth <= 567 else "電腦版"}')