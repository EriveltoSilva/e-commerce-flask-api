# e-commerce-flask-api

- Create database
```bash
flask shell
db.create_all()
db.session.commit()
exit()
```

- Update database
```bash
flask shell
db.drop_all()
db.create_all()
db.session.commit()
exit()
```