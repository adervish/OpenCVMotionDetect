ls  /Volumes/flash/  | grep MP4 | xargs -I {} -n 1 ffmpeg -start_number 1 -i {}_%06d.jpg {}_out.mp4
