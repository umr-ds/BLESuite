#
# btsnoop module
#
# TODO: Move stuff here to their corresponding modules
#
import binascii
import btsnoop.btsnoop as bts
import blesuite.replay.btsnoop.bt.hci_cmd as hci_cmd
import blesuite.replay.btsnoop.bt.hci_uart as hci_uart

from .android.snoopphone import SnoopPhone


def get_ltk(path=None):
	"""
	Get the Long Term Key
	"""
	records = get_records(path=path)
	cmds = get_cmds(records)
	start_enc_cmds = [opcode_length_data for opcode_length_data in cmds if opcode_length_data[0] == 0x2019]
	ltks = [binascii.hexlify(opcode_length_data1[2])[-32:] for opcode_length_data1 in start_enc_cmds]
	last_ltk = len(ltks) != 0 and ltks[-1] or ""
	return "".join(map(str.__add__, last_ltk[1::2] ,last_ltk[0::2]))


def get_rand_addr(path=None):
	"""
	Get the Host Private Random Address
	"""
	records = get_records(path=path)
	cmds = get_cmds(records)
	set_rand_addr = [opcode_length_data2 for opcode_length_data2 in cmds if opcode_length_data2[0] == 0x2005]
	addrs = [binascii.hexlify(opcode_length_data3[2])[-12:] for opcode_length_data3 in set_rand_addr]
	last_addr = len(addrs) != 0 and addrs[-1] or ""
	return "".join(map(str.__add__, last_addr[1::2], last_addr[0::2]))


def get_records(path=None):
	if not path:
		path = _pull_log()
	return bts.parse(path)


def get_cmds(records):
	hci_uarts = [hci_uart.parse(record[4]) for record in records]
	hci_cmds = [hci_type_hci_data for hci_type_hci_data in hci_uarts if hci_type_hci_data[0] == hci_uart.HCI_CMD]
	return [hci_cmd.parse(hci_type_hci_data4[1]) for hci_type_hci_data4 in hci_cmds]


def _pull_log():
	"""
	Pull the btsnoop log from a connected phone
	"""
	phone = SnoopPhone()
	return phone.pull_btsnoop()
