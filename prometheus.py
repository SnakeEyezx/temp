class Prometheus:
    def __init__(self):
        self.url = f'https://prometheus.org/api/v1/query'
        self.kwargs = {'headers': {'Accept': 'application/json'}, 'verify': False}

    def get_disk_usage(self, host):
        values = []
        start_time = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        end_time = (datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        query = 'node_filesystem_avail_bytes{mountpoint="/var/lib/postgresql", instance="%s:9100"}' % host

        for _time in [start_time, end_time]:
            try:
                req = requests.get(self.url, **self.kwargs, params={'query': query, 'time': _time})
            except Exception as e:
                logging.error(f'Prometheus request failed with query:{query}\nError: {e}')
            else:
                if req.status_code == 200:
                    try:
                        value = int(req.json()['data']['result'][0]['value'][1])
                    except Exception as e:
                        logging.error(f'Failed get value from response. Response: {req.json()}')
                    else:
                        values.append(value)
                else:
                    logging.error(f'Prometheus request status_code is not 200. Status_code: {req.status_code}')
        if len(values) == 2:
            values_diff = (values[0] - values[1]) / 1024**3
            if values_diff > 0:
                return round(values_diff * 1.5)
            else:
                logging.warning(f'get_disk_usage get zero or negative values_diff {values_diff}. Returning 0')
                return 0
        else:
            logging.error(f'get_disk_usage values != 2. Values: {values}')
            return None
