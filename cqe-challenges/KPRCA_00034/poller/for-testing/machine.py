from generator.actions import Actions
import array
import random
import struct

def random_alpha():
    alphabet = list(set([chr(x) for x in xrange(256)]) - set(['\0']))
    length = random.randint(10, 50)
    return ''.join([random.choice(alphabet) for x in xrange(length)])

def random_price():
    return random.randint(10, 100000)

def random_quantity():
    return random.randint(1, 10)

def escape(s):
    return s.replace('%', '%25').replace('\t', '%09').replace('\b', '%08').replace(';', '%3B')

class SystemPrng(object):
    def __init__(self):
        pass

    def get_bytes(self, cnt):
        return ''.join([chr(random.randint(0, 255)) for x in xrange(cnt)])

class Prng(object):
    def __init__(self):
        self.state = 1

    def next(self):
        self.state = (self.state * 6364136223846793005 + 1) & ((1 << 64) - 1)
        return self.state >> 32

    def get_bytes(self, cnt):
        s = ''
        while cnt:
            x = struct.pack('>I', self.next())
            if cnt > 4:
                s += x
                cnt -= 4
            else:
                s += x[0:cnt]
                cnt = 0
        return s

class CNull(object):
    def __init__(self, k):
        self.bsize = 32

    def encode(self, b):
        return b

    def decode(self, b):
        return b

class CBest(object):
    Kconst = [183, 110, 37, 220, 147, 74, 1, 184, 111, 38, 221, 148, 75, 2, 185, 112, 39, 222, 149, 76, 3, 186, 113, 40, 223, 150, 77, 4, 187, 114, 41, 224, 151, 78, 5, 188, 115, 42, 225, 152, 79, 6, 189, 116, 43, 226, 153, 80, 7, 190, 117, 44, 227, 154, 81, 8, 191, 118, 45, 228, 155, 82, 9, 192, 119, 46, 229, 156, 83, 10, 193, 120, 47, 230, 157, 84, 11, 194, 121, 48, 231, 158, 85, 12, 195, 122, 49, 232, 159, 86, 13, 196, 123, 50, 233, 160, 87, 14, 197, 124, 51, 234, 161, 88, 15, 198, 125, 52, 235, 162, 89, 16, 199, 126, 53, 236, 163, 90, 17, 200, 127, 54, 237, 164, 91, 18, 201, 128, 55, 238, 165, 92, 19, 202, 129, 56, 239, 166, 93, 20, 203, 130, 57, 240]
    S = [1, 91, 57, 47, 165, 109, 153, 45, 240, 252, 59, 229, 22, 203, 226, 6, 32, 85, 25, 219, 140, 147, 13, 155, 227, 97, 89, 132, 190, 71, 36, 192, 253, 150, 29, 69, 111, 78, 159, 77, 68, 20, 21, 112, 169, 216, 124, 233, 129, 174, 157, 152, 211, 183, 205, 151, 120, 126, 158, 243, 11, 230, 113, 3, 16, 171, 141, 238, 70, 202, 135, 206, 242, 177, 173, 66, 95, 164, 18, 96, 255, 75, 143, 163, 184, 39, 208, 167, 34, 10, 139, 56, 213, 108, 62, 245, 193, 87, 207, 76, 234, 220, 231, 204, 60, 63, 79, 250, 134, 115, 185, 130, 8, 214, 199, 119, 35, 101, 196, 103, 121, 217, 215, 33, 176, 82, 9, 48, 0, 166, 200, 210, 92, 148, 104, 212, 17, 5, 198, 28, 235, 54, 31, 251, 225, 172, 232, 38, 117, 110, 244, 102, 30, 160, 168, 125, 67, 186, 221, 65, 4, 107, 228, 188, 146, 179, 98, 180, 189, 237, 236, 145, 88, 41, 133, 24, 128, 83, 100, 105, 46, 74, 52, 106, 137, 131, 99, 14, 246, 27, 144, 254, 241, 86, 116, 19, 187, 55, 122, 51, 15, 80, 84, 191, 162, 93, 239, 161, 2, 182, 114, 94, 73, 218, 49, 90, 223, 247, 118, 201, 44, 149, 195, 12, 64, 170, 50, 181, 23, 37, 26, 53, 197, 194, 178, 7, 123, 142, 72, 127, 249, 43, 58, 138, 222, 156, 61, 154, 136, 40, 42, 224, 81, 175, 248, 209]
    Si = [128, 0, 208, 63, 160, 137, 15, 235, 112, 126, 89, 60, 223, 22, 187, 200, 64, 136, 78, 195, 41, 42, 12, 228, 175, 18, 230, 189, 139, 34, 152, 142, 16, 123, 88, 116, 30, 229, 147, 85, 249, 173, 250, 241, 220, 7, 180, 3, 127, 214, 226, 199, 182, 231, 141, 197, 91, 2, 242, 10, 104, 246, 94, 105, 224, 159, 75, 156, 40, 35, 68, 29, 238, 212, 181, 81, 99, 39, 37, 106, 201, 252, 125, 177, 202, 17, 193, 97, 172, 26, 215, 1, 132, 205, 211, 76, 79, 25, 166, 186, 178, 117, 151, 119, 134, 179, 183, 161, 93, 5, 149, 36, 43, 62, 210, 109, 194, 148, 218, 115, 56, 120, 198, 236, 46, 155, 57, 239, 176, 48, 111, 185, 27, 174, 108, 70, 248, 184, 243, 90, 20, 66, 237, 82, 190, 171, 164, 21, 133, 221, 33, 55, 51, 6, 247, 23, 245, 50, 58, 38, 153, 207, 204, 83, 77, 4, 129, 87, 154, 44, 225, 65, 145, 74, 49, 253, 124, 73, 234, 165, 167, 227, 209, 53, 84, 110, 157, 196, 163, 168, 28, 203, 31, 96, 233, 222, 118, 232, 138, 114, 130, 219, 69, 13, 103, 54, 71, 98, 86, 255, 131, 52, 135, 92, 113, 122, 45, 121, 213, 19, 101, 158, 244, 216, 251, 144, 14, 24, 162, 11, 61, 102, 146, 47, 100, 140, 170, 169, 67, 206, 8, 192, 72, 59, 150, 95, 188, 217, 254, 240, 107, 143, 9, 32, 191, 80]

    def __init__(self, k):
        assert len(k) == 16
        self.bsize = 64

        k1 = [ord(x) for x in k[8:]]
        k1 += [reduce(lambda x,y: x^y, k1)]
        self.K1 = array.array('B')
        for x in xrange(9):
            for y in xrange(8):
                i = (x + y) % 9
                k1[i] = ((k1[i] << 3) | (k1[i] >> 5)) & 0xff
                self.K1.append(k1[i] ^ self.Kconst[x*8 + y])

        k2 = [ord(x) for x in k[0:8]]
        k2 += [reduce(lambda x,y: x^y, k2)]
        self.K2 = array.array('B')
        for x in xrange(9):
            for y in xrange(8):
                i = (x + y) % 9
                k2[i] = ((k2[i] << 3) | (k2[i] >> 5)) & 0xff
                self.K2.append(k2[i] ^ self.Kconst[(9 + x)*8 + y])

    def R(self, K1, K2, b):
        b[0] = (self.S[(b[0] ^ self.K1[K1 + 0]) & 0xff] + self.K2[K2 + 0]) & 0xff
        b[1] = (self.Si[(b[1] + self.K1[K1 + 1]) & 0xff] ^ self.K2[K2 + 1]) & 0xff
        b[2] = (self.Si[(b[2] + self.K1[K1 + 2]) & 0xff] ^ self.K2[K2 + 2]) & 0xff
        b[3] = (self.S[(b[3] ^ self.K1[K1 + 3]) & 0xff] + self.K2[K2 + 3]) & 0xff
        b[4] = (self.S[(b[4] ^ self.K1[K1 + 4]) & 0xff] + self.K2[K2 + 4]) & 0xff
        b[5] = (self.Si[(b[5] + self.K1[K1 + 5]) & 0xff] ^ self.K2[K2 + 5]) & 0xff
        b[6] = (self.Si[(b[6] + self.K1[K1 + 6]) & 0xff] ^ self.K2[K2 + 6]) & 0xff
        b[7] = (self.S[(b[7] ^ self.K1[K1 + 7]) & 0xff] + self.K2[K2 + 7]) & 0xff

        b[0], b[1] = (2 * b[0] + b[1]) & 0xff, (b[0] + b[1]) & 0xff
        b[2], b[3] = (2 * b[2] + b[3]) & 0xff, (b[2] + b[3]) & 0xff
        b[4], b[5] = (2 * b[4] + b[5]) & 0xff, (b[4] + b[5]) & 0xff
        b[6], b[7] = (2 * b[6] + b[7]) & 0xff, (b[6] + b[7]) & 0xff
        b = [b[0], b[2], b[4], b[6], b[1], b[3], b[5], b[7]]
        b[0], b[1] = (2 * b[0] + b[1]) & 0xff, (b[0] + b[1]) & 0xff
        b[2], b[3] = (2 * b[2] + b[3]) & 0xff, (b[2] + b[3]) & 0xff
        b[4], b[5] = (2 * b[4] + b[5]) & 0xff, (b[4] + b[5]) & 0xff
        b[6], b[7] = (2 * b[6] + b[7]) & 0xff, (b[6] + b[7]) & 0xff
        b = [b[0], b[2], b[4], b[6], b[1], b[3], b[5], b[7]]
        b[0], b[1] = (2 * b[0] + b[1]) & 0xff, (b[0] + b[1]) & 0xff
        b[2], b[3] = (2 * b[2] + b[3]) & 0xff, (b[2] + b[3]) & 0xff
        b[4], b[5] = (2 * b[4] + b[5]) & 0xff, (b[4] + b[5]) & 0xff
        b[6], b[7] = (2 * b[6] + b[7]) & 0xff, (b[6] + b[7]) & 0xff

        return b

    def encode(self, b):
        b = [ord(x) for x in b]

        for x in xrange(8):
            b = self.R(8 * x, 8 * x, b)

        b[0] ^= self.K1[64]
        b[1] += self.K1[65]
        b[2] += self.K1[66]
        b[3] ^= self.K1[67]
        b[4] ^= self.K1[68]
        b[5] += self.K1[69]
        b[6] += self.K1[70]
        b[7] ^= self.K1[71]

        return ''.join([chr(x & 0xff) for x in b])

class CFaith(object):
    def S(self, a, b, c):
        tmp = (a + b + c) & 0xff
        return ((tmp << 2) | (tmp >> 6)) & 0xff

    def F(self, r, L, R):
        A = struct.unpack('<BBBB', struct.pack('>I', R))
        f1 = A[1] ^ (self.K[r] >> 8) ^ A[0]
        f2 = A[2] ^ (self.K[r] & 0xff) ^ A[3]
        f1 = self.S(f1, f2, 0)
        f2 = self.S(f2, f1, 1)
        f0 = self.S(A[0], f1, 1)
        f3 = self.S(A[3], f2, 0)
        return R, L ^ struct.unpack('>I', struct.pack('<BBBB', f0, f1, f2, f3))[0]

    def __init__(self, k):
        self.bsize = 64

        def FK(a, b):
            A = struct.unpack('<BBBB', struct.pack('>I', a))
            B = struct.unpack('<BBBB', struct.pack('>I', b))
            f1 = A[1] ^ A[0]
            f2 = A[2] ^ A[3]
            f1 = self.S(f1, f2 ^ B[0], 1)
            f2 = self.S(f2, f1 ^ B[1], 0)
            f0 = self.S(A[0], f1 ^ B[2], 0)
            f3 = self.S(A[3], f2 ^ B[3], 1)
            return struct.unpack('>HH', struct.pack('<BBBB', f0, f1, f2, f3))

        self.K = array.array('H')
        L1, L2, R1, R2 = struct.unpack('<IIII', k)
        A, B, D = L1, L2, 0
        for x in xrange(20):
            if (x % 3) == 0:
                Q = R1 ^ R2
            elif (x % 3) == 1:
                Q = R1
            else:
                Q = R2
            K1, K2 = FK(A, (B ^ D) ^ Q)
            self.K.append(K1)
            self.K.append(K2)
            D, A, B = A, B, (K1 << 16) | K2

    def encode(self, b):
        L, R = struct.unpack('<II', b)
        L ^= (self.K[32] << 16) | self.K[33]
        R ^= (self.K[34] << 16) | self.K[35]
        R ^= L

        for x in xrange(32):
            L, R = self.F(x, L, R)

        L ^= R
        R ^= (self.K[36] << 16) | self.K[37]
        L ^= (self.K[38] << 16) | self.K[39]

        return struct.pack('<II', R, L)

class CDolphin(object):
    const = [0x191bfb0c, 0x6b4b7e20, 0x945c7331, 0x612e191d, 0x87519d84, 0x985c6bb9, 0x18694bd0, 0xbeefc48b, 0x81aba442, 0x6b6d3b24, 0xf22a189d, 0x28c488e9, 0xd3a2220a, 0xaa1a79eb, 0xc2cc2370, 0xd361d467,    0x26a1efdd, 0x27276a0d, 0x1f3b8193, 0xd940b678, 0x950cb28d, 0x1e9b0548, 0xb5dffe7e, 0x49679407, 0x7fff83e5, 0x91d6b59a, 0x1ddac204, 0x8d09b0b0, 0x05de57a7, 0x0b0bb1b2, 0x51f82563, 0x7db18cea,    0x381b1873, 0x4f806e8b, 0x28f687d6, 0x5284a2be, 0xf1cdd86c, 0xbc044799, 0xe071aa81, 0x3573a2cb, 0x90f2abff, 0xf99f4754, 0x16611cbf, 0x8d92c460, 0x12bee831, 0x918fe093, 0x62649d0a, 0xf2b26b8a,    0x45dd07d1, 0xe8954ccc, 0x0d269b11, 0xddb22d1c, 0x8f6ce8ee, 0xf176d6c5, 0xaf21bb08, 0x8a43f133, 0xe349d94c, 0xfa1492dc, 0x4be96634, 0xa3fa1523, 0x5bbc306d, 0x041d7ed4, 0xfd8c362e, 0x89675b99,    0x00450dad, 0xa46df75e, 0x8a4eae9f, 0xf61e62b6, 0x4380a653, 0x4f38b637, 0x23ceccc5, 0x9547f0c9, 0x02c84969, 0x6ff972c0, 0x0e1ebc74, 0xf99b05ff, 0x108b85bd, 0xe8515ab9, 0xe27ec215, 0x8ee2d24d,    0x94d52d97, 0xd8520f49, 0x55acaa57, 0x7ab6427f, 0x1822d655, 0x6f1a175a, 0xe293dc12, 0x31eb22eb, 0xc5271dcc, 0xaf7bf1c8, 0x4566b486, 0xad556493, 0xfc4b9891, 0xc076000b, 0x9b26423c, 0xf9971015,    0x8c12b7ea, 0xc9114819, 0xedf0ab1b, 0x45a669bd, 0x47d12c82, 0x051bcf16, 0xfeb99c09, 0x03471d64, 0x43405a7f, 0x98c77113, 0x3beb886b, 0x51126d0d, 0x1b8d524f, 0xde0afb18, 0x9a8b24c8, 0xa7bf17df,    0xbe07040d, 0x214cf1fd, 0x65afee34, 0x1ad05112, 0x76d0da3a, 0x7086fd26, 0xc3b5e53a, 0x1e511208, 0xc7d23bb3, 0x58ac480f, 0x40492953, 0x60dd7537, 0x98acfda9, 0x61ca941b, 0x31bc3131, 0xdc38fc3a,    0x78e6960e, 0x03bcb05f, 0xc323f0ec, 0x13c9f5fa, 0x1abce755, 0xb3689952, 0x2d7e4b63, 0x964eaa09, 0xca17679d, 0xf7319bfe, 0x65dda0e4, 0xa38bf926, 0x8f77d62c, 0xd2cfda72, 0xf0a79722, 0x00d414b8,    0xe2863609, 0x27b87d34, 0x9f0b23ed, 0xbb65ee6e, 0x0d0af330, 0xddd5fb73, 0x612e7f56, 0x6ef3a018, 0x79d8d69d, 0xc72eb47a, 0xab59a0aa, 0x81805d64, 0x0416bbf1, 0x656bf39d, 0x8fb75ce6, 0xfc939563,    0xda7c602c, 0x63ed1072, 0x427760b3, 0x4cce9a3f, 0xc508aa00, 0x5081cb3d, 0xf4c567da, 0x37183fad, 0xccd9a0ee, 0x03b187fa, 0x14c4c5f9, 0x2ff3dfcf, 0x24314637, 0xbbb9e48f, 0x8379593e, 0x677d206e,    0xd5c13e40, 0xd9f118ab, 0x71f9f39b, 0x5a5fdad6, 0x4a3fb05f, 0x35f0a3f5, 0x326fe282, 0x567456a5, 0x55d2bcf1, 0x62c8ef6c, 0x6f27b095, 0x062a8a3a, 0x80c559d5, 0x6e3b71e5, 0xb2f87f6b, 0x932132ac,    0xd62abe42, 0x161236a2, 0xc8d65ace, 0xa27701b5, 0xb37cd32c, 0x14ebabe9, 0xb57e0889, 0x5476e761, 0x2e35cb30, 0x12035523, 0x8298cff6, 0xb021d251, 0x8b65e2df, 0x65f0d50b, 0x8972cfa2, 0x486f907e,    0xd8556a77, 0xd71c73d2, 0xe79e34d5, 0x59276d0b, 0xf7c51088, 0xd736e31a, 0x51e6ff42, 0x227f806f, 0x3544a718, 0x5af5f8e3, 0xa2c8c561, 0xcefefd53, 0x470d65b3, 0x29d25dee, 0x9b9920e9, 0x551890e2,    0x16ec3674, 0x524fb942, 0x7017128e, 0x05fe95ba, 0x20e23142, 0xb854ccce, 0x90c79653, 0xb4b76823, 0xf251bb7c, 0x9c91a650, 0x3681c939, 0x627cc5fe, 0xf12a8bc2, 0x9c85e070, 0xa865f6bf, 0xc0c6aa33,    0xf35bc63a, 0xffca6de8, 0x09d4ab72, 0x6d0ce79f, 0xb1b3da67, 0x66791b82, 0xfdbf2009, 0x0efbf58e, 0x159675c4, 0xfc9b7c72, 0xcf49d59f, 0x2fb5fc18, 0x97849788, 0x86bd6dfa, 0x26b53376, 0xf040b0e1,    0x5b3400fa, 0x5ad2003e, 0x1baaa002, 0x4ec3bf8c, 0xb3ecad1b, 0x42564dbc, 0x3a98bc72, 0x7a065a58, 0x9f11dc13, 0x95486e5e, 0xe466ff79, 0x509fb691, 0x819d31d5, 0x07dd2882, 0x03cdcdeb, 0x95fc5bbd,    0x0628c076, 0xa0b12288, 0x82b0a2db, 0x9b9d6034, 0x9e9742f3, 0x7397e794, 0x13a61621, 0x92d59685, 0x2946bd46, 0x1d505a90, 0x1e048b5a, 0x9d6e067e, 0xe0d3be33, 0x88bb64e1, 0xc4666318, 0x6b33b050,    0x137740aa, 0x6df80508, 0xdbb832f4, 0x93cfa680, 0x0fab0c53, 0xa6dba077, 0x7b6ba0b5, 0x1cbf3200, 0x63f72032, 0xb61df581, 0xdc714e9d, 0x4cfc991e, 0x12cb5c40, 0x89e160dc, 0x6b590113, 0x888b8b47,    0x9a2ff65a, 0x2628da1b, 0xe7f936c3, 0x23deda2a, 0x6182cee0, 0x315c5d9a, 0xbd62caee, 0xd1d88d9d, 0xee6712b4, 0x27e5e332, 0xeefc71b3, 0x2ff3dde0, 0x6d9d9d95, 0xb2670aa5, 0x482957c4, 0x5690189d,    0x09020af8, 0x48c557d9, 0xe13bd8e9, 0xd76e79d1, 0xc89d7d58, 0xe22f2091, 0x5fd647e1, 0x53da98b6, 0xa3dab66f, 0x2ecf8718, 0x0b135e93, 0x60b869e6, 0xbe48b999, 0xee766f07, 0x76efddde, 0xf23def99,    0xf7ac5b5b, 0x1862daff, 0xef45efa9, 0x5a8689d5, 0x9cf5a500, 0x72c3ddf4, 0x24d16856, 0xef4361e5, 0x43219415, 0x17572f09, 0x3901827c, 0x3bc3d99c, 0x582bc086, 0x82510de8, 0xb6bd0e4c, 0x2252e4a4,    0xa839f836, 0xd5012ac4, 0xe1bd0299, 0xbf89bf3f, 0xdd68f199, 0xd3a5f724, 0xcba050ab, 0x957e76e6, 0x91dd4d6b, 0x7aa32a6d, 0x8ad4e55c, 0x9103875e, 0x1efd21e1, 0x6ad3e0b5, 0xb515f24e, 0x3cbade34,    0xbf2f2cef, 0x12d466a6, 0xc826c76b, 0x27dd3693, 0x19729009, 0xec7404b5, 0xd216c5d1, 0x89b370dd, 0x8dd74216, 0x8ee540fc, 0x6e44666f, 0x8fc5f1c4, 0x5a99e837, 0x5132bd96, 0x32bd5ca8, 0xf0d46f9c,    0x9649336d, 0x637ce372, 0xe16897c0, 0x1e284276, 0x1a5f541a, 0x0b13444e, 0x576f08cd, 0x55f1b735, 0xd8ad7570, 0x6a61f472, 0xf167a029, 0xcbd3d6a7, 0x2ea15999, 0x6d6e87c7, 0x3ed7d79f, 0xef273f17,    0xd1f50dfd, 0xadc47606, 0x105d8bbf, 0x2e592ece, 0xcb5f0d87, 0xb77789ca, 0x598fb123, 0xff42ae8f, 0xe11abec4, 0x7045cf73, 0xe6a78e3e, 0x56d03d94, 0x99a9af2b, 0xe67801f1, 0x0a2370de, 0xd76fa137,    0xc6cf05dc, 0x228a22ac, 0x18d2fd60, 0x64888b21, 0xd108215c, 0xcbd72444, 0x52805ff5, 0xf7bb7888, 0x79c72f02, 0xe1a0495f, 0x12ebb6f4, 0xdcdee5da, 0xb1d6111a, 0x707e69c4, 0x8c0252e1, 0xd5f7428c,    0x1c888fcc, 0xb19a2a46, 0xf2369554, 0xc912a7f6, 0x5c579d88, 0x1f585fe8, 0x79822f56, 0xd9cfe387, 0x98c2fbcc, 0xad8893f0, 0xf4f88ede, 0x2e744801, 0xe73e7709, 0x8cf2445a, 0x1b51688d, 0x63d2053a,    0x4f872f8c, 0x1f2ddacb, 0x0d3e844f, 0x9e0fdb27, 0x871eba6e, 0x381859b6, 0x4420871c, 0x30182ae2, 0x7c26c634, 0x0537135c, 0x2abe1044, 0x3a0d9cd7, 0x9959e432, 0x986c9a7d, 0x2b5ddf47, 0xa6cf9559,    0x63f015ee, 0x41d34c9c, 0xebf475e3, 0xf1a0985e, 0xc79255e3, 0x1b666688, 0x24a03667, 0xa15f1d33, 0x0e24b63d, 0xb9f2838b, 0xfb761c19, 0x1d91836d, 0xc2bac2c4, 0xc4ceb6c3, 0x5d9df692, 0x6e86bbd5,    0xacb2fd95, 0xfbc0665f, 0x0b6e437d, 0xe2b344fd, 0x468866ce, 0x45c5753d, 0xa17f4088, 0x97638da2, 0xefdf8af7, 0x90907b49, 0xd984be77, 0x9832459c, 0x152494a9, 0x762135f0, 0x43cb6d05, 0x05ea696a,    0xa25cbcdf, 0x10e3ed20, 0x62879db2, 0x21aee32f, 0x74167457, 0x94de932a, 0x84fb383b, 0xebd7d1ff, 0xa375eee1, 0x74ad7d56, 0x304583de, 0x3895e597, 0x35c6fef9, 0x657240a4, 0x91b466c4, 0x85eff237,    0x6e14eb44, 0x6b3fdef6, 0x19555f1c, 0xe39ecc0e, 0xf87bca98, 0x621d53b3, 0x26666c6e, 0x85eae3cf, 0xed561b72, 0x76cf66d8, 0xe25c079b, 0x7f36d9f7, 0x14100000, 0xdf37b2d9, 0x1a11d2b9, 0xd21fff41,    0xed86cf03, 0x0dfc60ca, 0x854ca1c5, 0x8eee3bd5, 0x1747216d, 0xe75ad40d, 0xb8cad7d9, 0x75025ec3, 0x2afc8881, 0x35a663dd, 0x9db5a17e, 0x05573c3a, 0xd2ae05aa, 0x8b092ad3, 0xf01a82e9, 0x09f15f72,    0x85bd6f1f, 0xcb315550, 0xc5512215, 0xb5be20ab, 0x568a2a64, 0x0fb49c47, 0xcbe4b055, 0xf7e97d16, 0x1752a323, 0xe11a8145, 0x74914bc8, 0xd3c94c46, 0x0a6a3b99, 0xe6c3dc9f, 0x38fa28d5, 0x152b1439,    0x9c96489d, 0x32ce0668, 0xc7f6142d, 0x058a6834, 0x97b3afbc, 0xb17305b8, 0xf9e3e1fb, 0xd144c88f, 0x2e5aa51a, 0x7106f925, 0x4ff04f87, 0x3f0d1eb0, 0x53211e46, 0xc04d35fe, 0x2db332ef, 0x0d0bb1fa,    0x210a7ec8, 0x988f3724, 0xa91a57ba, 0x9d2ea296, 0x8447c1b7, 0xb0d08be1, 0x0a85f2e3, 0x5c78748a, 0x19b14e58, 0xe54fdf16, 0xe2de2a01, 0xab1b1e2f, 0x44deacd8, 0x6f48bd7a, 0xa057a4ac, 0x5fc7e636,    0x7322ff7b, 0xcde7ac43, 0xe401414d, 0x94b1b3e4, 0x4e8f20a9, 0x4b580883, 0xe8a316a1, 0x6ff0e35a, 0xcf81fd25, 0x61ac7891, 0x4ce37814, 0xc76d5bb7, 0xda778fd4, 0xa3417b1d, 0x2bda017a, 0xe8df55fd,    0x5df70ada, 0xa8afa263, 0x66eb27c5, 0xeeac1194, 0x2876c841, 0x3aa1f7b2, 0x7e3f05c9, 0x78f9cc7b, 0xe63cc880, 0x96eae054, 0x08cfff39, 0x7dcee399, 0xea675913, 0x8784b19e, 0x55426bb6, 0x707c525c,    0xc525e69f, 0x94752ca9, 0x70b9e3ed, 0x14667aa8, 0xaf2bae28, 0xf20c8598, 0xb01b560d, 0x04085df1, 0x5e544584, 0x233b0313, 0xc4406b6b, 0xfcb38bc8, 0xee34e24b, 0x546f7099, 0x83c05a04, 0x0fc2a2c6,    0x3312de3e, 0x04d3690f, 0x07f6245d, 0x6c35e6a5, 0x17327d9c, 0x3325fe81, 0xb836d56a, 0x6a89ca1f, 0x58f83cff, 0x78bab179, 0x0338ae26, 0xe6072bd0, 0x1d7d8c52, 0x614cef77, 0x4a9b65d7, 0x65a8507e,    0x86485b5a, 0x240cfb3f, 0x93b9b2cc, 0x3ee9a717, 0xce5007e0, 0x70e53371, 0x17dcde0a, 0x47c1c74d, 0x0ff4b953, 0x10044d3a, 0x7ad2a0a4, 0xc5fbbb4e, 0x77aba6fa, 0x88013515, 0x39f8c030, 0x9be8c6a0,    0xc97e477c, 0x4b1350ff, 0x2432660f, 0xa8e4206a, 0x19a04227, 0xb8fe500f, 0x7a10b9c0, 0x39c60b97, 0x38a67708, 0x6f315f79, 0x3ea6459e, 0x4e7c94fa, 0x85d82bf1, 0x80fea880, 0x7355ad35, 0x3ce3c17c,    0x28671763, 0x1fb38f37, 0x7ed700d3, 0x9bb1f7d6, 0x958303fc, 0x68a26517, 0x7fbdbf56, 0x9f1074ca, 0xcdf84fb8, 0x2e4a2485, 0xa4cf6522, 0xe07fcfd6, 0x6e93a307, 0x11a2a341, 0x144366ec, 0xf45cdafb,    0x4af824ad, 0xdba2618d, 0x6add42b6, 0x8ffaf8c8, 0xbc1c1d95, 0xb8b762e0, 0x9f046377, 0xe82799cb, 0x27461744, 0xdfd1d23b, 0x8c7b658b, 0xe2f63b50, 0xc9cf5d54, 0xb5c638a1, 0x891aa235, 0x6b724414,    0x45626ac8, 0x3e8e281f, 0x1f5c2f69, 0x73bff869, 0xd2642ac0, 0xc5ca073c, 0xef01d164, 0x37482f6b, 0xcf18890f, 0x8ce1a312, 0x34d20736, 0x74d997fc, 0x977ffddd, 0xb7df73e3, 0xca042c28, 0x7cbaeb67,    0xa9adc04d, 0x3b321b62, 0x8657332a, 0x1466bf82, 0xe7976923, 0x7a102edf, 0x6ac06d36, 0x7071180f, 0x1740b3e7, 0xba76e922, 0xbe233cf9, 0xf3734d87, 0x06c12e85, 0x56a96b4b, 0x32038e1f, 0x7c439a43,    0x8f3506cc, 0x75dcbf92, 0xb5162939, 0x69bdc3b4, 0x84d029dd, 0x49dac550, 0xf25178a2, 0x4b793dc4, 0x18491619, 0xe7282bf6, 0x5f8cbcd5, 0xf7f3b6bf, 0x24c83105, 0x35fdf8d8, 0x43d989bd, 0x6f1f51c8,    0xcf02a097, 0x08300e1d, 0x479c7c76, 0x87539e43, 0xeaf3a189, 0x8dc28c00, 0xedc54258, 0x4c4272e3, 0xaf3f8efe, 0x405fd433, 0x0b16774f, 0x68f8cd77, 0x18e209c5, 0x7f1882a3, 0xc51ee981, 0x00a80399,    0x1624f5de, 0x2c47c93f, 0x7d069607, 0xea27eb72, 0x74ffce34, 0x08220a07, 0x4733ec00, 0x0fb701e0, 0x97a0d081, 0xc0c21461, 0xd630289e, 0x3affe0ae, 0x260daed4, 0xde01ccb2, 0x4a59c0ae, 0xd9af51bd,    0x24f59d63, 0xa8b9ff1e, 0xce04df61, 0xe97c5e24, 0xc9a040ca, 0x5b07491e, 0xde0465f2, 0x754987f9, 0x767b8d2a, 0xdc61445b, 0xce9942fd, 0x9d32cd08, 0x94435f98, 0xfdfbdfe8, 0x1293fd4a, 0x6247615f,    0xcc750160, 0xae55639c, 0xb68cff33, 0x5f0eae57, 0x79c3c5bb, 0xdbe27b54, 0x22641f2b, 0x66a13e00, 0xbad67ba5, 0x1d6b153c, 0x606fa6d2, 0x8e6addd5, 0x15d84484, 0xab96cfe2, 0x2bdcf774, 0x7ba38cf6,    0xf2d73787, 0x354bbf4b, 0xd9c8f1f2, 0x664e963b, 0x917c2f8d, 0xb3dc25de, 0x2f94919f, 0xddb0237a, 0xdb30e9f9, 0xce2b8b68, 0xfe06ab67, 0x7dde4c37, 0xaed766f9, 0xd1324582, 0x22068f2c, 0x32332925,    0x2bcc98cb, 0x808e189f, 0x3d08a3da, 0x75ff4d9b, 0x92834b4a, 0x60303f0f, 0x207d0ef6, 0xf3430df9, 0x32426ed0, 0x15951ea0, 0x41fc8703, 0x8e296ea6, 0xaa0cfb94, 0x0ab5d78f, 0x0168b819, 0x9c8c85e6,    0x4190f9f2, 0x2e32295d, 0xaa6a9536, 0xae03bd80, 0xb2f9b9cf, 0xb1d929c5, 0xd70a7537, 0xb1fe004e, 0x04fbe6b1, 0xdae19bf3, 0x78de3f25, 0xacb6d21d, 0x43c2621c, 0x4612f49d, 0x56805365, 0x9f4c399a,    0x12e997b2, 0xb0ad2951, 0x5f1adeaa, 0x919fa3f2, 0xd86c7d91, 0xafe73014, 0x7068c4ea, 0xcd20b4c7, 0x4d09741b, 0xcaf0de35, 0x03f743a6, 0xb767bca8, 0xa780fb0f, 0x4c8671fe, 0xe57876d6, 0xc4e89941,    0x05540ff4, 0x2bf6ebb0, 0xaf3a4026, 0x883468d5, 0x3fb6b99b, 0x46f7e640, 0xdc489e13, 0x1b3a29d7, 0x5e1beca6, 0x217967df, 0x4c5e436e, 0x5e92ec10, 0xa0d4d3e0, 0x0bd1ed08, 0x6783dc52, 0xa5d6db01,    0x2ebbeb8e, 0x5189114e, 0x7212cb48, 0x68b2996f, 0x3bdd6abc, 0x40458a43, 0x7354b993, 0x11332948, 0x2a806abc, 0xf1142dfa, 0x454c6a3b, 0x1a32ed27, 0xa6e722ec, 0x7fff14d7, 0xf135d9e0, 0x119d20d4,    0x05722e37, 0xb4b614b4, 0xe357bf8f, 0x88840f2e, 0xb5c39791, 0x35d24c12, 0xabf7042d, 0x43f9c9fc, 0x1783c333, 0x4786b7b7, 0x1c40a5ed, 0x95cf741a, 0xd191df6a, 0x23c03e45, 0xcd4da12b, 0xf65fbe39,    0x0c351426, 0x815edaf5, 0x8b27c574, 0xbb03131b, 0xbbe940b4, 0xb5aefc05, 0xe28d574b, 0x49abc62d, 0x10edf932, 0x3a3e5d32, 0x4630ff39, 0x54dae0d1, 0x6d29fdec, 0x8b86bea9, 0x196f7d37, 0xdc1b8c93,    0xd0163f43, 0xee153b13, 0xb7691dec, 0xdfe3788b, 0x239ad086, 0xa262b4f3, 0x3b1d82f8, 0xc383e9a3, 0xa246433d, 0x6713362b, 0x75c6ecd7, 0x734d7b78, 0x28f7a836, 0x4ede1e0f, 0x44ebd138, 0x9005c8c5,    0x57e745f5, 0xc2c24e01, 0x83171ba4, 0x6dae7b3c, 0x20426bf0, 0xd568770f, 0x038e6842, 0xacb77f56, 0x98ce0786, 0xdce86c02, 0xb387c624, 0x14d960f8, 0x0565a934, 0xb3fcd7c2, 0x3fb5a4ee, 0x2dcdf0ee,    0x2ae8601f, 0x31e614fb, 0xdc9c1430, 0x8534a185, 0x411bbcfd, 0x831271e4, 0x0635d02e, 0x1b0ae310, 0x4d9abb48, 0xa6d28f3e, 0x5fbc4fad, 0x51ad0a20, 0xbf64820f, 0xe20645a0, 0xb7297528, 0xf0e51c2c,    0x024f3799, 0xf3737375, 0xef1f72a6, 0xaf0d39e1, 0xa1e684d8, 0x5e7f33d6, 0xf1f71c9b, 0x430e3e4e, 0x90c9ef19, 0xaff800bc, 0x96ed2958, 0x067355e8, 0x7c746dc6, 0xc082120f, 0xfd976f67, 0xf790c4f1,    0x5d268891, 0xd6d4e606, 0xf1f1c18d, 0x783b9efe, 0xb7c3d15e, 0xe38d046b, 0xf65ac6b2, 0xba6ea213, 0x7b4fb2f4, 0x88f5aee5, 0x731360ae, 0xb1dad100, 0x6ccc0415, 0xcea13f42, 0x44465082, 0x0d782f97,    0xb6bb13ef, 0x3ea7b81e]
    def F(self, x):
        X = struct.unpack('BBBB', struct.pack('>I', x))
        return (((self.S0[X[0]] + self.S1[X[1]]) ^ self.S2[X[2]]) + self.S3[X[3]]) & 0xffffffff

    def __init__(self, k):
        self.bsize = 64

        K = struct.unpack('<IIIIIIII', k)

        self.P = array.array('I', self.const[0:18])
        self.S0 = array.array('I', self.const[18:18+256])
        self.S1 = array.array('I', self.const[18+256:18+512])
        self.S2 = array.array('I', self.const[18+512:18+768])
        self.S3 = array.array('I', self.const[18+768:18+1024])

        for x in xrange(18):
            self.P[x] ^= K[x % len(K)]

        def mix(A):
            for x in xrange(0, len(A), 2):
                b = struct.pack('<II', A[x], A[x+1])
                b = self.encode(b)
                A[x], A[x+1] = struct.unpack('<II', b)
        mix(self.P)
        mix(self.S0)
        mix(self.S1)
        mix(self.S2)
        mix(self.S3)

    def encode(self, b):
        L, R = struct.unpack('<II', b)
        for x in xrange(16):
            L ^= self.P[x]
            L, R = R ^ self.F(L), L
        L, R = R ^ self.P[17], L ^ self.P[16]
        return struct.pack('<II', L, R)

class CCoffee(object):
    def __init__(self, k):
        self.bsize = 64
        longs = struct.unpack('<IIII', k)

        self.K = array.array('I')
        D = 0
        for x in xrange(32):
            self.K.append((longs[D % 4] + D) & 0xffffffff)
            D = (D + 0x517CC1B7) & 0xFFFFFFFF
            self.K.append((longs[((D >> 14) ^ (D << 3)) % 4] + D) & 0xffffffff)
            D = (D + 0x517CC1B7) & 0xFFFFFFFF

    def F(self, r, L, R):
        tmp = (R << 3) ^ (R >> 4)
        tmp = (tmp + R) & 0xffffffff
        tmp ^= self.K[r * 2]
        tmp = (tmp + L) & 0xffffffff
        L, R = R, tmp

        tmp = (R << 3) ^ (R >> 4)
        tmp = (tmp + R) & 0xffffffff
        tmp ^= self.K[r * 2 + 1]
        tmp = (tmp + L) & 0xffffffff
        L, R = R, tmp
        return L, R

    def encode(self, b):
        L, R = struct.unpack('<II', b)
        for x in xrange(32):
            L, R = self.F(x, L, R)
        return struct.pack('<II', R, L)

class Mode(object):
    def __init__(self, code):
        self.code = code

    def pad(self, data, bsize):
        bytesize = bsize / 8
        padding = len(data) % bytesize
        if padding:
            return data + chr(padding) * (bytesize - padding)
        else:
            return data + '\x00' * bytesize

    def xor(self, a, b):
        return ''.join([chr(ord(a[x]) ^ ord(b[x])) for x in xrange(len(a))])

class MNull(Mode):
    def __init__(self, code):
        super(MNull, self).__init__(code)

    def encode(self, data):
        data = self.pad(data, self.code.bsize)
        return data

class MBcm(Mode):
    def __init__(self, code):
        super(MBcm, self).__init__(code)
        self.ctr = 0
        self.ctr_mask = (1 << 64) - 1

    def encode(self, data):
        bytesize = self.code.bsize / 8
        data = self.pad(data, self.code.bsize)
        result = ''
        for x in xrange(0, len(data), bytesize):
            b = data[x:x+bytesize]
            c = struct.pack('>Q', self.ctr)[-bytesize:]
            c = self.code.encode(c)
            self.ctr = (self.ctr - 1) & self.ctr_mask
            b = self.xor(b, c)
            result += b
        return result

class MXim(Mode):
    def __init__(self, code):
        super(MXim, self).__init__(code)
        self.state = '\x00' * (self.code.bsize / 8)

    def encode(self, data):
        bytesize = self.code.bsize / 8
        data = self.pad(data, self.code.bsize)
        result = ''
        for x in xrange(0, len(data), bytesize):
            b = data[x:x+bytesize]
            b = self.xor(b, self.state)
            b = self.code.encode(b)
            self.state = self.xor(b, self.state)
            result += b
        return result

class MXom(Mode):
    def __init__(self, code):
        super(MXom, self).__init__(code)
        self.state = '\x00' * (self.code.bsize / 8)

    def encode(self, data):
        bytesize = self.code.bsize / 8
        data = self.pad(data, self.code.bsize)
        result = ''
        for x in xrange(0, len(data), bytesize):
            b = data[x:x+bytesize]
            d = self.xor(b, self.state)
            d = self.code.encode(d)
            self.state = self.xor(b, d)
            result += d
        return result

class Kx(object):
    GROUPS = {
        'GROUP_2048_256': {
            'P': 0x87A8E61DB4B6663CFFBBD19C651959998CEEF608660DD0F25D2CEED4435E3B00E00DF8F1D61957D4FAF7DF4561B2AA3016C3D91134096FAA3BF4296D830E9A7C209E0C6497517ABD5A8A9D306BCF67ED91F9E6725B4758C022E0B1EF4275BF7B6C5BFC11D45F9088B941F54EB1E59BB8BC39A0BF12307F5C4FDB70C581B23F76B63ACAE1CAA6B7902D52526735488A0EF13C6D9A51BFA4AB3AD8347796524D8EF6A167B5A41825D967E144E5140564251CCACB83E6B486F6B3CA3F7971506026C0B857F689962856DED4010ABD0BE621C3A3960A54E710C375F26375D7014103A4B54330C198AF126116D2276E11715F693877FAD7EF09CADB094AE91E1A1597,
            'Q': 0x8CF83642A709A097B447997640129DA299B1A47D1EB3750BA308B0FE64F5FBD3,
            'G': 0x3FB32C9B73134D0B2E77506660EDBD484CA7B18F21EF205407F4793A1A0BA12510DBC15077BE463FFF4FED4AAC0BB555BE3A6C1B0C6B47B1BC3773BF7E8C6F62901228F8C28CBB18A55AE31341000A650196F931C77A57F2DDF463E5E9EC144B777DE62AAAB8A8628AC376D282D6ED3864E67982428EBC831D14348F6F2F9193B5045AF2767164E1DFC967C1FB3F2E55A4BD1BFFE83B9C80D052B985D182EA0ADB2A3B7313D3FE14C8484B1E052588B9B7D2BBD2DF016199ECD06E1557CD0915B3353BBB64E0EC377FD028370DF92B52C7891428CDC67EB6184B523D1DB246C32F63078490F00EF8D647D148D47954515E2327CFEF98C582664B4C0F6CC41659
        },
        'GROUP_3072_3072': {
            'P': 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF,
            'Q': 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFE,
            'G': 0x2
        }
    }

    def __init__(self, group):
        self.P = self.GROUPS[group]['P']
        self.Q = self.GROUPS[group]['Q']
        self.G = self.GROUPS[group]['G']

    def _rand(self, rng):
        def from_bytes(s):
            longs = [struct.unpack('<I', s[x:x+4])[0] for x in xrange(0, len(s), 4)]
            return int(''.join(['%08x' % x for x in reversed(longs)]),16)
        bytesize = ((self.Q.bit_length() + 31) / 32) * 4
        mask = (1 << self.Q.bit_length())-1
        value = None
        while value is None or value >= self.Q:
            value = from_bytes(rng.get_bytes(bytesize)) & mask
        return value

    def gen_a(self, rng):
        self.a = self._rand(rng)
        self.A = pow(self.G, self.a, self.P)

    def gen_b(self, rng):
        self.b = self._rand(rng)
        self.B = pow(self.G, self.b, self.P)

    def get_k(self, bits):
        self.k = pow(self.B, self.a, self.P)
        mask = (1 << bits) - 1
        return self.k & mask

class Silk(Actions):
    C_NULL = 0
    C_FAITH = 1
    C_COFFEE = 2
    C_BEST = 3
    C_DOLPHIN = 4
    MODE_NULL = 16
    MODE_BCM = 17
    MODE_XIM = 18
    MODE_XOM = 19
    CODES = {
        C_NULL: {
            'ksize': 0,
            'bsize': 32,
            'cls': CNull
        },
        C_FAITH: {
            'ksize': 128,
            'bsize': 64,
            'cls': CFaith
        },
        C_COFFEE: {
            'ksize': 128,
            'bsize': 64,
            'cls': CCoffee
        },
        C_BEST: {
            'ksize': 128,
            'bsize': 64,
            'cls': CBest
        },
        C_DOLPHIN: {
            'ksize': 256,
            'bsize': 64,
            'cls': CDolphin
        }
    }
    MODES = {
        MODE_NULL: {
            'cls': MNull
        },
        MODE_BCM: {
            'cls': MBcm
        },
        MODE_XIM: {
            'cls': MXim
        },
        MODE_XOM: {
            'cls': MXom
        }
    }

    PKT_ERROR = 0
    PKT_NEGOTIATE = 1
    PKT_KX_PARAM = 2
    PKT_KX_REPLY = 3
    PKT_DATA = 4

    def recv(self, pktid, data):
        self.read(length=1, expect=chr(pktid))
        self.read(length=len(data), expect=data)

    def recvdata(self, data):
        data = self.state['mode'][0].encode(data)
        self.recv(self.PKT_DATA, struct.pack('<H', len(data)) + data)

    def send(self, pktid, data):
        self.write(chr(pktid) + data)

    def senddata(self, data):
        data = self.state['mode'][1].encode(data)
        self.send(self.PKT_DATA, struct.pack('<H', len(data)) + data)

    def start(self):
        self.state['rng'] = Prng()
        self.state['code'] = {}
        self.state['mode'] = {}
        self.state['products'] = []

    def negotiate(self):
        everything = reduce(lambda x, y: (1 << y)|x, self.CODES.keys() + self.MODES.keys(), 0)
        self.recv(self.PKT_NEGOTIATE, struct.pack('<I', everything))

        code = random.choice(self.CODES.keys())
        mode = random.choice(self.MODES.keys())
        self.send(self.PKT_NEGOTIATE, struct.pack('<I', (1 << code) | (1 << mode)))

        self.state['cdef'] = self.CODES[code]
        self.state['mdef'] = self.MODES[mode]

    def bn_to_bytes(self, n, bits=None):
        s = '%x' % n
        if len(s) % 2:
            s = '0' + s
        result = ''.join([chr(int(s[x:x+2],16)) for x in xrange(0, len(s), 2)])
        if bits is not None:
            bytesize = bits / 8
            result = ('\x00' * bytesize + result)[-bytesize:]
        return result

    def kx(self):
        if self.state['cdef']['ksize'] == 0:
            self.recv(self.PKT_KX_PARAM, struct.pack('<HHHH', 0, 0, 0, 0))
            self.send(self.PKT_KX_REPLY, struct.pack('<H', 0))

            self.state['code'][0] = self.state['cdef']['cls'](None)
            self.state['mode'][0] = self.state['mdef']['cls'](self.state['code'][0])

            self.state['code'][1] = self.state['cdef']['cls'](None)
            self.state['mode'][1] = self.state['mdef']['cls'](self.state['code'][1])
            return
        elif self.state['cdef']['ksize'] <= 128:
            kx = Kx('GROUP_2048_256')
        else:
            kx = Kx('GROUP_3072_3072')

        kx.gen_a(self.state['rng'])
        kx.gen_b(SystemPrng())

        P = self.bn_to_bytes(kx.P)
        Q = self.bn_to_bytes(kx.Q)
        G = self.bn_to_bytes(kx.G)
        A = self.bn_to_bytes(kx.A)
        self.recv(self.PKT_KX_PARAM, struct.pack('<HHHH', len(P), len(G), len(Q), len(A)) + P + G + Q + A)

        B = self.bn_to_bytes(kx.B)
        self.send(self.PKT_KX_REPLY, struct.pack('<H', len(B)) + B)

        ksize = self.state['cdef']['ksize']
        k = ('\x00' * 32 + self.bn_to_bytes(kx.get_k(ksize)))[-(ksize/8):]
        self.state['code'][0] = self.state['cdef']['cls'](k)
        self.state['mode'][0] = self.state['mdef']['cls'](self.state['code'][0])

        k2 = ''
        xorbyte = 0xFF
        for x in k:
            x = (ord(x) ^ xorbyte) & 0xff
            xorbyte ^= x >> 3
            k2 += chr(x)
        self.state['code'][1] = self.state['cdef']['cls'](k2)
        self.state['mode'][1] = self.state['mdef']['cls'](self.state['code'][1])

    def main(self):
        pass

    def buy(self):
        if len(self.state['products']):
            p = random.choice(self.state['products'])
            self.senddata('BUY\t%s\b' % escape(p[0]))
            self.recvdata('4096\tSuccess\b')
            if p[3] == 1:
                del self.state['products'][self.state['products'].index(p)]
            else:
                self.state['products'][self.state['products'].index(p)] = (p[0], p[1], p[2], p[3]-1)
        else:
            name = random_alpha()
            self.senddata('BUY\t%s\b' % name)
            self.recvdata('8194\tName not found\b')

    def sell(self):
        def req(p):
            return 'SELL\t%s;%s;%d;%d\b' % (escape(p[0]), escape(p[1]), p[2], p[3])

        p = (random_alpha(), random_alpha(), random_price(), random_quantity())
        resp_code = 0x1000
        resp_str = "Success"
        if self.chance(0.5) and len(self.state['products']):
            name, seller, price, quantity = random.choice(self.state['products'])
            if self.chance(0.1):
                p = (name, p[1], p[2], p[3])
                resp_code = 0x2001 
                resp_str = 'Name already in-use'
            else:
                i = self.state['products'].index((name, seller, price, quantity))
                p = (name, seller, p[2], p[3])
                self.state['products'][i] = (name, seller, p[2], p[3] + quantity)

                resp_code = 0x1001
                resp_str = 'Record updated'
        else:
            self.state['products'].insert(0, p)
        self.senddata(req(p))
        self.recvdata('%d\t%s\b' % (resp_code, resp_str))

    def list(self):
        self.senddata("LIST\b")
        self.recvdata("4096\t%d\b" % len(self.state['products']))
        for p in self.state['products']:
            self.recvdata('4098\t%s;%s;%d;%d\b' % p)

    def quit(self):
        self.senddata("QUIT\b")
        self.recvdata("4096\tSuccess\b")
