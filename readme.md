## Load Testing Sisense with PySense and Locust

### Overview

When load testing Sisense we simulate the load of dashboards by making the same API calls on behalf of different users. We track the response time to these queries in order to ascertain performance. 

Many API calls are made when a dashboard is loaded, most of which hit the mongoDB in Sisense. While this is a place that can cause performance issues, it is not required. 

The only API calls made that interact with the source data are to the "jaql" end point so these calls will be the focus of these tests.

What follows below is one way to load test Sisense. This code can be used roughly as is, but can also be modified to fit your exact requirements.  

### Setting up Sisense for Load Testing

To set up your test you will need to create users and dashboards for them to test. 

For ease of load testing ensure that each user being used for load testing has the same password and has some string in the username which separates load test from non load test users. 

For example in my case all users being created for the load test are named loadtest-1, loadtest-2, etc. So by running get users and filtering for usernames with "loadtest" in them, I can get all the users I need. We will refer to that string as user_name_key. In this case the username key is 'loadtest'  

Each user should be assigned a different data security rule as otherwise the results for all users will be the same. Sisense will cache these responses causing performance to appear faster than it actually is. 

The Dashboards do not actually need to be shared with the users if we are just testing the "jaql" calls. You only need to ensure that the user has query permissions on the elasticube/datamodel that is being tested. 

### Setting up Your Script for Load Testing

At the top of locustfile.py you will see the configurations that need to be set. 
- host: The host location of your sever, ex http://localhost:8081/
- version: The version of Sisense you are running (Linux or Windows)
- user_name_key: The identifier which we can use to separate load test users from non load test users
- password: The password for all the load test users. 
- dashboard_wait_time: If multiple dashboards for a user are being tested, this value reflects how long we should wait before calling the next dashboard. This should simulate time a user would spend actually looking at a dashboard before jumping to the next one.
- admin_config: A PySense config file for an admin user that will be used to run the test

Below these you will see we have two arrays, each containing all the jaql calls run by the dashboard.

To get these calls
- Open the developer console
- Navigate to the network tab in the developer console and clear it
- Load the dashboard you would like to load test
- From the network tab, find all calls made to the jaql end point
- Copy each jaql calls payload as an element in the dashboard array. 
- Repeat for each dashboard to be load tested. You should now have 1 array per dashboard you are testing
- Take all the arrays you have made, place them in an array, and pass that to the "dashboards" variable

### Running the Load Test

The actual load test is being performed by locust. Once you have set up your locustfile.py, you run the test by navigating to the terminal.

Locust is run from the command line with a series of arguments where you can customize things. Will go over some of the major ones here, but for additional information see the [Locust documentation](https://docs.locust.io/en/stable/)

Command line arguments of note:
- --headless: runs the test without opening the web browser
- -f: points to your locust file, ex -f locustfile.py
- -u: the number of concurrent users to test, ex for three users -u 3 
- -t: how long to run the test for. ex for 30 seconds: -t 30s
- --host: the host to connect to, just copy whatever is in your host variable in the config
- --csv: the name of the csv file to expor the results to, ex: --csv loadtest

So my sample run looked like this:

`locust --headless -f locustfile.py -u 3 -t 10s --host http://localhost:8081/ --csv loadtest`

The results from this run will appear in loadtest_stats.csv. 

### Final Notes

This script uses a lot of short cuts, making assumptions (like all users have the same password) that may not fit your use case. I hope this script can provide some value as a template/starting point for your own load testing. 

Cheers, 

Nathan 
 