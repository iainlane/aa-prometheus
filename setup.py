#!/usr/bin/python3

import os
import subprocess
import sys
from distutils.command.install_data import install_data
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.install import install


class InstallDataCommand(install_data):
    def run(self):
        files_to_delete = []
        for (_, data_files) in self.data_files:
            for data_file in data_files:
                if os.path.exists(data_file):
                    continue
                try:
                    with open(f"{data_file}.in", "r") as rf:
                        with open(f"{data_file}", "w") as wf:
                            for line in rf:
                                wf.write(
                                    line.replace("@PREFIX@", self.install_dir)
                                )
                        files_to_delete.append(data_file)
                except FileNotFoundError:
                    raise

        install_data.run(self)

        for file_to_delete in files_to_delete:
            os.unlink(file_to_delete)


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        systemd_unit = os.path.join(
            self.prefix,
            "lib",
            "systemd",
            "system",
            "aa-prometheus.service",
        )
        systemd_enable_unit = os.path.join(
            os.path.sep,
            "etc",
            "systemd",
            "system",
            "network.target.wants",
            "aa-prometheus.service",
        )

        if not os.path.exists(systemd_enable_unit) and os.path.exists(
            systemd_unit
        ):
            subprocess.check_call(
                ["systemctl", "enable", "aa-prometheus.service"]
            )


setup(
    name="AAPrometheus",
    version="0.1",
    install_requires=[
        "aiohttp",
        "prometheus-async",
        "prometheus-client",
        "requests",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["aa-prometheus = aa_prometheus.__main__:main"]
    },
    data_files=[
        (
            os.path.join("lib", "systemd", "system"),
            [os.path.join("data", "aa-prometheus.service")],
        )
    ],
    cmdclass={
        "install": PostInstallCommand,
        "install_data": InstallDataCommand,
    },
)
