from rest_framework.views import APIView
from odoo_app.xmlrpc_odoo import OdooWrapper, Odoo
from rest_framework.response import Response

odoo = OdooWrapper()
class Company(APIView):
    status = "Failed"
    msg = ''
    data = []

    def post(self, request):
        try:
            odoo.create_company(request.data)
            self.status = "Success"
            self.msg = "Record Created Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def get(self, request, id=None):
        try:
            if id:
                self.data = odoo.read_company(id)
            else:
                self.data = odoo.list_company()
            self.status = "Success"
            self.msg = "Record Retrived Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg, "data": self.data})

    def delete(self, request, id):
        try:
            odoo.delete_company(id)
            self.status = "Success"
            self.msg = "Record Deleted Successfully"
        except Exception as e:
            self.msg = str(e)
        return  Response({"status": self.status, "msg": self.msg})

    def put(self, request, id):
        try:
            odoo.update_company(id, request.data)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return  Response({"status": self.status, "msg": self.msg})


class Contact(APIView):
    status = "Failed"
    msg = ''
    data = []

    def post(self, request):
        try:
            odoo.create_contact(request.data)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def get(self, request, id=None):
        try:
            if id:
                self.data = odoo.read_contact(id)
            else:
                self.data = odoo.list_contact()
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def delete(self, request, id):
        try:
            odoo.delete_contact(id)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def put(self, request, id):
        try:
            odoo.update_contact(id, request.data)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})


class Project(APIView):
    status = "Failed"
    msg = ''
    data = []

    def post(self, request):
        try:
            res = odoo.create_project(request.data)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def get(self, request, id=None):
        try:
            if id:
                self.data = odoo.read_project(id)
            else:
                self.data = odoo.list_project()
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg, "data": self.data})

    def delete(self, request, id):
        try:
            odoo.delete_project(id)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def put(self, request, id):
        try:
            odoo.update_project(id, request.data)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})


class Task(APIView):
    status = "Failed"
    msg = ''
    data = []

    def post(self, request):
        try:
            odoo.create_task(request.data)
            self.status = "Success"
            self.msg = "Record created successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def get(self, request, id=None):
        try:
            if id:
                self.data = odoo.read_task(id)
            else:
                self.data = odoo.list_task()
            self.status = "Success"
            self.msg = "Record retrieved successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg, "data": self.data})

    def delete(self, request, id):
        try:
            odoo.delete_task(id)
            self.status = "Success"
            self.msg = "Record deleted successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def put(self, request, id):
        try:
            odoo.update_task(id, request.data)
            self.status = "Success"
            self.msg = "Record updated successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})


class Lookups(APIView):
    status = "Failed"
    msg = ""
    data = []
    model = ""

    def get(self, request):
        try:
            self.model = request.GET.get('model')
            self.data = odoo.lookups(self.model)
            self.status = "Success"
            self.msg = "Record retrieved successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg, "data": self.data})


class User(APIView):
    status = "Failed"
    msg = ''
    data = []
    model = "res.users"
    odoo = Odoo()

    def post(self, request):
        try:
            res = odoo.create(self.model, request.data)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def get(self, request, id=None):
        try:
            if id:
                self.data = odoo.read(self.model, id)
            else:
                models = odoo.conn("object")
                ids = models.execute_kw(odoo.db, odoo.uid(), odoo.password, self.model, "search", [[["name", "!=", ""]]])
                self.data = odoo.read(self.model, [ids])
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg, "data": self.data})

    def delete(self, request, id):
        try:
            odoo.delete(self.model)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

    def put(self, request, id):
        try:
            odoo.update(self.model, id, request.data)
            self.status = "Success"
            self.msg = "Record Updated Successfully"
        except Exception as e:
            self.msg = str(e)
        return Response({"status": self.status, "msg": self.msg})

