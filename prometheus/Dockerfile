FROM prom/prometheus:latest

COPY prometheus.yml /etc/prometheus/prometheus.yml


CMD        ["--config.file=/etc/prometheus/prometheus.yml", \
                "--storage.tsdb.path=/prometheus", \
                "--storage.tsdb.retention.time=365d", \
                "--web.console.libraries=/usr/share/prometheus/console_libraries", \
                "--web.console.templates=/usr/share/prometheus/consoles"]
