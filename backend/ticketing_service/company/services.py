from injector import inject
from .repositories import CompanyRepository
from rest_framework.exceptions import NotFound
from .models import Company  
from users_management.repositories import UserRepository
from rest_framework.response import Response
from rest_framework import status
class CompanyService:
    @inject
    def __init__(self, CompanyRepository: CompanyRepository):
        self.CompanyRepository = CompanyRepository
              

    def list_company(self):
        return self.CompanyRepository.get_all_company()

    def create_company(self, name, address, email):
        try:
        
            return self.CompanyRepository.create_company(name,address,email)
        except Exception as e:
            raise e
    
    def update_company(self, company_id, validated_data):
        try:
            company = self.CompanyRepository.get_company_by_id(company_id)
 
        except Company.DoesNotExist:
            raise NotFound("Company not found")
        return self.CompanyRepository.update_company(company, validated_data)

    def delete_company(self, company_id):
        try: 
            company = self.CompanyRepository.get_company_by_id(company_id)
 
        except Company.DoesNotExist:
            raise NotFound("Company not found")
        self.CompanyRepository.delete_company(company)    

    def search_company(self, company_id):
        try:
             company= self.CompanyRepository.get_company_by_id(company_id)
        except Company.DoesNotExist:
            raise NotFound("Company not found")
        return company
   
   

    def get_company_by_email(self,email):
        try:
             company= self.CompanyRepository.get_company_by_email(email)
        except Company.DoesNotExist:
            raise NotFound("Company not found")
        return company
    
    
    def toggle_auto_prioritize(self, company_id: int) -> Company:
        company = self.CompanyRepository.get_company_by_id(company_id)
        return self.CompanyRepository.toggle_auto_prioritize(company)

    def toggle_auto_categorize(self, company_id: int) -> Company:
        company = self.CompanyRepository.get_company_by_id(company_id)
        return self.CompanyRepository.toggle_auto_categorize(company)
    
    def toggle_auto_Assign(self, company_id: int) -> Company:
        company = self.CompanyRepository.get_company_by_id(company_id)
        return self.CompanyRepository.toggle_auto_Assign(company)