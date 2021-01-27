import mysql.connector


class ConnectionError(Exception):
    pass


class CredentialsError(Exception):
    pass


class SQLError(Exception):
    pass


class UseDatabase:
    def __init__(self, config: dict) -> None:
        '''Инициализация'''
        self.configuration = config
        # Параметры входа
    def __enter__(self) -> 'cursor':
        '''Подключение к ДБ с возвращением курсора'''
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()  # Подключение к ДБ
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError(err)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        '''Параметры выхода или уборка'''
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is mysql.connector.errors.ProgrammingError:  # Если возникло ProgrammingError возбудить SQLError
            raise SQLError(exc_val)
        elif exc_type:  # elif повторно возбудит любое другое исключение которое может возникнуть (доп защита)
            raise exc_type(exc_val)
