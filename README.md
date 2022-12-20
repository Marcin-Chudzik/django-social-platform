# Social platform

This app is a simple example of a social platform, built in Python/Django.
Main functionalities in the project:
- register and login by django forms.
- login by using Facebook or Google account (only with runserver_plus).
- notifications system.
- messages which inform user about actions on the account like a password change or publishing an image.
- followings and followers system.
- profile details are editable.
- resetting and changing an account password.
- bookmarklet which we can save in our Internet browser and use on any website to immediately publish a new image.
- liking an images.


## How to run

1. Using a GIT write the command.
    ``` bash
    git clone https://github.com/Marcin-Chudzik/django-social-platform.git
    ```

2. Create a new virtual environment.<br>
   Open a repository in the code editor (I'm using Pycharm).<br>
   Open a terminal and being in the "django-social-platform" directory type a command:
    ``` python
    python.exe -m venv venv
    ```

3. Activate a new venv, change directory on "bookmarks" and use command.
    ``` python
    pip install -r requirements.txt
    ```

4. Create a new text file ".env" in the "bookmarks" directory and write there.<br>(value of a SECRET_KEY can be a whatever else)
    ``` text
    SECRET_KEY=saduoanwodmawdmwioaiome2iomd2m1
    ```
5. Make a migrations and apply them into database, by typing followed commands into the terminal:
    ``` python
    python.exe .\manage.py makemigrations
    ```
    then
    ``` python
    python.exe .\manage.py migrate
    ```

6. Create a new superuser. Type command and follow the displayed instructions:
    ``` python
    python.exe .\manage.py createsuperuser
    ```

7. Run a project with followed command:
    ``` python
    python.exe .\manage.py runserver_plus --cert-file cert.crt
    ```
   **!IMPORTANT!** If you get an error like this one below:
   ``` commandline
   Traceback (most recent call last):
     File "C:\Users\Marcin-Chudzik\Desktop\django-social-platform\bookmarks\manage.py", line 22, in <module>
       main()
     File "C:\Users\Marcin-Chudzik\Desktop\django-social-platform\bookmarks\manage.py", line 18, in main
       execute_from_command_line(sys.argv)
     File "C:\Users\Marcin-Chudzik\Desktop\django-social-platform\venv\lib\site-packages\django\core\management\__init__.py", line 446, in execute_from_command_line
       utility.execute()
     File "C:\Users\Marcin-Chudzik\Desktop\django-social-platform\venv\lib\site-packages\django\core\management\__init__.py", line 440, in execute
       self.fetch_command(subcommand).run_from_argv(self.argv)
     File "C:\Users\Marcin-Chudzik\Desktop\django-social-platform\venv\lib\site-packages\django\core\management\__init__.py", line 279, in fetch_command
       klass = load_command_class(app_name, subcommand)
     File "C:\Users\Marcin-Chudzik\Desktop\django-social-platform\venv\lib\site-packages\django\core\management\__init__.py", line 49, in load_command_class
       return module.Command()
     File "C:\Users\Marcin-Chudzik\Desktop\django-social-platform\venv\lib\site-packages\django\core\management\base.py", line 274, in __init__
       raise TypeError("requires_system_checks must be a list or tuple.")
   TypeError: requires_system_checks must be a list or tuple.
   ```
   Just go to the "django-social-platform\venv\lib\site-packages\django\core\management\base.py"
   and add one line of code marked with arrow below:
   ``` python 
    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.stdout = OutputWrapper(stdout or sys.stdout)
        self.stderr = OutputWrapper(stderr or sys.stderr)
    --> self.requires_system_checks = []
        if no_color and force_color:
            raise CommandError("'no_color' and 'force_color' can't be used together.")
        if no_color:
            self.style = no_style()
        else:
            self.style = color_style(force_color)
            self.stderr.style_func = self.style.ERROR
        if (
            not isinstance(self.requires_system_checks, (list, tuple))
            and self.requires_system_checks != ALL_CHECKS
        ):
            raise TypeError("requires_system_checks must be a list or tuple.")
   ```

8. Register your account, login and check the project -> <a href="http://127.0.0.1:8000/account/login/">Check</a>