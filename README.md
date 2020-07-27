# Description

This is an automation written in Python for pinning Status Sticker Packs to our IPFS cluster.

In simple terms it talks to a [`go-ethereum`](https://github.com/ethereum/go-ethereum) node over RPC and waits for specific Ethereum Contract events to detect new Sticker Packs being added. When it detects such an event it talks to the IPFS cluster to pin the pack metadata and all the images.

# Requirements

This software assumes availability of two endpoints:

* `http://localhost:8545` - Geth RPC Admin API
* `/dns/localhost/tcp/9094/http` - IPFS Cluster Admin API

You can specify those with `--geth-addr` and `--ipfs-addr` respectively.

# Usage

The simplest way to use it is to just run it:
```
./main.py
INFO - Connecting to Geth RPC: http://localhost:8545
INFO - Connecting to IPFS Cluster: /dns/localhost/tcp/9094/http
INFO - Watching for events: ContenthashChanged,Register
```
Here's the available options:
```
Usage: main.py [options]

Utility for pinning images from Status Sticker packs.

Options:
  -h, --help            show this help message and exit
  -p, --pin-all         If all packs should be pinned on start.
  -g GETH_ADDR, --geth-addr=GETH_ADDR
                        IPFS Cluster API URL.
  -i IPFS_ADDR, --ipfs-addr=IPFS_ADDR
                        IPFS Cluster API MultiAddress.
  -e EVENTS, --events=EVENTS
                        Contract events to watch for.
  -c CONTRACT, --contract=CONTRACT
                        Sticker Pack contract address.
  -I LOG_LEVEL, --log-level=LOG_LEVEL
                        Level of logging.

Example: ./main.py --pin-all=true --events=ContenthashChanged
```

# Details

This software:

1. Connects to Geth Admin RCP API
2. Connects to IPFS Admin API
3. Pins all currently existing Sticker Packs to IPFS (__Optional__)
4. Listens via the synced Geth node for Sticker Pack contract events
5. On `ContenthashChanged` or `Register` events it:
  - Extracts `contenthash` from their arguments
  - Pins the Sticker Pack metadata file
  - Extracts from the metadata file image hashes
  - Pins the Sticker pack images to the IPFS cluster

# Docker Image

You can build a Docker image with:
```
docker build -t statusteam/auto-sticker-pinner:latest .
```

# Known Issues

* Currently IPFS Cluster API does not expose any info about possible pinning errors
  - We run `GET /pin/{chash}` to check if it was pinned as an alternative
* Checking pin status for a cluster returns multiple statuses
  - We check if all of them are of certain type, and ignore other mixed states
