!/bin/bash

rsync -av $1 $1_pkg
rsync -av shared $1_pkg
cp __init__.py $1_pkg && cp requirements.txt $1_pkg


fission spec apply --wait -v=2

rm -rf $1_pkg