import requests
import json
import os
import subprocess
from dotenv import load_dotenv
import secrets
import string


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Define variables
    grafana_host = os.getenv('GRAFANA_HOST')
    if grafana_host == '$host':
        grafana_host = [subprocess.run(['curl', '-s', '2ip.ru'], stdout=subprocess.PIPE, text=True).stdout.strip()][0]
    grafana_port = os.getenv('GRAFANA_PORT')
    grafana_user = os.getenv('GRAFANA_USER')

    password = os.getenv('GF_SECURITY_ADMIN_PASSWORD')
    # If there is default password
    if password == '$password':
        grafana_password = generate_password(10)
        # Write new password in .env file
        with open('.env', 'r') as f:
            old_data = f.read()

        new_data = old_data.replace('$password', grafana_password.strip())

        with open('.env', 'w') as f:
            f.write(new_data)
    else:
        grafana_password = os.getenv('GRAFANA_PASSWORD')

    prometheus_url = os.getenv('PROMETHEUS_URL')

    # Login in grafana
    session = auth(requests.Session(), grafana_host, grafana_port, grafana_user, grafana_password)
    add_datasource(session, prometheus_url, grafana_host, grafana_port)
    uid = get_prometheus_uid(session, grafana_host, grafana_port)
    prepare_app_json(uid)
    add_dashboard(session, "./node-exporter.json", grafana_host, grafana_port)
    add_dashboard(session, "./app.json", grafana_host, grafana_port)

    print('Congratulations! Grafana is running on http://{}:{}'.format(grafana_host, grafana_port))
    print('Login - {}'.format(grafana_user))
    print('Password - {}'.format(grafana_password))


def generate_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def prepare_app_json(uid):
    with open('app.json', 'r') as f:
        old_data = f.read()

    new_data = old_data.replace('${DS_PROMETHEUS}', uid.strip())

    with open('app.json', 'w') as f:
        f.write(new_data)


def auth(session, grafana_host, grafana_port, grafana_user, grafana_password):
    """Auth and establish session"""
    login_data = {
        'user': grafana_user,
        'email': '',
        'password': grafana_password
    }
    headers = {'Content-Type': 'application/json'}
    login_response = session.post(f'http://{grafana_host}:{grafana_port}/login', headers=headers,
                                  data=json.dumps(login_data))
    if not login_response.json()['message'] == 'Logged in':
        print('Issue with login!')
        exit(1)
    return session


def add_datasource(session, prometheus_url, grafana_host, grafana_port):
    """Add datasource into grafana"""
    # Add Prometheus datasource
    datasource_data = {
        'name': 'Prometheus',
        'type': 'prometheus',
        'url': prometheus_url,
        'access': 'proxy',
        'basicAuth': False,
        'isDefault': True,
        'jsonData': {
            'timeInterval': '5s'
        }
    }
    headers = {'Content-Type': 'application/json'}
    session.post(f'http://{grafana_host}:{grafana_port}/api/datasources', headers=headers,
                 data=json.dumps(datasource_data))


def get_prometheus_uid(session, grafana_host, grafana_port):
    # Send a GET request to the Grafana API to retrieve the list of data sources
    response = session.get(f'http://{grafana_host}:{grafana_port}/api/datasources')
    response.raise_for_status()
    datasources = json.loads(response.content)

    # Find the Prometheus datasource in the list of data sources and return its UID
    for datasource in datasources:
        if datasource['name'] == 'Prometheus':
            return datasource['uid']


def add_dashboard(session, dashboard_file, grafana_host, grafana_port):
    """Add dashboard into grafana"""
    # Read dashboard from file
    with open(dashboard_file, 'r') as f:
        dashboard_json = json.load(f)

    # Add dashboard
    dashboard_data = {
        'dashboard': dashboard_json,
        'overwrite': False
    }
    headers = {'Content-Type': 'application/json'}
    session.post(f'http://{grafana_host}:{grafana_port}/api/dashboards/db', headers=headers,
                 data=json.dumps(dashboard_data))


if __name__ == '__main__':
    main()
