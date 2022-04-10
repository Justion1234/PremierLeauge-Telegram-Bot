import requests
from bs4 import BeautifulSoup
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

token = "2079898984:AAFkLRSxAVj5zs6mRk4NWHhjjeFF0OWoNkM"
telegram_id = "1982453449"
bot = telegram.Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher

# 버튼 추가하는 함수
def cmd_task_buttons(update, context):
    task_buttons = [
        [
            InlineKeyboardButton("해축 뉴스", callback_data=1),  InlineKeyboardButton("프리미어리그 순위", callback_data=2)
        ],
        [
            InlineKeyboardButton("종료", callback_data=9)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(task_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="작업을 선택해주세요.",
        reply_markup=reply_markup
    )


# 텔레그램 안에서 버튼을 클릭하면 이벤트 발생 시켜주는 함수
def cb_button(update, context):
    query = update.callback_query
    data = query.data
    if data == "9":
        shutdown()
    if data == "1":
        news()

    if data == "2":
        ranking()

def shutdown():
        bot.sendMessage(telegram_id, text="작업이 종료되었습니다.")

# 해축 뉴스 불러오기
def news():
    recommendAddr = "https://sports.news.naver.com"
    res = requests.get(recommendAddr + "/wfootball/index")
    soup = BeautifulSoup(res.content, 'html.parser')
    myData = soup.find('ul', class_="home_news_list")
    recommend_list = myData.find_all('a')
    for item in recommend_list:
        title = item['title']
        addr = recommendAddr + item['href']
        bot.sendMessage(telegram_id, text=title + ": " + addr)

# 프리미어리그 순위
def ranking():
    naver_wfootball = "https://sports.news.naver.com/wfootball/index.nhn"
    premi_team_rank = requests.get(naver_wfootball)
    premi_team_rank_list = BeautifulSoup(premi_team_rank.content, "html.parser", from_encoding='utf=8')

    team_rank_list = premi_team_rank_list.select('#_team_rank_epl > table > tbody >tr')
    ranking_table = ""
    for o in team_rank_list:
        r = o.select('.blind')[0].text
        x = o.select('.name')[0].text
        ranking_table += r + ": " + x + "\n"
    bot.sendMessage(telegram_id, text=ranking_table)

# 버튼 생성
def add_handler(cmd, func):
    updater.dispatcher.add_handler(CommandHandler(cmd, func))


# handler 추가
def callback_handler(func):
    updater.dispatcher.add_handler(CallbackQueryHandler(func))

add_handler("task", cmd_task_buttons)
callback_handler(cb_button)
updater.start_polling()



