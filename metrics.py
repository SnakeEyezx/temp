import requests

x = requests.get('http://taskschedule-02.psql.travelata.lan:9100/metrics')

from prometheus_client.parser import text_string_to_metric_families
def parsemetrics(metrics):
    a = None
    b = None
    for family in text_string_to_metric_families(metrics):
        avail_bytes = [sample.value for sample in family.samples if sample.name == 'node_filesystem_avail_bytes' and
                sample.labels.get('mountpoint') == '/var/lib/postgresql' and
                sample.labels.get('fstype') == 'ext4']
        size_bytes = [sample.value for sample in family.samples if sample.name == 'node_filesystem_size_bytes' and
                sample.labels.get('mountpoint') == '/var/lib/postgresql' and
                sample.labels.get('fstype') == 'ext4']
        if len(avail_bytes) > 0:
            a = avail_bytes[0]
        elif len(size_bytes) > 0:
            b = size_bytes[0]
            # 100 - ((node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"} * 100)
            # / node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"})
    return 100 - ((a * 100) / b)

print(parsemetrics(x.text))
