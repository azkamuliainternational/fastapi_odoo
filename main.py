import sys
sys.path.append('/opt/odoo15')


from routers import secure, public
from fastapi import FastAPI,Depends
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



# def odoo_env() -> Environment:
#     """Set up Odoo Environment."""
#     # Initialize registry
#     registry = odoo.registry(odoo.tools.config['db_name']).check_signaling()
#     with registry.manage_changes():
#         with registry.cursor() as cr:
#             yield Environment(cr, odoo.SUPERUSER_ID, {})

# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     """Fetch user details from Odoo."""
#     with odoo_env() as env:
#         Users = env['res.users']
#         user = Users.browse(user_id)
#         if not user.exists():
#             return {"error": "User not found"}
#         return {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email,
#         }



@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/endpointname")
async def function_name():
  return {"message": "Write your message here"}
