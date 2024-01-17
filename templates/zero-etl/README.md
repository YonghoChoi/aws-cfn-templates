
## CloudFormation 실행 명령어
- 스택 생성
```
aws cloudformation create-stack \
  --region us-east-1 \
  --stack-name myteststack \
  --template-body file://aurora-to-redshift.yml \
  --parameters ParameterKey=myIp,ParameterValue=175.207.209.163
```

- 스택 업데이트
```
aws cloudformation update-stack \
  --region us-east-1 \
  --stack-name myteststack \
  --template-body file://aurora-to-redshift.yml \
  --parameters ParameterKey=myIp,ParameterValue=175.207.209.163
```

- 스택 제거
```
aws cloudformation delete-stack \
  --region us-east-1 \
  --stack-name myteststack
```

## 참고
1. DynamoDB 테이블용 더미 데이터 생성 (Python)
```
# pip install Faker
import csv
from faker import Faker
fake = Faker()

with open('dummy.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     writer.writerow(["Name", "Address", "Text"])
     for _ in range(10000):
      writer.writerow([fake.name(), fake.address(), fake.text()])
```