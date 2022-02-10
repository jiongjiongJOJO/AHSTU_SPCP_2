git clone https://gitee.com/jiongjiongJOJO/AHSTU_SPCP_2.git
mv ./AHSTU_SPCP_2/{.,}* ./src
rm -r ./AHSTU_SPCP_2
pip3 install -r ./src/requirements.txt -t ./src