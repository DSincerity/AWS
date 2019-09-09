def remove_bucket_objects(bucket_name:str, prefix_list:list):
    """
    delete object in specific prefix of S3
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    total_delete_obj_cnt=0

    for _prefix in prefix_list:

        try:
            #delete all objects under a sepecific path
            res= bucket.objects.filter(Prefix=_prefix).delete()
            if len(res)!=0:
                status_code = res[0]['ResponseMetadata']['HTTPStatusCode']
                delete_obj_cnt = len(res[0]['Deleted'])
                total_delete_obj_cnt +=delete_obj_cnt
                assert status_code ==200, f"delete object status code error : {status_code}"
            else:
                print(f'No objects on the prefix: {_prefix}' )
        except Exception as e:
            raise ResultError(f"There is an error in deleting object : {e}")

    return total_delete_obj_cnt


def remove_bucket_object(bucket_name, prefix):
    bucket_name = bucket_name
    prefix = prefix
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name )
    
    delete_obj_cnt=0
    for obj in bucket.objects.filter(Prefix=prefix):
        response = bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': obj.key,
                    }]})
        #print(response['ResponseMetadata'])
        delete_obj_cnt +=1
    return delete_obj_cnt
