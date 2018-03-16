set -v

# Install logging monitor to pick up logs sent to syslog
curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash
service google-fluentd restart &

# install dependencies necessary to download and run our python app
apt-get update
apt-get install -yq git build-essential supervisor python python-dev python-pip libffi-dev libssl-dev

# pip from apt is out of date, so make it update itself and install virtualenv.
pip install --upgrade pip virtualenv

# Create an app user - the app will run as this user
useradd -m -d /home/app app

# Pull our source code
export HOME=/root
git config --global credential.helper gcloud.sh
git clone https://github.com/morganjbruce/microservices-in-action.git /opt/app

# change to the app working directory
cd /opt/app/chapter-8/market-data

# Install app dependencies
virtualenv env
env/bin/pip install -r requirements.txt

# Make sure the app user owns the application code
chown -R app:app /opt/app

# Configure supervisor to start gunicorn inside of our virtualenv and run the
# application.
cat >/etc/supervisor/conf.d/market-data-app.conf << EOF
[program:app]
directory=/opt/app/chapter-8/market-data
command=/opt/app/chapter-8/market-data/env/bin/gunicorn -c config.py app:app --bind 0.0.0.0:8080
autostart=true
autorestart=true
user=app
# Environment variables ensure that the application runs inside of the
# configured virtualenv.
environment=VIRTUAL_ENV="/opt/app/env/chapter-8/market-data",PATH="/opt/app/chapter-8/market-data/env/bin",\
    HOME="/home/app",USER="app"
stdout_logfile=syslog
stderr_logfile=syslog
EOF

supervisorctl reread
supervisorctl update
