# API Delivery Pizza

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