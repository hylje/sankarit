import psycopg2

def get_cursor(app):
    return psycopg2.connect(
        username=app.config["PG_USERNAME"],
        password=app.config["PG_PASSWORD"],
        database=app.config["PG_DATABASE"]
    ).cursor()
