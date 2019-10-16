#!/usr/bin/env python
import logging
from tools.container_helper import container_handler

import docker

logger = logging.getLogger("main")


def docker_monitor(config):
    logger.info(config)
    docker_client = docker.APIClient(base_url="unix://var/run/docker.sock")
    logger.info("docker version: {} ".format(docker_client.version().get("Version")))
    containers = docker_client.containers(size=True)
    if not containers:
        logger.info("Can't find any running container on this machine.")
    else:
        for item in containers:
            container_name = item.get("Names")[0]
            SizeRw = item.get("SizeRw")
            SizeRootFs = item.get("SizeRootFs")
            docker_stats = docker_client.stats(container_name, stream=False)
            docker_stats["SizeRw"] = SizeRw
            docker_stats["SizeRootFs"] = SizeRootFs
            container_handler(config, docker_stats)
