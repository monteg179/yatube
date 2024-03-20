#!/bin/bash

OUT=setup.out
ERR=setup.err

docker_image_prune() {
    echo -n "Docker image prune ..."
    sudo docker image prune -af 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
    fi
    return $error
}

docker_compose_build() {
    echo -n "Docker compose build ..."
    docker compose build -q 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
    fi
    return $error
}

docker_compose_pull() {
    echo -n "Docker compose pull ..."
    docker compose pull -q 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
    fi
    return $error
}

docker_compose_up() {
    echo -n "Docker compose up ..."
    docker compose up -d --wait database django gateway 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
    fi
    return $error
}

docker_compose_down() {
    echo -n "Docker compose down ..."
    docker compose down 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
    fi
    return $error
}

docker_compose_remove() {
    echo -n "Docker compose remove ..."
    docker compose down -v 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
    fi
    return $error
}

docker_compose_init() {
    echo -n "[django] service: waiting [database] service "
    while ! sudo docker compose exec django nc -zv database 5432 >/dev/null 2>&1
    do
        echo -n "."
        sleep 1
    done
    echo " completed"
    echo -n "[django] service: django migrate ..."
    docker compose exec django \
        python manage.py migrate 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
        return $error
    fi

    echo -n "[django] service: create superuser ..."
    docker compose exec django \
        python manage.py superuser 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
        return $error
    fi
    echo -n "[django] service: import data ..."
    docker compose exec django \
        python manage.py import_db data/leo 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
        return $error
    fi
    echo -n "[django] service: collectstatic ..."
    docker compose exec django \
        python manage.py collectstatic --noinput 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
        return $error
    fi
    echo -n "[django] service: copy static ..."
    docker compose exec django \
        cp -r /app/static/. /staticfiles/static/ 1> $OUT 2>$ERR
    error=$?
    if [ $error -eq 0 ]; then
	    echo " completed"
    else
	    echo " error($error)"
    fi
    return $error
}

case "$1" in
	install)
	    docker_compose_build && docker_compose_up && docker_compose_init
		if [ $? -ne 0 ]; then
			exit 1
		fi
		;;
	uninstall)
        docker_compose_remove && docker_image_prune
		if [ $? -ne 0 ]; then
			exit 1
		fi
		;;
    *)
        echo "Usage: sudo bash $0 {install | uninstall}"
        exit 1
        ;;
esac

exit 0