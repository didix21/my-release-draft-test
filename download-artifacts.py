#!/usr/bin/env python


import http.client
import json
import os
import getopt, sys

def get_artifact_urls(token: str, user: str, repo_name: str, build_number: int):
    connection = http.client.HTTPSConnection("circleci.com")
    headers = { 'Circle-Token': f'{token}' }

    connection.request('GET', f'https://circleci.com/api/v2/project/gh/{user}/{repo_name}/{build_number}/artifacts', headers=headers)

    response = connection.getresponse()
    data = response.read()
    json_obj = json.loads(data.decode("utf-8"))

    urls = []
    for item in json_obj['items']:
        urls.append(item['url'])

    return urls

def main():
    try:
        optlist, args = getopt.getopt(sys.argv[1:], '', ['circleci-token=', 'user=', 'repo-name=', 'build-number=', 'download-dir='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    circle_ci_token = ''
    user = ''
    repo_name = ''
    build_number = ''
    download_dir = 'downloaded-artifacts'
    print(optlist)

    for option, argument in optlist:
        if option == '--circleci-token':
            circle_ci_token = argument
        elif option == '--user':
            user = argument
        elif option == '--repo-name':
            repo_name = argument
        elif option == '--build-number':
            build_number = int(argument)
        elif option == '--download-dir':
            if argument != "":
                download_dir = argument
        else:
            assert False, f'Unhandled option {option}'

    if circle_ci_token == '':
        print('Missing circle ci token')
        sys.exit(1)
    if user == '':
        print('Missing user')
        sys.exit(1)
    if repo_name == '':
        print('Missing repo name')
        sys.exit(1)
    if not build_number and build_number != 0:
        print('Missing build number')
        sys.exit(1)

    urls = get_artifact_urls(circle_ci_token, user, repo_name, build_number)
    os.system(f'mkdir -p {download_dir}')

    for url in urls:
        print(f'Downloading: {url} to path {download_dir}')
        os.system(f'(cd {download_dir} && curl -LO {url})')

if __name__ == '__main__':
    main()
