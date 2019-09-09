import boto3


def clean_versions_of_lambda(function_name:str, version:str=None):
    """
    clean specific or previous all versions of lambda
     
    :param function_name: name of lambda
    :param version: specific version of lambda. if None, delte all previous version of lambda
    """
    
    client = boto3.client('lambda')
    functions = client.list_functions()['Functions']
    for function in functions:
        if function['FunctionName'] == function_name:
            print('current version of function : ', function['Version'])
            
            versions = client.list_versions_by_function(FunctionName=function['FunctionArn'])['Versions']
            
            #if you delete all previous version except for latest
            for version in versions:
                
                if version is not None:
                    if version['Version'] == version:
                        arn = version['FunctionArn']
                        print(f'delete specific version : {version}')
                        print(f'delete_function(FunctionName={arn})')
                        #client.delete_function(FunctionName=arn) 
                else:
                    if version['Version'] != function['Version']:
                        arn = version['FunctionArn']
                        print('delete all previsou version')
                        print(f'delete_function(FunctionName={arn})')
                        #client.delete_function(FunctionName=arn) 


if __name__ == '__main__':
    clean_old_lambda_versions('ICT_FAMILY_FILTER_dev')
