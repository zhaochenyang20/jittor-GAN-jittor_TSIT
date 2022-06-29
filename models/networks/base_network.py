import jittor.nn as nn
import jittor.init as init
import jittor as jt
# from infastructure import Module
from IPython import embed


class BaseNetwork(nn.Module):
    def __init__(self):
        super(BaseNetwork, self).__init__()

    @staticmethod
    def modify_commandline_options(parser, is_train):
        return parser

    def print_network(self):
        if isinstance(self, list):
            self = self[0]
        num_params = 0
        for param in self.parameters():
            num_params += param.numel()
        print('Network [%s] was created. Total number of parameters: %.1f million. '
              % (type(self).__name__, num_params / 1000000))
        print(self, file=open(f"{type(self).__name__}.arch", "w"))

    def init_weights(self, init_type='normal', gain=0.02):
        def init_func(m):
            classname = m.__class__.__name__
            # m.weight = jt.Var(m.weight)
            if classname.find('BatchNorm2d') != -1:
                if hasattr(m, 'weight') and m.weight is not None:
                    init.gauss_(m.weight, 1.0, gain)
                if hasattr(m, 'bias') and m.bias is not None:
                    init.constant_(m.bias, 0.0)
            elif hasattr(m, 'weight') and (classname.find('Conv') != -1 or classname.find('Linear') != -1):
                if init_type == 'normal':
                    init.gauss_(m.weight, 0.0, gain)
                elif init_type == 'xavier':
                    init.xavier_gauss_(m.weight, gain=gain)
                elif init_type == 'xavier_uniform':
                    init.xavier_uniform_(m.weight, gain=1.0)
                elif init_type == 'kaiming':
                    init.kaiming_normal_(m.weight, a=0, mode='fan_in')
                elif init_type == 'orthogonal':
                    # init.orthogonal_(m.weight.data, gain=gain)
                    assert False  # TODO: orthogonal initialization
                elif init_type == 'none':  # uses jittor's default init method
                    m.reset_parameters()
                else:
                    raise NotImplementedError('initialization method [%s] is not implemented' % init_type)
                if hasattr(m, 'bias') and m.bias is not None:
                    init.constant_(m.bias, 0.0)
        print("initing weights for", self.__name__())
        self.apply(init_func)
        print("weights inited")

        # propagate to children
        for m in self.children():
            if hasattr(m, 'init_weights'):
                m.init_weights(init_type, gain)
