
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
