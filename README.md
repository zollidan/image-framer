# Image Framer

Image Framer is a web application that allows you to apply simple edits to your images, such as adding a white background or a decorative frame. It features a Python FastAPI backend for image processing and a React frontend for user interaction.

## Features

- **Add White Background**: Place any image onto a clean white background, with adjustable padding.
- **Add Frame**: Overlay a decorative frame onto your images (work in progress).
- **S3 Integration**: Processed images are stored in an S3-compatible object storage.
- **Database Tracking**: Information about processed images is stored in a SQLite database.

## Tech Stack

- **Backend**:
  - Python 3.11
  - FastAPI
  - SQLAlchemy
  - Pillow (PIL)
  - Uvicorn
- **Frontend**:
  - React
  - TypeScript
  - Vite
  - Tailwind CSS
  - shadcn/ui
- **Database**:
  - SQLite
- **Deployment**:
  - Docker & Docker Compose
  - Nginx
  - Let's Encrypt (for SSL)

---

## Local Development

To run the application on your local machine, you need to have Python and Node.js installed.

### Backend

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Install dependencies:**
    This project uses `uv` for package management.
    ```bash
    pip install uv
    uv sync
    ```

3.  **Create a `.env` file:**
    Create a `.env` file in the `backend/` directory and add the following environment variables for your S3-compatible storage:
    ```
    BUCKET_NAME=your-bucket-name
    ENDPOINT=https://your-s3-endpoint.com
    ACCESS_KEY=your-access-key
    SECRET_KEY=your-secret-key
    ```

4.  **Run the backend server:**
    ```bash
    uv run fastapi run app/main.py --host 0.0.0.0
    ```
    The backend API will be available at `http://localhost:8000`.

### Frontend

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    This project uses `bun` for package management.
    ```bash
    npm install -g bun
    bun install
    ```

3.  **Create a `.env` file:**
    Create a `.env` file in the `frontend/` directory and add the following environment variable to point to your backend API:
    ```
    VITE_API_URL=http://localhost:8000
    ```

4.  **Run the frontend development server:**
    ```bash
    bun run dev
    ```
    The frontend will be available at `http://localhost:5173`.

---

## Testing

To run the backend tests, navigate to the `backend/` directory and run the following command:

```bash
cd backend
uv run pytest
```

---

## Deployment

The repository includes a comprehensive setup for deploying the application to a production environment using Docker.

### Prerequisites

- An Ubuntu 20.04+ server with a public IP address.
- A domain name pointing to the server's IP.
- A Yandex Container Registry ID (or any other container registry).

### 1. Prepare the Server

Clone the repository onto your server:

```bash
git clone https://github.com/zollidan/image-framer.git
cd image-framer
```

### 2. Set Up Environment Variables

Export the following environment variables:

```bash
export MY_DOMAIN="your-domain.com"
export REGISTER_ID="your-yandex-registry-id"
```

### 3. Run the Setup Script

The `setup.sh` script automates the installation of Docker, Docker Compose, and obtains SSL certificates from Let's Encrypt.

```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- Update the system.
- Install Docker and Docker Compose.
- Obtain Let's Encrypt SSL certificates.
- Configure Nginx with SSL termination.
- Start all services using `docker-compose`.

### 4. Verify the Deployment

After the script finishes, you can check the status of the running containers:

```bash
docker compose ps
```

You can also view the logs for each service:

```bash
docker compose logs frontend
docker compose logs backend
docker compose logs nginx-proxy
```

The application should now be available at `https://your-domain.com`.

## Deployment Architecture

```
Internet → nginx-proxy (SSL) → frontend nginx → backend
  HTTPS         HTTP              HTTP            HTTP
```

- **nginx-proxy**: Handles SSL termination on ports 80/443.
- **frontend**: The React application served by Nginx on port 3000.
- **backend**: The FastAPI server running on port 8000.
- **certbot**: Automatically renews SSL certificates.

## Maintenance

### Updating Images

```bash
docker compose pull
docker compose up -d
```

### Viewing Logs

```bash
docker compose logs -f [service_name]
```

### Restarting Services

```bash
docker compose restart [service_name]
```

### Renewing SSL Certificates

Certificates are renewed automatically. To force a renewal:

```bash
docker compose exec certbot certbot renew
docker compose exec nginx-proxy nginx -s reload
```
