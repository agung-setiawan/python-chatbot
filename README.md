# 🤖 Smart Chatbot API

A robust FastAPI-based chatbot backend capable of entity extraction (Name, Phone, Address, Date/Time) and automated order logging into a MySQL database.

## 📋 Table of Contents
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contribution](#-contribution)

## 🏗 Architecture

The application follows a simple monolithic architecture designed for speed and reliability:

1.  **API Layer**: Built with **FastAPI** for high performance and automatic validation.
2.  **Logic Layer**: Custom Regex-based entity extractor to parse unstructured user messages.
3.  **Data Layer**: **MySQL** database for persistent storage of customer orders.

### Data Flow
1.  User sends a message to `/chat`.
2.  System extracts entities (Name, Address, Phone, Date).
3.  If entities are found -> Data is saved to MySQL -> Confirmation response.
4.  If no entities -> System checks for greetings or asks for clarification.

## 🛠 Technology Stack

-   **Language**: Python 3.9+
-   **Framework**: FastAPI
-   **Server**: Uvicorn
-   **Database**: MySQL 8.0
-   **Containerization**: Docker & Docker Compose
-   **Validation**: Pydantic

## 📦 Prerequisites

Before running the project, ensure you have the following installed:

-   [Docker Desktop](https://www.docker.com/products/docker-desktop) (Recommended)
-   **OR**
-   [Python 3.9+](https://www.python.org/downloads/)
-   [MySQL Server](https://dev.mysql.com/downloads/mysql/)

## 🚀 Installation & Setup

### Method 1: Docker (Recommended)

This method sets up both the application and the database automatically.

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd App
    ```

2.  **Start the services**
    ```bash
    docker-compose up -d --build
    ```

3.  **Verify Status**
    The API will be available at `http://localhost:8000`.

### Method 2: Manual Setup

1.  **Create a Virtual Environment**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Database**
    -   Start your MySQL server.
    -   Run the SQL script to create the schema:
        ```bash
        mysql -u root -p < database.sql
        ```

4.  **Configure Environment**
    -   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    -   Edit `.env` with your database credentials.

5.  **Run the Application**
    ```bash
    uvicorn main:app --reload
    ```

## ⚙ Configuration

The application uses a `.env` file for configuration. Available variables:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `DB_HOST` | Database hostname | `localhost` |
| `DB_USER` | Database username | `root` |
| `DB_PASSWORD` | Database password | `""` |
| `DB_NAME` | Database name | `chatbot_db` |

## 🚀 Deployment

### Production (Docker)
For production environments, use Docker Compose with the `-d` flag to run in detached mode. Ensure you update the `docker-compose.yml` or `.env` with strong passwords.

```bash
docker-compose up -d
```

### Production (Manual)
Use a process manager like Gunicorn with Uvicorn workers:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 📖 API Documentation

### POST `/chat`
Process a user message and extract order details.

**Request:**
```json
{
  "message": "Halo, saya mau kirim paket dari rumah Budi di Jalan Merdeka No 10 tanggal 20 Oktober 2023 jam 10"
}
```

**Response (Success - Data Captured):**
```json
{
  "reply": "Terima kasih, data pengiriman Anda berhasil dicatat.",
  "name": "Budi",
  "phone": null,
  "address": "Jalan Merdeka No 10",
  "datetime": "2023-10-20 10:00:00"
}
```

**Response (Greeting):**
```json
{
  "reply": "Halo 👋 Silakan kirim data pengiriman (nama, alamat, tanggal, dan nomor telepon)."
}
```

## 🧪 Testing

You can test the API using `curl` or Postman.

**Example `curl` command:**
```bash
curl -X 'POST' \
  'http://localhost:8000/chat' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "Halo, nama saya Budi, kirim ke Jalan Mawar jam 9"
}'
```

## 🔍 Troubleshooting

**Issue: Database Connection Error**
-   Check if MySQL is running.
-   Verify credentials in `.env` (Manual) or `docker-compose.yml` (Docker).
-   Ensure port 3306 is not occupied.

**Issue: "Module not found"**
-   Ensure you activated the virtual environment before running the app.
-   Run `pip install -r requirements.txt`.

## 🤝 Contribution

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.
