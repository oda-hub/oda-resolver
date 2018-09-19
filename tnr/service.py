from flask import Flask, jsonify
app = Flask(__name__)

import requests

from tnr.resolvers import RootResolver

@app.route('/api/v1.0/byname/<string:name>')
def resolve(name):
    root_resolver=RootResolver()

    return jsonify(root_resolver.resolve(name))

@app.route('/api/v1.0/timespan/byname/<string:name>')
def timespan_byname(name):
    root_resolver=RootResolver()

    data=root_resolver.resolve(name).values()[0]

    best_utc="unknown"
    for event in data['events']:
        if 'utc' in event:
            best_utc=event['utc']
            break

    return jsonify(dict(
                utc=best_utc,
            ))



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
