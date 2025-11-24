# Creating mode data with faker

```bash
pip install faker
```

---

# ✅ **2. Basic Usage (simplest example)**

```python
from faker import Faker

fake = Faker()

print(fake.name())
print(fake.email())
print(fake.address())
print(fake.date())
```

### Example Output

```
Johnathan Reid
carla92@example.org
123 Woodland Street
Denver, CO 80911
2024-03-19
```

---

# ✅ **3. Generate Multiple Random Records**

```python
from faker import Faker

fake = Faker()

for _ in range(5):
    print(fake.name(), fake.phone_number(), fake.city())
```

---

# ⭐ **4. Create Custom Mock Data (Loan Example)**

```python
from faker import Faker
import random

fake = Faker()

def generate_loan_record():
    return {
        "loan_id": fake.uuid4(),
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "loan_amount": random.randint(5000, 300000),
        "interest_rate": round(random.uniform(3.0, 12.0), 2),
        "loan_type": random.choice(["Home", "Auto", "Education", "Personal"]),
        "start_date": fake.date_between(start_date="-5y", end_date="today"),
        "term_months": random.choice([12, 24, 36, 60, 120, 180, 360]),
    }

# generate 3 rows
for _ in range(3):
    print(generate_loan_record())
```

### Sample Output

```
{
 'loan_id': '6a47f653-31b6-4ca2-a65e-6e04bb25e28b',
 'customer_name': 'Aaron Glover',
 'customer_email': 'aron.glover@live.com',
 'loan_amount': 223000,
 'interest_rate': 7.21,
 'loan_type': 'Auto',
 'start_date': datetime.date(2022, 1, 22),
 'term_months': 60
}
```

---

# ⭐ **5. Create Vehicle Pollution Check Mock Data**

```python
from faker import Faker
import random

fake = Faker()

def generate_pollution_check():
    vehicle_type = random.choice(["Car", "Bike", "Diesel-Truck"])
    allowed_limit = {"Car": 75, "Bike": 45, "Diesel-Truck": 110}[vehicle_type]
    pollution_level = round(random.uniform(allowed_limit * 0.5, allowed_limit * 1.4), 2)

    return {
        "test_id": fake.uuid4(),
        "vehicle_number": fake.license_plate(),
        "vehicle_type": vehicle_type,
        "pollution_level": pollution_level,
        "allowed_limit": allowed_limit,
        "passed": pollution_level <= allowed_limit,
        "test_date": fake.date_between(start_date="-2y", end_date="today")
    }

# Example
for _ in range(3):
    print(generate_pollution_check())
```

### Output Example

```
{
 'test_id': 'ad778691-dc4e-4c83-a350-3985b14f2eac',
 'vehicle_number': 'MH-20-1234',
 'vehicle_type': 'Bike',
 'pollution_level': 36.22,
 'allowed_limit': 45,
 'passed': True,
 'test_date': datetime.date(2023, 5, 12)
}
```

---

# 🔥 **6. Convert Generated Data to Pandas**

```python
import pandas as pd

loan_data = [generate_loan_record() for _ in range(100)]
df = pd.DataFrame(loan_data)
print(df.head())
```


# Large loan dataset - 10000+ rows

```python
from faker import Faker
import random
import pandas as pd

fake = Faker()

def generate_loan_record():
    return {
        "loan_id": fake.uuid4(),
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "customer_phone": fake.phone_number(),
        "loan_amount": random.randint(5000, 500000),
        "interest_rate": round(random.uniform(3.0, 12.0), 2),
        "loan_type": random.choice(["Home", "Auto", "Education", "Personal", "Business"]),
        "start_date": fake.date_between(start_date="-8y", end_date="today"),
        "term_months": random.choice([6, 12, 24, 36, 60, 120, 180, 240, 360]),
        "customer_city": fake.city(),
        "customer_state": fake.state(),
    }

# Generate 50,000 rows
n = 50000
loan_data = [generate_loan_record() for _ in range(n)]

df_loans = pd.DataFrame(loan_data)
print(df_loans.head(), len(df_loans))

```