* Run Gunicorn with Uvicorn Workers ("https://fastapi.tiangolo.com/deployment/server-workers/"):-

** Executable Command :- uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000


Let's see what each of those options mean:

* main:app: This is the same syntax used by Uvicorn, main means the Python module named "main", so, a file main.py. And app is the name of the variable that is the FastAPI application.

* You can imagine that main:app is equivalent to a Python import statement like:


* from main import app :- So, the colon in main:app would be equivalent to the Python import part in from main import app.

--workers: The number of worker processes to use, each will run a Uvicorn worker, in this case, 4 workers.
--worker-class: The Gunicorn-compatible worker class to use in the worker processes.
* Here we pass the class that Gunicorn can import and use with:


* import uvicorn.workers.UvicornWorker
--bind: This tells Gunicorn the IP and the port to listen to, using a colon (:) to separate the IP and the port.

* If you were running Uvicorn directly, instead of --bind 0.0.0.0:80 (the Gunicorn option) you would use --host 0.0.0.0 and --port 80.
* In the output, you can see that it shows the PID (process ID) of each process (it's just a number).

You can see that:

The Gunicorn process manager starts with PID 19499 (in your case it will be a different number).
Then it starts Listening at: http://0.0.0.0:80.
Then it detects that it has to use the worker class at uvicorn.workers.UvicornWorker.
And then it starts 4 workers, each with its own PID: 19511, 19513, 19514, and 19515.
Gunicorn would also take care of managing dead processes and restarting new ones if needed to keep the number of workers. So that helps in part with the restart concept from the list above.

Nevertheless, you would probably also want to have something outside making sure to restart Gunicorn if necessary, and also to run it on startup, etc.