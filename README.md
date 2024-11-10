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
user = User(full_name="Erivelto Silva", email="eriveltoclenio@gmail.com", username="admin", password="admin@1234")
db.session.add(user)
db.session.commit()
exit()
```