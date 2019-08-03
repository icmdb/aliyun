# Aliyun Contianer Service Registry

## Quick Start

```bash
# Start iwebhook-csr
docker-compose up -d

# Setting webhook csr webhook
http://your-webhook-server-addr/ali/csr/webhook?slackin=base64-encoded-str-of-your-slack-incoming-url&channer=your-target-channel
```

## Webhook

* [容器镜像服务 - Webhook使用说明](https://yq.aliyun.com/articles/64921)

```bash
POST /payload HTTP/1.1

Content-Type: application/json
Request URL: https://cs.console.aliyun.com/hook/trigger?triggerUrl=YzRmMWE5YzM2ZjMzYzQ0NmFiMGYzNWJlMmM2MjM2NzIyfGV4cHJlc3N8cmVkZXBsb3l8MThlMmllY2drdXYyZXw=&secret=365a4a664b45615438716a487a75695a7ac48329224b35b073c2197374e7d62a
Request method: POST

{
    "push_data": {
        "digest": "sha256:457f4aa83fc9a6663ab9d1b0a6e2dce25a12a943ed5bf2c1747c58d48bbb4917",
        "pushed_at": "2016-11-29 12:25:46",
        "tag": "latest"
    },
    "repository": {
        "date_created": "2016-10-28 21:31:42",
        "name": "repoTest",
        "namespace": "namespace",
        "region": "cn-hangzhou",
        "repo_authentication_type": "NO_CERTIFIED",
        "repo_full_name": "namespace/repoTest",
        "repo_origin_type": "NO_CERTIFIED",
        "repo_type": "PUBLIC"
    }
}
```

* Slack Payload

```bash
{
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
```
