ls *mp4 | xargs -n 1 -I {} echo 'file {}' > concat.txt
ffmpeg -f concat -i concat.txt -c copy adpt.mp4
