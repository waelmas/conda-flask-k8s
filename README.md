# Conda Flask App on Kubernetes


### Generating Conda environment config

Since many usually use a conda environment with more than the required for the app libraries, before creating the app we want to deploy, it's best to create a fresh environment.

To create a clean environment with no default libraries pre-installed, run the following command:
(Replace "myenv" with whatever name you want to give this new environment. Change 3.8 to whatever Python version you prefer)

```Bash
conda create --name myenv python=3.8 --no-default-packages
```

Once we have this clean environment, start installing whatever libraries are required by your app. You can install libraries using conda or pip as needed.
(A not-so-good but working approach would be to try to run the code install every library that you get an import error for until the code runs)

Once this part is done and you app can now run, use the following command to export the current environment libraries and configuration to a file called "environment.yml"

```Bash
conda env export | grep -v "^prefix: " > environment.yml
```

Replace the environment.yml file in this directory with the one you generated with the above command.


Note:
If you want to create an environment with the same exact setup somewhere else (or share it with someone else), you can create it using the following command:

```Bash
conda env create -f environment.yml
```


Add any conda packages in "environment.yml"
Any pip packages in "requirements.txt"

Write your functions in the Functions Block

Any files related to the app should live in /app directory

### Sample Flask endpoint (from there we call any other functions):

``` Python
@app.route('/my_flask_end', methods=['POST'])
def my_flask_end():
    data = request.get_json()
    # request data
    my_request_var = data['my_request_var']

    my_input = data['my_input']

    # function calls
    response_val1, response_val2 = my_normal_function(my_request_var)

    response_val3 = my_other_function(my_input)

    # response data
    res = {"val1": response_val1, "val2": response_val1, "val3": response_val3}
    return Response(response=json.dumps({"result": res}),
                    status=200,
                    mimetype='application/json')
```


### Testing

Install Docker Desktop
Install Postman (or user browser version)


Run:

$ docker build -t my_app .

$ docker run -p 80:80 my_app


Your app is now running on: http://localhost:80/

We can call our Flask endpoint like this:

In postman, URL is http://localhost:80/my_flask_end
Method: POST
Body: Raw > JSON

``` Typescript
{
    "my_request_var": "input101",
    "my_input": "another one"
}
```

We will get a response:

``` Typescript
{
    "val1": "something 101",
    "val2": "something else",
    "val3": "another value"
}
```