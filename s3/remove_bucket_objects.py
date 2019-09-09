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
