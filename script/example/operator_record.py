import asyncio
import os
from datetime import datetime
from typing import Union

from eth_typing import Address, ChecksumAddress

root = 'operate-record'


def file_lines(file_path):
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return len(lines)



def create_file_if_not_exists(file_dir: str, operate: str):
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{current_date}-{operate}.txt"
    file_path = f"{file_dir}/{file_name}"
    if not os.path.exists(file_path):
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(file_path, 'w') as file:
            print(f"文件 {file_path} 不存在，已创建。")
    else:
        print(f"文件 {file_path} 已存在。")


async def record_success_operator_address(address: Union[Address, ChecksumAddress], operate: str):
    file_path = record_today_file_path(operate)
    create_file_if_not_exists(root, operate)
    with open(file_path, 'a') as file:
        file.write('\n')
        file.write(address)
        pass


def record_today_file_path(operate: str):
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{current_date}-{operate}.txt"
    file_path = f"{root}/{file_name}"
    return file_path


if __name__ == '__main__':
    asyncio.run(record_success_operator_address('ssskkk', 'asd'))
