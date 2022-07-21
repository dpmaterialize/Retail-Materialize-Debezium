### Info

The file "data_gen.py" contains the code that generates the ecommerce data. The code uses the help of faker and faker-commerce to generate the data. The code runs infinitely to stop the program hit ctrl+c

The “data_gen.py” file uses ‘data_gen_config.json’. The input fields present in json are.

```database```: The DB name under which the data will be generated

```host```: Hostname of postgres instance

```port```: Port of the postgres instance

```user```: User defined in the postgres instance

```password```: Password for the user in the postgres instance

```table```: Table on which the data is generated

```schema```: Schema on which the table is defined under

Post data gen we insert it into the table with accordance to the schema below.

![image](https://user-images.githubusercontent.com/20200948/179387474-802de248-3fc3-45f2-afc1-7a14cc2ed7b7.png)

### Steps to setup the code

1) sudo apt install python3-dev gcc
2) sudo apt-get install --reinstall libpq-dev
3) sudo apt install python3-virtualenv
4) Create a virtualenv using ```virtualenv venv```
5) Activate the environment ```source venv/bin/activate```
6) Install the packages using ```pip3 install -r requirements.txt```

### Run the code
NOTE: Ensure you have created the table prior to running the script or else this will fail             

```python data_gen.py```
