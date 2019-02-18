cd /home/DonkeyBites/instaCharts
cp -f /home/InstaPy/app.py /home/DonkeyBites/instaCharts/Server/
cp -rf /home/InstaPy/static/* /home/DonkeyBites/instaCharts/Server/static/
cp -rf /home/InstaPy/templates/* /home/DonkeyBites/instaCharts/Server/templates/
git pull
git add Server/
git commit -m"Update Server"
git add *.json
git commit -m"Update json"
git add *.log
git commit -m"Update log"
git add index.html
git commit -m"Update index.html"
git add *.sh
git commit -m"Update Shell files"
git push origin master

