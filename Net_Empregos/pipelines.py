import mysql.connector
from Net_Empregos.items import NetEmpregosItem



class NetEmpregosPipeline:
    def process_item(self, item, spider):
        #print(item)

        self.save_myslq(item)

    def save_myslq(self, item):


        db_connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="998674629Th.",
        database="Scrapy_Empregos"
        )

        if db_connection.is_connected():
            print("Conexão com o banco de dados está ativa.")
        else:
            print("Conexão com o banco de dados falhou.")

        cursor = db_connection.cursor()

        cursor.execute(
           '''CREATE TABLE IF NOT EXISTS Empregos(
            Name VARCHAR(200),
            Description LONGTEXT,
            Organization VARCHAR(100),
            Location VARCHAR(100),
            Ref LONGTEXT
            );''' 
        )

        db_connection.commit()      

        insert_query = """
                        INSERT INTO  Empregos(Name, Description, Organization, Location, Ref)
                        VALUES (%s, %s, %s, %s, %s)"""
        

        cursor.execute(insert_query, (
            item["Name"],
            item["Organization"],
            item["Location"],
            item["Ref"],
            item["Description"]
        ))

        db_connection.commit()
        print("Dados salvos com sucesso!")

        cursor.close()
        db_connection.close()
