cd /home/admin/Workspace

while true; do
  date +"%Y.%m.%d %H:%M:%S"
  if ! pgrep -f task.py &> /dev/null; then
    echo "task.py is dead! Restart it now."
    nohup /home/admin/anaconda3/envs/py38/bin/python task.py < /dev/null &>> task.log &
  else
    echo "task.py is alive."
  fi
  sleep 60
done
