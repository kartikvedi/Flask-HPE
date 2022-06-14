from flask import Flask, render_template, request, url_for, redirect
import os , glob
from jinja2 import Template
BASE = os.path.dirname(os.path.abspath(__file__))
NEW_REQUESTS = os.path.join(BASE, 'ChangeRequest', 'New')
COMPLETED_REQUESTS = os.path.join(BASE, 'ChangeRequest', 'Completed')
FAILED_REQUESTS = os.path.join(BASE, 'ChangeRequest', 'Failed')
SCHEMA = os.path.join(BASE, 'schema')
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        data = {}
        mainKeys = ["HORCM Instance Number", "Username" , "Password" , "Array Serial Number",  "VSM", "Port"]
        hostGroupCreationKeys = ["Host Group Name", "Host Mode","Host Mode Options", "HBA wwn", "HBA wwn nickname"]

        formdata = request.form.to_dict()


        for key in mainKeys:
            data[key] = formdata[key]

        if "hgc" in formdata:
            data["Host Group Creation"] = {}
            for key in hostGroupCreationKeys:
                data["Host Group Creation"][key] = formdata[key]


        with open(os.path.join(SCHEMA, 'yaml.j2')) as f:
            rendered = Template(f.read()).render(data=data)

        with open(os.path.join(NEW_REQUESTS, formdata["Change Request Number"] + '.yaml'), "w+") as f:
            f.write(rendered)
            f.close()

        files = {
            "New": len(glob.glob(NEW_REQUESTS + "/*.yaml")),
            "Completed": len(glob.glob(COMPLETED_REQUESTS + "/*.yaml")),
            "Failed": len(glob.glob(FAILED_REQUESTS + "/*.yaml"))
        }

        return render_template("created.html", content=files, crn=formdata['Change Request Number'])
    files = {
        "New": len(glob.glob(NEW_REQUESTS + "/*.yaml")),
        "Completed": len(glob.glob(COMPLETED_REQUESTS + "/*.yaml")),
        "Failed": len(glob.glob(FAILED_REQUESTS + "/*.yaml"))
    }
    return render_template("index.html", content=files)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)