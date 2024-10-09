from flask import Flask, render_template
import json

app = Flask(__name__)
app.config['SECRET_KEY'] ='SECRET_KEY'



@app.route('/<int:page>')
def main(page): # individual pages for all stock
    f = open("robots.json", "r")
    temp=f.read()
    f.close()
    temp = json.loads(temp)
    robots =[]
    for i in temp:
        robots.append(temp[i])
    print(robots)
    f = open("tasks.json", "r")
    temp=f.read()
    f.close()
    temp = json.loads(temp)
    tasks =[]
    for i in temp:
        tasks.append(temp[i])
        
    print(tasks)
    
    return render_template('main.html',robots=robots,tasks=tasks,page=page)