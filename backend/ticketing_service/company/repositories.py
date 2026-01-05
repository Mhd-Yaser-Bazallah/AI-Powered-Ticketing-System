 
from injector import inject
from .models import Company  
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

class CompanyRepository:
    @inject

    def create_company(self ,name , address, email) -> Company:
        company = Company(name=name, address=address, email=email)
        company.save()
        return company
    

    def get_all_company(self) -> QuerySet:
        return Company.objects.all().order_by('created_at')
    
    def get_company_by_id(self, Company_id: int) -> Company:
 
        return Company.objects.get(id=Company_id)
         


    def get_company_by_email(self, email: str) -> Company:
        company= Company.objects.get(email=email) 
  
        return company
        
    def update_company(self, company: Company, updated_data: dict) -> Company:
        for attr, value in updated_data.items():
            setattr(company, attr, value)
        company.save()
        return company

    def delete_company(self, company: Company) -> None:
        company.delete()   
    
    def toggle_auto_prioritize(self, company: Company) -> Company:
        company.auto_prioritize = not company.auto_prioritize
        company.save()
        return company

    def toggle_auto_categorize(self, company: Company) -> Company:
        company.auto_categorize = not company.auto_categorize
        company.save()
        return company
    
    def toggle_auto_Assign(self, company: Company) -> Company:
        company.auto_assign = not company.auto_assign
        company.save()
        return company