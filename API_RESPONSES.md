# Example API Responses

This document contains actual examples of the JSON responses returned by the Banking API for demonstration purposes. 

### 1. User Registration (`/api/auth/register`)
```json
{
  "message": "User created successfully",
  "user_id": 1
}
```

### 2. User Login (`/api/auth/login`)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```

### 3. Create a Bank Account (`/api/accounts/`)
```json
{
  "account_id": 1,
  "account_number": "2068246428",
  "balance": "0.00",
  "message": "Account created successfully"
}
```

### 4. Deposit Funds (`/api/transactions/deposit`)
```json
{
  "message": "Deposit successful",
  "new_balance": "500.00"
}
```

### 5. View Transaction History (`/api/transactions/history/1`)
```json
[
  {
    "amount": "500.00",
    "balance_after": "500.00",
    "description": "Deposit",
    "related_account_id": null,
    "timestamp": "2026-03-18T04:08:02.535297",
    "transaction_id": 1,
    "type": "DEPOSIT"
  }
]
```

### 6. Verify Server Status (`/`)
```json
{
  "documentation": "Please refer to sample_requests.md for API documentation endpoints.",
  "message": "Welcome to the Banking API!",
  "status": "online"
}
```
