import argparse

from models import GCNmf
from train import Trainer
from utils import NodeClsData, apply_mask, generate_mask


parser = argparse.ArgumentParser()
parser.add_argument('--dataset',
                    default='cora',
                    choices=['cora', 'citeseer', 'amacomp', 'amaphoto'],
                    help='dataset name')
parser.add_argument('--type',
                    default='random',
                    choices=['random', 'struct'],
                    help="randomly missing or structurally missing")
parser.add_argument('--rate', default=0.1, type=float, help='missing rate')
parser.add_argument('--nhid', default=16, type=int, help='the number of hidden units')
parser.add_argument('--dropout', default=0.5, type=float, help='dropout rate')
parser.add_argument('--ncomp', default=5, type=int, help='the number of Gaussian components')
parser.add_argument('--lr', default=0.005, type=float, help='learning rate')
parser.add_argument('--wd', default=1e-2, type=float, help='weight decay')
parser.add_argument('--verbose', action='store_true', help='verbose')
parser.add_argument('--seed', default=17, type=int)

args = parser.parse_args()

if __name__ == '__main__':
    data = NodeClsData(args.dataset)
    mask = generate_mask(data.features, args.rate, args.type)
    apply_mask(data.features, mask)
    model = GCNmf(data, nhid=args.nhid, dropout=args.dropout, n_components=args.ncomp)
    trainer = Trainer(data, model, lr=args.lr, weight_decay=args.wd,
                      niter=20, patience=100, epochs=10000, verbose=args.verbose)
    trainer.run()
