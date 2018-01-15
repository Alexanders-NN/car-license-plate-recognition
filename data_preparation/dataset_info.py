#!/usr/bin/env python


import os
import json
import argparse

from termcolor import colored
from collections import defaultdict

from filestream import FileStream as ifstream
from hashes import get_hashers, update_hashers, hashers_result, file_hash


class Dataset:
    path = ""
    subsets = []
    content = []

    def __init__(self, path):

        self.path = os.path.abspath(path)

        abspath = lambda f: os.path.abspath(os.path.join(self.path, f))

        self.subsets = sorted([
            Dataset(abspath(directory)) for directory in os.listdir(self.path) \
                if os.path.isdir(abspath(directory))
        ])
        self.content = sorted([
            abspath(filename) for filename in os.listdir(self.path) \
                if os.path.isfile(abspath(filename))
        ])

    def hash(self, *methods, **kwargs):
        hashers = kwargs['hashers'] if 'hashers' in kwargs else get_hashers(*methods)

        for filename in self.content:
            with open(filename, 'rb') as f:
                update_hashers(hashers, f.read())
        for subset in self.subsets:
            hashers = subset.hash(*methods, hashers=hashers)

        return hashers if 'hashers' in kwargs else hashers_result(hashers)

    def hash_map(self, *args):
        hash2files = defaultdict(lambda:[])
        if not args:
            args = ['md5', 'sha1']
        if type(args) == str:
            args = [args]

        for filename in self.content:
            hash2files[file_hash(filename, *args)].append( filename )
        for subset in self.subsets:
            copies = subset.hash_map(*args)
            for hash_tuple in copies:
                hash2files[hash_tuple].extend(copies[hash_tuple])

        return {h: hash2files[h] for h in hash2files}


    def copies(self, *hash_methods):
        hash_map = self.hash_map(*hash_methods)
        hash_map = {h: hash_map[h] for h in hash_map if len(hash_map[h]) > 1}
        return {hash_map[h][0]: hash_map[h][1:] for h in  hash_map}


    def delete_copies(self, *hash_methods):
        copies = self.copies(*hash_methods)
        for h in copies:
            for filename in copies[h]:
                os.remove(filename)

        self = Dataset(self.path)



def argument_parser():
    parser = argparse.ArgumentParser(description='View information about dataset')
    parser.add_argument("-v", "--verify", action="store_true",
                        help="verify dataset")
    parser.add_argument("-c", "--find-copies", action="store_true",
                        help="find copies")
    parser.add_argument("--delete-all-copies", action="store_true",
                        help="delete all copies")
    parser.add_argument("-u", "--update", action="store_true",
                        help="update dataset map")
    parser.add_argument("--hash", action="store_true",
                        help="compute hashes od dataset")
    parser.add_argument('dataset', type=str, help='Path to dataset directory')
    return parser


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()

    verify = args.verify
    delete_all_copies = args.delete_all_copies
    find_copies = args.find_copies or args.delete_all_copies
    update = args.update
    calc_hashes = args.update or args.hash
    dataset_path = args.dataset

    if os.path.isdir(dataset_path):
        ds = Dataset(dataset_path)

        if find_copies:
            copies = ds.copies('md5')
            for name in copies:
                print name + colored(' :', 'blue')
                for copy in copies[name]:
                    print '\t{},'.format(copy)

            if delete_all_copies:
                ds.delete_copies('sha1', 'sha224')

        print '--------------'

        if calc_hashes:
            hashes = ds.hash('md5', 'sha1')
            for h in hashes:
                print colored(h, 'green') + ' : ' + hashes[h]
