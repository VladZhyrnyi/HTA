from app import db, create_app

db.create_all(app=create_app())

create_app().run(debug=True)