# API Delivery Pizza

This API is built with FastAPI. It uses Pydantic models, has a secure authentication system and implements SQLAlchemy for database management. It is fast and has everything you need to manage a delivery system.

## Quickstart

First of all, clone this repo.

``
git clone https://github.com/DD21S/api-delivery-pizza.git
``

Create a file with the name ``.env`` and set the environment variables. In this way:

	USER_DATABASE=username
	PASSWORD_DATABASE=123456789
	HOST_DATABASE=localhost
	NAME_DATABASE=delivery-pizza
	SECRET_KEY=YOUR_SECRET_KEY

Then, you install the requirements.

``
pip install -r requirements.txt
``

Run the API:

``
uvicorn main:app --reload
``

Ready, now your API is running :&#41;

---

It's recommended to use a virtual enviroment to run Python web applications.

Create one with this command:

``
python3 -m venv venv
``

## Routes

| **METHOD**  | **ROUTE**                | **FUNCTIONALITY**              | **ACCESS**  |
| ----------- | ------------------------ | ------------------------------ | ----------- |
| **POST**    | /auth/signup             | Create a new user              | All         |
| **POST**    | /auth/createsuperuser    | Create a new superuser         | All (SK)    |
| **POST**    | /auth/login              | Login						  | All         |
| **GET**     | /orders                  | Displays all orders placed     | User        |
| **POST**    | /orders				     | Create a new order             | User        |
| **PUT**     | /orders/{order_id}       | Edit the order                 | User        |
| **DELETE**  | /orders/{order_id}       | Delete the order               | User        |
| **GET**     | /admin/orders            | Displays all orders            | Superuser   |
| **DELETE**  | /admin/orders/{order_id} | Delete any order               | Superuser   |
| **PATCH**   | /admin/orders/{order_id} | Edit any order                 | Superuser   |
| **GET**     | /docs                    | Documentation                  | All         |

## Notes

You can create a secret key with this command:

``
openssl rand -hex 32
``