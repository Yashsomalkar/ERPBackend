

# **ERP Backend API Documentation**

This document outlines the implemented flows, endpoints, and checks for the ERP Backend.

---

## **Overview**

The ERP backend is designed to manage Users, Vendors, and Admins for an ERP system. The backend uses **Flask**, **MongoDB**, and **JWT authentication** to provide a secure and structured API.


---
## **FLows of all USER, ADMIN, VENDOR
https://github.com/user-attachments/assets/4964cd1a-a363-4cd9-b14b-2748d5432ebf

https://github.com/user-attachments/assets/2fef71d4-f7f3-471f-b647-c84f8d1ca2c8

https://github.com/user-attachments/assets/e511d91d-b4ea-42c5-be2a-9de28e596a48

---

## **Flows**

### 1. **User Flow**
Users can:
- Register and log in.
- View vendors and their products.
- Add products to the cart.
- Manage their cart (increment, decrement, or remove items).
- View and update their guest list.
- Place and view order statuses.

### 2. **Vendor Flow**
Vendors can:
- Register and log in.
- Add, update, and delete products.
- View transactions for their products.
- Fulfill orders placed by users.

### 3. **Admin Flow**
Admins can:
- Register and log in.
- Manage users and vendors.
  - Add, update, and delete users and vendors.
  - Manage memberships for users and vendors.

---

## **Endpoints**

### **Authentication**
1. **Register a User**
   - **Endpoint**: `/api/auth/register`
   - **Method**: `POST`
   - **Body**:
     ```json
     {
       "name": "John Doe",
       "email": "john.doe@example.com",
       "password": "password123",
       "role": "user"
     }
     ```
   - **Response**: `201 Created` with success message.
   - **Checks**:
     - Validates unique email.
     - Hashes password before storing.

2. **Login**
   - **Endpoint**: `/api/auth/login`
   - **Method**: `POST`
   - **Body**:
     ```json
     {
       "email": "john.doe@example.com",
       "password": "password123"
     }
     ```
   - **Response**: `200 OK` with JWT token.
   - **Checks**:
     - Validates email and password.

3. **Admin Registration/Login**
   - **Endpoints**:
     - **Register**: `/api/auth/register/admin`
     - **Login**: `/api/auth/login/admin`
   - **Role**: Must have `"role": "admin"` in the body for registration.

4. **Vendor Registration/Login**
   - **Endpoints**:
     - **Register**: `/api/auth/register/vendor`
     - **Login**: `/api/auth/login/vendor`
   - **Role**: Must have `"role": "vendor"` in the body for registration.

---

### **User**
1. **View Vendor Products**
   - **Endpoint**: `/api/user/vendors/<category>`
   - **Method**: `GET`
   - **Checks**:
     - Validates JWT for user role.
     - Filters vendors by category.

2. **Cart Operations**
   - **Endpoints**:
     - **Add to Cart**: `/api/user/cart/add`
     - **Update Cart**: `/api/user/cart/update`
     - **Clear Cart**: `/api/user/cart/clear`
   - **Methods**: `POST`
   - **Body**:
     ```json
     {
       "product_id": "abc123",
       "quantity": 2
     }
     ```
   - **Checks**:
     - Validates product existence.
     - Ensures stock availability.

3. **Guest List**
   - **Endpoints**:
     - **Add Guest**: `/api/user/guests/add`
     - **Update Guest**: `/api/user/guests/update`
     - **Delete Guest**: `/api/user/guests/delete`
   - **Methods**: `POST`
   - **Body**:
     ```json
     {
       "name": "Jane Doe",
       "email": "jane.doe@example.com",
       "phone": "1234567890"
     }
     ```

4. **Place Order**
   - **Endpoint**: `/api/user/orders/place`
   - **Method**: `POST`
   - **Body**:
     ```json
     {
       "cart": [
         {"product_id": "abc123", "quantity": 2},
         {"product_id": "def456", "quantity": 1}
       ]
     }
     ```

5. **View Order Status**
   - **Endpoint**: `/api/user/orders`
   - **Method**: `GET`
   - **Checks**:
     - Validates JWT for user role.

---

### **Vendor**
1. **Add Product**
   - **Endpoint**: `/api/vendor/products/add`
   - **Method**: `POST`
   - **Body**:
     ```json
     {
       "name": "Buffet Service",
       "price": 199.99,
       "quantity": 10,
       "category": "Catering"
     }
     ```

2. **Edit Product**
   - **Endpoint**: `/api/vendor/products/<product_id>/edit`
   - **Method**: `PUT`
   - **Checks**:
     - Ensures product belongs to the vendor.

3. **Delete Product**
   - **Endpoint**: `/api/vendor/products/<product_id>/delete`
   - **Method**: `DELETE`

4. **View Transactions**
   - **Endpoint**: `/api/vendor/transactions`
   - **Method**: `GET`

5. **Fulfill Order**
   - **Endpoint**: `/api/vendor/orders/<order_id>/fulfill`
   - **Method**: `PUT`

---

### **Admin**
1. **Manage Users**
   - **Endpoints**:
     - **View Users**: `/api/admin/users`
     - **Add User**: `/api/admin/users/add`
     - **Update User**: `/api/admin/users/update`
     - **Delete User**: `/api/admin/users/delete`
   - **Methods**: `GET`, `POST`, `PUT`, `DELETE`

2. **Manage Vendors**
   - **Endpoints**:
     - **View Vendors**: `/api/admin/vendors`
     - **Add Vendor**: `/api/admin/vendors/add`
     - **Update Vendor**: `/api/admin/vendors/update`
     - **Delete Vendor**: `/api/admin/vendors/delete`

3. **Membership Management**
   - **Endpoints**:
     - **Add Membership**: `/api/admin/memberships/add`
     - **Update Membership**: `/api/admin/memberships/update`

---

## **Authorization Checks**
- **JWT** is validated for each endpoint.
- **Role-Specific Authorization**:
  - Admin-only endpoints are accessible with the `"admin"` role.
  - Vendor-only endpoints are accessible with the `"vendor"` role.
  - User-only endpoints are accessible with the `"user"` role.

---

## **Dummy Data for Testing**
- **User Accounts**:
  - `john.doe@example.com` (User)
  - `jane.admin@example.com` (Admin)

- **Vendor Accounts**:
  - `vendor1@example.com` (Vendor - Catering)
  - `vendor2@example.com` (Vendor - Florist)

