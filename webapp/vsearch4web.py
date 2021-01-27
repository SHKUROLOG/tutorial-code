from flask import Flask, render_template, request, escape, session
from vsearch import search4letters
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
from checker import check_logged_in

app = Flask(__name__)

app.config['dbconfig'] = {'host': '**',
                          'user': '**',
                          'password': '**',
                          'database': 'vsearchlogDB', }


def log_request(req: 'flask_request', res: str) -> None:
    '''Журналирует запросы и возвращает результаты'''
    # установили параметры соедениения
    with UseDatabase(app.config['dbconfig']) as cursor:
        # импорт драйвера, установка соедениения, создание курсора
        _SQL = """insert into log
        (phrase, letters, ip, browser_string, results)
        values
        (%s, %s, %s, %s, %s)"""
        # str text -> db
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res,))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    '''Страница результатов'''
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    try:
        log_request(request, results)
    except Exception as err:
        print('*****Logging failed with this error:', str(err))
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results, )


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


@app.route('/login')
def do_login() -> str:
    '''Проверка ключа в списке'''
    session['logged_in'] = True
    return 'You are now logged in'


@app.route('/logout')
def do_logout() -> str:
    '''Удаление ключа из спика session'''
    session.pop('logged_in')
    return 'You are now logged out'


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    '''Функция отправляющая SQL запросы, полученные данные показывает на стр.viewlog в таблице'''
    try:
        with UseDatabase(app.config['dbconfig']) as cursor: # Управление контекстом при помощи класса UseDatabase
            _SQL = """select phrase, letters, ip, browser_string, results
            from log"""  # данная стр указывает на дб
            cursor.execute(_SQL)
            contents = cursor.fetchall()
            titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='view log',
                               the_row_titles=titles,
                               the_data=contents, )
    except ConnectionError as err:
        print('Is your database switched on? Error:', str(err))
    except CredentialsError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))


app.secret_key = '***'

if __name__ == '__main__':
    app.run(debug=True)
