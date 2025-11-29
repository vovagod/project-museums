# Образец
#!/bin/bash
set -e

cd $SRC_PATH

case "$1" in
    web)
       echo "Start gunicorn server"
       gunicorn django_app.wsgi -b=0.0.0.0:8080
       echo "Done gunicorn server"
       ;;
    grpc)
       python3 manage.py migrate
       echo "Migrations done"
       python3 manage.py parseyaml yamls;
       echo "Start gRPC server alpha"
       python3 manage.py run_celery celery_worker &
       echo "Start celery worker"
       python3 manage.py run_celery celery_beat &
       echo "Start celery beat"
       python3 -m grpc_api.server --alpha &
       echo "Start gRPC server UI"
       python3 -m grpc_api.server --ui &
       echo "Start gRPC server"
       python3 -m kafka_impl.kafka_comsumer &
       echo "Start kafka consumer"
       python3 -m grpc_api.server
       echo "Done gRPC server";
       ;;
    *)
      exec "$@"
esac

