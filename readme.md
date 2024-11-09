Creating the .tar

- 1.: docker build -t gruppe-b/flask_application:latest .
- 2.: docker-compose up -d
- 3.: docker save gruppe-b/flask_application:latest -o application.tar

Delete the image (to run everything from the .tar). Then:

- 1.: docker load --input application.tar
- 2.: docker-compose up -d 

