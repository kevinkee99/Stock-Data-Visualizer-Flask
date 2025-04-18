#Use an official Python Image
FROM python:3.8-slim-buster
#set the working directory in the container to app
WORKDIR /app
#Copy the connets of the current direcotry into the app directory
COPY . /app
#Upgrade pip
RUN pip install --upgrade pip
#Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt
#set the default commands to run when starting the container
CMD ["python", "app.py"]