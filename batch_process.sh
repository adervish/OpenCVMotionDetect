ls /Volumes/flash/ | grep MP4 | xargs -I {} -n 1 ./video_detect.py -o {} -v /Volumes/flash/{} -a 400 -s T
