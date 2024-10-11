import wrds
db = wrds.Connection(wrds_username='ejchung')
db.create_pgpass_file()
db.close()
db = wrds.Connection(wrds_username='joe')
db.close()