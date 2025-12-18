# Utility Scripts

This folder contains helper scripts for managing the BookMySeat application.

## Scripts

### `add_seats.py`
**Purpose**: Populate all theaters with cinema-style seats (10 rows × 12 seats)

**Usage**:
```bash
python scripts/add_seats.py
```

**When to use**: After creating new theaters or when setting up the project for the first time.

---

### `send_confirmation.py`
**Purpose**: Manually send a confirmation email for the latest booking

**Usage**:
```bash
python scripts/send_confirmation.py
```

**When to use**: For testing email functionality or resending confirmations.

---

### `test_email.py`
**Purpose**: Test email configuration (SMTP or Console backend)

**Usage**:
```bash
python scripts/test_email.py
```

**When to use**: To verify email settings are working correctly.

---

### `setup_project.py`
**Purpose**: Initial project setup (creates sample data)

**Usage**:
```bash
python scripts/setup_project.py
```

**When to use**: First-time project setup or database reset.

---

### `create_test_users.py`
**Purpose**: Create test user accounts for development

**Usage**:
```bash
python scripts/create_test_users.py
```

**When to use**: Setting up test accounts for development/demo.

---

### `apply_security_fixes.py`
**Purpose**: Apply security configurations and best practices

**Usage**:
```bash
python scripts/apply_security_fixes.py
```

**When to use**: Before deployment or security audits.

---

## Notes

- All scripts should be run from the project root directory
- Ensure virtual environment is activated before running scripts
- Scripts use Django's setup, so they have access to all models and settings
