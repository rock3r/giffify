#!/bin/bash

# License for any modification to the original (linked below):
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Sebastiano Poggi and Daniele Conti wrote this file. As long as you retain 
# this notice you can do whatever you want with this stuff. If we meet some day,
# and you think this stuff is worth it, you can buy us a beer in return.

if ! which "ffmpeg" > /dev/null 2>&1; then
  echo "You need ffmpeg in your path to run giffify" >&2
  exit 1
fi

show_usage() {
  echo "Usage:"
  echo ""
  echo "giffify -i input_path.mp4 -o output_path.gif [-w width] [-y height] [-f fps=15] [-s speed=2] [-h shows this message]"
}

input_path=""
output_path=""
dw=-1
dh=-1
fps=15
speed=1

while getopts ":i:o:w:y:f:s:h" opt; do
  case $opt in
    i )
      input_path=$OPTARG
      ;;
    o )
      output_path=$OPTARG
      ;;
    w )
      dw=$OPTARG
      ;;
    y )
      dh=$OPTARG
      ;;
    f )
      fps=$OPTARG
      ;;
    s )
      speed=$OPTARG
      ;;
    h )
      show_usage
      exit 0
      ;;
    \? )
      echo "Argument $OPTARG not recognized." >&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [[ -z "$input_path" ]]; then
  echo "You must specify an input file to process"
  echo ""
  show_usage
  exit 1
fi

if [[ -z "$output_path" ]]; then
  output_path="$input_path.gif"
fi

palette="palette.png"
filters="fps=$fps,setpts=1/$speed*PTS,scale=$dw:$dh:flags=lanczos"

ffmpeg -v warning -i $input_path -vf "$filters,palettegen" -y $palette
if [[ -f $palette ]]; then
  ffmpeg -v warning -i $input_path -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse" -y $output_path
  rm $palette
fi
