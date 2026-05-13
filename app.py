from flask import Flask, request, jsonify
from database import SessionLocal, init_db
from models import Student, Books, Transaction
from datetime import datetime,timedelta, UTC

app = Flask(__name__)

# creates table when the app starts
with app.app_context():
    init_db()


# --- Routes ---

@app.route("/",methods=["GET"])
def home():
    return {"message":"Welcome to my Flask App"}

@app.route("/borrow",methods=['POST'])
def borrow_book():
    data = request.json
    session = SessionLocal()

    try:
        student = session.query(Student).filter_by(
            id = data["student_id"]
        ).first()
        if not student:
            return jsonify({
                "error":"Student not found"
            })

        book = session.query(Books).filter_by(
            id = data["book_id"]
        ).first()
        if not book:
            return jsonify({
                "error":"Book Not Found"
            }),404
        if book.available_books <=0:
            return jsonify({
                "error":"No Copies Available"
            }),400
        book.available_books-=1

        new_loan = Transaction(
            student_id=data["student_id"],
            book_id=data["book_id"],
            return_date = datetime.now(UTC)+timedelta(days=10)
        )
        session.add(new_loan)
        session.commit()
        return jsonify({"message":"Book borrowed successfully!"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error":str(e)}),400
    finally:
        session.close()

@app.route("/books",methods=['GET','POST'])
def books():
    if request.method == 'POST':
        data = request.json
        session = SessionLocal()
        try:
            new_book = Books(
                title=data["title"],
                author=data["author"],
                total_books=data["total_books"],
                available_books = data["available_books"]
            )
            session.add(new_book)
            session.commit()

            return jsonify({
                "message":f"Book '{new_book.title}' added !",
                "id":new_book.id
            }), 201
        except Exception as e:
            session.rollback()
            return jsonify({"error":str(e)}),400
        finally:
            session.close()
    else:
        session = SessionLocal()
        try:
            books=session.query(Books).all()
            output=[
                {
                    "id": b.id,
                    "title": b.title,
                    "author": b.author,
                    "total_books": b.total_books,
                    "available_books": b.available_books
                }
                for b in books
            ]

            return jsonify(output)
        finally:
            session.close()


@app.route("/students",methods=['GET','POST'])
def student():
    if request.method == 'POST':
        data = request.json
        session = SessionLocal()
        try:
            new_student = Student(
                name = data["name"],
                email = data["email"],
                phone_number = data['phone_number']
            )
            session.add(new_student)
            session.commit()
            return jsonify({
                "message":f"Student '{new_student.name}' added!",
                "id":new_student.id
            }), 201
        except Exception as e:
            session.rollback()
            return jsonify({
                "error":str(e)
            }), 400
        finally:
            session.close()
    else:
        session = SessionLocal()
        students = session.query(Student).all()
        output=[
            {
                "id":s.id,
                "name":s.name,
                "email":s.email,
                "phone_number":s.phone_number
            }
            for s in students
        ]
        session.close()
        return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)