# /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

# from OpenOPC import client
# from time import sleep

# from general_func.database import *
from general_func.modbus import *
# from general_func.procedure import *
# from general_func.ctrl_tv1 import *
# from general_func.utils import *
from gui.msgbox_1 import *
# from gui.msgbox_2 import *

logging.basicConfig(filename="../TestScript.log",
                    level=logging.DEBUG,
                    encoding="utf-8",
                    format='[%(asctime)s: %(name)s: %(levelname)s] %(message)s')
# logging.getLogger('mysql').setLevel('INFO')
logger = logging.getLogger(__name__)


def main():
    # my_conn = MySQLConnect()
    # tv1_perv = PervObmTV1()
    # tv1_vtor = VtorObmTV1()
    # my_conn.mysql_add_message("mesaga 1")
    # my_conn.mysql_add_message("mesaga 2")
    # my_conn.mysql_add_message("mesaga 3")
    # # mb_cl = client()
    # # mb_cl.connect('arOPC.arOpcServer.1')
    # # sleep(1)
    # # mb_cl.close()
    # read_mb = ReadMB()
    # in_a0 = read_mb.read_discrete(0)
    # print(f"in_a0 = {in_a0}")
    # proc = Procedure()
    # proc.procedure_1_21_31()
    # tv1_perv.perv_obm_tv1(4.77)
    # tv1_vtor.vtor_obm_tv1(56.5)
    mb = DIRead()
    in_a0, in_a1 = mb.di_read("in_a0", "in_a1")
    print(in_a0, in_a1)


if __name__ == "__main__":
    try:
        main()
    # except HardwareException as hwe:
    #     my_msg(f'{hwe}', 'red')
    finally:
        my_msg('усе', 'orange')
