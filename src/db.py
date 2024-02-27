from firebase_admin import credentials, db, initialize_app

class DB:
    def __init__(self, database_url, credentials_path):
        creds = credentials.Certificate(credentials_path)
        initialize_app(creds, {'databaseURL': database_url})
        self.db = db

    def insert(self, path, data):
        ref = self.db.reference(path)
        ref.push(data)
        print(f"inserted {data} at {path}")
    
    def get(self, path):
        ref = self.db.reference(path)
        return ref.get()