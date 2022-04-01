# read registers and print result on stdout

from pyModbusTCP.client import ModbusClient
import time

def truncate(n, decimals=0):
    multiplier = 10**decimals
    return int(n* multiplier)/multiplier

SERVER_HOST = "172.16.4.112"
SERVER_PORT = 502

c = ModbusClient()

# uncomment this line to see debug message
#c.debug(True)

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, read register (modbus function 0x03)
    if c.is_open():
        # read 2 registers at address 2566, store result in regs list
        regs_energie_total = c.read_input_registers(0X0A06, 4)
        # read 2 registers at address 1294, store result in regs list
        regs_courant_instantane = c.read_input_registers(0X050E, 2)
        # read 2 registers at address 1308, store result in regs list
        regs_puissance_instantane = c.read_input_registers(0X051C, 2)
            # if success display registers
        if regs_energie_total:
            wh = regs_energie_total[0]*65536+regs_energie_total[1]
            Mwh = regs_energie_total[2]*65536+regs_energie_total[3]
            sortieEnergieTotale = wh + (Mwh*1000000)
            print('La puissance consomé est de '+str(sortieEnergieTotale)+' wh')
        if regs_courant_instantane:
            sortie_courant_instantane= truncate(regs_courant_instantane[1]/10000, 2)
            print('Le courant instantané est de '+str(sortie_courant_instantane)+' A')
        if regs_puissance_instantane:  
            sortie_puissance_instantane = regs_puissance_instantane[0]+regs_puissance_instantane[1]
            print('La Puissance instantané est de '+str(sortie_puissance_instantane)+' W')

    # sleep 15s before next polling
    time.sleep(15)