import sqlite3

# ==> DESCOMENTE APENAS O CÓDIGO QUE IRÁ RODAR.

# Cria o banco de dados 'records.sqlite3' e a tabela 'records'.
"""
con = sqlite3.connect('records.sqlite3')
cur = con.cursor()
cur.execute("CREATE TABLE records (record TEXT, pontuação INTEGER)")
cur.execute("INSERT INTO records VALUES('recorde', 0)")
con.commit()
con.close()
"""

# Zera o recorde salvo.
"""
con = sqlite3.connect('records.sqlite3')
cur = con.cursor()
cur.execute("UPDATE records SET pontuação=0 WHERE record='recorde'")
con.commit()
con.close()
"""
