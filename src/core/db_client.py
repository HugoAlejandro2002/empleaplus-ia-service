import boto3

from .config import get_settings

settings = get_settings()

dynamodb = boto3.resource(
    'dynamodb',
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key
)

def get_skills_table():
    return dynamodb.Table(settings.dynamodb_skills_table)

def get_users_table():
    return dynamodb.Table(settings.dynamodb_users_table)

def get_resumes_table():
    return dynamodb.Table(settings.dynamodb_resumes_table)
