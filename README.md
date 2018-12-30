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

The goal is to make a data storage to gurrant their integrity. Hyperledger Burrow is going to help to achive this case.
A hash value of the data is being generated and stored in the chain.

If the current data structure or values altered, the integrity will be faild.

The example demonstrates some pet store, named after Alice, that hosts exotic hamsters collection.
An owner of the store should be highly confident that all hamters in place and no one tried to customize their info.