cd ../docker
docker-compose up -d
timeout 5
start ..
docker exec -it anaconda jupyter notebook list > token.txt
python url_notebook.py