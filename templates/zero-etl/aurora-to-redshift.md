## Aurora MySQL과 Redshift 간 Zero-ETL 통합

Demo는 버지니아 리전(us-east-1)을 대상으로 테스트 되었습니다. 

1. AWS 콘솔에서 [CloudShell](https://us-east-1.console.aws.amazon.com/cloudshell/home?region=us-east-1) 실행
2. Git clone 후 디렉토리 이동
```
git clone https://github.com/YonghoChoi/aws-cfn-templates.git && cd ./aws-cfn-templates/templates/zero-etl
```
3. 데이터 확인용도로 Aurora MySQL과 Redshift에 접속할 클라이언트 Public IP 확인
```
# 브라우저에서 wgetip.com 입력해서 확인하거나 linux 또는 mac인 경우 아래 명령으로 확인
curl wgetip.com
```
4. CloudFormation 스택 생성
```
STACK_NAME=zeroetl-aurora-to-redshift
aws cloudformation create-stack \
  --region us-east-1 \
  --stack-name $STACK_NAME \
  --template-body file://aurora-to-redshift.yml \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=myIp,ParameterValue=<3번에서 확인한 IP 입력>

# 완료 될때까지 대기
echo "Waiting for stack to be created"
aws cloudformation wait stack-create-complete --stack-name $STACK_NAME  
```
4. 아래 명령 실행 결과에 따른 정보로 DBeaver 또는 MySQL CLI 도구로 데이터 확인
```
cat << EOF
==============DB Information==============
Redshift Endpoint : $(aws cloudformation describe-stacks --stack-name zeroetl-aurora-to-redshift --query 'Stacks[0].Outputs' | jq '.[] | select(.OutputKey=="RedshiftEndpoint")' | jq '.OutputValue')
  User: admin
  Password: Awsuser123
RDS Endpoint : $(aws cloudformation describe-stacks --stack-name zeroetl-aurora-to-redshift --query 'Stacks[0].Outputs' | jq '.[] | select(.OutputKey=="RDSEndpoint")' | jq '.OutputValue')
  User: admin
  Password: Awsuser123
==========================================
EOF
```
5. Aurora MySQL에 접속하여 데모용 데이터베이스 생성 및 데이터 로드
```
create database demodb;

use demodb;

create table region (
  r_regionkey int4 not null,
  r_name char(25) not null ,
  r_comment varchar(152) not null,
  Primary Key(R_REGIONKEY)                             
) ;

create table nation (
  n_nationkey int4 not null,
  n_name char(25) not null ,
  n_regionkey int4 not null,
  n_comment varchar(152) not null,
  Primary Key(N_NATIONKEY)                                
) ;

create table supplier (
  s_suppkey int4 not null,
  s_name char(25) not null,
  s_address varchar(40) not null,
  s_nationkey int4 not null,
  s_phone char(15) not null,
  s_acctbal numeric(12,2) not null,
  s_comment varchar(101) not null,
  Primary Key(S_SUPPKEY)
);

create table customer (
  c_custkey int8 not null ,
  c_nationkey int4 not null,
  c_acctbal numeric(12,2) not null,
  c_mktsegment char(10) not null,
  Primary Key(C_CUSTKEY)
);

create table orders (
  o_orderkey int8 not null,
  o_custkey int8 not null,
  o_orderstatus char(1) not null,
  o_orderpriority char(15) not null,
  o_shippriority int4 not null,
  o_clerk char(15) not null,
  Primary Key(O_ORDERKEY)
) ;

create table lineitem (
  l_orderkey int8 not null ,
  l_partkey int8 not null,
  l_suppkey int4 not null,
  l_linenumber int4 not null,
  l_returnflag char(1) not null,
  l_linestatus char(1) not null,
  l_shipmode char(10) not null,
  Primary Key(L_ORDERKEY, L_LINENUMBER)
)  ;

create table part (
  p_partkey int8 not null ,
  p_name varchar(55) not null,
  p_mfgr char(25) not null,
  p_brand char(10) not null,
  p_type varchar(25) not null,
  p_size int4 not null,
  PRIMARY KEY (P_PARTKEY)
) ;

create table partsupp (
  ps_partkey int8 not null,
  ps_suppkey int4 not null,
  ps_availqty int4 not null,
  ps_supplycost numeric(12,2) not null,
  Primary Key(PS_PARTKEY, PS_SUPPKEY)
) ;

--- For IAD (us-east-1, N Virginia) region, please use below load scripts:
LOAD DATA FROM S3 PREFIX 's3://redshift-demos/ri2023/ant307/data/order-line/region/' INTO TABLE region FIELDS TERMINATED BY '|';          
LOAD DATA FROM S3 PREFIX 's3://redshift-demos/ri2023/ant307/data/order-line/nation/' INTO TABLE nation FIELDS TERMINATED BY '|';            
LOAD DATA FROM S3 PREFIX 's3://redshift-demos/ri2023/ant307/data/order-line/supplier/' INTO TABLE supplier FIELDS TERMINATED BY '|';            
LOAD DATA FROM S3 PREFIX 's3://redshift-demos/ri2023/ant307/data/order-line/customer/' INTO TABLE customer FIELDS TERMINATED BY '|';            
LOAD DATA FROM S3 PREFIX 's3://redshift-demos/ri2023/ant307/data/order-line/orders/' INTO TABLE orders FIELDS TERMINATED BY '|';            
LOAD DATA FROM S3 PREFIX 's3://redshift-demos/ri2023/ant307/data/order-line/lineitem/' INTO TABLE lineitem FIELDS TERMINATED BY '|';            
LOAD DATA FROM S3 PREFIX 's3://redshift-demos/ri2023/ant307/data/order-line/part/' INTO TABLE part FIELDS TERMINATED BY '|';            
LOAD DATA FROM S3 PREFIX 's3://redshift-demos/ri2023/ant307/data/order-line/partsupp/' INTO TABLE partsupp FIELDS TERMINATED BY '|';
```

## Trouble shooting
1. Aurora MySQL engine 버전이 존재하지 않다는 오류가 발생할 경우 (마이너버전이 없어질 수 있음)
```
# 아래 명령으로 버전 확인
aws rds describe-db-engine-versions --engine aurora-mysql --engine-version 8.0
```