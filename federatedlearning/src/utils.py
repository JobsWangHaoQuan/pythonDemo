import copy
import torch
from torchvision import datasets, transforms
from sampling import mnist_iid, mnist_noniid, mnist_noniid_unequal
from sampling import cifar_iid, cifar_noniid


def get_dataset(args):
    if args.dataset == 'cifar':
        data_dir = '/share/home/gpu1002/Federated-Learning-PyTorch-master/data/cifar/'
        apply_transform = transforms.Compose(
            [transforms.ToTensor(),
             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
        )
        train_dataset = datasets.CIFAR10(data_dir, train=True, download=True, transform=apply_transform)
        test_dataset = datasets.CIFAR10(data_dir, train=False, download=True, transform=apply_transform)

        if args.iid:
            user_groups = cifar_iid(train_dataset, args.num_users)
        else:
            if args.unequal:
                raise NotImplementedError()
            else:
                user_groups = cifar_noniid(train_dataset, args.num_users)

    elif args.dataset == 'mnist' or 'fmnist':
        if args.dataset == 'mnist':
            data_dir = '/share/home/gpu1002/Federated-Learning-PyTorch-master/data/mnist/'
        else:
            data_dir = '/share/home/gpu1002/Federated-Learning-PyTorch-master/data/fmnist/'
        apply_transform = transforms.Compose([transforms.ToTensor(),
                                              transforms.Normalize((0.1307, 0.3081))])
        train_dataset = datasets.MNIST(data_dir, train=True, download=True, transform=apply_transform)
        test_dataset = datasets.MNIST(data_dir, train=True, download=True, transform=apply_transform)

        if args.iid:
            user_groups = mnist_iid(train_dataset, args.num_users)
        else:
            if args.unequal:
                user_groups = mnist_noniid_unequal(train_dataset, args.num_users)
            else:
                user_groups = mnist_noniid(train_dataset, args.num_users)
    return train_dataset, test_dataset, user_groups

def average_weights(w):
    w_avg = copy.deepcopy(w[0])
    for key in w_avg.keys():
        for i in range(1, len(w)):
            w_avg[key] += w[i][key]
        w_avg[key] = torch.div(w_avg[key], len(w))
    return  w_avg

def exp_details(args):
    print('\nExperimental details:')
    print(f'     Model     :{args.model}')
    print(f'     Optimizer :{args.optimizer}')
    print(f'     Learning  :{args.lr}')
    print(f'     Global Rounds   :{args.epochs}\n')

    print('      Federated parameters   :')

    if args.iid:
        print('    IID')
    else:
        print('    Non-IID')
    print(f'    Fraction of users  :{args.frac}')
    print(f'    Local Batch size   :{args.local_bs}')
    print(f'    Local Epochs       :{args.local_ep}')
    return

