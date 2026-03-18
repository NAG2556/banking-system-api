# Sample Requests (API Tests)

Once your server is running (`python run.py`), you can test the APIs.

*(Note: Replace `YOUR_ACCESS_TOKEN` with the actual token returned by the login API in the subsequent requests)*

## 1. Auth 

### Register
```bash
curl -X POST http://127.0.0.1:5001/api/auth/register \
-H "Content-Type: application/json" \
-d '{"username": "johndoe", "password": "password123"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:5001/api/auth/login \
-H "Content-Type: application/json" \
-d '{"username": "johndoe", "password": "password123"}'
```
> Copy the `"access_token"` from the response for the steps below.

---

## 2. Accounts

### Create a Bank Account
```bash
curl -X POST http://127.0.0.1:5001/api/accounts/ \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
> Note the `account_id` and `account_number` returned in the response.

### Get User's Accounts
```bash
curl -X GET http://127.0.0.1:5001/api/accounts/ \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Account Details
```bash
# Assuming account_id is 1
curl -X GET http://127.0.0.1:5001/api/accounts/1 \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 3. Transactions

### Deposit Money
```bash
curl -X POST http://127.0.0.1:5001/api/transactions/deposit \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{"account_id": 1, "amount": 500.00}'
```

### Withdraw Money
```bash
curl -X POST http://127.0.0.1:5001/api/transactions/withdraw \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{"account_id": 1, "amount": 150.00}'
```

### Transfer Money
*You will need a second account to test this feature. Feel free to create another account using the Create Account endpoint.*

```bash
# Assuming from_account_id is 1 and to_account_number is "1234567890" (replace with real number from creation)
curl -X POST http://127.0.0.1:5001/api/transactions/transfer \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{
    "from_account_id": 1,
    "to_account_number": "ACTUAL_ACCOUNT_NUMBER_HERE",
    "amount": 100.00
}'
```

### Get Transaction History
```bash
# Get history for account_id 1
curl -X GET http://127.0.0.1:5001/api/transactions/history/1 \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
