Installation


Clone repository 
```bash
git clone https://gitlab.com/Myortv/test-task.git  
```

Create virtual envirement
```bash
python -m venv env
```

Activate envirement
```bash
. env/bin/activate
```

Install dependendencies
```bash
pip install -r test-task/req.txt
```

You need to install Postgres somehow. Follow guides for your linux destribution or official guide
https://www.postgresql.org/docs/current/installation.html
Also arch wiki link:
https://wiki.archlinux.org/title/PostgreSQL

You also need to get Prometheus, but it is optional. Here an download link:
https://prometheus.io/download/ 



You need to specify your envirement variables to get things done. I leave file called env.sh in root of repo.

```sh
export POSTGRES_HOST='127.0.0.1'
export POSTGRES_USER='postgres'
export POSTGRES_PASSWORD='postgres'
export POSTGRES_DB='mailing'
export OAUTHDOMAIN=''
export OAUTHAUDIENCE=''
export MAILING_SERVER_URL=''
export AUTHTOKEN=''
export LOGGING_FILE=''
```

If you fresh install postgres locally, you should not change next lines:

```sh
export postgres_host='127.0.0.1'
export postgres_user='postgres'
export postgres_password='postgres'
export postgres_db='mailing'
```

It is oauth0 dependency. Follow oauth0 guides to obtaing domain and audience.

```sh
export OAUTHDOMAIN=''
export OAUTHAUDIENCE=''
```

Add url to endpont recieve messages

```sh
export MAILING_SERVER_URL=''
```

JWT token from recieving message service

```sh
export AUTHTOKEN=''
```

Path to your logging file. It is must be file, not derictory

```sh
export LOGGING_FILE=''
```



And, last thing you need is create postgres database.
I leave database dump with schema, for fast cration of new database.

```sh
psql mailing < test-task/mailing.sql
```

Now, just run
```sh
uvicorn app.main:app
```



Tasks done:
1. Tests. (they can be runned, but i make totally 0 tests, but pytest runs well)
5. Swagger 
7. Oauth0 integration
9. Exception handling
10. Prometheus-formatted data output
11. Additional buisness logic
12. Logging

