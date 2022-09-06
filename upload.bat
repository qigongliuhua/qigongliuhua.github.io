set http_proxy=http://127.0.0.1:7890 & set https_proxy=http://127.0.0.1:7890

call update_index.bat
git add .
git commit -m "update"
git push
call clean_index.bat

pause