import ctypes
                        # AQUI VC COLOCAR CAMINHO DA DLL
acbr_lib = ctypes.CDLL(r'C:\Users\Particular\OneDrive\ProjetosPython\ApiPosPrinter\ACBrLib\x64\ACBrPosPrinter64.dll')

#Criando o ponteiro pra ser utilizado em MT
ponteiro = ctypes.c_int()
ponteiro = ctypes.POINTER(ctypes.c_int)()

# Verificação de tipo para Inicializar 
acbr_lib.POS_Inicializar.argtypes = ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.c_char_p, ctypes.c_char_p
acbr_lib.POS_Inicializar.restype = ctypes.c_int


                        # AQUI VC COLOCAR CAMINHO DO ARQUIVO INI
acbr_lib.POS_Inicializar(ponteiro, r'C:\Users\Particular\OneDrive\ProjetosPython\ApiPosPrinter\ACBrLIB.INI'.encode("utf-8"), "".encode("utf-8"))

texto = f"""</ce><qrcode>www.google.com</qrcode>
OLÁ ESTA É UMA MENSAGEM DE TESTE


COMPREENDIDO ESTOU TESTANDO!









"""
acbr_lib.POS_Ativar(ponteiro)

eString = ctypes.create_string_buffer(len(texto))
ctypes.memmove(eString, texto.encode('utf-8'), len(texto))

Copias = 1

acbr_lib.POS_InicializarPos(ponteiro)

acbr_lib.POS_Imprimir(ponteiro,eString, True, True, True, Copias)

acbr_lib.POS_CortarPapel(ponteiro,False)

acbr_lib.POS_Desativar(ponteiro)

acbr_lib.POS_Finalizar(ponteiro)