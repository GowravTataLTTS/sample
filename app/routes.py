from flask import Blueprint, request, jsonify
from app import db
from app.models import Account

bp = Blueprint("api", __name__)

@bp.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = Account.query.all()
    return jsonify([account.__dict__ for account in accounts])

@bp.route("/accounts/<account_number>", methods=["GET"])
def get_account(account_number):
    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account.__dict__)

@bp.route("/accounts", methods=["POST"])
def create_account():
    data = request.json
    account_number = data.get("account_number")
    if not account_number:
        return jsonify({"error": "Missing account_number"}), 400
    
    account = Account(account_number=account_number)
    db.session.add(account)
    db.session.commit()
    
    return jsonify(account.__dict__), 201

@bp.route("/accounts/<account_number>/deposit", methods=["POST"])
def deposit(account_number):
    data = request.json
    amount = data.get("amount")
    if not amount:
        return jsonify({"error": "Missing amount"}), 400

    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    account.balance += amount
    db.session.commit()
    
    return jsonify(account.__dict__)

@bp.route("/accounts/<account_number>/withdraw", methods=["POST"])
def withdraw(account_number):
    data = request.json
    amount = data.get("amount")
    if not amount:
        return jsonify({"error": "Missing amount"}), 400

    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    if account.balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    
    account.balance -= amount
    db.session.commit()
    
    return jsonify(account.__dict__)
