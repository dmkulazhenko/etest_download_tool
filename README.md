# ETest Download Tool

Tool for students of [BSMU](https://www.bsmu.by/),
which can download lectures from [Moodle-ETest](http://etest.bsmu.by/login/index.php).

***

## Deployment

### Requirements
* Docker

### FAST! How to start app?
Configure app using ``.env`` file, example: ``example.env``.
File structure described above.
* ``etest_download_tool $> MIGRATE=true docker-compose up --build``
  — build + start + migrate db.
* ``etest_download_tool $> docker-compose up --build``
  — build + start + run migrations, if something new added to ``migrations``.
* ``etest_download_tool $> docker-compouse up``
  — start + run migrations, if something new added to ``migrations``.
  
  
### OK! Now tell me the story...
#### Env vars for docker:
* MIGRATE — Optional[bool] (true/false/none) if ``true`` — DB migrations will
  be executed on start up.
  
#### Configuration files
* ``.env`` — credentials / secret keys.
  If you don't want to use ``.env`` file — just use environment variables.
* ``etest_download/config.py`` — config for main flask-app.
* ``etest_worker/config.py`` — config for ETest API Client.
* ``edt.sh`` — start script, you can modify workers/threads num.

#### ``.env`` / environment variables structure
* SECRET_KEY = secret-key-for-flask-tools

* MYSQL_ROOT_PASSWORD = password-for-root-user-of-database
* MYSQL_USER = username-of-edt-database-user
* MYSQL_DATABASE = database-name-for-edt
* MYSQL_PASSWORD = password-of-edt-database-user

To use ``.env`` file configuration – create file ``.env`` in project root dir.
Example of ``.env`` file — ``example.env``

***

### Main points:
* Authorize to edt service via your credentials for BSMU ETest.
* !WARNING! Your credentials will be saved as plain text to DB,
  this is necessary in order to authorize in ETest.
* If your password for ETest changed:
  * Login to service via your old password;
  * Update your password to new.
