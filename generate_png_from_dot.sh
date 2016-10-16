cat $1 > tmp.dot
dot -Tpng tmp.dot -o $2.png
rm tmp.dot
