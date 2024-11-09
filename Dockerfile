FROM python:3.11-alpine
# Upgrade pip
RUN pip install --upgrade pip

WORKDIR ./gruppe-b

RUN apk add proj-util
RUN apk add --no-cache build-base proj proj-dev

# Copy requirements.txt
COPY backend/requirements.txt ./backend/requirements.txt
# Install all the dependencies
RUN pip install -r ./backend/requirements.txt

# Copy the folders
COPY . .

# Start
CMD ["python", "backend/config.py"]