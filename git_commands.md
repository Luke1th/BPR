#create a new repository on the command line

echo "git_commands" >> README.md 
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Luke1th/BPR.git
git push -u origin main

git status   #check the status of the files/folders available
git add simplefile.py   #adds a single file/folder
git add .               #adds all the files and folders to GitHub


#or push an existing repository from the command line
git remote add origin https://github.com/Luke1th/BPR.git
git branch -M main
git push -u origin main
