from app import db


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100))
    amount = db.Column(db.Float)
    status = db.Column(db.String(100))  # Alterado para campo de texto
    name = db.Column(db.String(100))
    cpf = db.Column(db.String(11))
    orderNumber = db.Column(db.String(10))  # Adicionado campo orderNumber

    def __init__(self, product, amount, status, name, cpf, orderNumber):
        self.product = product
        self.amount = amount
        self.status = status
        self.name = name
        self.cpf = cpf
        self.orderNumber = orderNumber
