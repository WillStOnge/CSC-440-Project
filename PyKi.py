from wiki import create_app
import os


directory = os.getcwd()
app = create_app(directory)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)