# -*- coding: utf-8 -*-
#
# @reference:
#   https://api.slack.com/incoming-webhooks
#   https://api.slack.com/tools/block-kit-builder
#   https://yq.aliyun.com/articles/64921
#
"""
{
    "push_data": {
        "digest": "sha256:14bf0c9f45293f4783bd75e51ea68689103k89da6e51db75ef30b8564fe8d3cc",
        "pushed_at": "2019-08-03 15:02:58",
        "tag": "latest"
    },
    "repository": {
        "date_created": "2019-08-03 12:37:44",
        "name": "webhook-acr",
        "namespace": "icmdb",
        "region": "cn-hongkong",
        "repo_authentication_type": "NO_CERTIFIED",
        "repo_full_name": "icmdb/webhook-acr",
        "repo_origin_type": "NO_CERTIFIED",
        "repo_type": "PUBLIC"
    }
}
"""

import os
import sys
import json
import base64
import logging
from logging.config import dictConfig

import requests
from flask import Flask, request


APP_ADDR  = os.getenv("APP_ADDR", '0.0.0.0')
APP_PORT  = os.getenv("APP_PORT", 8888)
APP_DEBUG = os.getenv("APP_DEBUG", True)


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)


@app.route("/debug", methods=["GET"])
def test():
    with open("debug.html", "r") as f:
        content = f.read()
        f.close()
        return content


@app.route('/ali/csr/webhook', methods=['POST', 'GET'])
def ali_csr_webook():
    payload = {
        "channel": u"#ops-builds",
        "username": u"阿里云容器镜像服务",
        "attachments": [
            {
                "fallback": "Image [<https://cr.console.aliyun.com/repository/REGION/NAMESPACE/PROJECT/details|NAMESPACE/PROJECT>] pushed sucessfully!",
                "pretext": "Image [<https://cr.console.aliyun.com/repository/REGION/NAMESPACE/PROJECT/details|NAMESPACE/PROJECT>] pushed sucessfully!",
                "color": "#D00000",
                "fields": [
                    {
                        "title":"image: NAMESPACE/PROJECT",
                        "value":"region: REGION\n tag: TAG\n at: PUSH_AT",
                        "short": "false"
                    }
                ]
            }
        ]
    }

    if request.method == "POST":
        req_args = request.args.to_dict()
        req_data = request.get_data()
        req_json = json.loads(req_data)
        if APP_DEBUG == True:
            print("%s" % (req_json))

        region    = req_json["repository"]["region"]
        namespace = req_json["repository"]["namespace"]
        registry  = req_json["repository"]["name"]
        tag       = req_json["push_data"]["tag"]
        pushed_at = req_json["push_data"]["pushed_at"]
        repo_type = req_json["repository"]["repo_type"]
        image     = "/".join([namespace, registry])
        info      = "Image [<https://cr.console.aliyun.com/repository/%s/%s/details|%s>] pushed sucessfully!" % (region, image, image)

        payload["attachments"][0]["fallback"] = info
        payload["attachments"][0]["pretext"]  = info
        payload["attachments"][0]["fields"][0]["title"] = "image: %s" % (image)
        payload["attachments"][0]["fields"][0]["value"] = "\n".join([
            "*pushed_at*: _%s_" % (pushed_at),
            "*region*: _%s_" % (region),
            "*type*: _%s_" % (repo_type.lower()),
            "*tag*: _%s_" % (tag),
        ])
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        slack_incoming_url = ""

        if "slackin" in req_args.keys():
            slack_incoming_url = base64.b64decode(req_args["slackin"])
        if "channel" in req_args.keys():
            payload["channel"] = '#' + req_args["channel"]

        if APP_DEBUG == True:
            print("slack_incoming_url: %s | payload:%s | headers:%s" % (slack_incoming_url, json.dumps(payload), headers))
            print("curl -X POST --data-urlencode 'payload=%s' %s" % (json.dumps(payload), slack_incoming_url))

        r = requests.post(slack_incoming_url, data=json.dumps(payload), headers=headers)
        if r.ok == False:
            app.logger.error("slack_incoming failed.")
            with open("debug.html", "w") as f:
                f.write(r.content)
            f.close()
            return '{"status": "error"}'
        return '{"status": "ok"}'
    return '{"status": "ok"}'


if __name__ == '__main__':
    #handler = logging.FileHandler("flask.log")
    #app.logger.addHandler(handler)
    app.run(host=APP_ADDR, port=APP_PORT, debug=APP_DEBUG)
