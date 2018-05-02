# Installation

- First, `cd` into the `phealth-backup`

```

cd phealth-backup

```

- Next, activate the virtualenv

```
workon django

```

- After this, do a `git pull`

```

git pull origin dev --rebase

```

- After this restart the gunicorn processes

```
sudo killall gunicorn
cd phealth/phealth
gunicorn 

```

- Last (_optional_) Restart nginx

```
sudo nginx -s reload

```


