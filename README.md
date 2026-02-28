# MedLink — Pharmacy API

A Django REST Framework backend for connecting patients with pharmacies. Patients can search for medications and place orders. Pharmacies can manage their inventory and handle incoming orders. Admins verify pharmacies and validate via the Django admin panel.

---

## Tech Stack

- Python / Django
- Django REST Framework
- PostgreSQL
- JWT Authentication (via `djangorestframework-simplejwt`)
- Django session-based auth (for HTML views)

---

## Project Structure

```
pharmacy_api/        # Core project (settings, root urls)
accounts/            # Custom user model, registration, login
pharmacies/          # Pharmacy profiles, inventory management
medications/         # Medication catalogue, pharmacy stock
prescriptions/       # Prescription uploads
orders/              # Patient orders, pharmacy order management
templates/           # Skeleton HTML templates
```

---

## Setup

### 1. Clone and install dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary python-dotenv Pillow
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 3. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 5. Run the server

```bash
python manage.py runserver
```

---

## HTML Pages (Browser)

| URL | Description |
|---|---|
| `/` | Home page |
| `/register/patient/` | Patient registration form |
| `/register/pharmacy/` | Pharmacy registration form |
| `/login/` | Login page |
| `/dashboard/` | Role-based dashboard (patient / pharmacy / admin) |
| `/search/` | Medication search (patients only) |
| `/logout/` | Logout |
| `/admin/` | Django admin panel |

---

## REST API Endpoints

All API endpoints are prefixed with `/api/`. JWT token required in the `Authorization` header for protected routes:

```
Authorization: Bearer <access_token>
```

---

### Authentication

#### Obtain JWT Token
```
POST /api/token/
```
Body:
```json
{
  "username": "john",
  "password": "password123"
}
```
Response:
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

#### Refresh Token
```
POST /api/token/refresh/
```
Body:
```json
{
  "refresh": "<refresh_token>"
}
```

---

### Accounts — `/api/accounts/`

#### List users
```
GET /api/accounts/users/
Authorization: Bearer <token>
```

#### Get current user
```
GET /api/accounts/users/me/
Authorization: Bearer <token>
```

#### Register a new user (patient via API)
```
POST /api/accounts/users/
```
Body:
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123",
  "role": "patient"
}
```

---

### Pharmacies — `/api/pharmacies/`

#### List all pharmacies
```
GET /api/pharmacies/
Authorization: Bearer <token>
```

#### Get a single pharmacy
```
GET /api/pharmacies/<id>/
Authorization: Bearer <token>
```

#### Create a pharmacy profile (linked to logged-in user)
```
POST /api/pharmacies/
Authorization: Bearer <token>
```
Body:
```json
{
  "name": "City Pharmacy",
  "license_number": "PH-2024-001",
  "address": "123 Main Street"
}
```
> Note: `user` is automatically set to the authenticated user.

---

### Medications — `/api/medications/`

#### List all medications (supports search)
```
GET /api/medications/drugs/
GET /api/medications/drugs/?q=amoxicillin
Authorization: Bearer <token>
```

#### Create a medication (admin only in practice)
```
POST /api/medications/drugs/
Authorization: Bearer <token>
```
Body:
```json
{
  "name": "Amoxicillin",
  "category": "Antibiotic"
}
```

#### List pharmacy inventory (supports filters)
```
GET /api/medications/inventory/
GET /api/medications/inventory/?q=ibuprofen
GET /api/medications/inventory/?pharmacy=city
GET /api/medications/inventory/?in_stock=true
Authorization: Bearer <token>
```

#### Add medication to pharmacy inventory
```
POST /api/medications/inventory/
Authorization: Bearer <token>  (pharmacy user)
```
Body:
```json
{
  "medication": 1,
  "stock": 100,
  "price": "5.99"
}
```
> Note: `pharmacy` is automatically set to the authenticated pharmacy user's profile.

#### Update inventory item
```
PATCH /api/medications/inventory/<id>/
Authorization: Bearer <token>
```
Body:
```json
{
  "stock": 80,
  "price": "4.99"
}
```

---

### Orders — `/api/orders/`

#### List orders
```
GET /api/orders/
Authorization: Bearer <token>
```
> Returns all orders for the authenticated user. Admins see all. Pharmacies see their own. Patients see their own.

#### Place an order
```
POST /api/orders/
Authorization: Bearer <token>  (patient)
```
Body:
```json
{
  "pharmacy": 1,
  "medication": 2,
  "pharmacy_medication": 3
}
```
> Note: `patient` is automatically set to the authenticated user. `status` defaults to `pending`.

#### Accept an order (pharmacy)
```
POST /api/orders/<id>/accept/
Authorization: Bearer <token>  (pharmacy)
```

#### Reject an order (pharmacy)
```
POST /api/orders/<id>/reject/
Authorization: Bearer <token>  (pharmacy)
```

#### Mark order as complete (pharmacy)
```
POST /api/orders/<id>/complete/
Authorization: Bearer <token>  (pharmacy)
```

---

### Prescriptions — `/api/prescriptions/`

#### List prescriptions
```
GET /api/prescriptions/
Authorization: Bearer <token>
```

#### Upload a prescription
```
POST /api/prescriptions/
Authorization: Bearer <token>  (patient)
Content-Type: multipart/form-data
```
Body:
```
image: <file>
pharmacy: 1   (optional)
```
> Note: `patient` is set automatically. `status` defaults to `pending`.

---

## Testing the APIs with Postman or curl

### Step-by-step flow

**1. Get a token**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "password123"}'
```

**2. Use the token in subsequent requests**
```bash
curl http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer <access_token>"
```

**3. Place an order**
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"pharmacy": 1, "medication": 1, "pharmacy_medication": 1}'
```

**4. Pharmacy accepts the order**
```bash
curl -X POST http://127.0.0.1:8000/api/orders/1/accept/ \
  -H "Authorization: Bearer <pharmacy_access_token>"
```

---

## Admin Panel

Visit `/admin/` and log in with your superuser credentials.

Key things to do in the admin:
- **Verify a pharmacy** — go to Pharmacies, tick `is_verified` on the pharmacy record
- **Add medications** to the global catalogue (Medications → Add)
- **Manage users** and change roles if needed
- **View all orders** and prescriptions

---

## Notes

- Passwords must be at least 8 characters
- Pharmacies cannot manage inventory or accept orders until an admin sets `is_verified = True`
- The global `Medication` catalogue is managed by admins — pharmacies pick from this catalogue to add to their own inventory
- Media files (prescription images) are stored in the `/media/` directory
- The `requests` app was renamed to `orders` to avoid conflict with Python's built-in `requests` library
