import datetime
import os

from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired
from flask import redirect

from data import db_session
from flask import session
from flask_socketio import SocketIO, send

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/database.db")
db_sess = db_session.create_session()
socketio = SocketIO(app, cors_allowed_origins='*', manage_session=False)
ch_lst = []


class LoginForm(FlaskForm):
    username_l = StringField('Username', validators=[InputRequired("Заполните поле!")],
                             render_kw={'style': "width:370px; height:45;", "placeholder": "Username"})
    password_l = PasswordField('Password', validators=[InputRequired("Заполните поле!")],
                               render_kw={'style': "width:370px; height:45;", "placeholder": "Password123"})
    remember_me = BooleanField('Запомнить меня')


class RegForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired("Заполните поле!")],
                           render_kw={'style': "width:370px; height:45;", "placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired("Заполните поле!")],
                             render_kw={'style': "width:370px; height:45;", "placeholder": "Password123"})
    c_password = PasswordField('c_Password', validators=[InputRequired("Заполните поле!")],
                               render_kw={'style': "width:370px; height:45;", "placeholder": "Password123"})


class add_news(FlaskForm):
    title = StringField('Заголовок', validators=[InputRequired("Поле не может быть пустым!")],
                        render_kw={'style': "width:500px; height:45;", "placeholder": "Заголовок"})
    description = TextAreaField("Текст новости", validators=[InputRequired("Поле не может быть пустым!")],
                                render_kw={'style': "width:500px; max-width:500px; min-width:500px; height: 250px;", "placeholder": "Текст новости"})
    file = FileField(validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Файл должен иметь разрешение jpg/png/jpeg'),
                                 FileSize(0.5 * 1024 * 1024, 0, "Размер файла не должен превышать 512КБ")])


class add_vinils(FlaskForm):
    name = StringField('Имя винила', validators=[InputRequired("Это поле обязательно")],
                       render_kw={'style': "width:500px; height:45;", "placeholder": "Имя винила"})
    description = TextAreaField("Описание", validators=[InputRequired("Это поле обязательно")],
                                render_kw={'style': "width:500px; max-width:500px; min-width:500px; height: 250px;", "placeholder": "Описание"})
    car_type = SelectField("Выберите автомобиль", render_kw={'style': "width:500px; max-width:500px; height:45;"},
                           choices=['hachi-roku', 'panther m5 90-s', 'vz 210', 'panther m5', 'bimmy p30', 'hachi-go',
                                    'dacohosu', 'solar', 'wütend', 'phoenix nx', 'thunderstrike', 'black fox',
                                    'caravan g6', 'mifune', 'vz212', 'lynx', 'pirate', 'imperior', 'godzilla r3',
                                    'dtm 46', 'penguin', 'equator d', 'raven rv8', 'syberia swi', 'sorrow',
                                    'piranha x', 'falcon fc 90-s', 'wellington 20', 'midnight', 'burner jdm',
                                    'hornet gt', 'inferno', 'eva mr', 'horizon gt4', 'cargo', 'corona',
                                    'mira', 'fujin sx', 'falcon rz', 'gloriousxz', 'interstate', 'kanniedood',
                                    'hotrod', 'hakosuka', 'hunter', 'eleganto', 'samurai ii', 'asura m1',
                                    'udm 3', 'hummel', 'last prince', 'magnum rt', 'syberia wdc', 'bandit', 'warden',
                                    'eva x', 'unicorn', 'kitsune', 'flash', 'spark zr', 'spector rs', 'rolla zr',
                                    'carrot ii', 'DLC', 'wanderer l30', 'cobra gt530', 'vanguard', 'loki 4m',
                                    'atlas gt', 'zismo', 'speedline gt', 'black jack x22', 'shadow xtr', 'nomad gt',
                                    'karnage 7c', 'voodoo', 'grace gt', 'shark gt', 'patron gt', 'warrior',
                                    'flanker f', 'spaceknight', 'black jack x150'])  # все в lower!!!!!!!
    img_f = FileField('Загрузите изображение', validators=[FileRequired("Это поле обязательно"),
                                                           FileAllowed(['jpg', 'png', 'jpeg'],
                                                                       'Файл должен иметь разрешение jpg/png/jpeg'),
                                                           FileSize(0.5 * 1024 * 1024, 0,
                                                                    "Размер файла не должен превышать 512КБ")])
    file = FileField('Загрузите файл', validators=[FileRequired("Это поле обязательно"),
                                                   FileAllowed(['knvis'], 'Файл должен иметь разрешение knvis'),
                                                   FileSize(0.5 * 1024 * 1024, 0,
                                                            "Размер файла не должен превышать 512КБ")])


class add_tuns(FlaskForm):
    name = StringField('Имя тюнинга', validators=[InputRequired("Это поле обязательно")],
                       render_kw={'style': "width:500px; height:45;", "placeholder": "Название тюнинга"})
    description = TextAreaField("Описание", validators=[InputRequired("Это поле обязательно")],
                                render_kw={'style': "width:500px; max-width:500px; min-width:500px; height: 250px;", "placeholder": "Описание"})
    car_type = SelectField("Выберите автомобиль", render_kw={'style': "width:500px; max-width:500px; height:45;"},
                           choices=['hachi-roku', 'panther m5 90-s', 'vz 210', 'panther m5', 'bimmy p30', 'hachi-go',
                                    'dacohosu', 'solar', 'wütend', 'phoenix nx', 'thunderstrike', 'black fox',
                                    'caravan g6', 'mifune', 'vz212', 'lynx', 'pirate', 'imperior', 'godzilla r3',
                                    'dtm 46', 'penguin', 'equator d', 'raven rv8', 'syberia swi', 'sorrow',
                                    'piranha x', 'falcon fc 90-s', 'wellington 20', 'midnight', 'burner jdm',
                                    'hornet gt', 'inferno', 'eva mr', 'horizon gt4', 'cargo', 'corona',
                                    'mira', 'fujin sx', 'falcon rz', 'gloriousxz', 'interstate', 'kanniedood',
                                    'hotrod', 'hakosuka', 'hunter', 'eleganto', 'samurai ii', 'asura m1',
                                    'udm 3', 'hummel', 'last prince', 'magnum rt', 'syberia wdc', 'bandit', 'warden',
                                    'eva x', 'unicorn', 'kitsune', 'flash', 'spark zr', 'spector rs', 'rolla zr',
                                    'carrot ii', 'DLC', 'wanderer l30', 'cobra gt530', 'vanguard', 'loki 4m',
                                    'atlas gt', 'zismo', 'speedline gt', 'black jack x22', 'shadow xtr', 'nomad gt',
                                    'karnage 7c', 'voodoo', 'grace gt', 'shark gt', 'patron gt', 'warrior',
                                    'flanker f', 'spaceknight', 'black jack x150'])  # все в lower!!!!!!!
    img_f = FileField('Загрузите изображение', validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                                                       'Файл должен иметь разрешение jpg/png/jpeg'),
                                                           FileSize(0.5 * 1024 * 1024, 0,
                                                                    "Размер файла не должен превышать 512КБ")])
    file = FileField('Загрузите файл', validators=[FileRequired("Это поле обязательно"),
                                                   FileAllowed(['knd'], 'Файл должен иметь разрешение knd'),
                                                   FileSize(0.5 * 1024 * 1024, 0,
                                                            "Размер файла не должен превышать 512КБ")])


class Vins(FlaskForm):
    ct = StringField(validators=[InputRequired()],
                     render_kw={'style': "width:202px; height:50;", "placeholder": "Введите название автомобиля"})


@app.route('/login', methods=['GET', 'POST'])
def login():
    from data.usrs import User
    form = LoginForm()
    if form.validate_on_submit():
        pswd_name_check = db_sess.query(User).all()
        flg_p = 0
        p_f = 0
        lst = []
        for i in pswd_name_check:
            if not check_password_hash(i.hashed_password, request.form['password_l']) or request.form['username_l'] != i.name:
                flg_p = 1
            elif check_password_hash(i.hashed_password, request.form['password_l']) and request.form['username_l'] == i.name:
                flg_p = 0
                break
        if flg_p == 1:
            flash("Неверное имя пользователя или пароль")
            p_f = 1
        if p_f == 0:
            session['name'] = request.form['username_l']
            return redirect('/')
    return render_template('lg.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def reg():
    from data.usrs import User
    form = RegForm()
    if form.validate_on_submit():
        p_f = 0
        name_check = db_sess.query(User).all()
        if request.form['username'] in [i.name for i in name_check]:
            flash(f'Пользователь с таким именем уже зарегестрирован')
            p_f = 1
        for el in request.form['username']:
            if el in " *?!'^+%&;/()=}][{$#":
                flash(f'Логин не должен содержать символ "{el}"')
                p_f = 1
                break
        if len(request.form["username"]) < 3:
            flash("Длина логина должна быть больше 3 символов")
            p_f = 1
        if len(request.form["username"]) > 10:
            flash("Длина логина должна быть меньше 10 символов")
            p_f = 1
        if len(request.form['password']) < 6:
            flash("Длина пароля должна быть больше 6 символов")
            p_f = 1
        if True not in [True if i in request.form['password'] else False for i in "1234567890"]:
            p_f = 1
            flash("Пароль должен содержать цифры")
        if request.form['password'].lower() == request.form['password'] or request.form['password'] == request.form[
            'password'].upper():
            flash("Пароль должен содержать буквы разных регистров")
            p_f = 1
        if request.form['password'] != request.form['c_password']:
            flash("Пароли не совпадают")
            p_f = 1
        if p_f == 0:
            user = User()
            user.name = request.form['username']
            user.hashed_password = generate_password_hash(request.form['password'])
            user.created_date = datetime.date.today()
            db_sess.add(user)
            db_sess.commit()
            session['name'] = request.form['username']
            return redirect('/')

    return render_template('reg.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def start():
    return redirect("/news/1")


@app.route('/news/<num>', methods=['GET', 'POST'])
def main(num):
    from data.news import News
    dbg = db_sess.query(News).all()
    res = dbg[::-1][int(num) - 1]
    cd = str(res.created_date.strftime('%d, %b %Y'))
    file = f"static/img/news/{res.id}.jpg"
    can_del = False
    try:
        if session["name"] == "tehno_py" or session["name"] == "ya_lyceum":
            can_del = True
    except KeyError:
        pass
    if not os.path.exists(file):
        file = 0
    if (int(num) - 1) < (len(dbg) - 1):
        return render_template('news.html', fut=int(num) + 1, last=int(num) - 1, num=num, title=res.title,
                               desc=res.description, dt=cd, file=file, can_del=can_del, idd=res.id)
    else:
        return render_template('news.html', fut=505, last=int(num) - 1, num=int(num), title=res.title,
                               desc=res.description, dt=cd, file=file, can_del=can_del, idd=res.id)


@app.route('/vinils/<num>', methods=['GET', 'POST'])
def vinils(num):
    from data.vins import Vinils
    form = Vins()
    ct = None
    if form.validate_on_submit():
        ct = request.form['ct'].lower()
        num = 1
    dbg = db_sess.query(Vinils).all()
    ress = dbg[::-1]
    res = []
    for i in range(len(ress)):
        if ress[i].car_type == ct:
            res.append(ress[i])
    if not res and ct is None:
        res = ress
    ln = len(res)
    res = res[int(num) - 1]
    cd = str(res.created_date.strftime('%d, %b %Y'))
    img_f = f"static/img/vins/imgs/{res.id}.jpg"
    file = f"static/img/vins/knvis/{res.id}.knvis"
    can_del = False
    try:
        if session["name"] == res.user or session["name"] == "tehno_py" or session["name"] == "ya_lyceum":
            can_del = True
    except KeyError:
        pass
    if (int(num) - 1) < (ln - 1):
        return render_template('vin.html', fut=int(num) + 1, last=int(num) - 1, num=num, name=res.name,
                               desc=res.description, dt=cd, car=res.car_type, form=form, usr=res.user, img_f=img_f,
                               file=file, can_del=can_del, idd=res.id)
    else:
        return render_template('vin.html', fut=505, last=int(num) - 1, num=int(num), name=res.name,
                               desc=res.description, dt=cd, car=res.car_type, form=form, usr=res.user, img_f=img_f,
                               file=file, can_del=can_del, idd=res.id)


@app.route('/tuning/<num>', methods=['GET', 'POST'])
def tun(num):
    from data.tuns import Tuns
    form = Vins()
    ct = None
    if form.validate_on_submit():
        ct = request.form['ct'].lower()
        num = 1
    dbg = db_sess.query(Tuns).all()
    ress = dbg[::-1]
    res = []
    for i in range(len(ress)):
        if ress[i].car_type == ct:
            res.append(ress[i])
    if not res and ct is None:
        res = ress
    ln = len(res)
    res = res[int(num) - 1]
    cd = str(res.created_date.strftime('%d, %b %Y'))
    img_f = f"static/img/tunes/imgs/{res.id}.jpg"
    if not os.path.exists(img_f):
        img_f = 0
    file = f"static/img/tunes/knd/{res.id}.knd"
    can_del = False
    try:
        if session["name"] == res.user or session["name"] == "tehno_py" or session["name"] == "ya_lyceum":
            can_del = True
    except KeyError:
        pass
    if (int(num) - 1) < (ln - 1):
        return render_template('tun.html', fut=int(num) + 1, last=int(num) - 1, num=num, name=res.name,
                               desc=res.description, dt=cd, car=res.car_type, form=form, usr=res.user, img_f=img_f,
                               file=file, can_del=can_del, idd=res.id)
    else:
        return render_template('tun.html', fut=505, last=int(num) - 1, num=int(num), name=res.name,
                               desc=res.description, dt=cd, car=res.car_type, form=form, usr=res.user, img_f=img_f,
                               file=file, can_del=can_del, idd=res.id)
   

@socketio.on('message')
def handleMessage(dat):
        global ch_lst
        send(dat, broadcast=True)
        from data.messages import Msg
        message = Msg(user=dat['username'], message=dat['msg'])
        db_sess.add(message)
        db_sess.commit()


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    from data.messages import Msg
    get_all = db_sess.query(Msg).all()
    lst = []
    for el in get_all:
        lst.append(f'<li><strong>{el.user}:</strong> {el.message}</li>')
    if session.get("name"):
        return render_template('chat.html', username=session.get("name"), msgs="".join(lst), session=session)
    else:
        return redirect("login")


@app.route('/rules', methods=['GET', 'POST'])
def rules():
    return render_template('rules.html')


@app.route('/profile')
def acc():
    try:
        return render_template('acc.html', nme=session["name"], fl=0)
    except KeyError:
        return render_template('acc.html', nme="Гость", fl=1)


@app.route('/add_news', methods=['GET', 'POST'])
def add_n():
    from data.news import News
    form = add_news()
    eflg = 0
    sug = False
    if form.validate_on_submit():
        if len(request.form['title']) < 3:
            flash("Длина заголовка должна быть больше 3 символов")
            eflg = 1
        if len(request.form['description']) < 10:
            flash("Длина новости должна быть не меньше 10 символов")
            eflg = 1
        if eflg == 0:
            news = News(title=request.form['title'], description=request.form['description'],
                        created_date=datetime.date.today())
            db_sess.add(news)
            db_sess.commit()
            dbg = db_sess.query(News).all()
            for i in dbg:
                if i == news:
                    try:
                        form.file.data.save(f'static/img/news/{i.id}.jpg')
                        break
                    except AttributeError:
                        pass
            sug = True
            return redirect("/done")
    return render_template('ad_news.html', form=form, sug=sug)


@app.route("/add_vinils", methods=['GET', 'POST'])
def adv():
    form = add_vinils()
    eflg = 0
    sug = False
    if form.validate_on_submit():
        if len(request.form['name']) < 3:
            flash("Длина имени винила должна быть больше 3 символов")
            eflg = 1
        if len(request.form['description']) < 10:
            flash("Длина описания должна быть не меньше 10 символов")
            eflg = 1
        if eflg == 0:
            from data.vins import Vinils
            sug = True
            vins = Vinils(user=session["name"], name=request.form['name'], description=request.form['description'],
                          car_type=request.form['car_type'], created_date=datetime.date.today())
            db_sess.add(vins)
            db_sess.commit()
            dbg = db_sess.query(Vinils).all()
            for i in dbg:
                if i == vins:
                    try:
                        form.file.data.save(f'static/img/vins/knvis/{i.id}.knvis')
                        form.img_f.data.save(f'static/img/vins/imgs/{i.id}.jpg')
                        break
                    except AttributeError:
                        pass
            return redirect("/done")
    return render_template('ad_vins.html', form=form, sug=sug)


@app.route("/add_tuning", methods=['GET', 'POST'])
def ad_t():
    form = add_tuns()
    eflg = 0
    sug = False
    if form.validate_on_submit():
        if len(request.form['name']) < 3:
            flash("Длина названия тюнинга должна быть больше 3 символов")
            eflg = 1
        if len(request.form['description']) < 10:
            flash("Длина описания должна быть не меньше 10 символов")
            eflg = 1
        if eflg == 0:
            from data.tuns import Tuns
            sug = True
            vins = Tuns(user=session["name"], name=request.form['name'], description=request.form['description'],
                          car_type=request.form['car_type'], created_date=datetime.date.today())
            db_sess.add(vins)
            db_sess.commit()
            dbg = db_sess.query(Tuns).all()
            for i in dbg:
                if i == vins:
                    try:
                        form.file.data.save(f'static/img/tunes/knd/{i.id}.knd')
                        form.img_f.data.save(f'static/img/tunes/imgs/{i.id}.jpg')
                        break
                    except AttributeError:
                        pass
            return redirect("/done")
    return render_template('ad_tuns.html', form=form, sug=sug)


@app.route("/done")
def dn():
    return render_template('done.html')


@app.route('/tuning/delete/<idd>', methods=['GET', 'POST'])
def delete_t(idd):
    from data.tuns import Tuns
    db_sess = db_session.create_session()
    itm = db_sess.query(Tuns).filter(Tuns.id == int(idd), Tuns.user == session["name"]).first()
    if itm:
        db_sess.delete(itm)
        db_sess.commit()
        os.remove(f'static/img/tunes/knd/{idd}.knd')
        if os.path.exists(f"static/img/tunes/imgs/{idd}.jpg"):
            os.remove(f"static/img/tunes/imgs/{idd}.jpg")
        return redirect("/done")
    elif session['name'] == 'tehno_py' or session["name"] == "ya_lyceum":
        db_sess.delete(db_sess.query(Tuns).filter(Tuns.id == int(idd)).first())
        db_sess.commit()
        os.remove(f"static/img/tunes/knd/{idd}.knd")
        if os.path.exists(f"static/img/tunes/imgs/{idd}.jpg"):
            os.remove(f"static/img/tunes/imgs/{idd}.jpg")
        return redirect("/done")


@app.route('/vinils/delete/<idd>', methods=['GET', 'POST'])
def delete_v(idd):
    from data.vins import Vinils
    db_sess = db_session.create_session()
    itm = db_sess.query(Vinils).filter(Vinils.id == int(idd), Vinils.user == session["name"]).first()
    if itm:
        db_sess.delete(itm)
        db_sess.commit()
        os.remove(f"static/img/vins/knvis/{idd}.knvis")
        os.remove(f"static/img/vins/imgs/{idd}.jpg")
        return redirect("/done")
    elif session['name'] == 'tehno_py' or session["name"] == "ya_lyceum":
        db_sess.delete(db_sess.query(Vinils).filter(Vinils.id == int(idd)).first())
        db_sess.commit()
        os.remove(f"static/img/vins/knvis/{idd}.knvis")
        os.remove(f"static/img/vins/imgs/{idd}.jpg")
        return redirect("/done")


@app.route('/news/delete/<idd>', methods=['GET', 'POST'])
def delete_n(idd):
    from data.news import News
    db_sess = db_session.create_session()
    itm = db_sess.query(News).filter(News.id == int(idd)).first()
    if itm:
        db_sess.delete(itm)
        db_sess.commit()
        if os.path.exists(f"static/img/news/{idd}.jpg"):
            os.remove(f"static/img/news/{idd}.jpg")
        return redirect("/done")


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("name")
    return redirect("/login")


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=8080)


#акк яндекса
#логин ya_lyceum
#пароль Kbwtqkbwtq22
