# E-commerce Admin API (FastAPI + PostgreSQL)

This is a simple back-end application built with FastAPI and PostgreSQL. It powers an admin dashboard for managing products, checking sales, and keeping an eye on inventory.

It's lightweight, easy to deploy, and containerized so anyone can spin it up without worrying about setting up databases or environments manually.

---

## How to Start the Application

1. Ensure Docker and Docker Compose are installed on your machine.

2. Clone this repository and navigate to the root folder.

3. From your terminal, run:

```bash
docker-compose up --build
```

4. The FastAPI app will be available at:
```
http://localhost:8000
```

PostgreSQL will be running in the background on port 5432.

---

## What This App Can Do

The app simulates a small admin panel with basic capabilities:

- View and add products
- Check and update inventory levels
- Monitor sales and view revenue summaries

All of this data is stored in PostgreSQL and accessed using raw SQL queries.

---

## Available Endpoints

### Products
- `GET /products/` → List all products
- `GET /products/{id}` → Get a product by ID
- `POST /products/` → Add a new product

### Inventory
- `GET /inventory/` → View inventory
- `GET /inventory/low_stock` → Items with low stock (≤5)
- `PUT /inventory/update/{product_id}?new_stock=10` → Update stock level

### Sales
- `GET /sales/` → List all sales
- `GET /sales/summary?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` → Revenue summary
- `GET /sales/by_product/{product_id}` → Sales data for a product

---

## Behind the Scenes

- The app connects to PostgreSQL using psycopg2
- Migrations and demo data are run automatically at startup using raw SQL files
- Environment variables are stored in a `.env` file and loaded using python-dotenv
- The entire project is containerized with Docker

---

## Database Schema

The application uses a PostgreSQL database with the following tables:

### products
- **id**: Primary key
- **name**: Name of the product
- **category**: Category to which the product belongs
- **price**: Product price
- **created_at**: Timestamp when the product was added

### inventory
- **id**: Primary key
- **product_id**: Foreign key referencing `products(id)`
- **stock_level**: Number of units currently in stock
- **updated_at**: Timestamp of the last update to the stock level

### sales
- **id**: Primary key
- **product_id**: Foreign key referencing `products(id)`
- **quantity**: Number of units sold
- **total_amount**: Total amount for the transaction
- **sale_date**: Date and time of the sale

### migration_versions
- **id**: Primary key
- **name**: Unique name of the SQL script or migration step
- **applied_at**: Timestamp when the migration was applied

This structure enables effective tracking of product availability, stock levels, and historical sales performance.

## Notes

- On every start, the app checks if tables and data already exist before re-inserting
- All SQL is tracked using a simple `migration_versions` table (similar to Liquibase)
- You can modify or extend this setup easily to add authentication, analytics, or admin dashboards

---

## Contribution

This is a foundational project and can be extended in various directions. If you find a bug or want to improve something, feel free to fork, suggest changes, or open a pull request.
