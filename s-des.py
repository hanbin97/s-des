p10 = [3,5,2,7,4,10,1,9,8,6]
p8 = [6,3,7,4,8,5,10,9]
ip = [2,6,3,1,4,8,5,7]
ip1 = [4,1,3,5,7,2,8,6]
ep = [4,1,2,3,2,3,4,1]  #E/P
s0 = [[1,0,3,2],
      [3,2,1,0],
      [0,2,1,3],
      [3,1,3,2]]
s1 = [[0,1,2,3],
      [2,0,1,3],
      [3,0,1,0],
      [2,1,0,3]]
p4 = [2,4,3,1]

key1 = [0,0,0,0,
        0,0,0,0]

key2 = [0,0,0,0,
        0,0,0,0]

def dtob(num, len):     #이진수로 변환(decimal to binary number)
    x1 = format(num, 'b')
    x2 = x1.zfill(len)
    return x2   #길이len에 맞춰 0을채워서 문자열로 반환

def shift(lst): #왼쪽으로 쉬프트하는 함수
    temp = lst[0]   #첫번째 요소 할당

    #왼쪽으로 시프트
    for i in range(1, len(lst)):
        lst[i-1] = lst[i]

    # 첫번째 요소를 리스트 마지막 위치로 옮기기
    lst[len(lst) - 1] = temp

def key(n):  #키 생성 함수, 10자리정수 리스트를 받아옴
    global key1, key2   #전역변수를 사용함

    temp = [0,0,0,0,0,
            0,0,0,0,0]

    for i in range(10):
        if n[p10[i]-1] == 1:
            temp[i] = 1

    print("P10(key) :", "".join(map(str, temp)))

    temp1 = temp[0:5]
    temp2 = temp[5:10]

    shift(temp1)        #왼쪽으로 1칸 쉬프트
    shift(temp2)

    ls1 = temp1 + temp2
    print("LS-1 :", "".join(map(str, ls1)))



    for i in range(8):      #ls1값을 P8을 통해 치환
        if ls1[p8[i]-1] == 1:
            key1[i] = 1

    print("P8(key1) :", "".join(map(str, key1)))

    for i in range(2):  # 왼쪽으로 2칸 쉬프트
        shift(temp1)
        shift(temp2)

    ls2 = temp1 + temp2
    print("LS-2 :", "".join(map(str, ls2)))



    for i in range(8):      #ls2값을 P8을 통해 치환
        if ls2[p8[i]-1] == 1:
            key2[i] = 1

    print("P8(key2) :", "".join(map(str, key2)))
    print("")

def encoding(lst):  #암호화
    global key1, key2  # 전역변수를 사용함

    temp = [0,0,0,0,
            0,0,0,0]

    for i in range(8):  # 받은 메시지를 IP를 통해 치환
        if lst[ip[i] - 1] == 1:
            temp[i] = 1

    print("IP : ", "".join(map(str, temp)))

    temp1 = temp[0:4]   #4개씩 분리
    temp2 = temp[4:8]

    temp3 = [0,0,0,0,
             0,0,0,0]

    for i in range(8):  #E/P를 통해 8비트로 변환
        if temp2[ep[i] - 1] == 1:
            temp3[i] = 1

    temp4 = [0,0,0,0,
             0,0,0,0]

    for i in range(8):  #E/P와 KEY1의 XOR연산
        if temp3[i] ^ key1[i]:
            temp4[i] = 1

    s0_1_1 = temp4[0:4]
    s1_1_1 = temp4[4:8]

    # 여기서부터
    s0_1_2 = [0,0]
    s1_1_2 = [0,0]

    s0_1_2[0] = s0_1_1[0]*2 + s0_1_1[3]
    s0_1_2[1] = s0_1_1[1]*2 + s0_1_1[2]

    s1_1_2[0] = s1_1_1[0]*2 + s1_1_1[3]
    s1_1_2[1] = s1_1_1[1]*2 + s1_1_1[2]
    # 여기까지 4자리 2진수를 1,4 / 2,3 인자로 나눠서 정수로 변환

    s0_1_out = s0[s0_1_2[0]][s0_1_2[1]] #S0 표에서 정수값 도출
    s1_1_out = s1[s1_1_2[0]][s1_1_2[1]] #S1 표에서 정수값 도출

    s0_1_b = dtob(int(s0_1_out), 2)  # key값을 이진수로 변환(b_key는 문자열)
    s0_1_l = list(s0_1_b)  # 문자열 b_key를 리스트로 변환
    s0_1 = list(map(int, s0_1_l))  # 리스트 k_key의 인자를 정수로 변환)

    s1_1_b = dtob(int(s1_1_out), 2)  # key값을 이진수로 변환(b_key는 문자열)
    s1_1_l = list(s1_1_b)  # 문자열 b_key를 리스트로 변환
    s1_1 = list(map(int, s1_1_l))  # 리스트 k_key의 인자를 정수로 변환)

    temp5 = s0_1 + s1_1

    temp6 = [0,0,0,0]
    for i in range(4):  # S0 + S1 를 P4를 통해 치환
        if temp5[p4[i] - 1] == 1:
            temp6[i] = 1


    temp7 = [0,0,0,0]

    for i in range(4):  #P4를 통해 치환한 값과 처음에 구했던 IP의 앞 4자리 XOR연산
        if temp6[i] ^ temp1[i]:
            temp7[i] = 1


    print("Fk1 :", "".join(map(str, temp7+temp2)))
    #여기까지 첫번째. 최종적으로 Fk1로 SW진입

    temp8 = temp2 + temp7

    print("SW :", "".join(map(str, temp2+temp7)))



    temp9 = temp8[0:4]  # 4개씩 분리
    temp10 = temp8[4:8]

    temp11 = [0, 0, 0, 0,
             0, 0, 0, 0]

    for i in range(8):  # E/P를 통해 8비트로 변환
        if temp10[ep[i] - 1] == 1:
            temp11[i] = 1

    temp12 = [0, 0, 0, 0,
             0, 0, 0, 0]

    for i in range(8):  # E/P와 KEY2의 XOR연산
        if temp11[i] ^ key2[i]:
            temp12[i] = 1

    s0_2_1 = temp12[0:4]
    s1_2_1 = temp12[4:8]

    # 여기서부터
    s0_2_2 = [0, 0]
    s1_2_2 = [0, 0]

    s0_2_2[0] = s0_2_1[0]*2 + s0_2_1[3]
    s0_2_2[1] = s0_2_1[1]*2 + s0_2_1[2]

    s1_2_2[0] = s1_2_1[0]*2 + s1_2_1[3]
    s1_2_2[1] = s1_2_1[1]*2 + s1_2_1[2]
    # 여기까지 4자리 2진수를 1,4 / 2,3 인자로 나눠서 정수로 변환

    s0_2_out = s0[s0_2_2[0]][s0_2_2[1]]  # S0 표에서 정수값 도출
    s1_2_out = s1[s1_2_2[0]][s1_2_2[1]]  # S1 표에서 정수값 도출

    s0_2_b = dtob(int(s0_2_out), 2)  # key값을 이진수로 변환(b_key는 문자열)
    s0_2_l = list(s0_2_b)  # 문자열 b_key를 리스트로 변환
    s0_2 = list(map(int, s0_2_l))  # 리스트 k_key의 인자를 정수로 변환)

    s1_2_b = dtob(int(s1_2_out), 2)  # key값을 이진수로 변환(b_key는 문자열)
    s1_2_l = list(s1_2_b)  # 문자열 b_key를 리스트로 변환
    s1_2 = list(map(int, s1_2_l))  # 리스트 k_key의 인자를 정수로 변환)

    temp13 = s0_2 + s1_2

    temp14 = [0, 0, 0, 0]
    for i in range(4):  # S0 + S1 를 P4를 통해 치환
        if temp13[p4[i] - 1] == 1:
            temp14[i] = 1

    temp15 = [0, 0, 0, 0]
    for i in range(4):  # P4를 통해 치환한 값과 처음에 구했던 IP의 앞 4자리 XOR연산
        if temp14[i] ^ temp9[i]:
            temp15[i] = 1

    temp16 = temp15 + temp10
    # 마지막 temp16으로 IP-1 진입
    print("Fk2 :", "".join(map(str, temp16)))
    temp17 = [0,0,0,0,
                0,0,0,0]
    for i in range(8):  # IP-1을 통해 치환
        if temp16[ip1[i] - 1] == 1:
            temp17[i] = 1

    print("Final :", "".join(map(str, temp17)))
    STR = "".join(map(str, temp17))
    print("Encrypted characters :", chr(int(STR, 2)))  # 최종적으로 이진수를 문자로 변환
    print("")

def decoding(lst):
    global key1, key2  # 전역변수를 사용함

    temp = [0, 0, 0, 0,
            0, 0, 0, 0]

    for i in range(8):  # 받은 메시지를 IP를 통해 치환
        if lst[ip[i] - 1] == 1:
            temp[i] = 1

    print("IP :", "".join(map(str, temp)))

    temp1 = temp[0:4]  # 4개씩 분리
    temp2 = temp[4:8]

    temp3 = [0, 0, 0, 0,
             0, 0, 0, 0]

    for i in range(8):  # E/P를 통해 8비트로 변환
        if temp2[ep[i] - 1] == 1:
            temp3[i] = 1

    temp4 = [0, 0, 0, 0,
             0, 0, 0, 0]

    for i in range(8):  # E/P와 KEY2의 XOR연산
        if temp3[i] ^ key2[i]:
            temp4[i] = 1

    s0_1_1 = temp4[0:4]
    s1_1_1 = temp4[4:8]

    # 여기서부터
    s0_1_2 = [0, 0]
    s1_1_2 = [0, 0]

    s0_1_2[0] = s0_1_1[0] * 2 + s0_1_1[3]
    s0_1_2[1] = s0_1_1[1] * 2 + s0_1_1[2]

    s1_1_2[0] = s1_1_1[0] * 2 + s1_1_1[3]
    s1_1_2[1] = s1_1_1[1] * 2 + s1_1_1[2]
    # 여기까지 4자리 2진수를 1,4 / 2,3 인자로 나눠서 정수로 변환

    s0_1_out = s0[s0_1_2[0]][s0_1_2[1]]  # S0 표에서 정수값 도출
    s1_1_out = s1[s1_1_2[0]][s1_1_2[1]]  # S1 표에서 정수값 도출

    s0_1_b = dtob(int(s0_1_out), 2)  # key값을 이진수로 변환(b_key는 문자열)
    s0_1_l = list(s0_1_b)  # 문자열 b_key를 리스트로 변환
    s0_1 = list(map(int, s0_1_l))  # 리스트 k_key의 인자를 정수로 변환)

    s1_1_b = dtob(int(s1_1_out), 2)  # key값을 이진수로 변환(b_key는 문자열)
    s1_1_l = list(s1_1_b)  # 문자열 b_key를 리스트로 변환
    s1_1 = list(map(int, s1_1_l))  # 리스트 k_key의 인자를 정수로 변환)

    temp5 = s0_1 + s1_1

    temp6 = [0, 0, 0, 0]
    for i in range(4):  # S0 + S1 를 P4를 통해 치환
        if temp5[p4[i] - 1] == 1:
            temp6[i] = 1

    temp7 = [0, 0, 0, 0]

    for i in range(4):  # P4를 통해 치환한 값과 처음에 구했던 IP의 앞 4자리 XOR연산
        if temp6[i] ^ temp1[i]:
            temp7[i] = 1

    print("Fk1 :", "".join(map(str, temp7+temp2)))
    # 여기까지 첫번째. 최종적으로 Fk1로 SW진입

    temp8 = temp2 + temp7

    print("SW :", "".join(map(str, temp2+temp7)))

    temp9 = temp8[0:4]  # 4개씩 분리
    temp10 = temp8[4:8]

    temp11 = [0, 0, 0, 0,
              0, 0, 0, 0]

    for i in range(8):  # E/P를 통해 8비트로 변환
        if temp10[ep[i] - 1] == 1:
            temp11[i] = 1

    temp12 = [0, 0, 0, 0,
              0, 0, 0, 0]

    for i in range(8):  # E/P와 KEY1의 XOR연산
        if temp11[i] ^ key1[i]:
            temp12[i] = 1

    s0_2_1 = temp12[0:4]
    s1_2_1 = temp12[4:8]

    # 여기서부터
    s0_2_2 = [0, 0]
    s1_2_2 = [0, 0]

    s0_2_2[0] = s0_2_1[0] * 2 + s0_2_1[3]
    s0_2_2[1] = s0_2_1[1] * 2 + s0_2_1[2]

    s1_2_2[0] = s1_2_1[0] * 2 + s1_2_1[3]
    s1_2_2[1] = s1_2_1[1] * 2 + s1_2_1[2]
    # 여기까지 4자리 2진수를 1,4 / 2,3 인자로 나눠서 정수로 변환

    s0_2_out = s0[s0_2_2[0]][s0_2_2[1]]  # S0 표에서 정수값 도출
    s1_2_out = s1[s1_2_2[0]][s1_2_2[1]]  # S1 표에서 정수값 도출

    s0_2_b = dtob(int(s0_2_out), 2)  # key값을 이진수로 변환(b_key는 문자열)
    s0_2_l = list(s0_2_b)  # 문자열 b_key를 리스트로 변환
    s0_2 = list(map(int, s0_2_l))  # 리스트 k_key의 인자를 정수로 변환)

    s1_2_b = dtob(int(s1_2_out), 2)  # key값을 이진수로 변환(b_key는 문자열)
    s1_2_l = list(s1_2_b)  # 문자열 b_key를 리스트로 변환
    s1_2 = list(map(int, s1_2_l))  # 리스트 k_key의 인자를 정수로 변환)

    temp13 = s0_2 + s1_2

    temp14 = [0, 0, 0, 0]
    for i in range(4):  # S0 + S1 를 P4를 통해 치환
        if temp13[p4[i] - 1] == 1:
            temp14[i] = 1

    temp15 = [0, 0, 0, 0]
    for i in range(4):  # P4를 통해 치환한 값과 처음에 구했던 IP의 앞 4자리 XOR연산
        if temp14[i] ^ temp9[i]:
            temp15[i] = 1

    temp16 = temp15 + temp10
    # 마지막 temp16으로 IP-1 진입
    print("Fk2 :", "".join(map(str, temp16)))
    temp17 = [0, 0, 0, 0,
              0, 0, 0, 0]
    for i in range(8):  # IP-1을 통해 치환
        if temp16[ip1[i] - 1] == 1:
            temp17[i] = 1

    print("Final :", "".join(map(str, temp17)))
    STR = "".join(map(str, temp17))
    print("Decrypted characters :", chr(int(STR, 2)))     #최종적으로 이진수를 문자로 변환
    print("")

#프로그램 시작
while True:
    print("Please choose a menu.")
    n=input("1.Encryption 2.Decryption 3.Exit \nSelect Number : ")
    if n=='1':
        key_value = input("Please enter a Key value : ")
        b_key = dtob(int(key_value), 10)  # key값을 이진수로 변환(b_key는 문자열)
        l_key = list(b_key)  # 문자열 b_key를 리스트로 변환
        i_key = list(map(int, l_key))  # 리스트 k_key의 인자를 정수로 변환)

        key(i_key)  # 키(key1, key2) 생성

        plaintext = input("Please enter Plain text : ")
        t1 = dtob(ord(plaintext), 8)  # 문자 => 아스키코드 => 2진수
        l_t1 = list(t1)  # 문자열 b_key를 리스트로 변환
        i_t1 = list(map(int, l_t1))  # 리스트 k_key의 인자를 정수로 변환)

        encoding(i_t1)
    elif n=='2':
        key_value = input("Please enter a Key value : ")
        b_key = dtob(int(key_value), 10)  # key값을 이진수로 변환(b_key는 문자열)
        l_key = list(b_key)  # 문자열 b_key를 리스트로 변환
        i_key = list(map(int, l_key))  # 리스트 k_key의 인자를 정수로 변환)

        key(i_key)  # 키(key1, key2) 생성

        plaintext = input("Please enter Plain text : ")
        t1 = dtob(ord(plaintext), 8)  # 문자 => 아스키코드 => 2진수
        l_t1 = list(t1)  # 문자열 b_key를 리스트로 변환
        i_t1 = list(map(int, l_t1))  # 리스트 k_key의 인자를 정수로 변환)

        decoding(i_t1)
    else:
        break


