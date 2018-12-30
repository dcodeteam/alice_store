pragma solidity >=0.4.22 <0.6.0;

contract Owned {
    address public owner;
    address public newOwner;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor() public {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) onlyOwner public {
        newOwner = _newOwner;
    }

    function acceptOwnership() onlyOwner public {
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    event OwnershipTransferred(address indexed _from, address indexed _to);
}

contract AliceStore is Owned {

    address[] hashes;
    mapping(address => uint) hashIndex;

    function reg_hams(bytes memory str)
        onlyOwner
        public returns (address)
    {
        uint lastIndex = hashes.length;
        bytes32 hsh = keccak256(str);

        address humanize = address(uint(hsh));
        hashes.push(humanize);
        hashIndex[humanize] = lastIndex;

        return humanize;
    }

    function vld_hams(bytes memory str)
        onlyOwner
        public view returns (bool)
    {
        bytes32 hsh_1 = keccak256(str);
        address humanize = address(uint(hsh_1));

        if (hashIndex[humanize] != 0) {
            return true;
        }
        else {
            return false;
        }
    }

    function get_hashes() public view returns (address[] memory) {
        return hashes;
    }

    function get_hashes_length() public view returns (uint) {
        return hashes.length;
    }
}