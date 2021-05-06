import re

##################
# Main bot Sett  #
##################

KARMA_ACTION_DELAY = 15 #задержка между действиями с кармой
KARMA_VAL_NEW_USER = 0 #начальное количество кармы у нового юзера
KARMA_TO_KTOP = 15  # КОЛ-ВО КАРМЫ ДЛЯ ПРОСМОТРА ТОПА
KARMA_TOP_Q = 9  # ДЛИННА СПИСКА ТОПА
KARMA_TO_BITE_USE = 10  # КОЛ-ВО КАРМЫ ДЛЯ ИСПОЛЬЗОВАНИЯ КОМАНДЫ КУСЬ
NAME_SCRIPT = "🅚🅐🅡🅜🅐ⒷⓄⓉ" # Not use
NAME_CHAT = "Anruschat_bot"

##################
# Log Settings   #
##################

##################
#     Command    #
##################
# dict (command : [alias1, alias2, ...] алиасы регистронезависимые

COM = { 'help' : ['карма?', 'karma?'],
        'bite' : ['bite', 'кусь'], 
        'ktop' : ['ktop', 'ктоп'],
        'karm' : ['karm', 'карма']}


##################
# DB Settings    #
##################

DB_LOCATION = 'script.db'
DB_ECHO = True # False для отмены вывода отладки

##################
# RE Settings    #
##################

RE_USER_OUT = re.compile(r'\[Bot\] #\w+ .* выходит из чата\.')
RE_USER_INCOME = re.compile(r'\[Bot\] #\w+ .* входит в чат\.$')
RE_SLAP = re.compile(r'\s{0,1}\* #\w+ .* слегка шлёпнул #\w+ .* большой форелью\.')
RE_HUG = re.compile(r'\s{0,1}\* #\w+ .* крепко обнимает #\w+ .*\.')
RE_CHANGE_NICK = re.compile(r'\[Bot\] #\w+ .* сменил ник на .*')
RE_MUTE = re.compile(r'\[Bot\] #\w+ .* лишен голоса на .*')
RE_KICK = re.compile(r'\[Bot\] #\w+ .* выгнан из чата на .*')
RE_BAN =  re.compile(r'\[Bot\] #\w+ .* забанен в чате навсегда!')
RE_HIDE_VIDEO = re.compile(r'Скрытое видео от #\w+ (.*)[\.,:]{1}.*')
RE_HIDE_PHOTO = re.compile(r'Скрытое фото от #\w+ (.*)[\.,:]{1}.*')
RE_INFO =  re.compile(r'\[BOT\] Информация о .+? #\w+ (.*?):.*')
RE_NEW_USER =re.compile(r'\[Bot\] #\w+ .* входит в чат. Он новенький!')
RE_NM = re.compile(r'(.*?): .*')
RE_KARMA_INCREASE = re.compile(r'(.*?):\s{1,2}\+{1,}$')
RE_KARMA_MORE_INCREASE = re.compile(r'(.*?):\s{1,2}\+{3,}$') # not use
RE_KARMA_LESS_INCREASE = re.compile(r'(.*?):\s{1,2}\+{1,2}$')
RE_KARMA_DECREASE = re.compile(r'(.*?):\s{1,2}-{1,}$')
RE_KARMA_MORE_DECREASE = re.compile(r'(.*?):\s{1,2}-{3,}$') # not use
RE_KARMA_LESS_DECREASE = re.compile(r'(.*?):\s{1,2}-{1,2}$')
#commands
RE_BITE = re.compile(r'(.*?):\s{1,2}кусь$', re.IGNORECASE)
RE_CARMA_HELP = re.compile(r'(.*?):\s{1,2}карма$', re.IGNORECASE)
RE_CARMA_INFO = re.compile(r'(.*?):\s{1,2}инфо$', re.IGNORECASE)
RE_CARMA_TOP = re.compile(r'(.*?):\s{1,2}рейт$', re.IGNORECASE)
