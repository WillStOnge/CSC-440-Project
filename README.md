Riki is the version that is modified to be executed from Ubuntu server. 
You can use PyCharm and command line tools to start the Flask/Wiki system with “python Riki.py”.
You can access the wiki [http://wiki440.ms2ms.com](http://wiki440.ms2ms.com).

## Configuration
    
1. Update CONTENT_DIR and USER_DIR in config.py. 
    * CONTENT_DIR should point to the directory where your `content' is located.
    * USER_DIR should point to the directory where your `user' is located.
2. When you want to use login, make PRIVATE = True in config.py. Remember you can use id "name" and password "1234".
3. Always use virtualenv and pip.
    * pip install -r requirements.txt

## Additional Features

1. Moved the user file to a sqllite database using pyodbc for database agnosticism.
2. Added roles so user's access (editing, deleting, etc.) can be limited.
3. Added tags so pages can be categorized.
4. Allow users to upload files to the server.
5. Allow images to be added to and displayed on page.

## Authors
1. Alexander Jung-Loddenkemper (original author)
2. [Will Sie](https://github.com/Willsie) (team leader)
3. [Will St. Onge](https://github.com/WillStOnge)
4. [Cory Knoll](https://github.com/kryptonianCodeMonkey/)
5. [Justin Gallagher](https://github.com/ThisJustin-code)
6. [Anthony Bosch](https://github.com/boscha1)
