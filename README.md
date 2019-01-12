
# Build a real world alerting service for Elasticsearch

### How it works
The idea of this project is to use the Raspberry Pi to control the relay module and light on the warning light. There are many alarm lights on the store, they are very simple, you plug power, it start to flash, you unplug it, it stop flash, simple enough for us to use, but wait, they usually need to power up with higher voltage, like 12v, 36v or even 220v, but Pi can only support 5v or 3.3v, so we can’t control it directly with Pi, but with relay, we can make it happen, a relay is an electrically operated switch, it use a very low power electromagnet to mechanically operate a switch, and that switch can be the bridge to connect the high power power supply and our warning light.

Then we will build a webhook service, the service is used to send the command to the relay, tell the relay to switch on or off, which also means control the alarm light.

And finally we will use Elasticsearch’s alerting feature to trigger the webhook once we found some interesting events in Elasticsearch.


### Diagram

<img width="800" alt="Real alarm warning light!" src="https://github.com/medcl/pi-warning-light-for-elasticsearch/raw/master/fritzing.png">

### Setup

<img width="800" alt="Real alarm warning light!" src="https://github.com/medcl/pi-warning-light-for-elasticsearch/raw/master/wiring_diagram.jpg">

### How to use

- Start webhook

```
python web.py
```

- Testing

```
➜  ~ curl -XPOST http://pi:9000/ -d'{"a":1}'
{"success":true}
```

- Create watch in Elasticsearch

```
curl -XPUT "http://192.168.1.202:9200/_xpack/watcher/watch/server_is_down" -H 'Content-Type: application/json' -d'
{
  "trigger": {
    "schedule": {
      "interval": "1s"
    }
  },
  "input": {
    "search": {
      "request": {
        "search_type": "query_then_fetch",
        "indices": [
          "heartbeat-*"
        ],
        "types": [],
        "body": {
          "size": 0,
          "query": {
            "bool": {
              "must": [
                {
                  "range": {
                    "@timestamp": {
                      "gte": "now-3s"
                    }
                  }
                },
                {
                  "match": {
                    "monitor.status": "down"
                  }
                }
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": {
      "ctx.payload.hits.total": {
        "gte": 1
      }
    }
  },
  "actions": {
    "alarm_webhook": {
      "webhook": {
        "scheme": "http",
        "host": "192.168.1.200",
        "port": 9000,
        "method": "post",
        "params": {},
        "headers": {},
        "body": "SOS, server is down!"
      }
    }
  },
  "throttle_period_in_millis": 5000
}'

```

### Demo
Youtube: [https://www.youtube.com/watch?v=Zy6_Yk5DVBo](https://www.youtube.com/watch?v=Zy6_Yk5DVBo)

<iframe width="560" height="315" src="https://www.youtube.com/embed/Zy6_Yk5DVBo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

