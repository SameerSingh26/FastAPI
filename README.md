# FastAPI CRUD Application

## Overview
This is a simple CRUD API application that stores posts in a database and allows you to retrieve and delete them.

## Tech Stack
- **FastAPI** - Web framework for building APIs
- **SQLAlchemy** - Database ORM (Object Relational Mapping)
- **MySQL** - Database (hosted on freesqldatabase.com)
- **Python** - Programming language

## Project Structure
```
app/
├── app.py                 # Main API endpoints
├── databaseconnect.py    # Database connection and models
├── schemas.py            # Data validation models
└── __init__.py
```

## API Endpoints

### 1. Create a New Post (CREATE)
**Endpoint:** `POST /posts`

**Description:** Creates a new post in the database.

**Request Body:**
```json
{
  "caption": "My first post",
  "url": "https://example.com/image.jpg",
  "file_type": "image/jpeg",
  "file_name": "image.jpg"
}
```

**Response Example (Success - 200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "caption": "My first post",
  "url": "https://example.com/image.jpg",
  "file_type": "image/jpeg",
  "file_name": "image.jpg",
  "created_at": "2026-09-04T10:30:00"
}
```

**Error Response:**
```json
{
  "detail": "Invalid input data"
}
```

---

### 2. Get All Posts (READ)
**Endpoint:** `GET /posts`

**Description:** Fetches all posts from the database, sorted by newest first.

**Query Parameters (Optional):**
- `limit` - Number of posts to return (default: all)
- `skip` - Number of posts to skip for pagination (default: 0)

**Response Example:**
```json
{
  "posts": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "caption": "My first post",
      "url": "https://example.com/image.jpg",
      "file_type": "image/jpeg",
      "file_name": "image.jpg",
      "created_at": "2026-09-04T10:30:00"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "caption": "Second post",
      "url": "https://example.com/image2.jpg",
      "file_type": "image/jpeg",
      "file_name": "image2.jpg",
      "created_at": "2026-09-03T15:45:00"
    }
  ]
}
```

---

### 3. Get a Post by ID (READ)
**Endpoint:** `GET /posts/{post_id}`

**Description:** Fetches a specific post by its ID.

**Request Parameters:**
- `post_id` (required) - The ID of the post to fetch (UUID format)

**Response Example (Success - 200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "caption": "My first post",
  "url": "https://example.com/image.jpg",
  "file_type": "image/jpeg",
  "file_name": "image.jpg",
  "created_at": "2026-09-04T10:30:00"
}
```

**Error Response:**
```json
{
  "detail": "Post not found"
}
```

---

### 4. Update a Post (UPDATE)
**Endpoint:** `PUT /posts/{post_id}`

**Description:** Updates an existing post by its ID.

**Request Parameters:**
- `post_id` (required) - The ID of the post to update (UUID format)

**Request Body (all fields are optional, only include what you want to update):**
```json
{
  "caption": "Updated caption",
  "url": "https://example.com/new-image.jpg",
  "file_type": "image/png",
  "file_name": "new-image.png"
}
```

**Response Example (Success - 200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "caption": "Updated caption",
  "url": "https://example.com/new-image.jpg",
  "file_type": "image/png",
  "file_name": "new-image.png",
  "created_at": "2026-09-04T10:30:00"
}
```

**Error Response:**
```json
{
  "detail": "Post not found"
}
```

---

### 5. Delete a Post (DELETE)
**Endpoint:** `DELETE /posts/{post_id}`

**Description:** Deletes a specific post by its ID.

**Request Parameters:**
- `post_id` (required) - The ID of the post to delete (UUID format)

**Response Example (Success - 200):**
```json
{
  "Success": true,
  "message": "Post deleted successfully"
}
```

**Error Response:**
```json
{
  "detail": "Post not found"
}
```

## Database Schema

### Posts Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Unique identifier for each post |
| caption | String | Text description of the post |
| url | String | URL/link for the post |
| file_type | String | Type of file (e.g., image/jpeg) |
| file_name | String | Name of the file |
| created_at | DateTime | Timestamp when post was created |

## How to Use These APIs

### 1. Create a Post
```bash
curl -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "Beautiful sunset",
    "url": "https://example.com/sunset.jpg",
    "file_type": "image/jpeg",
    "file_name": "sunset.jpg"
  }'
```

### 2. Get All Posts
```bash
curl -X GET "http://localhost:8000/posts"
```

### 3. Get a Post by ID
```bash
curl -X GET "http://localhost:8000/posts/550e8400-e29b-41d4-a716-446655440000"
```

### 4. Update a Post
```bash
curl -X PUT "http://localhost:8000/posts/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "Amazing sunset view",
    "url": "https://example.com/new-sunset.jpg"
  }'
```

### 5. Delete a Post
```bash
curl -X DELETE "http://localhost:8000/posts/550e8400-e29b-41d4-a716-446655440000"
```

## HTTP Status Codes
- **200** - Success (GET, PUT, DELETE operations)
- **201** - Created (POST operations)
- **400** - Bad request (invalid data)
- **404** - Not found (post doesn't exist)
- **500** - Server error

## Future Features
- Add JWT authentication to all endpoints
- Add pagination to the posts endpoint
- Add search/filter functionality
- Add image upload support
- Add email notifications for new posts