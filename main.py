import sys
sys.path.append('/opt/odoo15')
import datetime

from odoo import fields
from odoo.http import db_monodb, request, root
from odoo.service import security
from pydantic import BaseModel  # Import BaseModel from Pydantic

# from odoo.addons.base_rest import restapi
# from odoo.addons.component.core import Component


from routers import secure, public
from fastapi import FastAPI,Depends, HTTPException, Query
from auth import get_user


import odoo
from odoo.api import Environment
# untuk operasi file
from contextlib import contextmanager

app = FastAPI()
app.include_router(
    public.router,
    prefix="/api/v1/public"
)
app.include_router(
    secure.router,
    prefix="/api/v1/secure",
    dependencies=[Depends(get_user)]
)
    
    

    
odoo.tools.config.parse_config(['--config=/etc/odoo/odoo15.conf'])

@contextmanager




def odoo_env() -> Environment:
    """Set up Odoo Environment."""
    # Initialize registry
    registry = odoo.registry(odoo.tools.config['db_name']).check_signaling()
    with registry.manage_changes():
        with registry.cursor() as cr:
            yield Environment(cr, odoo.SUPERUSER_ID, {})

class SQLQuery(BaseModel):
    query: str            
            
@app.post("/execute_sql")
def execute_sql(sql_query: SQLQuery):
    """Execute a SQL query against the Odoo database."""
    with odoo_env() as env:
        try:
            # Get the cursor from the environment
            cr = env.cr
            # Execute the SQL query
            cr.execute(sql_query.query)
            # Fetch all results
            results = cr.fetchall()
            # Get column names
            columns = [desc[0] for desc in cr.description]
            # Format results as a list of dictionaries
            formatted_results = [dict(zip(columns, row)) for row in results]
            return {"results": formatted_results}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
                

@app.get("/users/{user_id}")
def get_user(user_id: int, user: dict = Depends(get_user)):
    """Fetch user details from Odoo."""
    with odoo_env() as env:
        Users = env['res.users']
        user = Users.browse(user_id)
        if not user.exists():
            return {"error": "User not found"}
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }


@app.get("/apikey/{user_id}")
def get_apikey(user_id: int):
    """Fetch user details from Odoo."""
    with odoo_env() as env:
        Apikeys = env['auth.api.key']
        apikey = Apikeys.browse(user_id)
        if not apikey.exists():
            return {"error": "User not found"}
        return {
            "id": apikey.id,
            "name": apikey.name,
            "key": apikey.key,
        }
        


# @app.get("/")
# async def root():
#   return {"message": "Hello World"}

# @app.get("/endpointname")
# async def function_name():
#   return {"message": "Write your message here"}
