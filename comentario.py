import boto3
import uuid
import os

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    DB_response = table.put_item(Item=comentario)

    # Tambien vamos a guardar el comentario en un bucket de S3
    s3 = boto3.client('s3')
    bucket_name = os.environ["S3_BUCKET_NAME"]
    S3_response = s3.put_object(
        Bucket=bucket_name,
        Key=f'comentarios/{tenant_id}/{uuidv1}.json',
        Body=str(comentario),
        ContentType='application/json'
    )
    
    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'DB_response': DB_response,
        'S3_response': S3_response
    }
