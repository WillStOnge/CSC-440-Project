Riki is the version that is modified to be executed from Ubuntu server. 
You can use PyCharm and command line tools to start the Flask/Wiki system with “python Riki.py”.
You can access the wiki [http://wiki440.ms2ms.com](http://wiki440.ms2ms.com).

## Configuration
    
1. Update CONTENT_DIR in config.py. 
    * CONTENT_DIR should point to the directory where your `content` is located.
2. When you want to use login, make PRIVATE = True in config.py.
3. Install requirements using `pip install -r requirements.txt`

## Additional Features

1. Moved the user file to a sqlite database using pyodbc for database agnosticism.
2. Added roles so a user's access can be limited.
3. Implement blank routes in routes.py.
4. Allow users to upload files to the server.
5. Allow images to be added to and displayed on pages.

## Authors
1. Alexander Jung-Loddenkemper (original author)
2. [Anthony Bosch](https://github.com/boscha1) (team leader)
3. [Will Sie](https://github.com/Willsie)
4. [Will St. Onge](https://github.com/WillStOnge)
5. [Cory Knoll](https://github.com/kryptonianCodeMonkey/)
6. [Justin Gallagher](https://github.com/ThisJustin-code)
