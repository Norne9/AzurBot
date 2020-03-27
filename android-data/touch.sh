while [ 1 ]; do
  read x y
  kill -SIGINT $pid
  input swipe $x $y $x $y 1000 &
  pid=$!
  echo "ok-ok"
done