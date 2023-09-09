from flask import Blueprint, request, jsonify
from database import db
from models.payment import Payment

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/api/payment/save-payment', methods=['POST'])
def save_payment():
    try:
        data = request.get_json()
        product = data['product']
        amount = data['amount']
        status = data['status']  # Não é mais boolean, mas sim uma string
        name = data['customerName']
        cpf = data['customerCPF']
        # Antes de salvar o CPF no banco de dados, remova pontos e hífens e garanta 11 dígitos
        cpf = ''.join(filter(str.isdigit, data['customerCPF']))
        cpf = cpf.zfill(11)
        orderNumber = data['orderNumber']
        new_payment = Payment(product=product, amount=amount, status=status, name=name, cpf=cpf, orderNumber=orderNumber)
        db.session.add(new_payment)
        db.session.commit()

        print(f"Payment saved - Product: {product}, Amount: {amount}, Status: {status}, Name: {name}, CPF: {cpf}, Order Number: {orderNumber}")

        return jsonify({'message': 'Payment saved successfully'}), 200
    except Exception as e:
        print(f"Error saving payment: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500
    # Sua função save_payment aqui...

@payment_bp.route('/api/payment/update-status/<orderNumber>', methods=['PUT'])
def update_payment_status(orderNumber):
    try:
        data = request.get_json()
        new_status = data['status']

        payment = Payment.query.filter_by(orderNumber=orderNumber).first()
        if payment:
            payment.status = new_status
            db.session.commit()
            print(f"Payment status updated to: {new_status}")
            return jsonify({'message': 'Payment status updated successfully'}), 200
        else:
            return jsonify({'error': 'Payment not found'}), 404
    except Exception as e:
        print(f"Error updating payment status: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@payment_bp.route('/api/payment/get-payments', methods=['GET'])
def get_payments():
    try:
        payments = Payment.query.all()
        payment_list = []
        for payment in payments:
            payment_data = {
                'orderNumber': payment.orderNumber,
                'product': payment.product,
                'amount': payment.amount,
                'status': payment.status,
                'name': payment.name,  # Adicione o campo 'name'
                'cpf': payment.cpf      # Adicione o campo 'cpf'
            }
            payment_list.append(payment_data)
        return jsonify(payment_list)
    except Exception as e:
        print(f"Error getting payments: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

