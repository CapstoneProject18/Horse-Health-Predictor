# Horse Health Predictor
Predicting the survival rate of a horse using the given date set.
.

.

.

The project is Flask based Web App that predicts if a horse will survive hospitalization,

.

.

.

MongoDB has handled the task of data storage install and run before starting project

.

.

.

```console
foo@bar:~$ echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
```
```console
foo@bar:~$ sudo apt-get update
```
```console
foo@bar:~$ sudo apt-get install -y mongodb-org
```
```console
foo@bar:~$ sudo systemctl start mongod
```
.

.

.

Once the repository has been cloned, change directory to the repository's clone

.

.

.

```console
foo@bar:~$ cd Horse-Health-Predictor-master/

```
.

.

.

Install requirements using pip 

.

.

.

```console
foo@bar:~/Horse-Health-Predictor-master$ sudo pip install -r requirements.txt

```
.

.

.

Start running the server 

.

.

.

```console
foo@bar:~/Horse-Health-Predictor-master$ cd Flask/ 

foo@bar:~/Horse-Health-Predictor/Flask$ python fla.py

```
