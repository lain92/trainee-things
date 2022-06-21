# trainee-things

This project is only for trainee purposes!

## Serverless
First configure serverless to use the correct credentials:
``serverless config credentials --provider aws --key <your_key> --secret <your_secret>``
If you already have configured a profiel you can overwrite it with the the parameter ```-o```

The service can be deployed with following command:
``serverless deploy``


## Enpoints 

```GET https://jf2pztfvga.execute-api.eu-central-1.amazonaws.com/```
will return a HTTP 200 with a JSON body that contains the incoming Lambda event



