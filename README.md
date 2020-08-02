# Horse Health Predictor
*A dockerized flask app demonstrating experience in deploying machine learning models* 

.

MongoDB has handled the task of data storage install and run before starting project

.

```console
foo@bar:~$ echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

foo@bar:~$ sudo apt-get update

foo@bar:~$ sudo apt-get install -y mongodb-org

foo@bar:~$ sudo systemctl start mongod
```
.

Once the repository has been cloned, change directory to the repository's clone

.

```console
foo@bar:~$ cd Horse-Health-Predictor-master/

```
.

Install requirements using pip 
.

```console
foo@bar:~/Horse-Health-Predictor-master$ sudo pip install -r requirements.txt

```
.

Start running the server 

.

```console
foo@bar:~/Horse-Health-Predictor-master$ cd Flask/ 

foo@bar:~/Horse-Health-Predictor/Flask$ python fla.py

```
.

Dockerfile has been generated, an image has been uploaded to the repository to clone and run

.

```console
foo@bar:~/Horse-Health-Predictor-master$ docker run -p 4000:5000 prashkurella/horsesurvival:final

```

