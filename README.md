
# Secret Searching
## Discription:
Search tool for code directories. This tool identifies sensitive content embedded in code. 
Currently set to search AWS secrets (aw secret access key) and private key (RSA private key) but could be set to search any other sensitive content.

## Prerequisites
Python 3.6 , pip , requests.

requests : https://requests.readthedocs.io/en/master/

## Example - Run the script (locally): 

The example is for wolfssh repo (from above) which cotains 3 rsa keys.
If you would like you can decide which key to look for by sending an appropriate string as the 3rd parameter:
* private key rsa : rsa_key
* AW secret - access key : aws_access_key

* Download a public repos from github (example)
```
$ git clone https://github.com/wolfSSL/wolfssh.git
```

you can run this code from script path:
```
> python FindSecret.py /path-to-cloned-project-containning-keys rsa_key
```

 you will see on your screen all rsa_key in wolfSSL repo (3 rsa keys)
result:
```
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

```
