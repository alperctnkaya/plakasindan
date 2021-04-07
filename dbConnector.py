from mysql.connector import connect, Error

class dbConnector:
    def __init__(self, host, user, password, dbName):
        try:
            self.connection = connect(host=host, user=user, password=password, db=dbName)
        except Error as e:
            print(e)

        self.cursor = self.connection.cursor(buffered=True)

    def execute(self, command):
        self.cursor.execute(command)
        if "select" in command:
            result = self.cursor.fetchall()
            return result

        elif "insert" in command:
            self.connection.commit()


class queries:
    def __init__(self):
        self.advTable = "advertisements"
        self.brandTreeTable = "brandTree"
        self.urlsToScrapTable = "urls"
        self.trChars = {'ç':'c', 'Ç':'C', 'ğ':'g', 'Ğ':'G', 'ı':'i', 'İ':'I', 'ö':'o', 'Ö':'O', 'ş':'s', 'Ş':'S', 'ü':'u', 'Ü':'U'}

    def insertAd(self, ad):
        columnNames = ""
        values = ''
        for column in vars(ad):
            columnNames += column + ","
            values += '"' + str(vars(ad)[column]) + '"' + ","

        columnNames = columnNames[:-1]
        values = values[:-1]
        for char in self.trChars:
            values = values.replace(char, self.trChars[char])

        sql = "insert into {} ({}) values({})".format(self.advTable, columnNames, values)

        return sql

