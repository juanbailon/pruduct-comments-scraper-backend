# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Firefox

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN install -d -m 0755 /etc/apt/keyrings
RUN apt-get install wget
RUN wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
RUN  gpg -n -q --import --import-options import-show /etc/apt/keyrings/packages.mozilla.org.asc | awk '/pub/{getline; gsub(/^ +| +$/,""); if($0 == "35BAA0B33E9EB396F59CA838C0BA5CE6DC6315A3") print "\nThe key fingerprint matches ("$0").\n"; else print "\nVerification failed: the fingerprint ("$0") does not match the expected one.\n"}'
RUN echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null

RUN echo '\
Package: *\
Pin: origin packages.mozilla.org\
Pin-Priority: 1000\
' | tee /etc/apt/preferences.d/mozilla

RUN apt-get update && apt-get install -y firefox

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
COPY .env /app/.env

# Run app.py when the container launches
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]