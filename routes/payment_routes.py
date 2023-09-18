from flask import Blueprint, request, jsonify
from database import db
from models.payment import Payment

# Cria um Blueprint para rotas relacionadas a pagamentos
payment_bp = Blueprint('payment', __name__)

# Rota para salvar um pagamento
@payment_bp.route('/api/payment/save-payment', methods=['POST'])
def save_payment():
    try:
        data = request.get_json()
        product = data['product']
        amount = data['amount']
        status = data['status']  
        name = data['customerName']
        cpf = data['customerCPF']
        
        # Antes de salvar o CPF no banco de dados, remova pontos e hífens e garanta 11 dígitos
        cpf = ''.join(filter(str.isdigit, data['customerCPF']))
        cpf = cpf.zfill(11)
        orderNumber = data['orderNumber']
        
        # Cria um novo objeto de pagamento
        new_payment = Payment(product=product, amount=amount, status=status, name=name, cpf=cpf, orderNumber=orderNumber)
        
        # Adiciona o novo pagamento ao banco de dados e faz o commit
        db.session.add(new_payment)
        db.session.commit()

        print(f"Payment saved - Product: {product}, Amount: {amount}, Status: {status}, Name: {name}, CPF: {cpf}, Order Number: {orderNumber}")

        return jsonify({'message': 'Payment saved successfully'}), 200
    except Exception as e:
        print(f"Error saving payment: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

# Rota para atualizar o status de um pagamento
@payment_bp.route('/api/payment/update-status/<orderNumber>', methods=['PUT'])
def update_payment_status(orderNumber):
    try:
        data = request.get_json()
        new_status = data['status']

        # Encontra o pagamento pelo número do pedido
        payment = Payment.query.filter_by(orderNumber=orderNumber).first()
        
        if payment:
            # Atualiza o status do pagamento e faz o commit
            payment.status = new_status
            db.session.commit()
            print(f"Payment status updated to: {new_status}")
            return jsonify({'message': 'Payment status updated successfully'}), 200
        else:
            return jsonify({'error': 'Payment not found'}), 404
    except Exception as e:
        print(f"Error updating payment status: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

# Rota para excluir um pagamento
@payment_bp.route('/api/payment/delete-payment/<orderNumber>', methods=['DELETE'])
def delete_payment(orderNumber):
    try:
        payment = Payment.query.filter_by(orderNumber=orderNumber).first()
        
        if payment:
            # Exclui o pagamento e faz o commit
            db.session.delete(payment)
            db.session.commit()
            print(f"Payment with Order Number {orderNumber} deleted successfully")
            return jsonify({'message': f'Payment with Order Number {orderNumber} deleted successfully'}), 200
        else:
            return jsonify({'error': 'Payment not found'}), 404
    except Exception as e:
        print(f"Error deleting payment: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

# Rota para obter a lista de pagamentos
@payment_bp.route('/api/payment/get-payments', methods=['GET'])
def get_payments():
    try:
        # Consulta todos os pagamentos no banco de dados
        payments = Payment.query.all()
        payment_list = []
        for payment in payments:
            payment_data = {
                'orderNumber': payment.orderNumber,
                'product': payment.product,
                'amount': payment.amount,
                'status': payment.status,
                'name': payment.name, 
                'cpf': payment.cpf      
            }
            payment_list.append(payment_data)
        return jsonify(payment_list)
    except Exception as e:
        print(f"Error getting payments: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500
