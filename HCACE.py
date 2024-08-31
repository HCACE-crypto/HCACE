from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from building_blocks import CD_ABACE, A_KP_ABE, Attribute, Policy, SE
from building_blocks.boolean2lsss import boolean2lsss
from building_blocks.transform_policy import transform_policy

groupObj = PairingGroup('BN254')
cpabe = CD_ABACE(groupObj)

class HCACE:
    def __init__(self, groupObj, ID_size) -> None:
        self.group: PairingGroup = groupObj
        self.ID_size: int = ID_size
        self.n_list = list(map(str, range(self.ID_size - 1, -1, -1)))
        self.CD_ABACE = CD_ABACE(groupObj)
        self.SE = SE()
        self.A_KP_ABE = A_KP_ABE(groupObj)

    def setup(self):
        self.A_KP_ABE.setup()

    def CD_ABACE_RAGen(self, U):
        return self.CD_ABACE.RAgen(len(U), U)
    
    def CD_ABACE_SAGen(self, pk):
        return self.CD_ABACE.SAgen(pk)
    
    def CD_ABACE_DecKGen(self, pk, mk, B, U):
        return self.CD_ABACE.DecKGen(pk, mk, B, U)
    
    def CD_ABACE_EncKGen(self, pk, sgk, vk, P, U):
        return self.CD_ABACE.EncKGen(pk, sgk, vk, P, U)

    def encrypt(self, ID, msg, pk, vk, ek, sign, P, send_to_ID):
        S = Attribute(self.n_list, list(format(ID, f'0{self.ID_size}b')))
        
        map_ct = {}

        sc1 = self.SE.encrypt(msg)  
        random_GT = self.group.random(GT)
        map_ct[random_GT] = self.SE.key
        sc2 = self.A_KP_ABE.encrypt(self.A_KP_ABE.pk, S, random_GT)

        # generate random GT for sc1.ct
        random_GT1 = self.group.random(GT)
        while random_GT1 in map_ct.keys():
            random_GT1 = self.group.random(GT)

        random_GT2 = self.group.random(GT)
        while random_GT2 in map_ct.keys():
            random_GT2 = self.group.random(GT)

        map_ct[random_GT1] = sc1
        map_ct[random_GT2] = sc2

        ct1, Rand1 = self.CD_ABACE.encrypt(pk, vk, random_GT1, ek, sign, P)
        ct2, Rand2 = self.CD_ABACE.encrypt(pk, vk, random_GT2, ek, sign, P)

        return {"ct1" : ct1, "Rand1" : Rand1, 
                "ct2" : ct2, "Rand2" : Rand2,
                "map" : map_ct, "send_to_ID": send_to_ID}

    def S_sanitization(self, pk, vk, ct, s_revocation_list):
        if ct["send_to_ID"] in s_revocation_list:
            print("The receiver you are trying to send to is on the revocation list and cannot pass sanitization!")
            return
        ct1 = ct["ct1"]
        Rand1 = ct["Rand1"]
        ct2 = ct["ct2"]
        Rand2 = ct["Rand2"]

        ctt = {}

        ctt1 = self.CD_ABACE.Sanitization(pk, vk, ct1, Rand1)

        if ctt1:
            ctt["ctt1"] = { 'C':ctt1["Cprime"] ,'C1':ctt1["C1prime"], 'C2':ctt1["C2prime"], 'policy':ctt1["policy"]}
            ctt["Rand1"] = Rand1

        ctt2 = self.CD_ABACE.Sanitization(pk, vk, ct2, Rand2)
        if ctt2:
            ctt["ctt2"] = { 'C':ctt2["Cprime"] ,'C1':ctt2["C1prime"], 'C2':ctt2["C2prime"], 'policy':ctt2["policy"]}
            ctt["Rand2"] = Rand2

        ctt["map"] = ct["map"]

        return ctt
        
    def R_sanitization(self, pk, vk, ctt):
        ctt1 = ctt["ctt1"]
        Rand1 = ctt["Rand1"]
        ctt2 = ctt["ctt2"]
        Rand2 = ctt["Rand2"]

        res_ctt = {}

        res_ctt["ctt1"] = self.CD_ABACE.Sanitization(pk, vk, ctt1, Rand1)

        res_ctt["ctt2"] = self.CD_ABACE.Sanitization(pk, vk, ctt2, Rand2)

        res_ctt["map"] = ctt["map"]

        return res_ctt

        
    def DecKGen2(self, r_list):
        return self.A_KP_ABE.keygen(transform_policy(r_list, self.ID_size))
    
    def decrypt(self, pk, dk, ctt):
        ctt1 = ctt["ctt1"]
        ctt2 = ctt["ctt2"]
        map_ct = ctt["map"]

        dk1 = dk["dk1"]
        dk2 = dk["dk2"]

        msg1 = self.CD_ABACE.decrypt(pk, dk1, ctt1)
        msg2 = self.CD_ABACE.decrypt(pk, dk1, ctt2)

        if msg1 not in map_ct.keys() or msg2 not in map_ct.keys():
            return None

        se_key2GT = None 
        for key in map_ct.keys():
            if key != msg1 and key != msg2:
                key_se2GT = key

        key_se = self.A_KP_ABE.decrypt(map_ct[msg2], dk2, key_se2GT, self.ID_size)
        if key_se == key_se2GT:
            msg = self.SE.decrypt(map_ct[msg1]).decode('utf-8')
            return msg
            
        return None
        



