# vedomosti

The project is meant to be ran on Linux Ubuntu 22.10

## Deployment method:
1. Download the source code from the repository.
2. cd \<project directory\>
3. source vedomosti/bin/activate
4. cd vedsite/
5. python manage.py migrate
6. python manage.py runserver (add 0.0.0.0:8000 next to the line in order to expose the server to foreign connections, if needed).
