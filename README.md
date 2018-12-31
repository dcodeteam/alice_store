# Alice Store
Simple proof of concept to use on Hyperledger Burrow(https://www.hyperledger.org/projects/hyperledger-burrow)

## Dependency requirements
- Go1.10 or higher
- Solc
- Burrow
- Python3.6 or higher
- Flask

## Burrow
Hyperledger Burrow is a permissioned blockchain node that executes smart contract code following the Ethereum specification.

More details you can find in their official GitHub page.

### Install Burrow
```
go get github.com/hyperledger/burrow
cd $GOPATH/src/github.com/hyperledger/burrow
make build
```

### Start Burrow
```
burrow start --validator-index=0
```


In this example we run a single node blockchain, but the example can be run on multi-node chains.

The goal is to make a data storage to secure its integrity. Hyperledger Burrow is going to help to achive this scenario.
A hash value of the data is being generated and stored in the ledger(blockchain).

If the current data structure or values altered, the integrity will be broken.

A demo example demonstrates some pet store, named after Alice, that hosts exotic hamsters collection.
An owner of the store should be highly confident that all hamsters data in place and no one tried to customize their data info.

## Deploy contract
Chain contract located in the project root path _alicestore.sol_.
To deploy the contract into the chain Burrow has YAML configuration files that contains rules to connect to the chain.

Create a yaml file _alice_store_deploy.yaml_:
```
jobs:

- name: deployAliceStore
  deploy:
      contract: alicestore.sol

- name: getHashes
  call:
      destination: $deployAliceStore
      function: get_hashes
```

Here we create a job to deploy a contract and at the same time call its function **get_hashes** to check it.

And run deploy:
```
burrow deploy --address C53497E8B1708259F3768E677D7405F7673B52B5 -f alice_store_deploy.yaml
```

Here an address is the address of the chain validator, it can be found in **burrow.toml** file in chain config directories.
The file description can be found here: https://github.com/hyperledger/burrow/blob/develop/docs/quickstart/single-full-node.md#configure-burrow

After deploying the contract, it will be labeled an address, contract address, save it since it'll be used in the our script.

## What the script performing
Alice store, in the demo, has **five** unique pets(hams). Each ham can be edited, deleted and validated.

On the top-right corner of the page you will notice **Chain Synchronize** button which is intended to perform data integrity check within Hyperledger Burrow chain.
For now it checks for the data existence only rather then data structure.

If we try to manipulate with any data by editing or deleting them it will lead to data structure failure of the store by meaning that unauthorized operation has been done.

The project contains three YAML files:
 - alice_store.yaml
 - alice_store_integrity.yaml
 - alice_store_validate.yaml

The contract generates a hash value of the input data(input is intended to be on JSON format, that is, we can handle our a data structure as well)
To load the initial data in to the chain run:
```
python load_chain.py
```

Then run the Flask:
```
python AliceStore.py
```
In the demo page Mexican Ham has been changed, if you click to Validate button it should wanr you that data is not identical with the ledger stored one

![alt Alice store demo](https://github.com/dcodeteam/alice_store/raw/master/screendemo.png)

## TODO
 - Planning to check for within the chain per data.
 - Add a function to be able to change a structure of the data
 - Make a permissioned access to allow a validator users only to make change in the ledger


