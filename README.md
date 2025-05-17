# Search API

A Django REST API for advanced product, brand, and category search with support for English/Arabic, fuzzy matching, partial keywords, and misspellings.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL (or change DB backend in `core/settings.py`)
- `venv` (optional, recommended)

### 1. Clone the Repository
```bash
git clone git@github.com:OmniaOsman/search-API.git
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate (Linux)
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Copy `.env.example` to `.env` and update with your DB and secret settings.

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

---

## API Documentation

### OpenAPI/Swagger
- Interactive docs available at `/api/schema/swagger-ui/`
- Full OpenAPI schema at `/api/schema/` (see `schema.yml` for reference)


### Data for text
There is 3 text files contains small data for test 
- products_data.txt
- catagory_data.txt
- brands_data.txt

### Main Endpoints
#### 1. Product Endpoints (MAIN ENDPOINT)
##### Search Products
- **GET** `/api/v1/products/search`
- **Query Params:**
  - `query` (string, optional): partial name/brand/category (fuzzy + multilingual)
  - `category_id` (int, optional)
  - `brand_id` (int, optional)
- **Response:** Paginated list of products matching criteria

##### Add Product
- **POST** `/api/v1/products/`
- **Request Body:**
  - `name_en` (string, required)
  - `name_ar` (string, required)
  - `brand` (int, required)
  - `category` (int, required)
  - `nutrition_facts` (string, optional)
- **Response:** `201 Created` with product data


#### 2. Category Endpoints

##### List Categories
- **GET** `/api/v1/categories/`
- **Response:** List of categories

##### Add Category
- **POST** `/api/v1/categories/`
- **Request Body:**
  - `name_en` (string, required)
  - `name_ar` (string, required)
- **Response:** `201 Created` with category data

#### 3. Brand Endpoints

##### List Brands
- **GET** `/api/v1/brands/`
- **Response:** List of brands

##### Add Brand
- **POST** `/api/v1/brands/`
- **Request Body:**
  - `name_en` (string, required)
  - `name_ar` (string, required)
- **Response:** `201 Created` with brand data

---

## Pagination
- Default: 20 results per page
- Use `?page=<n>&page_size=<m>` on list/search endpoints

## Throttling
- Anonymous search requests are rate-limited (see `SearchAnonRateThrottle` in code)

## Error Handling
- Standard HTTP error codes: `400 Bad Request`, `404 Not Found`, `500 Internal Server Error`
- Validation errors return detailed messages

---
