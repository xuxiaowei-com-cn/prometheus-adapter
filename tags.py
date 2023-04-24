import os

import requests

tags_url = 'https://api.github.com/repos/kubernetes-sigs/prometheus-adapter/tags'
# 从环境变量中获取参数
num = os.getenv("num")
print(f'num={num}')
page = os.getenv("page")
print(f'page={page}')

if num is not None:
    num = int(num)
if page is not None:
    page = int(page)
    tags_url += f'?page={page}'

resp = requests.get(tags_url)

resp_json = resp.json()

file_name = 'tags.sh'
if os.path.exists(file_name):
    os.remove(file_name)

file = open(file_name, 'w')

i = 0
for tag in resp_json:
    i = i + 1
    image = f"registry.k8s.io/prometheus-adapter/prometheus-adapter:{tag['name']}"
    msg = f"docker pull {image} || echo '不存在：{image}'"
    print(msg)
    file.write(msg)
    file.write('\n')

file.write('\n')

i = 0
for tag in resp_json:
    i = i + 1
    image = f"registry.k8s.io/prometheus-adapter/prometheus-adapter:{tag['name']}"
    msg = f"docker tag {image} $DOCKER_USERNAME/prometheus-adapter:{tag['name']} || echo '打标签失败：{image}'"
    print(msg)
    file.write(msg)
    file.write('\n')

    if num is not None and i >= num:
        break
