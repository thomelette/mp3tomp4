# mp3tomp4

__main__.py is the main entry point

[ ] bugfix/feature: video rendering status isn't reported dynamically (please wait a few minutes for it to finish)

[ ] bugfix: terrible issue i've seen with occasional savify downloaded files,
https://stackoverflow.com/questions/48687852/non-monotonous-dts-in-output-stream-when-concat-videos-using-ffmpeg

# example usage

### batch album example operation,
python3 mp3tomp4 -s "./input" -a

### single long playlist example operation,
python3 mp3tomp4 -d "./playlist-mp3s" --shuffle -m 60 -p "videoname-prefix"

### single long updated playlist example operation,
python3 mp3tomp4 -d "./playlist-mp3s" --shuffle -m 60 -p "videoname-prefix" --update