from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from HCACE import HCACE
import random, time

groupObj = PairingGroup('BN254')
hcace = HCACE(groupObj, 10)

ID_size = 10
sender_ID = 4
receiver_ID = 5

s_revocation_list = [2, 7, 12]
r_revocation_list = [6, 12]

print("s revocation list: ", s_revocation_list)
print("r revocation list: ", r_revocation_list)

U = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN']
(pk, mk) = hcace.CD_ABACE_RAGen(U)

# SA setup
(sgk,vk) = hcace.CD_ABACE_SAGen(pk)

P = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE']
(ek,sign) = hcace.CD_ABACE_EncKGen(pk, sgk, vk, P, U)

print("Signature :=>", sign)

# Decryption key generation
B = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX']
dk1 = hcace.CD_ABACE_DecKGen(pk, mk, B, U)

dk2 = hcace.DecKGen2(r_revocation_list)

dk = {}
dk["dk1"] = dk1
dk["dk2"] = dk2

print("dk: ", dk)

rand_msg = "Hello, this is a secret message!"

ct = hcace.encrypt(sender_ID, rand_msg, pk, vk, ek, sign, P, receiver_ID)
print("ct", ct)

ctt_s = hcace.S_sanitization(pk, vk, ct, s_revocation_list)
print("ctt_s: \n", ctt_s)

ctt_r = hcace.R_sanitization(pk, vk, ctt_s)
print("ctt_r: ", ctt_r)


msg = hcace.decrypt(pk, dk, ctt_r)

print("random msg: ", rand_msg)
print("msg: ", msg)
print(msg == rand_msg)

