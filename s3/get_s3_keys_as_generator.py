def get_s3_keys_as_generator(s3_client,bucket, prefix):
    """Generate all the keys in an S3 bucket."""
    kwargs = {'Bucket': bucket, 'Prefix' : prefix}
    while True:
        resp = s3_client.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            yield obj

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break
