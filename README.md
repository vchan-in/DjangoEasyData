# DjangoEasyData - User list with PI Information
### With Randtronics DPM easyData API capabilities.
### Developed merely for demonstrations. Not for production.


## Docker Deployment
### Prerequisite
1. Docker (latest)
2. Make

### Steps
1. Create a `.env` file from the `.env.example` file:
    ```sh
    cp .env.example .env
    ```
2. Update the `.env` file with the following configuration as required:
    ```text
    # MySQL Environment Variables (Optional)
    MYSQL_DATABASE="userslist"
    MYSQL_USER="dbuser"
    MYSQL_PASSWORD="dbuser@123"
    MYSQL_HOST="mysql"
    MYSQL_PORT="3306"

    # Randtronics EasyData Environment Variables (Must match your easyData settings)
    RANDTRONICS_EASYDATA_API="https://192.168.2.144:8643"
    RANDTRONICS_EASYDATA_CLIENT_USERNAME="demoappnew"
    RANDTRONICS_EASYDATA_CLIENT_PASSWORD="demoappnew@123"
    ```

3. Build and start the containers:
    ```sh
    make build
    make up
    ```

4. The application will be available at `http://localhost:8000`.

5. To stop the containers, press `Ctrl+C` and then run:
    ```sh
    make down
    ```

## Manual Deployment

### Prerequisites
1. Python 3.8
2. Git
3. OS - Linux/Windows
4. MySQL 8

### Get the Code
    ```sh
    git clone https://github.com/vchan-in/DjangoEasyData
    cd DjangoEasyData
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

### Configure the Server
1. Create a `.env` file from the `.env.example` file:
    ```sh
    cp .env.example .env
    ```
2. Update the `.env` file with the following configuration as required:
    ```text
    # MySQL Environment Variables (Optional)
    MYSQL_DATABASE="userslist"
    MYSQL_USER="dbuser"
    MYSQL_PASSWORD="dbuser@123"
    MYSQL_HOST="mysql"
    MYSQL_PORT="3306"

    # Randtronics EasyData Environment Variables (Must match your easyData settings)
    RANDTRONICS_EASYDATA_API="https://192.168.2.144:8643"
    RANDTRONICS_EASYDATA_CLIENT_USERNAME="demoappnew"
    RANDTRONICS_EASYDATA_CLIENT_PASSWORD="demoappnew@123"
    ```

### Run the Server
    ```sh
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
    ```
