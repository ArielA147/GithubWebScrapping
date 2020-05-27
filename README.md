
# Secret Searching
## Discription:
Search tool for code directories.
This tool identifies sensitive content embedded in code.
Currently set to search AWS secrets (aw secret access key) and private key (RSA private key) but could be set to search any other sensitive content.

- More example for different secrets REGEX can be found in regexes.json

## Prerequisites
Python 3.6 , pip , requests.

requests : https://requests.readthedocs.io/en/master/

## Example -

###Running with a docker container:
```
$ docker build -t webscraper .

$ docker run webscraper
```

* Please notice that the Dockerfile contains the example repository as the search project.
In order to clone from a different repository please edit the docker file to contain the url of your chosen repository.


###Run the script (locally):

The example is for repository as the search project.
The repository (from Github) artifactory-user-plugins repo cotains 9 artifactory tokens.

You can decide which key you look for by sending an appropriate string as a parameter:
* private key rsa : rsa_key
* aws access key : aws_access_key
* artifactory password : artifactory_password
* artifactory token : artifactory_token
* aws secret : aws_secret_key



* Download a public repos from github (example)
```
$ git clone https://github.com/jfrog/artifactory-user-plugins.git
```

* Run this code from script path:
```
> python FindSecret.py /path-to-cloned-project-containning-keys artifactory_token
```

 you will see on your screen all artifactory tokens in artifactory-user-plugins repository overall - 9 artifactory tokens

Result:
```
you are searching for :  artifactory_token  in this path :  ~\artifactory-user-plugins
the file is:  ~\artifactory-user-plugins\build\buildSync\buildSync.json  there are  3  keys:  ['AKCp2UNCd8uK7hQoxZnszftnogpgLcjo2EVFaFE4PGtRHnAcBHr43H7nJmWb4JhVUqBwa2iwX', 'AKCp2UNCd7wqJLNMF7teKBWL7MeWRBuXLQRWQ2cxrCw6WbEHZrjVXYP6HyDoLYHTxqiSgbirQ', 'AKCp2UNCd7xAH5guHik92Ctdtdxw4utwkfsdcTPxxNNiD1UwdB8ft44yHwk4AmpHdM7uVkYzy']
the file is:  ~\artifactory-user-plugins\security\oldPasswordRealm\oldPasswordRealm.json  there are  3  keys:  ['AKCp2UNCd8uK7hQoxZnszftnogpgLcjo2EVFaFE4PGtRHnAcBHr43H7nJmWb4JhVUqBwa2iwX', 'AKCp2UNCd7wqJLNMF7teKBWL7MeWRBuXLQRWQ2cxrCw6WbEHZrjVXYP6HyDoLYHTxqiSgbirQ', 'AKCp2UNCd7xAH5guHik92Ctdtdxw4utwkfsdcTPxxNNiD1UwdB8ft44yHwk4AmpHdM7uVkYzy']
the file is:  ~\artifactory-user-plugins\security\securityReplication\test\sec1-56.json  there are  1  keys:  ['AKCp2V77CZw9VKd8J97FttrGpxqcPcpKwZxrf9zcwhaeAV9oSLrT14m9qLH2msUbRbJssQ6iz']
the file is:  ~\artifactory-user-plugins\security\securityReplication\test\sec1.json  there are  1  keys:  ['AKCp2V77CZw9VKd8J97FttrGpxqcPcpKwZxrf9zcwhaeAV9oSLrT14m9qLH2msUbRbJssQ6iz']
the file is:  ~\artifactory-user-plugins\security\securityReplication\test\sec1old.json  there are  1  keys:  ['AKCp2V77CZw9VKd8J97FttrGpxqcPcpKwZxrf9zcwhaeAV9oSLrT14m9qLH2msUbRbJssQ6iz']

```
