def unpack(encoded_flag):
    flag = ""
    for packed_char in encoded_flag:
        start_int = ord(packed_char) #get the integer value of the packed unicode character
        highChar = ord(packed_char)>>8  #bit shift the integer 8 bits to the right, which in essence divides by 256
        flag += chr(highChar)
        lowChar = start_int - (highChar<<8) #difference between sum of 2 packed characters, and the first character multiplied by 256 or <<8
        lowChar = ord(packed_char)%256 #or you could simply use the modulus operator to get the remainder, which will be the lower char
        # explanation for retrieving lowChar.  If you multiple a number by 256 
        # and then add another number that is less than 256, 
        # the number added will always be the remainder when dividing the 
        # sum of those two numbers by 256.
        flag += chr(lowChar)
    print(flag)
 
# def pack(flag):
#     if(len(flag)%2):  #must be divisible by 2 since two chars are packed into a single char during encoding
#         flag+=" "     #add blank space for padding
#     encoded_flag = ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
#     print(encoded_flag)
#     return encoded_flag
 
 
flag = ""
# enc = pack(flag)
enc = "乵癃呆笱㙟戱㝟㑲㍟洰爳張挴特強栴湟㡟戱㜵素"
unpack(enc)
# print(enc)