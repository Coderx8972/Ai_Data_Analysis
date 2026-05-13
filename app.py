from flask import Flask, request, jsonify
from database import SessionLocal, init_db
from models import Student, Books, Transaction
from datetime import datetime,timedelta

app = Flask(__name__)

# creates table when the app starts
with app.app_context():
    init_db()

@app.teardown_appcontext
def shutdown_session(exception=None): # closes the session after each request
    session = SessionLocal()
    session.close()

# --- Routes ---

@app.route("/",methods=["GET"])
def home():
    return {"message":"Welcome to my Flask App"}

@app.route("/borrow",methods=['POST'])
def borrow_book():
    data = request.json
    session = SessionLocal()

    try:
        new_loan = Transaction(
            student_id=data["student_id"],
            book_id=data["book_id"]
        )
        session.add(new_loan)
        session.commit()
        return jsonify({"message":"Book borrowed successfully!"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error":str(e)}),400
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)