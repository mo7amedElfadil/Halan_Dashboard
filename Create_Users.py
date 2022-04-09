from Halanweb import db,bcrypt
from Halanweb.models import User


User.__table__.drop(db.engine)
db.create_all()
 

admin =User(username='admin',email='admin@halan.com',image_file="default.jpg" ,password=bcrypt.generate_password_hash('admin').decode('utf-8'),role="admin")
db.session.add(admin)
db.session.commit()

Ceo =User(username='Ceo',email='Ceo@halan.com',image_file="default.jpg",password=bcrypt.generate_password_hash('Ceo').decode('utf-8'), role='Upper Management')
db.session.add(Ceo)
db.session.commit()


Gm =User(username='Gm',email='Gm@halan.com',image_file="default.jpg",password=bcrypt.generate_password_hash('Gm').decode('utf-8'), role='Upper Management')
db.session.add(Gm)
db.session.commit()

Op =User(username='Op',email='Op@halan.com',image_file="default.jpg",password=bcrypt.generate_password_hash('Op').decode('utf-8'),role='Operations Manager')
db.session.add(Op)
db.session.commit()


Ds =User(username='Ds',email='Ds@halan.com',image_file="default.jpg",password=bcrypt.generate_password_hash('Ds').decode('utf-8'),role='Drivers Supervisor')
db.session.add(Ds)
db.session.commit()


Deo =User(username='Deo',email='Deo@halan.com',image_file="default.jpg",password=bcrypt.generate_password_hash('Deo').decode('utf-8'),role='Data Entry Officer')
db.session.add(Deo)
db.session.commit()

