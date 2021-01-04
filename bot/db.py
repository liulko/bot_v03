import pymysql
import pymysql.cursors
import config
#6N9A7pHy96Ecd3iN
# Подключиться к базе данных.
connection = pymysql.connect(host='localhost',
                             user='yuri',
                             password='6N9A7pHy96Ecd3iN',
                             db='db_test2',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print("connect successful!!")
question = connection.cursor()
answers = connection.cursor()
def getTable():
    try:
        with connection.cursor():
                # SQl
                questionsql = "SELECT question FROM " + config.name
                answerssql = "SELECT id,ans1,ans2,ans3,ans4,trueans FROM " + config.name
                # Выполнить команду запроса (Execute Query).
                question.execute(questionsql)
                answers.execute(answerssql)

            #
            # print("cursor.description: ", cursor.description)
            #
            # print()
            #
            # for row in cursor:
            #     print(row)

    finally:
        # Закрыть соединение (Close connection).
        connection.close()