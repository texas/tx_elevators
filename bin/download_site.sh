# run from root directory
set +e

PROJECT=./example_project
PORT=8008


DEBUG=0 python $PROJECT/manage.py runserver --nothreading --noreload $PORT &
pid=$!
echo "runserver pid: $pid"

# make sure to kill the server if terminated early
trap "kill $pid; echo bye $pid" EXIT

# give time for the servers to get up
sleep 1

python $PROJECT/manage.py collectstatic --noinput

mkdir -p site
cd site && wget -r localhost:$PORT --force-html -e robots=off -nH -nv --max-redirect 0

# kill server, run in a subprocess so we can suppress "Terminated" message
(kill $pid 2>&1) > /dev/null

echo "bye"
