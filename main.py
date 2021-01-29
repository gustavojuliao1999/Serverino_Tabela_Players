import valve.source
import valve.source.a2s
import valve.source.master_server
import os
from requests import get
import mysql.connector
#pip install mysql-connector-python.
from datetime import datetime
import time
try:
  import discord
except ImportError:
  print ("Trying to Install required module: discord\n")
  os.system('py -3 -m pip install -U discord.py')

ext_ip = get('http://meuip.com/api/meuip.php').text
print(ext_ip)

print ("Checking in from IP#: %s " % ext_ip)


def usuarios():
    users = []
    with valve.source.master_server.MasterServerQuerier() as msq:
        #address = ('179.210.86.67', 27016)
        address = (ext_ip, 27016)
        try:
            with valve.source.a2s.ServerQuerier(address) as server:
                print(str(address))
                info = server.info()
                players = server.players()
                for player in sorted(players["players"],
                                 key=lambda p: p["score"], reverse=True):
                    play = ("{name}".format(**player))
                    users.append(play)
                    print("play")

        except valve.source.NoResponseError:
            print("Server {}:{} timed out!".format(*address))

        print("{player_count}/{max_players} {server_name}".format(**info))
    print(users)
    return users
def send_ip():
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%Y-%m-%d %H:%M:%S')
    print(data_e_hora_em_texto)

    mydb = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    mycursor = mydb.cursor()
    ext_ip = get('http://meuip.com/api/meuip.php').text

    sql = "INSERT INTO ip_server (ipv4, data) VALUES (%s, %s)"
    val = (ext_ip, data_e_hora_em_texto)
    mycursor.execute(sql, val)
    mydb.commit()

    #Discord Send New IP

    client = discord.Client()

    async def on_ready():
        await client.wait_until_ready()
        conselho = client.get_channel(287685479057588225)
        await conselho.send("Ip Servidor ")
        await conselho.send(ext_ip)
    client.loop.create_task(on_ready())
    client.run('')

def send_db(users):
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%Y-%m-%d %H:%M:%S')
    print(data_e_hora_em_texto)

    mydb = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    mycursor = mydb.cursor()
    for x in users:
        sql = "INSERT INTO players_online (quantidade_online, data_hora) VALUES (%s, %s)"
        val = (x, data_e_hora_em_texto)
        mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")
while True:
    send_db(usuarios())
    ext_ip2 = get('http://meuip.com/api/meuip.php').text
    if ext_ip != ext_ip2:
        send_ip()
        ext_ip = ext_ip2
    time.sleep(300)