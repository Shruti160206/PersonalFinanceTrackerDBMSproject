# DbmsProjectFix

## Clone the Repository

```bash
git clone https://github.com/Shruti160206/PersonalFinanceTrackerDBMSproject.git
cd PersonalFinanceTrackerDBMSproject
```

---

## Create and Activate Virtual Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

If virtual environment activation fails on Windows, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Then activate the virtual environment again:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root directory.

Copy the contents of `.env.example` into `.env` and update the database credentials:

```env
DB_PASSWORD=your_mysql_root_password
```

---

## Database Configuration

1. Install MySQL Workbench.
2. Update the database configuration in the `.env` file.

### Initialize the Database

Run the following script to initialize the database:

```bash
python3 scripts/initialize_db.py
```

---

## Run the Backend Server

```bash
python3 app.py
```