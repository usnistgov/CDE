import yaml
import json
import httplib2
import requests

def push_to_corr(config_path=None, project_name=None):
    if config_path:
        config = {}
        with open(config_path, 'r') as config_file:
            config = json.loads(config_file.read())

        scope = config.get('default', {})
        api = scope.get('api',{})
        host = api.get('host','')
        port = api.get('port', 80)
        key = api.get('key', '')
        path = api.get('path', '')
        token = scope.get('app', '')
        client = httplib2.Http('.cache', disable_ssl_certificate_validation=False)
        server_url = "{0}:{1}{2}/private/{3}/{4}/".format(host, port, path, key, token)
        url = "%sprojects" % (server_url)
        project = None
        response, content = http_get(client, url)
        if response.status == 200:
            json_content = json.loads(content)['content']
            exist = False
            if json_content['total_projects'] > 0:
                for _project in json_content['projects']:
                    if _project['name'] == project_name:
                        exist = True
                        project = _project
                        break
            if not exist:
                response, content = put_project(client, server_url, project_name)
                project = json.loads(content)['content']

            push_record(client, server_url, project)
        else:
            print(content)
    else:
        print("Config file not provided.")

def http_get(client, url):
    headers = {'Accept': 'application/json'}
    response, content = client.request(url, headers=headers)
    return response, content.decode('utf-8')

def put_project(client, url, project_name, long_name='No goals provided.', description='No description provided.'):
        url = "%sproject/create" % (url)
        content = {'name':project_name, 'goals':long_name, 'description':description}
        headers = {'Content-Type': 'application/json'}
        response, content = client.request(url, 'POST', json.dumps(content), headers=headers)
        return response, content.decode('utf-8')

def rpz_conf_to_corr():
    stream = open('.reprozip-trace/config.yml', "r")
    config_yaml = yaml.load(stream)
    return config_yaml

def push_record(client, server_url, project):
        record_id = None
        config_yaml = rpz_conf_to_corr()
        url = "%sproject/record/create/%s" % (server_url, project['id'])
        headers = {'Content-Type': 'application/json'}
        _content = {}
        _content['label'] = 'no label provided'
        _content['tags'] = []
        _content['system'] = {}
        _content['inputs'] = []
        _content['outputs'] = []
        _content['dependencies'] = []
        _content['execution'] = {}
        _content['status'] = 'finished'
        _content['timestamp'] = 'not captured'
        _content['reason'] = 'no reason provided'
        _content['duration'] ='not captured'
        _content['executable'] = {}
        _content['repository'] = {}
        _content['main_file'] = ''
        _content['version'] = ''
        _content['parameters'] = {}
        _content['script_arguments'] = 'not captured'
        _content['datastore'] = {}
        _content['input_datastore'] = {}
        _content['outcome'] = 'no outcome provided'
        _content['stdout_stderr'] = 'not captured'
        _content['diff'] = 'not captured'
        _content['user'] = ''
        response, content = client.request(url, 'POST', json.dumps(_content), headers=headers)
        content = content.decode('utf-8')
        if response.status == 200:
            record = json.loads(content)['content']
            record_id = record['head']['id']
            # print(record)
            response = upload_file(server_url, record_id, 'cde-package.zip', 'resource-record')
            # print(response)
        else:
            print(content)

def upload_file(server_url, record_id, file_path, group):
    url = "%sfile/upload/%s/%s" % (server_url, group, record_id)
    files = {'file':open(file_path, "rb")}
    response = requests.post(url, files=files, verify=True)
    return response