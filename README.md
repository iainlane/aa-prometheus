# A&A prometheus

Load the remaining quota provided by AAISP and expose the `quota_remaining`
(number of bytes remaining) as a Prometheus metric.

## Installation

Install with `pip` from a `git` checkout. On Ubuntu or Debian:

```
apt install python3-pip
cd /path/to/git/checkout
pip3 install -r requirements.txt .
systemctl start aa-prometheus
```

And then it should be available on `http://your.host:8000/metrics`.

## WTF

The nonsense with `--no-binaries` in requirements.txt is needed because when
we build the wheel, the systemd unit gets an incorrect prefix substituted -
the `install_data` hook is run when packing up the wheel and not when
installing onto the target system.

If you know how to perform the substitution when we are *actually*
installing, please let me know and I can remove that.