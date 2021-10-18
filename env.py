host = "157.230.209.171"
username = "germain_1467"
password = "8A486YgW1XMLedoP5mgqBlgw0L3NKoNC"

def get_db_url(username,password,host,db_name):
    return f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
