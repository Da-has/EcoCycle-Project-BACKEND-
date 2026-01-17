from config import create_app, db

app = create_app()

@app.route('/')
def index():
    return {"message": "EcoCycle API running"}

if __name__ == '__main__':
    app.run(debug=True)
