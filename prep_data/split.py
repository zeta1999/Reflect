import sys
import os
import errno
import random
from util.text_util import deps_from_tsv, deps_to_tsv

def make_splits(fname, expr_dir, prop_train=0.1, prop_valid=0.01):

    # for reproducibility
    random.seed(42)

    print('| read in the data')
    data = deps_from_tsv(fname)
    print('| shuffling')
    random.shuffle(data)

    n_train = int(len(data) * prop_train)
    n_valid = int(len(data) * prop_valid)
    train = data[:n_train]
    valid = data[n_train: n_train+n_valid]
    test = data[n_train+n_valid:]
    try:
        os.mkdir(expr_dir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    print('| splitting')
    deps_to_tsv(train, os.path.join(expr_dir, 'train.tsv'))
    deps_to_tsv(valid, os.path.join(expr_dir, 'valid.tsv'))
    deps_to_tsv(test, os.path.join(expr_dir, 'test.tsv'))
    print('| done!')


if __name__ == '__main__':
    make_splits(sys.argv[1], sys.argv[2])