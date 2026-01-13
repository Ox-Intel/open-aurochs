import os
import datetime

release_image = os.environ.get('DOCKER_IMAGE')
commit_hash = os.environ.get('IMAGE_TAG')
file_path = os.environ.get('RELEASE_DIR', "ox-release")
file = os.path.join(f'release/{file_path}', "release_version.txt")

with open(file, "w") as file:
    file.write(f'Release generated: {datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")}Z\n')
    file.write(f'Release source image: {release_image}\n')
    file.write(f'Source identifier: {commit_hash}\n')
