from my_project.auth.DAO.models import BankDetail
from extensions import db

class BankDetailService:
    @staticmethod
    def get_all_bankdetails():
        return BankDetail.query.all()

    @staticmethod
    def get_bankdetail_by_id(bankdetail_id):
        return BankDetail.query.get(bankdetail_id)

    @staticmethod
    def create_bankdetail(data):
        new_bankdetail = BankDetail(
            CustomerID=data['CustomerID'],
            BankName=data['BankName'],
            BankCode=data['BankCode'],
            CardID=data['CardID']
        )
        db.session.add(new_bankdetail)
        db.session.commit()
        return new_bankdetail

    @staticmethod
    def update_bankdetail(bankdetail_id, data):
        bankdetail = BankDetail.query.get(bankdetail_id)
        if bankdetail:
            bankdetail.BankName = data['BankName']
            bankdetail.BankCode = data['BankCode']
            bankdetail.CardID = data['CardID']
            db.session.commit()
            return bankdetail
        return None

    @staticmethod
    def delete_bankdetail(bankdetail_id):
        bankdetail = BankDetail.query.get(bankdetail_id)
        if bankdetail:
            db.session.delete(bankdetail)
            db.session.commit()
            return bankdetail
        return None
