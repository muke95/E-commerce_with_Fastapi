from routers import users , products , categories  , auth , carts ,categories
from fastapi import FastAPI


description = """
Welcome to the E-commerce API! 🚀

This API provides a comprehensive set of functionalities for managing your e-commerce platform.

Key features include:

- **Crud**
	- Create, Read, Update, and Delete endpoints.
- **Search**
	- Find specific information with parameters and pagination.
- **Auth**
	- Verify user/system identity.
	- Secure with Access and Refresh tokens.
- **Permission**
	- Assign roles with specific permissions.
	- Different access levels for User/Admin.
- **Validation**
	- Ensure accurate and secure input data.


For any inquiries, please contact:

* Github: https://github.com/
"""

app = FastAPI(
    title="E-commerce API",
    version="1.0.0",
    description=description,
    contact={
        "name": "Mukesh Patanwar",
        "url": "https://yourwebsite.com",  # Optional
        "email": "mukesh@example.com",     # Replace with your real contact
    },
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "layout": "BaseLayout",
        "filter": True,
        "tryItOutEnabled": True,
        "onComplete": "Ok"
    },
)
@app.get("/")
def start():
    return {"hello":"dh"}

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(carts.router)
app.include_router(users.router)
# app.include_router(accounts.router)
app.include_router(auth.router)
