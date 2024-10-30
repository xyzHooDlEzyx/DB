from my_project.auth.DAO.models import Card
from extensions import db

class CardService:
    @staticmethod
    def get_all_cards():
        return Card.query.all()

    @staticmethod
    def get_card_by_id(card_id):
        return Card.query.get(card_id)

    @staticmethod
    def create_card(data):
        new_card = Card(
            AccountID=data['AccountID'],
            CardNumber=data['CardNumber'],
            ExpiryDate=data['ExpiryDate'],
            CardType=data['CardType']
        )
        db.session.add(new_card)
        db.session.commit()
        return new_card

    @staticmethod
    def update_card(card_id, data):
        card = Card.query.get(card_id)
        if card:
            card.ExpiryDate = data['ExpiryDate']
            card.CardType = data['CardType']
            db.session.commit()
            return card
        return None

    @staticmethod
    def delete_card(card_id):
        card = Card.query.get(card_id)
        if card:
            db.session.delete(card)
            db.session.commit()
            return card
        return None
