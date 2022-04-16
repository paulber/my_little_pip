import sys
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox


def initiate_thumbnail():

    database = QSqlDatabase.addDatabase("QSQLITE")  # SQLite version 3
    database.setDatabaseName("bin/pip_db/functions.db")

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1)  # Error code 1 - signifies error

    tables_needed = {'functions'}

    if tables_not_found := tables_needed - set(database.tables()):
        QMessageBox.Icon.critical(None, 'Error',
                                  f'The following tables tables are missing from the database: {tables_not_found}')
        sys.exit(1)  # Error code 1 - signifies error

    query = QSqlQuery()
    query.exec("SELECT name_id, symbol, number_input, number_output FROM functions")

    return query

def find_import_list_for_gui(gui_name : str):

    database = QSqlDatabase.addDatabase("QSQLITE")  # SQLite version 3
    database.setDatabaseName("bin/pip_db/functions.db")

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1)  # Error code 1 - signifies error

    tables_needed = {'imports'}

    if tables_not_found := tables_needed - set(database.tables()):
        QMessageBox.Icon.critical(None, 'Error',
                                  f'The following tables tables are missing from the database: {tables_not_found}')
        sys.exit(1)  # Error code 1 - signifies error

    query = QSqlQuery()
    print(gui_name)
    query.exec("SELECT import_functions FROM imports WHERE GUI = '" + gui_name + "'")

    return query
