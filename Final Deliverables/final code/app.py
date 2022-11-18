{
  "metadata": {
    "kernelspec": {
      "name": "python",
      "display_name": "Python (Pyodide)",
      "language": "python"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "python",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8"
    }
  },
  "nbformat_minor": 5,
  "nbformat": 4,
  "cells": [
    {
      "cell_type": "code",
      "source": "from flask import Flask,request,render_template\nimport pickle\nimport cv2\nfrom skimage import feature\nimport os.path\n\napp = Flask(__name__)\n\n\n@app.route('/')\ndef hello_world():\n    return render_template(\"index.html\")\nclass my_dictionary(dict):\n  def __init__(self):\n    self = dict()\n  def add(self, key, value):\n    self[key] = value\ndatabase=my_dictionary()\n\n\n@app.route('/form_reg',methods=['POST','GET'])\ndef reg():\n    name2=request.form['userid']\n    pwd1=request.form['pwd']\n    if name2 in database:\n        return render_template('index.html',info='UserName Already Taken!!')\n    else:\n        database.add(name2,pwd1)\n        return render_template(\"index.html\")\n@app.route('/form_login',methods=['POST','GET'])\ndef login():\n    name1=request.form['userid']\n    pwd=request.form['pwd']\n    if name1 not in database:\n\t    return render_template('index.html',info='Invalid User!!')\n    else:\n        if database[name1]!=pwd:\n            return render_template('index.html',info='Invalid Password!!')\n        else:\n\t         return render_template('home.html',name=name1)\n@app.route(\"/\") \ndef about():\n    return render_template(\"home.html\")#rendering html page\n\n@app.route(\"/home\") \ndef home():\n    return render_template(\"home.html\")\n\n@app.route(\"/upload\")\ndef test():\n    return render_template(\"pred.html\")\n\n@app.route(\"/logout\")\ndef log():\n    return render_template(\"index.html\")\n\n@app.route('/predict', methods=['GET', 'POST'])\ndef upload():\n    if request.method == 'POST':\n        f=request.files['file'] #requesting the file\n        basepath=os.path.dirname(os.path.realpath('__file__'))#storing the file directory\n        filepath=os.path.join(basepath,\"uploads\",f.filename)#storing the file in uploads folder\n        f.save(filepath)#saving the file\n\n        #Loading the saved model\n        print(\"[INFO] loading model...\")\n        model = pickle.loads(open('parkinson_Deploy.pkl', \"rb\").read())\n\n        # Pre-process the image in the same manner we did earlier\n        image = cv2.imread(filepath)\n        output = image.copy()\n\n        # Load the input image, convert it to grayscale, and resize\n        output = cv2.resize(output, (128, 128))\n        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n        image = cv2.resize(image, (200, 200))\n        image = cv2.threshold(image, 0, 255,\n    \tcv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]\n\n    \t# Quantify the image and make predictions based on the extracted features using the last trained Random Forest\n        features = feature.hog(image, orientations=9,\n\t\tpixels_per_cell=(10, 10), cells_per_block=(2, 2),\n\t\ttransform_sqrt=True, block_norm=\"L1\")\n        preds = model.predict([features])\n        print(preds)\n        ls=[\"healthy\",\"parkinson\"]\n        result = ls[preds[0]] \n        return result\n    return None\n\n    \nif __name__ == '__main__':\n    app.run()",
      "metadata": {},
      "execution_count": null,
      "outputs": [],
      "id": "618fef5b-2128-4dc8-86ba-df90f1a4c655"
    }
  ]
}