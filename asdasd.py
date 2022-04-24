import datetime
import urllib

from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor

TOKEN = "5288298713:AAFW6cXZ2YmVb3sP6xfyzgNBjLqt8XIA7NY"
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def s(message: types.Message):
    await message.answer(f"Привет! Отправь мне файлы с расширением .knd или .knvis")


@dp.message_handler(commands=['help'])
async def h(message: types.Message):
    await message.answer(f"Привет! Отправь мне файлы с расширением .knd или .knvis")


@dp.message_handler(content_types=['document'])
async def tun(message: types.Message):
    # добавить описание и кнопки с моделямим машины
    while True:
        try:
            document_id = message.document.file_id
            file_info = await bot.get_file(document_id)
            fi = file_info.file_path
            name = message.document.file_name
            print(name)
            if name[-4::] == ".knd":
                from data import db_session
                db_session.global_init("db/database.db")
                db_sess = db_session.create_session()
                from data.tuns import Tuns
                vins = Tuns(user="CarX.bot", name=name,
                            description="Файл добавлен через бота, описание отсутствует",
                            car_type="CarX.bot", created_date=datetime.date.today())
                db_sess.add(vins)
                db_sess.commit()
                dbg = db_sess.query(Tuns).all()
                for i in dbg:
                    if i == vins:
                        try:
                            urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}',
                                                       f'./static/img/tunes/knd/{i.id}.knd')
                            break
                        except AttributeError:
                            pass
                await message.answer('Тюнинг успешно сохранён')
                break
            elif ".knvis" == name[-6::]:
                print("QQ")
                from data import db_session
                db_session.global_init("db/database.db")
                db_sess = db_session.create_session()
                from data.vins import Vinils
                vins = Vinils(user="CarX.bot", name=name,
                              description="Файл добавлен через бота, описание отсутствует",
                              car_type="CarX.bot", created_date=datetime.date.today())
                db_sess.add(vins)
                db_sess.commit()
                dbg = db_sess.query(Vinils).all()
                for i in dbg:
                    if i == vins:
                        try:
                            urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}',
                                                       f'./static/img/vins/knvis/{i.id}.knvis')
                            from PIL import Image
                            image = Image.open('bot.jpg')
                            image.save(f'static/img/vins/imgs/{i.id}.jpg')
                            break
                        except AttributeError:
                            pass
                #ftp.quit()
                await message.answer('Винил успешно сохранён')
                break
        except Exception as e:
            print(e)
            await message.answer(f'Произошла ошибка\n{e}')



@dp.message_handler()
async def main(message: types.Message):
    await message.answer(f'Я получил сообщение {message["text"]}, у меня нет такой команды(\n Чтобы получить список команд, напишите /help')


executor.start_polling(dp, skip_updates=True)