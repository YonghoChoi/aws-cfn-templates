import csv
import uuid
from faker import Faker
fake = Faker()

with open('dummy.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     writer.writerow(["CustomerId", "Name", "Address", "Text"])
     for _ in range(10000):
      writer.writerow([uuid.uuid4().hex, fake.name(), fake.address(), fake.text()])

