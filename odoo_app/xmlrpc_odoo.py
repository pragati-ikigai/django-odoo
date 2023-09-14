import xmlrpc.client
from django.conf import settings


class Odoo():

    def __init__(self):
        self.host = settings.ODOO_ADDRESS
        self.db = settings.ODOO_DB
        self.username = settings.ODOO_USER
        self.password = settings.ODOO_PASS

    def conn(self, str="common"):
        try:
            return xmlrpc.client.ServerProxy(f"{self.host}/xmlrpc/2/{str}")
        except Exception as e: 
            print('conn', e)

    def uid(self):
        info = self.conn()
        return info.authenticate(self.db, self.username, self.password, {})

    def create(self, model, data):
        models = self.conn("object")
        return models.execute_kw(self.db, self.uid(), self.password, model, "create", [data])

    def delete(self, model, id):
        models = self.conn("object")
        return models.execute_kw(self.db, self.uid(), self.password, model, "unlink", [[id]])

    def read(self, model, id, fields = None):
        models = self.conn("object")
        return (
            models.execute_kw(
                self.db,
                self.uid(),
                self.password,
                model,
                "read",
                id,
                {"fields": fields},
            )
            if fields
            else models.execute_kw(
                self.db, self.uid(), self.password, model, "read", id
            )
        )

    def update(self, model, id, data):
        models = self.conn("object")
        return models.execute_kw(self.db, self.uid(), self.password, model, "write", [[id], data])

    def search(self, model, str):
        models = self.conn("object")
        return models.execute_kw(self.db, self.uid(), self.password, model, "search", str)

    def lookups(self, model):
        models = self.conn("object")
        return models.execute_kw(self.db, self.uid(), self.password, model, 'fields_get', [], {'attributes': ['string', 'help', 'type']})

class OdooWrapper(Odoo):
    COMPANY = "res.company"
    TASK = "project.task"
    PROJECT = "project.project"
    PARTNER = "res.partner"
    COUNTRY = "res.country"
    STATE = "res.country.state"
    CURRENCY = "res.currency"

    def __init__(self):
        super().__init__()
    
    ###############################################
    ######## FUNCTION RELATED TO COMPANY ##########
    ###############################################

    def create_company(self, data):
        if data.get("parent", None):
            str = [[["name", "=", data["parent"]]]]
            company = self.search(self.COMPANY, str)
            if company:
                data["parent_id"] = company[0]
            data.pop('parent')

        if data.get("country", None):
            str = [[["name", "=", data["country"]]]]
            country = self.search(self.COUNTRY, str)
            if country:
                data["country_id"] = country[0]
            data.pop('country')

        if data.get("state", None):
            str = [[["name", "=", data["state"]]]]
            state = self.search(self.STATE, str)
            if state:
                data["state_id"] = state[0]
            data.pop('state')
        
        if data.get("currency", None):
            str = [[["name", "=", data["currency"]]]]
            currency = self.search(self.CURRENCY, str)
            if currency:
                data["currency_id"] = currency[0]
            data.pop('currency')
        
        return self.create(self.COMPANY, data)

    def read_company(self,ids=None):
        if type(ids) != list:
            ids = [ids]
        fields = ["name", "street", "street2", "city", "state_id", "zip", "vat", "phone", "mobile", "email", "website", "country_id"]

        return self.read(self.COMPANY, ids, fields)

    def list_company(self):
        models = self.conn("object")
        ids = models.execute_kw(self.db, self.uid(), self.password, self.COMPANY, "search", [[["name", "!=", ""]]])
        fields = ["name", "street", "street2", "city", "state_id", "zip", "vat", "phone", "mobile", "email", "website", "country_id"]

        return self.read(self.COMPANY, [ids])

    def delete_company(self, id):
        return self.delete(self.COMPANY, id)

    def update_company(self, id, data):
        return self.update(self.COMPANY, id, data)


    ###############################################
    ######## FUNCTION RELATED TO CONTACT #########
    ##############################################

    def create_contact(self, data):
        if data.get("parent", None):
            strng = [[["name", "=", data["parent"]]]]
            if company := self.search(self.COMPANY, strng):
                data["parent_id"] = company[0]
            data.pop('parent')

        if data.get("country", None):
            strng = [[["name", "=", data["country"]]]]
            if country := self.search(self.COUNTRY, strng):
                data["country_id"] = country[0]
            data.pop('country')

        if data.get("state", None):
            strng = [[["name", "=", data["state"]]]]
            if state := self.search(self.STATE, strng):
                data["state_id"] = state[0]
            data.pop('state')

        return self.create(self.PARTNER, data)

    def read_contact(self, ids):
        if type(ids) != list:
            ids = [ids]
        fields = ["name", "street", "street2", "city", "state_id", "zip", "vat", "phone", "mobile", "email", "website", "country_id"]

        return self.read(self.PARTNER, ids, fields)

    def list_contact(self):
        models =  self.conn("object")
        ids = models.execute_kw(self.db, self.uid(), self.password, self.PARTNER, "search", [[["name", "!=", ""]]])

        return self.read(self.PARTNER, [ids])

    def delete_contact(self, id):
        return self.delete(self.PARTNER, id)

    def update_contact(self, id, data):
        return self.update(self.PARTNER, id, data)


    ############################################
    ######## FUNCTION RELATED TO PROJECT ##########
    ###########################################

    def create_project(self, data):
        if data.get("project", None):
            str = [[["name", "=", data["project"]]]]
            project = self.search(self.PROJECT, str)
            data["project_id"] = project

        if data.get("company", None):
            str = [[["name", "=", data["company"]], ["is_company", "=", True]]]
            company = self.search(self.COMPANY, str)
            data["company_id"] = company

        if data.get("partner", None):
            str = [[["name", "=", data["partner"]], ["is_company", "=", True]]]
            partner = self.search(self.PARTNER, str)
            data["partner_id"] = partner
        
        return self.create(self.PROJECT, data)

    def read_project(self, ids):
        if type(ids) != list:
            ids = [ids]
        fields = ["name", "project_id", "partner_id", "company_id", "user_ids", "planned_date_begin", "planned_date_end", "date_deadline", "tag_ids"]

        return self.read(self.PROJECT, ids, fields)

    def list_project(self):
        models = self.conn("object")
        ids = models.execute_kw(self.db, self.uid(), self.password, self.TASK, "search", [[["name", "!=", ""]]])

        return self.read(self.PROJECT, [ids])

    def delete_project(self, id):
        return self.delete(self.PROJECT, id)

    def update_project(self, id, data):
        return self.update(self.PROJECT, id, data)


    ############################################
    ######## FUNCTION RELATED TO TASK ##########
    ###########################################

    def create_task(self, data):
        if data.get("project", None):
            str = [[["name", "=", data["project"]]]]
            project = self.search(self.PROJECT, str)
            data["project_id"] = project

        if data.get("company", None):
            str = [[["name", "=", data["company"]], ["is_company", "=", True]]]
            company = self.search(self.COMPANY, str)
            data["company_id"] = company

        if data.get("partner", None):
            str = [[["name", "=", data["partner"]], ["is_company", "=", True]]]
            partner = self.search(self.PARTNER, str)
            data["partner_id"] = partner
        
        return self.create(self.TASK, data)

    def read_task(self, ids):
        if type(ids) != list:
            ids = [ids]
        fields = ["name", "project_id", "partner_id", "company_id", "user_ids", "planned_date_begin", "planned_date_end", "date_deadline", "tag_ids"]

        return self.read(self.TASK, ids, fields)

    def list_task(self):
        models = self.conn("object")
        ids = models.execute_kw(self.db, self.uid(), self.password, self.TASK, "search", [[["name", "!=", ""]]])

        return self.read(self.TASK, [ids])

    def delete_task(self, id):
        return self.delete(self.TASK, id)

    def update_task(self, id, data):
        return self.update(self.TASK, id, data)


