import json
import os

import requests


def download_file(repo, local_filename):
    path = os.getcwd()
    path_without_filename = path + "/gkd-subs/"
    if not os.path.exists(path_without_filename):
        os.makedirs(path_without_filename)

    response = requests.get(f'https://api.github.com/repos/{repo}/releases/latest')
    resp = response.json()
    assets = resp['assets']
    if len(assets) > 0:
        asset = assets[0]
        release_url = asset['browser_download_url']
        response2 = requests.get(release_url)
        if response2.status_code == 200:
            with open(path_without_filename + local_filename, 'wb') as file:
                file.write(response2.content)
            print(f'文件已保存到 {local_filename}')
        else:
            print(f'下载失败，状态码：{response2.status_code}')

if __name__ == '__main__':
    # 读取当前路径下的 config.json 文件
    with open('config.json', 'r') as file:
        data = json.load(file)

    # 假设 JSON 文件中有一个名为 'settings' 的数组
    configs = data.get('configs', [])

    # 遍历数组中的对象
    for config in configs:
        repo = config.get('repo')
        file_name = config.get('file_name')
        print(f'Repo: {repo}, output_file_name: {file_name}')
        download_file(repo, file_name)
