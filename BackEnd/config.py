# Connecting the flask with my local SQL db i created  {Bada Abdulrahman}
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:january07W@localhost/ceoldhut"
    SQLALCHEMY_TRACK_MODIFICATIONS = False