from odoo_rpc_client import Client as OdooClient
import odoorpc
import logging
import xmlrpc

# from odoo_app.settings import ODOO_DB, ODOO_HOST, ODOO_PASS, ODOO_PORT, ODOO_USER

def get_odoo():
    return odoorpc.ODOO(host=ODOO_HOST)

def get_db():
    try:
        odoo = odoorpc.ODOO(host=ODOO_HOST)  
    except Exception as e:
        print(e)
        return [False]
    return odoo.db.list()

def get_user():
    odoo = get_odoo()
    try:
        odoo.login(ODOO_DB, ODOO_USER, ODOO_PASS)
        user = odoo.env.user
        res = {
            'user_name':user.name,
            'company':user.company_id.name
        }
    except:
        res = {
            'response':'Not be able to login'
        }
    return res
    
def get_project():
    odoo = get_odoo()
    try:
        odoo.login(ODOO_DB, ODOO_USER, ODOO_PASS)
        res = []
        if 'project.project' in odoo.env:
            project = odoo.env['project.project'].search([])
            for pr in project:
                project_rec = odoo.env['project.project'].browse(pr)
                res.append({pr:project_rec.name})
    except:
        res.append('Project not found')
    return res    

def create_project(name=None):
    odoo = get_odoo()
    odoo.login(ODOO_DB, ODOO_USER, ODOO_PASS)
    values = {
        'name':name
    }
    if 'project.project' in odoo.env:
        project = odoo.env['project.project']
        project.create(values)
    return True

def get_project_task(param):
    if id:
        odoo = get_odoo()
        res = {}
        odoo.login(ODOO_DB, ODOO_USER, ODOO_PASS)
        pname = param.get('pname', None)
        pid = param.get('pid', None)
        if pname:
            try:
                pid = odoo.env['project.project'].search([('name', '=', pname)])[0]
                ptask = odoo.env['project.task'].search([('display_project_id', '=', pid)])
            except:
                res.append('Project Not found')
        else:
            try:
                ptask = odoo.env['project.task'].search([('display_project_id', '=', pid)])
            except:
                res.append('Project not fount')
        res.append({'count':len(ptask)})
        if not len(ptask):
            res.append('Task not found')
        else:
            for task in ptask:
                task_rec = odoo.env['project.task'].browse(task)
                result = {
                    'project_id':pid,
                    'project_name': pname,
                    'task_id':task,
                    'task_name': task_rec.name
                }
                res.append(result)
    return res if id else []

def create_project_task(param):
    odoo = get_odoo()
    res = []
    odoo.login(ODOO_DB, ODOO_USER, ODOO_PASS)
    pname = param.get('pname', None)
    tname = param.get('tname', None)
    pid = int(param.get('pid', None))
    if pname:
        pid = odoo.env['project.project'].search([('name', '=', pname)])[0]
    values ={
        'name':tname,
        'project_id':pid,
        'display_project_id':pid
    }
    if 'project.task' in odoo.env:
        task = odoo.env['project.task']
        task.create(values)
    return True
    
def update_project(pname=None, newName=None):
    odoo = get_odoo()
    odoo.login(ODOO_DB, ODOO_USER, ODOO_PASS)
    res = []
    project = odoo.env['project.project'].search([('name', '=', pname)])
    pid = project[0] if project else None 
    if not pid:
        res.append('Project does not exist...')
    else:
        if 'project.project' in odoo.env:
            project = odoo.env['project.project'].browse(pid)
            project.name = newName
        res.append('Project updated successfully..')
    return res        

    
def get_good_dict(values):
    d = DictNoNone()
    for k in values:
        if values[k]:
            d.update({k: values[k]})
    return dict(d)

class DictNoNone(dict):
    def __setitem__(self, key, value):
        if value:
            dict.__setitem__(self, key, value)