from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.hash_module import Hash
from charm.toolbox.ABEnc import ABEnc, Input, Output
import random
import numpy as np
import itertools

class Attribute:
    def __init__(self, n, v) -> None:
        self.u : list  = []
        self.n : list = n
        self.v : list = v
        if len(n) == len(v):
            self.u = [[n[i], v[i]] for i in range(len(n))]

class Policy:
    def __init__(self, M, pai_map, map_value) -> None:
        self.M = M 
        self.pai_map = pai_map
        self.map_value : list = map_value
    
    def __str__(self) -> str:
        M_str = f"M matrix: {self.M}\n"
        pai_map_str = f"Pai map: {self.pai_map}\n"
        map_value_str = f"Map values: {self.map_value}\n"
        return M_str + pai_map_str + map_value_str

class A_KP_ABE:
    def __init__(self, group) -> None:
        self.group = group
        self.setup()
        
    def setup(self):
        g1 = self.group.random(G1)
        g2 = self.group.random(G2)

        alpha = self.group.random(ZR)
        b1 = self.group.random(ZR)
        b2 = self.group.random(ZR)

        g2_b1 = g2 ** b1
        g2_b2 = g2 ** b2
        H = self.group.hash
        e_gg_alpha = pair(g1, g2) ** alpha
        self.pk = {'pair': pair, 'G1':G1, 'G2':G2, 'GT':GT, 'g1': g1, 'g2': g2, 'group': self.group,
                    'H': H, 'g2_b1': g2_b1, 'g2_b2': g2_b2, 'e_gg_alpha': e_gg_alpha}
        self.msk = {'alpha': alpha, 'b1': b1, 'b2': b2}
        return self.pk, self.msk

    @staticmethod
    def fun(a, b):
        c = 0
        for i in range(len(a)):
            c += a[i] * b[i]
        return c
        
    def keygen(self, A : Policy):
        l = A.M.shape[0]
        n = A.M.shape[1]
    
        r = self.group.random(ZR)

        alpha_V = [self.group.random(ZR) for i in range (n-1)]
        alpha_V.insert(0, self.msk['alpha'])

        g1 = self.pk['g1']
        g2 = self.pk['g2']
        H = self.pk['H']

        b1 = self.msk['b1']
        b2 = self.msk['b2']
                
        dk1 = g2 ** r 

        dk2 = []
        dk3 = []
        for i in range(l):
            tmp = A_KP_ABE.fun(A.M[i], alpha_V)
            hash_key = A.map_value[0][i] + A.map_value[1][i]
            dk2_i = ((g1 ** tmp) * (H(hash_key, G1) ** r) ) ** (1 / b1)
            dk3_i = ((g1 ** tmp) * (H(hash_key, G1) ** r) ) ** (1 / b2)
            dk2.append(dk2_i)
            dk3.append(dk3_i)

        policy = {
            'M': A.M,
            'pai_map': A.pai_map,
            'n': A.map_value[0]
        }

        dk = {
            'policy': policy,
            'dk1': dk1,
            'dk2': dk2,
            'dk3': dk3
        }

        return dk

    @staticmethod
    def encrypt(pk, S : Attribute, msg):
        group = pk['group']
        s1 = group.random(ZR)
        s2 = group.random(ZR)
        s = s1 + s2

        H = pk['H']
        g2_b1 = pk['g2_b1']
        g2_b2 = pk['g2_b2']
        e_gg_alpha = pk['e_gg_alpha']

        ct = []
        ct1 = []
        for u in S.u:
            combined_input = u[0] + u[1]
            ct1.append(H(combined_input, G1) ** s)

        ct2 = g2_b1 ** s1
        ct3 = g2_b2 ** s2
        ct4 = (e_gg_alpha ** s) * msg

        ct = {
            'n': S.n, 
            'ct1': ct1, 'ct2': ct2, 'ct3': ct3, 'ct4': ct4,
        }

        return ct

    @staticmethod
    def split_list_by_gap(lst, gap):
        return [lst[i:i + gap] for i in range(0, len(lst), gap)]

    @staticmethod
    def generate_combinations(splitted_list):
        return list(itertools.product(*splitted_list))

    def decrypt_check(length, ID_size):
        l = list(range(0, length))
        return A_KP_ABE.generate_combinations(A_KP_ABE.split_list_by_gap(l, ID_size))

    def decrypt(self, ct, dk, m, ID_size):
        combinations = A_KP_ABE.decrypt_check(len(dk['policy']['n']), ID_size)
        if len(combinations) == 0:
            return None

        M = dk['policy']['M']
        res = None 
        for I in combinations:
            tmp_M = np.array([M[i] for i in I])
            b = [0] * int(tmp_M.shape[1])
            b[0] = 1

            gamma = np.linalg.solve(tmp_M.T, b).astype(int).tolist()

            pair = self.pk['pair']
            
            dk1 = dk['dk1']
            dk2 = dk['dk2']
            dk3 = dk['dk3']

            ct1 = ct['ct1']
            ct2 = ct['ct2']
            ct3 = ct['ct3']

            tmp_tk2 = tmp_tk3 = tmp_ct1 = 1

            for i in range(len(I)):
                tmp_tk2 *= dk2[I[i]] ** gamma[i]
                tmp_tk3 *= dk3[I[i]] ** gamma[i]
                tmp_ct1 *= ct1[I[i] % ID_size] ** gamma[i]

            rt1 = pair(tmp_tk2, ct2) * pair(tmp_tk3, ct3) / pair(tmp_ct1, dk1)
            rt2 = ct['ct4']

            msg = rt2 / rt1
            if msg == m:
                res = msg

        return res
    
