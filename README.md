

## Project installation and running
1. Start Redis server on your computer on on the default port (6379)
1. in root folder "final" run `pipenv shell`
2. in root folder "final" run `pipenv install`
3. in root folder "final" run `cd final_main_root`
4. in "final_main_root" folder run `python manage.py runserver`
5. open a separate new terminal in root folder "final", run `pipenv shell` to get into virtual environment. Change directory to "final_main_root" by running `cd final_main_root`. Then in "final_main_root" folder
    run `celery -A final_main worker -l INFO`

## Notes
- *Redis server software is required to run on the computer on the default port (6379) for celery tasks to do async image processing and for channels for chat.*
- This UoL tutor tutorial was used in setting up the project https://pedbad.hashnode.dev/getting-started-with-django
- pipenv is the virtual environment package used. use pipenv shell to enter virtual environment, install packages using requirements.txt and then start celery in a seperate terminal.
- Run redis server software on the computer on the default port (6379) for celery workers to do async image processing. 
- **The image uploaded for user profile photo has to be jpeg format, only jpeg accepted.** 
- Command to run celery for async tasks: celery -A final_main worker -l INFO     (https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)
- cd into final_main (root) and start the celery python package in a seperate terminal in the root. This is for image processing.
- cd into final_main (root) and then run "python manage.py runserver" in the pipenv shell, to start django server http://127.0.0.1:8000/.
- create a new user at http://127.0.0.1:8000/register/ and then login http://127.0.0.1:8000/login/
- You can then test the chat by creating a new room, and using the url in incognito and normal browser. python channels package is used for chat.
- you can upload media at http://127.0.0.1:8000/media/ which will run a celery async worker to resize the image. **The image uploaded for user profile photo has to be jpeg format, only jpeg accepted.** 
- there is a full git commit history
- there are also tests you can run with manage.py
- unit test can be run with `python manage.py test`. 
- python manage.py seed final_main_app --number=100    (this is used to populate the database with dummy data)